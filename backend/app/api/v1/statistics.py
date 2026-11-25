from typing import Dict, List
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func
from app.core.database import get_db
from app.models.entities import MissingPersonReport, GeographicLocation, ReportStatus

router = APIRouter(prefix="/statistics", tags=["Estadísticas Agregadas"])

@router.get("/by-department")
def get_stats_by_department(db: Session = Depends(get_db)):
    """
    Retorna el total de casos autorizados agrupados por departamento para gráficos y visualización cívica.
    """
    results = db.query(
        GeographicLocation.department,
        func.count(MissingPersonReport.id).label("total_cases")
    ).join(
        MissingPersonReport, MissingPersonReport.location_id == GeographicLocation.id
    ).filter(
        MissingPersonReport.is_public == True
    ).group_by(
        GeographicLocation.department
    ).all()
    
    return [{"department": r[0], "count": r[1]} for r in results]

@router.get("/summary-public")
def get_public_summary(db: Session = Depends(get_db)):
    """Resumen estadístico general público para la portada."""
    active_cases = db.query(MissingPersonReport).filter(
        MissingPersonReport.is_public == True,
        MissingPersonReport.status.in_([ReportStatus.APPROVED_PUBLISHED.value, ReportStatus.UNDER_INVESTIGATION.value])
    ).count()
    
    resolved_cases = db.query(MissingPersonReport).filter(
        MissingPersonReport.status.in_([ReportStatus.CLOSED_FOUND.value, ReportStatus.CLOSED_RESOLVED.value])
    ).count()
    
    minors_active = db.query(MissingPersonReport).filter(
        MissingPersonReport.is_public == True,
        MissingPersonReport.is_minor == True
    ).count()
    
    return {
        "active_cases": active_cases,
        "resolved_cases": resolved_cases,
        "minors_under_search": minors_active,
        "departments_covered": 17
    }
