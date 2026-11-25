from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.entities import MissingPersonReport, User
from app.schemas.schemas import AIDuplicateCheckResponse, AISummaryResponse
from app.api.deps import require_moderator
from app.services.ai_service import detect_duplicates, generate_moderator_summary

router = APIRouter(prefix="/ai", tags=["Herramientas de IA Supervisada"])

@router.post("/check-duplicates/{report_id}", response_model=AIDuplicateCheckResponse)
def check_report_duplicates(
    report_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_moderator)
):
    """
    Analiza de forma asistida si el reporte presenta coincidencias semánticas o
    nominales con otros casos existentes, para prevenir duplicaciones.
    IMPORTANTE: La IA asiste y sugiere coincidencias, la decisión final es estrictamente humana.
    """
    report = db.query(MissingPersonReport).filter(MissingPersonReport.id == report_id).first()
    if not report:
        raise HTTPException(status_code=404, detail="Reporte no encontrado")
        
    return detect_duplicates(db, report)

@router.get("/summary/{report_id}", response_model=AISummaryResponse)
def get_case_summary(
    report_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_moderator)
):
    """
    Genera una ficha sintética y lista de chequeo de completitud para asistir la revisión del moderador.
    """
    report = db.query(MissingPersonReport).filter(MissingPersonReport.id == report_id).first()
    if not report:
        raise HTTPException(status_code=404, detail="Reporte no encontrado")
        
    return generate_moderator_summary(report)
