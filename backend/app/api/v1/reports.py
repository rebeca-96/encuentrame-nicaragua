import os
import hashlib
from datetime import datetime, timezone
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status, Query, UploadFile, File, Request
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
from sqlalchemy import or_, desc
from app.core.database import get_db
from app.core.config import settings
from app.models.entities import (
    MissingPersonReport, GeographicLocation, ReportPhoto, 
    ReportStatusHistory, ConsentRecord, User, UserRole, 
    ReportStatus, ModerationReview, DeletionRequest, DeletionStatus
)
from app.schemas.schemas import (
    ReportCreate, ReportUpdate, ReportPublicListItem, ReportDetailPublic,
    ReportDetailAdmin, ReportPhotoResponse, CloseReportRequest,
    DeletionRequestCreate, DeletionRequestResponse
)
from app.api.deps import get_current_user, get_optional_current_user, require_moderator
from app.services.geo_service import get_approximate_coords
from app.services.storage_service import sanitize_and_save_image, get_file_path
from app.services.audit_service import log_audit_event

router = APIRouter(prefix="/reports", tags=["Reportes de Personas Desaparecidas"])

def generate_case_number(db: Session) -> str:
    current_year = datetime.now().year
    count = db.query(MissingPersonReport).count() + 1
    return f"EN-{current_year}-{count:04d}"

@router.get("/", response_model=List[ReportPublicListItem])
def list_public_reports(
    department: Optional[str] = None,
    municipality: Optional[str] = None,
    gender: Optional[str] = None,
    is_minor: Optional[bool] = None,
    age_min: Optional[int] = None,
    age_max: Optional[int] = None,
    status: Optional[str] = None,
    q: Optional[str] = None,
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=100),
    db: Session = Depends(get_db)
):
    """
    Lista pública de reportes verificados y autorizados para publicación.
    Permite filtrar entre casos activos (búsqueda en curso) y casos no activos (concluidos/localizados).
    Los reportes en estado PENDIENTE_REVISION o BORRADOR están estrictamente excluidos.
    """
    query = db.query(MissingPersonReport).join(GeographicLocation)

    # Filtrado por estado de caso (Activo vs No Activo/Localizado)
    if status in ("active", "published", "activos"):
        query = query.filter(
            MissingPersonReport.is_public == True,
            MissingPersonReport.status.in_([
                ReportStatus.APPROVED_PUBLISHED.value,
                ReportStatus.UNDER_INVESTIGATION.value
            ])
        )
    elif status in ("inactive", "closed", "resolved", "no_activos", "closed_found", "closed_resolved"):
        query = query.filter(
            MissingPersonReport.status.in_([
                ReportStatus.CLOSED_FOUND.value,
                ReportStatus.CLOSED_RESOLVED.value
            ])
        )
    elif status in ("all", "todos"):
        pass
    else:
        # Por defecto muestra reportes públicos y aprobados/en investigación
        query = query.filter(
            MissingPersonReport.is_public == True,
            MissingPersonReport.status.in_([
                ReportStatus.APPROVED_PUBLISHED.value,
                ReportStatus.UNDER_INVESTIGATION.value
            ])
        )

    if q and q.strip():
        q_clean = f"%{q.strip()}%"
        query = query.filter(
            or_(
                MissingPersonReport.first_name.ilike(q_clean),
                MissingPersonReport.last_name.ilike(q_clean),
                MissingPersonReport.case_number.ilike(q_clean),
                MissingPersonReport.physical_description.ilike(q_clean),
            )
        )
    
    if department:
        query = query.filter(GeographicLocation.department.ilike(f"%{department}%"))
    if municipality:
        query = query.filter(GeographicLocation.municipality.ilike(f"%{municipality}%"))
    if gender and gender != "all":
        query = query.filter(MissingPersonReport.gender == gender)
    if is_minor is not None:
        query = query.filter(MissingPersonReport.is_minor == is_minor)
    if age_min is not None:
        query = query.filter(MissingPersonReport.age_at_disappearance >= age_min)
    if age_max is not None:
        query = query.filter(MissingPersonReport.age_at_disappearance <= age_max)
        
    reports = query.order_by(desc(MissingPersonReport.created_at), desc(MissingPersonReport.published_at)).offset(skip).limit(limit).all()
    
    result = []
    for r in reports:
        photo_url = None
        primary_photo = next((p for p in r.photos if p.is_primary and p.is_approved), None)
        if not primary_photo and r.photos:
            primary_photo = r.photos[0]
        if primary_photo:
            photo_url = f"/api/v1/reports/photos/{primary_photo.storage_key}"
            
        result.append(ReportPublicListItem(
            id=r.id,
            case_number=r.case_number,
            first_name=r.first_name,
            last_name=r.last_name,
            age_at_disappearance=r.age_at_disappearance,
            gender=r.gender,
            disappearance_date=r.disappearance_date,
            department=r.location.department,
            municipality=r.location.municipality,
            physical_description=r.physical_description,
            primary_photo_url=photo_url,
            is_minor=r.is_minor,
            status=r.status,
            published_at=r.published_at
        ))
    return result

@router.get("/my-reports")
def list_my_reports(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Retorna los reportes creados por el usuario autenticado con su estado de revisión."""
    reports = db.query(MissingPersonReport).filter(
        MissingPersonReport.reporter_id == current_user.id
    ).order_by(desc(MissingPersonReport.created_at)).all()
    
    return [{
        "id": r.id,
        "case_number": r.case_number,
        "first_name": r.first_name,
        "last_name": r.last_name,
        "status": r.status,
        "is_public": r.is_public,
        "department": r.location.department if r.location else "",
        "municipality": r.location.municipality if r.location else "",
        "created_at": r.created_at,
        "published_at": r.published_at
    } for r in reports]

@router.get("/{id_or_case}", response_model=ReportDetailPublic)
def get_report_detail(
    id_or_case: str,
    db: Session = Depends(get_db),
    current_user: Optional[User] = Depends(get_optional_current_user)
):
    """
    Obtiene el detalle de un reporte.
    Si el reporte no está publicado, solo puede ser consultado por moderadores, administradores o su autor.
    """
    report = db.query(MissingPersonReport).filter(
        or_(MissingPersonReport.id == id_or_case, MissingPersonReport.case_number == id_or_case)
    ).first()
    
    if not report:
        raise HTTPException(status_code=404, detail="Reporte no encontrado")
        
    # Check view permissions if not public
    if not report.is_public:
        if not current_user:
            raise HTTPException(
                status_code=403, 
                detail="Este reporte se encuentra en revisión y no está disponible públicamente."
            )
        is_owner = (report.reporter_id == current_user.id)
        is_mod = (current_user.role in [UserRole.MODERATOR.value, UserRole.ADMIN.value])
        if not (is_owner or is_mod):
            raise HTTPException(
                status_code=403,
                detail="No tienes permiso para consultar este reporte en estado confidencial."
            )
            
    photos_resp = []
    for p in report.photos:
        photos_resp.append(ReportPhotoResponse(
            id=p.id,
            storage_key=p.storage_key,
            url=f"/api/v1/reports/photos/{p.storage_key}",
            is_primary=p.is_primary,
            original_filename=p.original_filename
        ))
        
    return ReportDetailPublic(
        id=report.id,
        case_number=report.case_number,
        first_name=report.first_name,
        last_name=report.last_name,
        nickname=report.nickname,
        age_at_disappearance=report.age_at_disappearance,
        gender=report.gender,
        disappearance_date=report.disappearance_date,
        department=report.location.department,
        municipality=report.location.municipality,
        neighborhood_zone=report.location.neighborhood_zone,
        approximate_latitude=report.location.approximate_latitude,
        approximate_longitude=report.location.approximate_longitude,
        physical_description=report.physical_description,
        clothing_description=report.clothing_description,
        circumstances=report.circumstances,
        medical_conditions=report.medical_conditions,
        is_minor=report.is_minor,
        vulnerability_flag=report.vulnerability_flag,
        status=report.status,
        published_at=report.published_at,
        photos=photos_resp
    )

@router.post("/", status_code=status.HTTP_201_CREATED)
def create_report(
    data: ReportCreate,
    request: Request,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Crea un reporte de desaparición.
    POR SEGURIDAD:
    - Todo reporte se crea en estado 'pending_review' y 'is_public=False'.
    - Requiere consentimiento documentado del reportante.
    """
    if not data.consent.accepted_terms:
        raise HTTPException(
            status_code=400,
            detail="Debe aceptar expresamente los términos de consentimiento y la Ley 787 de Nicaragua"
        )
        
    # Get approximate coordinates
    lat, lng = get_approximate_coords(data.department, data.municipality)
    if data.approximate_latitude and data.approximate_longitude:
        lat = data.approximate_latitude
        lng = data.approximate_longitude
        
    location = GeographicLocation(
        department=data.department,
        municipality=data.municipality,
        neighborhood_zone=data.neighborhood_zone,
        approximate_latitude=lat,
        approximate_longitude=lng,
        is_sensitive=True
    )
    db.add(location)
    db.flush()
    
    case_num = generate_case_number(db)
    is_minor = (data.age_at_disappearance < 18) or data.is_minor
    
    new_report = MissingPersonReport(
        case_number=case_num,
        reporter_id=current_user.id,
        first_name=data.first_name.strip(),
        last_name=data.last_name.strip(),
        nickname=data.nickname.strip() if data.nickname else None,
        age_at_disappearance=data.age_at_disappearance,
        birth_date=data.birth_date,
        gender=data.gender,
        disappearance_date=data.disappearance_date,
        location_id=location.id,
        physical_description=data.physical_description.strip(),
        clothing_description=data.clothing_description.strip(),
        medical_conditions=data.medical_conditions.strip() if data.medical_conditions else None,
        circumstances=data.circumstances.strip(),
        is_minor=is_minor,
        vulnerability_flag=data.vulnerability_flag or is_minor or (data.age_at_disappearance >= 65),
        is_public=False,
        status=ReportStatus.PENDING_REVIEW.value,
        published_at=None
    )
    db.add(new_report)
    db.flush()
    
    # Store consent record
    ip_addr = request.client.host if request.client else "127.0.0.1"
    doc_hash = hashlib.sha256(data.consent.identity_doc_number.encode()).hexdigest()
    ip_hash = hashlib.sha256(ip_addr.encode()).hexdigest()
    
    consent = ConsentRecord(
        report_id=new_report.id,
        reporter_id=current_user.id,
        relationship_to_victim=data.consent.relationship_to_victim,
        identity_doc_hash=doc_hash,
        consent_text_version="v1.0-Ley787",
        ip_address_hash=ip_hash
    )
    db.add(consent)
    
    # Status history initial
    history = ReportStatusHistory(
        report_id=new_report.id,
        changed_by=current_user.id,
        previous_status="draft",
        new_status=ReportStatus.PENDING_REVIEW.value,
        reason="Creación inicial del reporte por usuario reportante"
    )
    db.add(history)
    db.commit()
    db.refresh(new_report)
    
    log_audit_event(
        db=db,
        action="REPORT_CREATED",
        entity_name="missing_person_reports",
        entity_id=new_report.id,
        user_id=current_user.id,
        ip_address=ip_addr,
        details={"case_number": case_num, "is_minor": is_minor}
    )
    
    return {
        "id": new_report.id,
        "case_number": new_report.case_number,
        "status": new_report.status,
        "message": "Reporte registrado exitosamente. Ha ingresado a revisión previa de moderación por seguridad."
    }

@router.put("/{report_id}")
def update_report(
    report_id: str,
    update_data: ReportUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Actualiza datos de un reporte existente.
    Permisos:
    - Autor del reporte: solo si está en 'draft' o 'pending_review'.
    - Moderador o Administrador: en cualquier estado activo.
    """
    report = db.query(MissingPersonReport).filter(MissingPersonReport.id == report_id).first()
    if not report:
        raise HTTPException(status_code=404, detail="Reporte no encontrado")

    is_owner = (report.reporter_id == current_user.id)
    is_mod = (current_user.role in [UserRole.MODERATOR.value, UserRole.ADMIN.value])

    if not (is_owner or is_mod):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No tienes permiso para modificar este reporte"
        )

    if is_owner and not is_mod:
        if report.status not in [ReportStatus.DRAFT.value, ReportStatus.PENDING_REVIEW.value]:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="El reporte ya ha sido aprobado o está en investigación. Solicite las modificaciones a moderación."
            )

    update_dict = update_data.model_dump(exclude_unset=True)
    for field, val in update_dict.items():
        if field == "neighborhood_zone" and report.location:
            report.location.neighborhood_zone = val
        elif hasattr(report, field):
            setattr(report, field, val)

    report.updated_at = datetime.now(timezone.utc)
    db.commit()
    db.refresh(report)

    log_audit_event(
        db=db,
        action="REPORT_UPDATED",
        entity_name="missing_person_reports",
        entity_id=report.id,
        user_id=current_user.id,
        details={"updated_fields": list(update_dict.keys())}
    )

    return {
        "id": report.id,
        "case_number": report.case_number,
        "message": "Reporte actualizado correctamente"
    }

@router.post("/{report_id}/photos")
def upload_report_photo(
    report_id: str,
    file: UploadFile = File(...),
    is_primary: bool = True,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Sube y sanitiza una fotografía para el reporte.
    Elimina automáticamente todos los metadatos EXIF (GPS, modelo, hora) para proteger la privacidad.
    """
    report = db.query(MissingPersonReport).filter(MissingPersonReport.id == report_id).first()
    if not report:
        raise HTTPException(status_code=404, detail="Reporte no encontrado")
        
    is_owner = (report.reporter_id == current_user.id)
    is_mod = (current_user.role in [UserRole.MODERATOR.value, UserRole.ADMIN.value])
    if not (is_owner or is_mod):
        raise HTTPException(status_code=403, detail="No tienes permiso para adjuntar fotos a este reporte")
        
    if file.content_type and file.content_type not in settings.ALLOWED_IMAGE_TYPES:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Tipo de archivo no permitido ({file.content_type}). Solo se permiten: {', '.join(settings.ALLOWED_IMAGE_TYPES)}"
        )

    file_bytes = file.file.read()
    if len(file_bytes) > settings.MAX_UPLOAD_SIZE_MB * 1024 * 1024:
        raise HTTPException(status_code=400, detail="El archivo excede el tamaño máximo permitido (5MB)")
        
    storage_key, sha256_hash = sanitize_and_save_image(file_bytes, file.filename)
    
    # If primary, reset other photos' primary flag
    if is_primary:
        for p in report.photos:
            p.is_primary = False
            
    photo = ReportPhoto(
        report_id=report.id,
        storage_key=storage_key,
        is_primary=is_primary,
        is_approved=True,  # Moderator approval inherits or validates
        blur_level=0,
        original_filename=file.filename,
        file_hash_sha256=sha256_hash
    )
    db.add(photo)
    db.commit()
    db.refresh(photo)
    
    return {
        "id": photo.id,
        "storage_key": photo.storage_key,
        "url": f"/api/v1/reports/photos/{photo.storage_key}",
        "message": "Fotografía sanitizada (metadatos EXIF eliminados) y almacenada con éxito"
    }

@router.get("/photos/{storage_key}")
def get_photo_file(storage_key: str):
    """Retorna la imagen sanitizada."""
    path = get_file_path(storage_key)
    if not os.path.exists(path):
        raise HTTPException(status_code=404, detail="Fotografía no encontrada")
    return FileResponse(path, media_type="image/webp")

@router.post("/{report_id}/request-close")
def request_close_case(
    report_id: str,
    data: CloseReportRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    El reportante solicita el cierre del caso (persona localizada o resolución pacífica).
    """
    report = db.query(MissingPersonReport).filter(MissingPersonReport.id == report_id).first()
    if not report:
        raise HTTPException(status_code=404, detail="Reporte no encontrado")
        
    is_owner = (report.reporter_id == current_user.id)
    is_mod = (current_user.role in [UserRole.MODERATOR.value, UserRole.ADMIN.value])
    if not (is_owner or is_mod):
        raise HTTPException(status_code=403, detail="No tienes autorización para solicitar el cierre de este caso")
        
    prev = report.status
    report.status = ReportStatus.CLOSED_FOUND.value if "localizada" in data.reason.lower() else ReportStatus.CLOSED_RESOLVED.value
    report.is_public = False  # De-publish immediately upon resolution to protect privacy
    
    history = ReportStatusHistory(
        report_id=report.id,
        changed_by=current_user.id,
        previous_status=prev,
        new_status=report.status,
        reason=f"Solicitud de cierre: {data.reason}. {data.details or ''}"
    )
    db.add(history)
    db.commit()
    
    log_audit_event(
        db=db,
        action="CASE_CLOSED",
        entity_name="missing_person_reports",
        entity_id=report.id,
        user_id=current_user.id,
        details={"reason": data.reason}
    )
    
    return {"message": "El caso ha sido cerrado y retirado de la publicación pública para proteger la dignidad de la persona."}


@router.post("/{report_id}/request-deletion", response_model=DeletionRequestResponse, status_code=status.HTTP_201_CREATED)
def request_deletion_case(
    report_id: str,
    data: DeletionRequestCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Solicitud formal de supresión de datos conforme al artículo 16 de la Ley N.° 787 de Nicaragua.
    Acceso exclusivo para el reportante legal o personal de moderación/administración.
    Despublica inmediatamente el caso para salvaguardar la privacidad durante el trámite.
    """
    report = db.query(MissingPersonReport).filter(MissingPersonReport.id == report_id).first()
    if not report:
        raise HTTPException(status_code=404, detail="Reporte no encontrado")

    is_owner = (report.reporter_id == current_user.id)
    is_mod = (current_user.role in [UserRole.MODERATOR.value, UserRole.ADMIN.value])
    if not (is_owner or is_mod):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No tienes autorización para solicitar la supresión de datos de este expediente."
        )

    # Inmediatamente despublicar preventivamente
    report.is_public = False
    
    del_req = DeletionRequest(
        report_id=report.id,
        requested_by=current_user.id,
        reason=data.reason.strip(),
        status=DeletionStatus.PENDING.value
    )
    db.add(del_req)
    db.commit()
    db.refresh(del_req)

    log_audit_event(
        db=db,
        action="DATA_DELETION_REQUESTED",
        entity_name="deletion_requests",
        entity_id=del_req.id,
        user_id=current_user.id,
        details={"case_number": report.case_number, "reason": data.reason}
    )

    return DeletionRequestResponse(
        id=del_req.id,
        report_id=report.id,
        case_number=report.case_number,
        reason=del_req.reason,
        status=del_req.status,
        created_at=del_req.created_at,
        message="Solicitud de supresión de datos recibida y en cola de procesamiento conforme a la Ley N.° 787."
    )
