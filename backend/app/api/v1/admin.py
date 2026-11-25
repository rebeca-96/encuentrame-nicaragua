from datetime import datetime, timezone
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status, Query, Request
from sqlalchemy.orm import Session
from sqlalchemy import desc
from app.core.database import get_db
from app.models.entities import (
    MissingPersonReport, ReportStatus, ModerationReview, 
    ReportStatusHistory, ConfidentialTip, AuditLog, User,
    GeographicLocation, DeletionRequest, DeletionStatus
)
from app.schemas.schemas import (
    ModerationAction, AuditLogItem, SystemMetricsResponse, 
    TipAdminDetail, ReportDetailAdmin, ReportPhotoResponse,
    DeletionRequestResponse
)
from app.api.deps import require_moderator, require_admin
from app.services.audit_service import log_audit_event

router = APIRouter(prefix="/admin", tags=["Administración y Moderación"])

@router.get("/metrics", response_model=SystemMetricsResponse)
def get_system_metrics(
    db: Session = Depends(get_db),
    current_user: User = Depends(require_moderator)
):
    """Estadísticas operativas consolidadas para el panel de control."""
    total_rep = db.query(MissingPersonReport).count()
    pending = db.query(MissingPersonReport).filter(MissingPersonReport.status == ReportStatus.PENDING_REVIEW.value).count()
    approved = db.query(MissingPersonReport).filter(MissingPersonReport.status == ReportStatus.APPROVED_PUBLISHED.value).count()
    closed_f = db.query(MissingPersonReport).filter(MissingPersonReport.status == ReportStatus.CLOSED_FOUND.value).count()
    closed_r = db.query(MissingPersonReport).filter(MissingPersonReport.status == ReportStatus.CLOSED_RESOLVED.value).count()
    rejected = db.query(MissingPersonReport).filter(MissingPersonReport.status == ReportStatus.REJECTED.value).count()
    total_tips = db.query(ConfidentialTip).count()
    total_users = db.query(User).count()
    
    return SystemMetricsResponse(
        total_reports=total_rep,
        pending_review=pending,
        approved_published=approved,
        closed_found=closed_f,
        closed_resolved=closed_r,
        rejected=rejected,
        total_tips=total_tips,
        total_users=total_users
    )

@router.get("/reports/pending", response_model=List[ReportDetailAdmin])
def list_pending_reports(
    db: Session = Depends(get_db),
    current_user: User = Depends(require_moderator)
):
    """Lista de reportes en cola de moderación pendientes de validación."""
    reports = db.query(MissingPersonReport).filter(
        MissingPersonReport.status == ReportStatus.PENDING_REVIEW.value
    ).order_by(desc(MissingPersonReport.created_at)).all()
    
    results = []
    for r in reports:
        photos_resp = [
            ReportPhotoResponse(
                id=p.id,
                storage_key=p.storage_key,
                url=f"/api/v1/reports/photos/{p.storage_key}",
                is_primary=p.is_primary,
                original_filename=p.original_filename
            ) for p in r.photos
        ]
        
        reporter_name = r.reporter.full_name if r.reporter else "Desconocido"
        reporter_email = r.reporter.email if r.reporter else ""
        reporter_phone = r.reporter.phone_number if r.reporter else ""
        rel = r.consent_record.relationship_to_victim if r.consent_record else "No especificada"
        
        results.append(ReportDetailAdmin(
            id=r.id,
            case_number=r.case_number,
            first_name=r.first_name,
            last_name=r.last_name,
            nickname=r.nickname,
            age_at_disappearance=r.age_at_disappearance,
            gender=r.gender,
            disappearance_date=r.disappearance_date,
            department=r.location.department,
            municipality=r.location.municipality,
            neighborhood_zone=r.location.neighborhood_zone,
            approximate_latitude=r.location.approximate_latitude,
            approximate_longitude=r.location.approximate_longitude,
            physical_description=r.physical_description,
            clothing_description=r.clothing_description,
            circumstances=r.circumstances,
            medical_conditions=r.medical_conditions,
            is_minor=r.is_minor,
            vulnerability_flag=r.vulnerability_flag,
            status=r.status,
            published_at=r.published_at,
            photos=photos_resp,
            reporter_id=r.reporter_id,
            reporter_name=reporter_name,
            reporter_email=reporter_email,
            reporter_phone=reporter_phone,
            relationship_to_victim=rel,
            created_at=r.created_at,
            updated_at=r.updated_at,
            moderation_notes=None
        ))
    return results

@router.post("/reports/{report_id}/moderate")
def moderate_report(
    report_id: str,
    action: ModerationAction,
    request: Request,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_moderator)
):
    """
    Decisión de moderación humana:
    - 'approve': Publica el caso oficialmente y lo habilita en el buscador y mapa.
    - 'reject': Rechaza el caso impidiendo su difusión con justificación.
    - 'request_changes': Regresa a estado borrador para corrección de datos.
    """
    report = db.query(MissingPersonReport).filter(MissingPersonReport.id == report_id).first()
    if not report:
        raise HTTPException(status_code=404, detail="Reporte no encontrado")
        
    prev_status = report.status
    
    if action.decision == "approve":
        report.status = ReportStatus.APPROVED_PUBLISHED.value
        report.is_public = True
        report.published_at = datetime.now(timezone.utc)
    elif action.decision == "reject":
        report.status = ReportStatus.REJECTED.value
        report.is_public = False
    elif action.decision == "request_changes":
        report.status = ReportStatus.DRAFT.value
        report.is_public = False
        
    # Moderation review record
    review = ModerationReview(
        report_id=report.id,
        moderator_id=current_user.id,
        decision=action.decision,
        notes_internal=action.notes_internal,
        rejection_reason=action.rejection_reason
    )
    db.add(review)
    
    # Status history log
    history = ReportStatusHistory(
        report_id=report.id,
        changed_by=current_user.id,
        previous_status=prev_status,
        new_status=report.status,
        reason=f"Decisión de moderación: {action.decision}. Notas: {action.notes_internal or 'Sin notas'}"
    )
    db.add(history)
    db.commit()
    db.refresh(report)
    
    log_audit_event(
        db=db,
        action=f"REPORT_MODERATED_{action.decision.upper()}",
        entity_name="missing_person_reports",
        entity_id=report.id,
        user_id=current_user.id,
        ip_address=request.client.host if request.client else None,
        details={"case_number": report.case_number, "decision": action.decision}
    )
    
    return {
        "message": f"Reporte moderado exitosamente. Nuevo estado: {report.status}",
        "report_id": report.id,
        "status": report.status,
        "is_public": report.is_public
    }

@router.get("/tips", response_model=List[TipAdminDetail])
def list_tips_for_admin(
    status_filter: Optional[str] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_moderator)
):
    """
    Lista y triaje de pistas confidenciales.
    ACCESO EXCLUSIVO: Solo usuarios con rol moderador o administrador.
    """
    query = db.query(ConfidentialTip).join(MissingPersonReport)
    if status_filter:
        query = query.filter(ConfidentialTip.status == status_filter)
        
    tips = query.order_by(desc(ConfidentialTip.created_at)).all()
    
    # Audit access to confidential tips
    log_audit_event(
        db=db,
        action="VIEW_CONFIDENTIAL_TIPS_LIST",
        entity_name="confidential_tips",
        entity_id="ALL",
        user_id=current_user.id
    )
    
    results = []
    for t in tips:
        results.append(TipAdminDetail(
            id=t.id,
            tip_code=t.tip_code,
            report_id=t.report_id,
            case_number=t.report.case_number,
            missing_person_name=f"{t.report.first_name} {t.report.last_name}",
            description=t.description,
            sighting_date=t.sighting_date,
            informant_contact=t.informant_contact,
            confidentiality_level=t.confidentiality_level,
            status=t.status,
            created_at=t.created_at
        ))
    return results

@router.patch("/tips/{tip_id}/status")
def update_tip_status(
    tip_id: str,
    new_status: str = Query(..., pattern="^(received|triaged|escalated|discarded)$"),
    db: Session = Depends(get_db),
    current_user: User = Depends(require_moderator)
):
    """Actualiza el estado de investigación y triaje de una pista."""
    tip = db.query(ConfidentialTip).filter(ConfidentialTip.id == tip_id).first()
    if not tip:
        raise HTTPException(status_code=404, detail="Pista no encontrada")
        
    tip.status = new_status
    tip.reviewed_by = current_user.id
    db.commit()
    
    log_audit_event(
        db=db,
        action="TIP_STATUS_UPDATED",
        entity_name="confidential_tips",
        entity_id=tip.id,
        user_id=current_user.id,
        details={"tip_code": tip.tip_code, "new_status": new_status}
    )
    
    return {"message": "Estado de la pista actualizado", "tip_code": tip.tip_code, "status": tip.status}

@router.get("/audit-logs", response_model=List[AuditLogItem])
def list_audit_logs(
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=200),
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin)
):
    """Consulta de logs inmutables de auditoría (exclusivo para Administrador General)."""
    logs = db.query(AuditLog).order_by(desc(AuditLog.created_at)).offset(skip).limit(limit).all()
    
    return [
        AuditLogItem(
            id=log.id,
            user_email=log.user.email if log.user else "Sistema / Anónimo",
            action=log.action,
            entity_name=log.entity_name,
            entity_id=log.entity_id,
            ip_address=log.ip_address,
            details_json=log.details_json,
            created_at=log.created_at
        ) for log in logs
    ]


@router.get("/deletion-requests", response_model=List[DeletionRequestResponse])
def list_deletion_requests(
    db: Session = Depends(get_db),
    current_user: User = Depends(require_moderator)
):
    """
    Lista las solicitudes ciudadanas de supresión de datos y derecho al olvido (Ley N.° 787).
    """
    requests = db.query(DeletionRequest).order_by(desc(DeletionRequest.created_at)).all()
    return [
        DeletionRequestResponse(
            id=req.id,
            report_id=req.report_id,
            case_number=req.report.case_number if req.report else None,
            reason=req.reason,
            status=req.status,
            created_at=req.created_at,
            message="Solicitud registrada."
        ) for req in requests
    ]


@router.patch("/deletion-requests/{request_id}/status")
def resolve_deletion_request(
    request_id: str,
    action: str = Query(..., pattern="^(processed|denied)$", description="'processed' para suprimir o 'denied' para rechazar"),
    db: Session = Depends(get_db),
    current_user: User = Depends(require_moderator)
):
    """
    Resuelve administrativamente una solicitud de supresión de datos conforme a la Ley 787.
    Si se procesa, garantiza que el expediente sea retirado permanentemente de difusión pública.
    """
    del_req = db.query(DeletionRequest).filter(DeletionRequest.id == request_id).first()
    if not del_req:
        raise HTTPException(status_code=404, detail="Solicitud de supresión no encontrada")

    del_req.status = action
    del_req.processed_by = current_user.id
    del_req.resolved_at = datetime.now(timezone.utc)

    if action == "processed" and del_req.report:
        del_req.report.is_public = False
        del_req.report.status = ReportStatus.CLOSED_RESOLVED.value

    db.commit()

    log_audit_event(
        db=db,
        action=f"DATA_DELETION_{action.upper()}",
        entity_name="deletion_requests",
        entity_id=del_req.id,
        user_id=current_user.id,
        details={"report_id": del_req.report_id, "action": action}
    )

    return {
        "message": f"Solicitud de supresión de datos actualizada como '{action}'.",
        "request_id": del_req.id,
        "status": del_req.status
    }
