from typing import Optional, Any
from sqlalchemy.orm import Session
from app.models.entities import AuditLog

def log_audit_event(
    db: Session,
    action: str,
    entity_name: str,
    entity_id: str,
    user_id: Optional[str] = None,
    ip_address: Optional[str] = None,
    user_agent: Optional[str] = None,
    details: Optional[Any] = None
) -> AuditLog:
    log_entry = AuditLog(
        user_id=user_id,
        action=action,
        entity_name=entity_name,
        entity_id=str(entity_id),
        ip_address=ip_address,
        user_agent=user_agent,
        details_json=details
    )
    db.add(log_entry)
    db.commit()
    db.refresh(log_entry)
    return log_entry
