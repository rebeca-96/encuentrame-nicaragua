import secrets
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.entities import NotificationSubscription
from app.schemas.schemas import NotificationSubscribeRequest, NotificationSubscriptionResponse
from app.services.audit_service import log_audit_event

router = APIRouter(prefix="/notifications", tags=["Notificaciones y Alertas"])

@router.post("/subscribe", response_model=NotificationSubscriptionResponse, status_code=status.HTTP_201_CREATED)
def subscribe_notification(
    data: NotificationSubscribeRequest,
    db: Session = Depends(get_db)
):
    """
    Permite a los ciudadanos registrarse voluntariamente para recibir alertas públicas de personas no localizadas.
    Cumple con la Ley N.° 787 de Protección de Datos Personales, proveyendo token de cancelación inmediata.
    """
    clean_email = data.email.lower().strip()
    clean_dept = data.department.strip() if data.department and data.department.lower() != "all" else None
    
    # Check if existing active subscription exists
    existing = db.query(NotificationSubscription).filter(
        NotificationSubscription.email == clean_email,
        NotificationSubscription.department == clean_dept
    ).first()
    
    if existing:
        if not existing.is_active:
            existing.is_active = True
            db.commit()
            db.refresh(existing)
        return NotificationSubscriptionResponse(
            id=existing.id,
            email=existing.email,
            department=existing.department,
            is_active=existing.is_active,
            token_unsubscribe=existing.token_unsubscribe,
            message="Su suscripción a alertas ya se encontraba activa o ha sido reactivada."
        )

    unsubscribe_token = secrets.token_hex(32)
    sub = NotificationSubscription(
        email=clean_email,
        department=clean_dept,
        is_active=True,
        token_unsubscribe=unsubscribe_token
    )
    db.add(sub)
    db.commit()
    db.refresh(sub)
    
    log_audit_event(
        db=db,
        action="SUBSCRIPTION_CREATED",
        entity_name="notification_subscriptions",
        entity_id=sub.id,
        details={"email": clean_email, "department": clean_dept}
    )
    
    return NotificationSubscriptionResponse(
        id=sub.id,
        email=sub.email,
        department=sub.department,
        is_active=sub.is_active,
        token_unsubscribe=sub.token_unsubscribe,
        message="Suscripción a alertas cívicas activada exitosamente."
    )

@router.get("/unsubscribe/{token}")
def unsubscribe_notification(token: str, db: Session = Depends(get_db)):
    """
    Permite a un usuario cancelar voluntariamente su suscripción de alertas mediante su token único.
    """
    sub = db.query(NotificationSubscription).filter(
        NotificationSubscription.token_unsubscribe == token.strip()
    ).first()
    
    if not sub:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="El enlace de cancelación no es válido o ya fue procesado."
        )
        
    sub.is_active = False
    db.commit()
    
    log_audit_event(
        db=db,
        action="SUBSCRIPTION_CANCELLED",
        entity_name="notification_subscriptions",
        entity_id=sub.id,
        details={"email": sub.email, "department": sub.department}
    )
    
    return {
        "status": "success",
        "message": f"Su suscripción de alertas para {sub.email} ha sido cancelada exitosamente."
    }
