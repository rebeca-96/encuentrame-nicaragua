from typing import List, Optional
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from sqlalchemy import or_, desc
from app.core.database import get_db
from app.models.entities import MissingPersonReport, GeographicLocation, ReportStatus
from app.schemas.schemas import ReportPublicListItem

router = APIRouter(prefix="/search", tags=["Buscador Inteligente"])

@router.get("/", response_model=List[ReportPublicListItem])
def search_reports(
    q: Optional[str] = Query(None, description="Término de búsqueda: nombre, apodo o rasgos"),
    department: Optional[str] = None,
    municipality: Optional[str] = None,
    gender: Optional[str] = None,
    is_minor: Optional[bool] = None,
    age_min: Optional[int] = None,
    age_max: Optional[int] = None,
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    db: Session = Depends(get_db)
):
    """
    Búsqueda multifiltro tolerante y combinada sobre reportes aprobados y públicos.
    """
    query = db.query(MissingPersonReport).join(GeographicLocation).filter(
        MissingPersonReport.is_public == True,
        MissingPersonReport.status.in_([
            ReportStatus.APPROVED_PUBLISHED.value,
            ReportStatus.UNDER_INVESTIGATION.value
        ])
    )
    
    if q and q.strip():
        term = f"%{q.strip()}%"
        query = query.filter(
            or_(
                MissingPersonReport.first_name.ilike(term),
                MissingPersonReport.last_name.ilike(term),
                MissingPersonReport.nickname.ilike(term),
                MissingPersonReport.case_number.ilike(term),
                MissingPersonReport.physical_description.ilike(term),
                MissingPersonReport.clothing_description.ilike(term),
                MissingPersonReport.circumstances.ilike(term)
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
        
    reports = query.order_by(desc(MissingPersonReport.published_at)).offset(skip).limit(limit).all()
    
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

@router.get("/semantic", response_model=List[ReportPublicListItem])
def semantic_search_reports(
    description_query: str = Query(..., min_length=3, description="Descripción semántica o rasgos"),
    department: Optional[str] = None,
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=50),
    db: Session = Depends(get_db)
):
    """
    Búsqueda semántica asistida basada en rasgos físicos particulares (tatuajes, lunares, cicatrices, contextura).
    """
    tokens = [t.strip() for t in description_query.split() if len(t.strip()) > 3]
    if not tokens:
        tokens = [description_query.strip()]
        
    query = db.query(MissingPersonReport).join(GeographicLocation).filter(
        MissingPersonReport.is_public == True,
        MissingPersonReport.status.in_([
            ReportStatus.APPROVED_PUBLISHED.value,
            ReportStatus.UNDER_INVESTIGATION.value
        ])
    )
    
    if department:
        query = query.filter(GeographicLocation.department.ilike(f"%{department}%"))
        
    clauses = []
    for t in tokens:
        term = f"%{t}%"
        clauses.append(MissingPersonReport.physical_description.ilike(term))
        clauses.append(MissingPersonReport.clothing_description.ilike(term))
        clauses.append(MissingPersonReport.circumstances.ilike(term))
        
    query = query.filter(or_(*clauses))
    reports = query.order_by(desc(MissingPersonReport.published_at)).offset(skip).limit(limit).all()
    
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
