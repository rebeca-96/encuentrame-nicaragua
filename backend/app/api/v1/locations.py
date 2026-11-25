import logging
from typing import List, Optional, Union, Any
from datetime import datetime, timezone
from fastapi import APIRouter, Depends, Query, Path, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import func
from app.core.database import get_db
from app.models.entities import (
    MissingPersonReport, GeographicLocation, ReportStatus, 
    Department, Municipality, User, UserRole
)
from app.schemas.schemas import (
    MapPointItem, DepartmentCreate, DepartmentUpdate, DepartmentResponse,
    MunicipalityCreate, MunicipalityUpdate, MunicipalityResponse,
    GeographicSummaryResponse
)
from app.services.geo_service import (
    get_departments, get_municipalities, normalize_department_name,
    validate_nicaragua_coordinates, NICARAGUA_GEOGRAPHY
)
from app.api.deps import get_current_user, require_admin

logger = logging.getLogger("encuentrame.locations")

router = APIRouter(prefix="/locations", tags=["Ubicaciones Geográficas"])


# ==============================================================================
# 1. DEPARTAMENTOS Y REGIONES AUTÓNOMAS
# ==============================================================================

@router.get("/departments", response_model=Union[List[DepartmentResponse], List[str]])
def list_departments(
    format: Optional[str] = Query("objects", description="'objects' para objetos completos o 'names' para lista de nombres"),
    active_only: bool = Query(True, description="Filtrar solo divisiones territoriales activas"),
    search: Optional[str] = Query(None, description="Búsqueda por nombre de departamento"),
    db: Session = Depends(get_db)
):
    """
    Retorna el catálogo oficial de los 15 departamentos y 2 regiones autónomas de Nicaragua.
    Soporta formato de nombres planos ('names') para compatibilidad o enriquecido ('objects').
    """
    try:
        query = db.query(Department)
        if active_only:
            query = query.filter(Department.is_active == True)
        if search:
            query = query.filter(Department.name.ilike(f"%{search.strip()}%"))
            
        departments = query.order_by(Department.name.asc()).all()
    except Exception as e:
        logger.error(f"Error consultando departamentos en base de datos: {e}", exc_info=True)
        departments = []

    # Si la base de datos aún no ha sido sembrada o falla la consulta, proveer fallback oficial
    if not departments:
        names = get_departments()
        if format == "names":
            return names
        # Si se piden objetos y la BD está vacía, responder con catálogo estructurado
        return [
            DepartmentResponse(
                id=f"fallback-{i}",
                name=n,
                code=f"DEP-{i:02d}",
                type="autonomous_region" if "Costa Caribe" in n else "department",
                latitude=12.1364,
                longitude=-86.2514,
                is_active=True,
                created_at=datetime.now(timezone.utc),
                municipalities_count=len(get_municipalities(n))
            )
            for i, n in enumerate(names, 1)
        ]

    if format == "names":
        return [d.name for d in departments]

    results = []
    for d in departments:
        try:
            mun_count = db.query(func.count(Municipality.id)).filter(
                Municipality.department_id == d.id,
                Municipality.is_active == True
            ).scalar() or 0
        except Exception:
            mun_count = len(get_municipalities(d.name))
        
        resp = DepartmentResponse.model_validate(d)
        resp.municipalities_count = mun_count
        results.append(resp)

    return results


@router.get("/departments/{department_id}", response_model=DepartmentResponse)
def get_department_by_id(
    department_id: str = Path(..., description="ID o código del departamento"),
    db: Session = Depends(get_db)
):
    """Consulta la información detallada de un departamento o región autónoma."""
    dept = db.query(Department).filter(
        (Department.id == department_id) | (Department.code == department_id.upper())
    ).first()

    if not dept:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Departamento o región con identificador '{department_id}' no encontrado."
        )

    mun_count = db.query(func.count(Municipality.id)).filter(
        Municipality.department_id == dept.id
    ).scalar() or 0

    resp = DepartmentResponse.model_validate(dept)
    resp.municipalities_count = mun_count
    return resp


@router.post("/departments", response_model=DepartmentResponse, status_code=status.HTTP_201_CREATED)
def create_department(
    data: DepartmentCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin)
):
    """
    Crea un nuevo departamento o división territorial.
    Exclusivo para administradores autorizados (RBAC).
    """
    if not validate_nicaragua_coordinates(data.latitude, data.longitude):
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Las coordenadas geográficas están fuera del territorio nacional de Nicaragua (Lat: 10.70-15.10, Lon: -87.70--82.50)."
        )

    existing = db.query(Department).filter(
        (Department.name.ilike(data.name.strip())) | (Department.code == data.code.strip().upper())
    ).first()

    if existing:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Ya existe un departamento con el nombre '{data.name}' o código '{data.code}'."
        )

    dept = Department(
        name=data.name.strip(),
        code=data.code.strip().upper(),
        type=data.type,
        latitude=data.latitude,
        longitude=data.longitude,
        is_active=True
    )
    db.add(dept)
    db.commit()
    db.refresh(dept)

    resp = DepartmentResponse.model_validate(dept)
    resp.municipalities_count = 0
    return resp


@router.patch("/departments/{department_id}", response_model=DepartmentResponse)
def update_department(
    department_id: str,
    data: DepartmentUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin)
):
    """
    Actualiza la información de un departamento existente o modifica su estado activo/inactivo.
    Exclusivo para administradores (RBAC).
    """
    dept = db.query(Department).filter(Department.id == department_id).first()
    if not dept:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Departamento '{department_id}' no encontrado."
        )

    if data.latitude is not None or data.longitude is not None:
        lat = data.latitude if data.latitude is not None else dept.latitude
        lon = data.longitude if data.longitude is not None else dept.longitude
        if not validate_nicaragua_coordinates(lat, lon):
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail="Las coordenadas geográficas deben ubicarse dentro de las fronteras de Nicaragua."
            )
        dept.latitude = lat
        dept.longitude = lon

    if data.name:
        existing_name = db.query(Department).filter(
            Department.name.ilike(data.name.strip()),
            Department.id != department_id
        ).first()
        if existing_name:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"Ya existe otro departamento con el nombre '{data.name}'."
            )
        dept.name = data.name.strip()

    if data.code:
        code_clean = data.code.strip().upper()
        existing_code = db.query(Department).filter(
            Department.code == code_clean,
            Department.id != department_id
        ).first()
        if existing_code:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"Ya existe otro departamento con el código '{code_clean}'."
            )
        dept.code = code_clean

    if data.type:
        dept.type = data.type

    if data.is_active is not None:
        dept.is_active = data.is_active

    dept.updated_at = datetime.now(timezone.utc)
    db.commit()
    db.refresh(dept)

    mun_count = db.query(func.count(Municipality.id)).filter(
        Municipality.department_id == dept.id
    ).scalar() or 0

    resp = DepartmentResponse.model_validate(dept)
    resp.municipalities_count = mun_count
    return resp


# ==============================================================================
# 2. MUNICIPIOS DE NICARAGUA
# ==============================================================================

@router.get("/municipalities", response_model=Union[List[MunicipalityResponse], List[str]])
def list_municipalities(
    department_id: Optional[str] = Query(None, description="Filtrar por ID del departamento"),
    department: Optional[str] = Query(None, description="Filtrar por nombre del departamento"),
    format: Optional[str] = Query("objects", description="'objects' para detalle o 'names' para nombres planos"),
    active_only: bool = Query(True, description="Filtrar solo municipios activos"),
    search: Optional[str] = Query(None, description="Búsqueda por nombre de municipio"),
    db: Session = Depends(get_db)
):
    """
    Retorna la lista de municipios de Nicaragua.
    Permite filtrar por department_id o por nombre de departamento para selectores dependientes.
    """
    try:
        query = db.query(Municipality).join(Department)

        if active_only:
            query = query.filter(Municipality.is_active == True)

        if department_id and department_id != "all":
            query = query.filter(Municipality.department_id == department_id)
        elif department and department.strip().lower() != "all":
            canon = normalize_department_name(department)
            target_name = canon if canon else department.strip()
            query = query.filter(Department.name.ilike(f"%{target_name}%"))

        if search:
            query = query.filter(Municipality.name.ilike(f"%{search.strip()}%"))

        municipalities = query.order_by(Municipality.name.asc()).all()
    except Exception as e:
        logger.error(f"Error consultando municipios en base de datos: {e}", exc_info=True)
        municipalities = []

    # Fallback si no hay registros en DB
    if not municipalities:
        dept_name = department if (department and department.strip().lower() != "all") else "Managua"
        muns = get_municipalities(dept_name)
        if format == "names":
            return muns
        return [
            MunicipalityResponse(
                id=f"mun-fallback-{i}",
                department_id="dept-fallback",
                department_name=dept_name,
                name=m,
                code=f"MUN-{i:03d}",
                latitude=12.1364,
                longitude=-86.2514,
                is_active=True,
                created_at=datetime.now(timezone.utc)
            )
            for i, m in enumerate(muns, 1)
        ]

    if format == "names":
        return [m.name for m in municipalities]

    results = []
    for m in municipalities:
        item = MunicipalityResponse.model_validate(m)
        item.department_name = m.department.name if m.department else None
        results.append(item)

    return results


@router.get("/municipalities/{municipality_id}", response_model=MunicipalityResponse)
def get_municipality_by_id(
    municipality_id: str = Path(..., description="ID o código del municipio"),
    db: Session = Depends(get_db)
):
    """Consulta los datos geográficos de un municipio específico."""
    mun = db.query(Municipality).join(Department).filter(
        (Municipality.id == municipality_id) | (Municipality.code == municipality_id.upper())
    ).first()

    if not mun:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Municipio '{municipality_id}' no encontrado."
        )

    resp = MunicipalityResponse.model_validate(mun)
    resp.department_name = mun.department.name if mun.department else None
    return resp


@router.post("/municipalities", response_model=MunicipalityResponse, status_code=status.HTTP_201_CREATED)
def create_municipality(
    data: MunicipalityCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin)
):
    """
    Agrega un nuevo municipio al catálogo oficial asociado a un departamento.
    Exclusivo para administradores (RBAC).
    """
    # Validar coordenadas
    if not validate_nicaragua_coordinates(data.latitude, data.longitude):
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Las coordenadas del municipio deben ubicarse dentro de Nicaragua."
        )

    # Validar existencia de departamento superior
    dept = db.query(Department).filter(Department.id == data.department_id).first()
    if not dept:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"El departamento con ID '{data.department_id}' no existe."
        )

    # Validar unicidad de código
    code_clean = data.code.strip().upper()
    existing_code = db.query(Municipality).filter(Municipality.code == code_clean).first()
    if existing_code:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Ya existe un municipio con el código '{code_clean}'."
        )

    # Validar unicidad de nombre dentro del mismo departamento
    existing_name = db.query(Municipality).filter(
        Municipality.department_id == dept.id,
        Municipality.name.ilike(data.name.strip())
    ).first()
    if existing_name:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"El municipio '{data.name}' ya está registrado en el departamento '{dept.name}'."
        )

    mun = Municipality(
        department_id=dept.id,
        name=data.name.strip(),
        code=code_clean,
        latitude=data.latitude,
        longitude=data.longitude,
        is_active=True
    )
    db.add(mun)
    db.commit()
    db.refresh(mun)

    resp = MunicipalityResponse.model_validate(mun)
    resp.department_name = dept.name
    return resp


@router.patch("/municipalities/{municipality_id}", response_model=MunicipalityResponse)
def update_municipality(
    municipality_id: str,
    data: MunicipalityUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin)
):
    """
    Actualiza la información geográfica de un municipio o cambia su estado.
    Exclusivo para administradores (RBAC).
    """
    mun = db.query(Municipality).join(Department).filter(Municipality.id == municipality_id).first()
    if not mun:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Municipio '{municipality_id}' no encontrado."
        )

    if data.department_id:
        target_dept = db.query(Department).filter(Department.id == data.department_id).first()
        if not target_dept:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Departamento destino '{data.department_id}' no existe."
            )
        mun.department_id = target_dept.id

    if data.latitude is not None or data.longitude is not None:
        lat = data.latitude if data.latitude is not None else mun.latitude
        lon = data.longitude if data.longitude is not None else mun.longitude
        if not validate_nicaragua_coordinates(lat, lon):
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail="Las coordenadas geográficas están fuera de los límites de Nicaragua."
            )
        mun.latitude = lat
        mun.longitude = lon

    if data.name:
        clean_name = data.name.strip()
        existing_name = db.query(Municipality).filter(
            Municipality.department_id == mun.department_id,
            Municipality.name.ilike(clean_name),
            Municipality.id != municipality_id
        ).first()
        if existing_name:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"Ya existe un municipio con el nombre '{clean_name}' en este departamento."
            )
        mun.name = clean_name

    if data.code:
        code_clean = data.code.strip().upper()
        existing_code = db.query(Municipality).filter(
            Municipality.code == code_clean,
            Municipality.id != municipality_id
        ).first()
        if existing_code:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"El código '{code_clean}' ya está en uso por otro municipio."
            )
        mun.code = code_clean

    if data.is_active is not None:
        mun.is_active = data.is_active

    mun.updated_at = datetime.now(timezone.utc)
    db.commit()
    db.refresh(mun)

    resp = MunicipalityResponse.model_validate(mun)
    resp.department_name = mun.department.name if mun.department else None
    return resp


# ==============================================================================
# 3. RESUMEN TERRITORIAL Y MAPA AGREGADO
# ==============================================================================

@router.get("/summary", response_model=GeographicSummaryResponse)
def get_geographic_summary(db: Session = Depends(get_db)):
    """Retorna un consolidado cuantitativo de la división territorial nacional."""
    try:
        total_depts = db.query(Department).count()
        active_depts = db.query(Department).filter(Department.is_active == True).count()
        total_muns = db.query(Municipality).count()
        active_muns = db.query(Municipality).filter(Municipality.is_active == True).count()
    except Exception as e:
        logger.error(f"Error consultando resumen territorial: {e}", exc_info=True)
        total_depts, active_depts, total_muns, active_muns = 17, 17, 153, 153

    return GeographicSummaryResponse(
        total_departments=total_depts or 17,
        active_departments=active_depts or 17,
        total_municipalities=total_muns or 153,
        active_municipalities=active_muns or 153,
        source="INETER / Ley N.° 59 de División Política Administrativa",
        last_update="Noviembre 2026"
    )


@router.get("/map-aggregated", response_model=List[MapPointItem])
def get_map_aggregated_cases(
    department: Optional[str] = Query(None, description="Filtrar por departamento"),
    municipality: Optional[str] = Query(None, description="Filtrar por municipio"),
    is_minor: Optional[bool] = Query(None, description="Filtrar menores de edad"),
    db: Session = Depends(get_db)
):
    """
    Retorna puntos geográficos aproximados de casos autorizados y activos para el mapa interactivo.
    IMPORTANTE: Nunca retorna coordenadas exactas ni domicilios privados por salvaguarda de seguridad.
    """
    try:
        query = db.query(MissingPersonReport).join(GeographicLocation).filter(
            MissingPersonReport.is_public == True,
            MissingPersonReport.status.in_([
                ReportStatus.APPROVED_PUBLISHED.value,
                ReportStatus.UNDER_INVESTIGATION.value
            ])
        )
        
        if department and department.strip().lower() != "all":
            canon = normalize_department_name(department)
            target_name = canon if canon else department.strip()
            query = query.filter(GeographicLocation.department.ilike(f"%{target_name}%"))

        if municipality and municipality.strip().lower() != "all":
            query = query.filter(GeographicLocation.municipality.ilike(f"%{municipality.strip()}%"))
            
        if is_minor is not None:
            query = query.filter(MissingPersonReport.is_minor == is_minor)
            
        reports = query.all()
    except Exception as e:
        logger.error(f"Error consultando puntos de mapa: {e}", exc_info=True)
        reports = []

    results = []
    
    for r in reports:
        photo_url = None
        primary_photo = next((p for p in r.photos if p.is_primary and p.is_approved), None)
        if not primary_photo and r.photos:
            primary_photo = r.photos[0]
        if primary_photo:
            photo_url = f"/api/v1/reports/photos/{primary_photo.storage_key}"

        loc_dept = r.location.department if r.location else "Desconocido"
        loc_mun = r.location.municipality if r.location else "Desconocido"
        approx_lat = (
            r.location.approximate_latitude 
            if r.location and r.location.approximate_latitude is not None 
            else 12.1364
        )
        approx_lon = (
            r.location.approximate_longitude 
            if r.location and r.location.approximate_longitude is not None 
            else -86.2514
        )
            
        results.append(MapPointItem(
            id=r.id,
            case_number=r.case_number,
            full_name=f"{r.first_name} {r.last_name}",
            age_at_disappearance=r.age_at_disappearance,
            gender=r.gender,
            department=loc_dept,
            municipality=loc_mun,
            disappearance_date=r.disappearance_date,
            approximate_latitude=approx_lat,
            approximate_longitude=approx_lon,
            photo_url=photo_url,
            is_minor=r.is_minor,
            status=r.status
        ))
        
    return results
