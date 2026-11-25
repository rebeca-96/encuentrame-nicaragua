import secrets
from datetime import datetime, timezone
from fastapi import APIRouter, Depends, HTTPException, status, Request
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.rate_limit import rate_limit_tips
from app.models.entities import (
    ConfidentialTip, MissingPersonReport, GeographicLocation, 
    TipStatus, ConfidentialityLevel, ReportStatus
)
from app.schemas.schemas import TipCreate, TipCreateResponse, TipTrackResponse
from app.services.geo_service import get_approximate_coords
from app.services.audit_service import log_audit_event

router = APIRouter(prefix="/tips", tags=["Pistas Confidenciales"])

def generate_tip_code() -> str:
    # Generates a random unguessable tracking code e.g. PISTA-9A4K-2B7Z
    token = secrets.token_hex(4).upper()
    return f"PISTA-{token[:4]}-{token[4:]}"

@router.post("/", response_model=TipCreateResponse, status_code=status.HTTP_201_CREATED, dependencies=[Depends(rate_limit_tips)])
def submit_confidential_tip(
    data: TipCreate,
    request: Request,
    db: Session = Depends(get_db)
):
    """
    Permite a los ciudadanos aportar pistas e información confidencial sobre un caso.
    LA PISTA NUNCA ES PÚBLICA. Solo el personal de moderación autorizado tiene acceso.
    """
    report = db.query(MissingPersonReport).filter(MissingPersonReport.id == data.report_id).first()
    if not report:
        raise HTTPException(status_code=404, detail="El reporte indicado no existe")
        
    if report.status in [ReportStatus.CLOSED_FOUND.value, ReportStatus.CLOSED_RESOLVED.value]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Este caso ya ha sido cerrado o resuelto. No se reciben pistas para casos inactivos."
        )
        
    sighting_loc_id = None
    if data.sighting_department:
        lat, lng = get_approximate_coords(data.sighting_department, data.sighting_municipality)
        loc = GeographicLocation(
            department=data.sighting_department,
            municipality=data.sighting_municipality or "Zona no especificada",
            approximate_latitude=lat,
            approximate_longitude=lng,
            is_sensitive=True
        )
        db.add(loc)
        db.flush()
        sighting_loc_id = loc.id
        
    tip_code = generate_tip_code()
    
    tip = ConfidentialTip(
        report_id=report.id,
        tip_code=tip_code,
        description=data.description.strip(),
        sighting_date=data.sighting_date,
        sighting_location_id=sighting_loc_id,
        informant_contact=data.informant_contact.strip() if data.informant_contact else None,
        confidentiality_level=data.confidentiality_level or ConfidentialityLevel.STRICT_ANONYMOUS.value,
        status=TipStatus.RECEIVED.value
    )
    db.add(tip)
    db.commit()
    db.refresh(tip)
    
    log_audit_event(
        db=db,
        action="TIP_RECEIVED",
        entity_name="confidential_tips",
        entity_id=tip.id,
        ip_address=request.client.host if request.client else None,
        details={"case_number": report.case_number, "tip_code": tip_code}
    )
    
    return TipCreateResponse(
        tip_code=tip_code,
        message="Su pista ha sido recibida de manera confidencial y protegida. Guarde su código para consultar el estado.",
        status=tip.status,
        created_at=tip.created_at
    )

@router.get("/track/{tip_code}", response_model=TipTrackResponse)
def track_tip_status(tip_code: str, db: Session = Depends(get_db)):
    """
    Consulta anónima del estado de trámite de una pista ciudadana.
    No expone ningún dato sensible de la investigación.
    """
    tip = db.query(ConfidentialTip).filter(ConfidentialTip.tip_code == tip_code.strip().upper()).first()
    if not tip:
        raise HTTPException(
            status_code=404,
            detail="No se encontró ninguna pista asociada al código suministrado."
        )
        
    status_messages = {
        TipStatus.RECEIVED.value: "Su pista ha sido registrada y está en cola de evaluación por el equipo de moderación.",
        TipStatus.TRIAGED.value: "La información ha sido evaluada y verificada preliminarmente.",
        TipStatus.ESCALATED.value: "La información ha sido canalizada formalmente con las entidades correspondientes.",
        TipStatus.DISCARDED.value: "La pista fue revisada pero no se encontraron elementos suficientes de coincidencia."
    }
    
    return TipTrackResponse(
        tip_code=tip.tip_code,
        status=tip.status,
        created_at=tip.created_at,
        message=status_messages.get(tip.status, "En proceso de revisión.")
    )
