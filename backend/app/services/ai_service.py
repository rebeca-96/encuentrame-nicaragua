import re
from typing import List, Dict, Any, Tuple
from sqlalchemy.orm import Session
from app.models.entities import MissingPersonReport, ReportStatus
from app.schemas.schemas import DuplicateMatch, AIDuplicateCheckResponse, AISummaryResponse

def _normalize_text(text: str) -> str:
    if not text:
        return ""
    text = text.lower().strip()
    text = re.sub(r'[áàä]', 'a', text)
    text = re.sub(r'[éèë]', 'e', text)
    text = re.sub(r'[íìï]', 'i', text)
    text = re.sub(r'[óòö]', 'o', text)
    text = re.sub(r'[úùü]', 'u', text)
    text = re.sub(r'[^a-z0-9\s]', '', text)
    return text

def _calculate_string_similarity(str1: str, str2: str) -> float:
    s1 = set(_normalize_text(str1).split())
    s2 = set(_normalize_text(str2).split())
    if not s1 or not s2:
        return 0.0
    intersection = s1.intersection(s2)
    union = s1.union(s2)
    return len(intersection) / len(union)

def detect_duplicates(
    db: Session, 
    report: MissingPersonReport, 
    threshold: float = 0.50
) -> AIDuplicateCheckResponse:
    """
    Evaluates existing reports to find potential duplicates based on:
    - Name token similarity
    - Age closeness (+/- 2 years)
    - Geographical match (same department or municipality)
    - Physical description matching tokens
    """
    candidates = db.query(MissingPersonReport).filter(
        MissingPersonReport.id != report.id,
        MissingPersonReport.status.in_([
            ReportStatus.PENDING_REVIEW.value,
            ReportStatus.APPROVED_PUBLISHED.value,
            ReportStatus.UNDER_INVESTIGATION.value
        ])
    ).all()
    
    matches: List[DuplicateMatch] = []
    
    rep_full_name = f"{report.first_name} {report.last_name}"
    
    for candidate in candidates:
        cand_full_name = f"{candidate.first_name} {candidate.last_name}"
        name_sim = _calculate_string_similarity(rep_full_name, cand_full_name)
        
        reasons = []
        score = 0.0
        
        # Name score (weight 0.50)
        if name_sim >= 0.8:
            score += 0.50
            reasons.append("Nombre y apellidos altamente coincidentes")
        elif name_sim >= 0.5:
            score += 0.30
            reasons.append("Coincidencia parcial en nombres")
            
        # Age score (weight 0.20)
        age_diff = abs(report.age_at_disappearance - candidate.age_at_disappearance)
        if age_diff == 0:
            score += 0.20
            reasons.append("Misma edad registrada")
        elif age_diff <= 2:
            score += 0.10
            reasons.append("Edad aproximada dentro de ±2 años")
            
        # Location score (weight 0.20)
        if (report.location and candidate.location and 
            report.location.department.lower() == candidate.location.department.lower()):
            score += 0.15
            reasons.append(f"Mismo departamento ({report.location.department})")
            if report.location.municipality.lower() == candidate.location.municipality.lower():
                score += 0.05
                reasons.append(f"Mismo municipio ({report.location.municipality})")
                
        # Description tokens (weight 0.10)
        desc_sim = _calculate_string_similarity(
            report.physical_description, 
            candidate.physical_description
        )
        if desc_sim > 0.3:
            score += 0.10
            reasons.append("Similitud en señas y descripción física")
            
        if score >= threshold:
            matches.append(DuplicateMatch(
                existing_report_id=candidate.id,
                case_number=candidate.case_number,
                full_name=cand_full_name,
                similarity_score=round(score, 2),
                reasons=reasons
            ))
            
    matches.sort(key=lambda x: x.similarity_score, reverse=True)
    has_high = any(m.similarity_score >= 0.75 for m in matches)
    
    return AIDuplicateCheckResponse(
        report_id=report.id,
        potential_duplicates=matches,
        has_high_confidence_duplicate=has_high
    )

def generate_moderator_summary(report: MissingPersonReport) -> AISummaryResponse:
    """
    Generates a structured, human-in-the-loop executive summary for moderators.
    Highlights critical vulnerabilities, physical markers, and data completeness.
    """
    missing_fields = []
    score = 1.0
    
    if not report.clothing_description or len(report.clothing_description) < 15:
        missing_fields.append("Descripción de vestimenta poco detallada")
        score -= 0.15
        
    if not report.medical_conditions:
        missing_fields.append("No se indicaron condiciones médicas o necesidad de medicamentos")
        score -= 0.10
        
    if not report.photos or len(report.photos) == 0:
        missing_fields.append("Falta fotografía autorizada para publicación")
        score -= 0.25
        
    priority = "Normal"
    if report.is_minor:
        priority = "URGENTE — Menor de edad"
    elif report.vulnerability_flag or (report.age_at_disappearance >= 65):
        priority = "ALTA — Persona en situación de vulnerabilidad o adulto mayor"
        
    loc_str = f"{report.location.municipality}, {report.location.department}" if report.location else "Nicaragua"
    
    summary_text = (
        f"Ficha Asistida de Revisión: {report.first_name} {report.last_name} ({report.age_at_disappearance} años). "
        f"Última ubicación: {loc_str}, fecha: {report.disappearance_date.strftime('%d/%m/%Y')}. "
        f"Características principales: {report.physical_description[:160]}... "
        f"Prioridad sugerida: {priority}."
    )
    
    return AISummaryResponse(
        report_id=report.id,
        case_number=report.case_number,
        summary_text=summary_text,
        completeness_score=max(0.2, round(score, 2)),
        missing_or_weak_fields=missing_fields,
        suggested_priority=priority
    )
