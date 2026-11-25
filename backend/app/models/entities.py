import uuid
from datetime import datetime, timezone
from sqlalchemy import (
    Column, String, Integer, Float, Boolean, DateTime, Date, 
    Text, ForeignKey, Enum as SQLEnum, JSON, UniqueConstraint
)
from sqlalchemy.orm import relationship
import enum
from app.core.database import Base

def generate_uuid() -> str:
    return str(uuid.uuid4())

class UserRole(str, enum.Enum):
    ADMIN = "admin"
    MODERATOR = "moderator"
    REPORTER = "reporter"
    CITIZEN = "citizen"

class ReportStatus(str, enum.Enum):
    DRAFT = "draft"
    PENDING_REVIEW = "pending_review"
    UNDER_INVESTIGATION = "under_investigation"
    APPROVED_PUBLISHED = "approved_published"
    REJECTED = "rejected"
    CLOSED_FOUND = "closed_found"
    CLOSED_RESOLVED = "closed_resolved"

class GenderEnum(str, enum.Enum):
    MALE = "male"
    FEMALE = "female"
    NON_BINARY = "non_binary"
    UNSPECIFIED = "unspecified"

class TipStatus(str, enum.Enum):
    RECEIVED = "received"
    TRIAGED = "triaged"
    ESCALATED = "escalated"
    DISCARDED = "discarded"

class ConfidentialityLevel(str, enum.Enum):
    STRICT_ANONYMOUS = "strict_anonymous"
    CONTACTABLE_MODERATOR_ONLY = "contactable_moderator_only"

class ModerationDecision(str, enum.Enum):
    APPROVE = "approve"
    REJECT = "reject"
    REQUEST_CHANGES = "request_changes"

class DeletionStatus(str, enum.Enum):
    PENDING = "pending"
    PROCESSED = "processed"
    DENIED = "denied"

class TerritorialType(str, enum.Enum):
    DEPARTMENT = "department"
    AUTONOMOUS_REGION = "autonomous_region"


class Department(Base):
    __tablename__ = "departments"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    name = Column(String(100), unique=True, index=True, nullable=False)
    code = Column(String(10), unique=True, index=True, nullable=False)
    type = Column(String(32), default=TerritorialType.DEPARTMENT.value, nullable=False)
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)
    updated_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

    municipalities = relationship("Municipality", back_populates="department", cascade="all, delete-orphan")


class Municipality(Base):
    __tablename__ = "municipalities"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    department_id = Column(String(36), ForeignKey("departments.id"), index=True, nullable=False)
    name = Column(String(100), index=True, nullable=False)
    code = Column(String(15), unique=True, index=True, nullable=False)
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)
    updated_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

    __table_args__ = (
        UniqueConstraint("department_id", "name", name="uq_department_municipality_name"),
    )

    department = relationship("Department", back_populates="municipalities")


class User(Base):
    __tablename__ = "users"
    
    id = Column(String(36), primary_key=True, default=generate_uuid)
    email = Column(String(255), unique=True, index=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    full_name = Column(String(255), nullable=False)
    phone_number = Column(String(100), nullable=True)  # Encrypted in production
    role = Column(String(32), default=UserRole.CITIZEN.value, nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)
    is_verified = Column(Boolean, default=False, nullable=False)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)
    updated_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

    reports = relationship("MissingPersonReport", back_populates="reporter")
    audit_logs = relationship("AuditLog", back_populates="user")
    subscriptions = relationship("NotificationSubscription", back_populates="user")


class GeographicLocation(Base):
    __tablename__ = "geographic_locations"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    department = Column(String(100), index=True, nullable=False)
    municipality = Column(String(100), index=True, nullable=False)
    neighborhood_zone = Column(String(150), nullable=True)
    approximate_latitude = Column(Float, nullable=False)
    approximate_longitude = Column(Float, nullable=False)
    is_sensitive = Column(Boolean, default=True, nullable=False)

    reports = relationship("MissingPersonReport", back_populates="location")


class MissingPersonReport(Base):
    __tablename__ = "missing_person_reports"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    case_number = Column(String(32), unique=True, index=True, nullable=False)
    reporter_id = Column(String(36), ForeignKey("users.id"), index=True, nullable=False)
    status = Column(String(32), default=ReportStatus.PENDING_REVIEW.value, index=True, nullable=False)
    
    first_name = Column(String(100), nullable=False)
    last_name = Column(String(100), nullable=False)
    nickname = Column(String(100), nullable=True)
    age_at_disappearance = Column(Integer, nullable=False)
    birth_date = Column(Date, nullable=True)
    gender = Column(String(32), default=GenderEnum.UNSPECIFIED.value, nullable=False)
    disappearance_date = Column(DateTime, nullable=False)
    
    location_id = Column(String(36), ForeignKey("geographic_locations.id"), index=True, nullable=False)
    physical_description = Column(Text, nullable=False)
    clothing_description = Column(Text, nullable=False)
    medical_conditions = Column(Text, nullable=True)
    circumstances = Column(Text, nullable=False)
    
    is_minor = Column(Boolean, default=False, nullable=False)
    vulnerability_flag = Column(Boolean, default=False, nullable=False)
    is_public = Column(Boolean, default=False, index=True, nullable=False)
    published_at = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)
    updated_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

    # Relationships
    reporter = relationship("User", back_populates="reports")
    location = relationship("GeographicLocation", back_populates="reports")
    photos = relationship("ReportPhoto", back_populates="report", cascade="all, delete-orphan")
    status_history = relationship("ReportStatusHistory", back_populates="report", cascade="all, delete-orphan")
    tips = relationship("ConfidentialTip", back_populates="report", cascade="all, delete-orphan")
    moderation_reviews = relationship("ModerationReview", back_populates="report", cascade="all, delete-orphan")
    consent_record = relationship("ConsentRecord", back_populates="report", uselist=False, cascade="all, delete-orphan")
    ai_results = relationship("AIAnalysisResult", foreign_keys="AIAnalysisResult.report_id", back_populates="report")
    deletion_requests = relationship("DeletionRequest", back_populates="report", cascade="all, delete-orphan")


class ReportPhoto(Base):
    __tablename__ = "report_photos"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    report_id = Column(String(36), ForeignKey("missing_person_reports.id"), nullable=False)
    storage_key = Column(String(255), nullable=False)
    is_primary = Column(Boolean, default=False, nullable=False)
    is_approved = Column(Boolean, default=False, nullable=False)
    blur_level = Column(Integer, default=0, nullable=False)
    original_filename = Column(String(255), nullable=False)
    file_hash_sha256 = Column(String(64), nullable=False)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)

    report = relationship("MissingPersonReport", back_populates="photos")


class ConfidentialTip(Base):
    __tablename__ = "confidential_tips"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    report_id = Column(String(36), ForeignKey("missing_person_reports.id"), nullable=False)
    tip_code = Column(String(32), unique=True, index=True, nullable=False)
    description = Column(Text, nullable=False)
    sighting_date = Column(DateTime, nullable=True)
    sighting_location_id = Column(String(36), ForeignKey("geographic_locations.id"), nullable=True)
    informant_contact = Column(String(255), nullable=True)
    confidentiality_level = Column(String(32), default=ConfidentialityLevel.STRICT_ANONYMOUS.value, nullable=False)
    status = Column(String(32), default=TipStatus.RECEIVED.value, nullable=False)
    reviewed_by = Column(String(36), ForeignKey("users.id"), nullable=True)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)

    report = relationship("MissingPersonReport", back_populates="tips")
    sightings = relationship("Sighting", back_populates="tip", cascade="all, delete-orphan")


class Sighting(Base):
    __tablename__ = "sightings"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    tip_id = Column(String(36), ForeignKey("confidential_tips.id"), nullable=False)
    evidence_storage_key = Column(String(255), nullable=True)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)

    tip = relationship("ConfidentialTip", back_populates="sightings")


class ReportStatusHistory(Base):
    __tablename__ = "report_status_history"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    report_id = Column(String(36), ForeignKey("missing_person_reports.id"), nullable=False)
    changed_by = Column(String(36), ForeignKey("users.id"), nullable=False)
    previous_status = Column(String(32), nullable=False)
    new_status = Column(String(32), nullable=False)
    reason = Column(Text, nullable=True)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)

    report = relationship("MissingPersonReport", back_populates="status_history")


class ModerationReview(Base):
    __tablename__ = "moderation_reviews"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    report_id = Column(String(36), ForeignKey("missing_person_reports.id"), nullable=False)
    moderator_id = Column(String(36), ForeignKey("users.id"), nullable=False)
    decision = Column(String(32), nullable=False)
    notes_internal = Column(Text, nullable=True)
    rejection_reason = Column(Text, nullable=True)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)

    report = relationship("MissingPersonReport", back_populates="moderation_reviews")


class ConsentRecord(Base):
    __tablename__ = "consent_records"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    report_id = Column(String(36), ForeignKey("missing_person_reports.id"), nullable=False)
    reporter_id = Column(String(36), ForeignKey("users.id"), nullable=False)
    relationship_to_victim = Column(String(100), nullable=False)
    identity_doc_hash = Column(String(64), nullable=False)
    consent_text_version = Column(String(32), default="v1.0-Ley787", nullable=False)
    accepted_terms_timestamp = Column(DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)
    ip_address_hash = Column(String(64), nullable=False)

    report = relationship("MissingPersonReport", back_populates="consent_record")


class DeletionRequest(Base):
    __tablename__ = "deletion_requests"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    report_id = Column(String(36), ForeignKey("missing_person_reports.id"), nullable=False)
    requested_by = Column(String(36), ForeignKey("users.id"), nullable=False)
    reason = Column(Text, nullable=False)
    status = Column(String(32), default=DeletionStatus.PENDING.value, nullable=False)
    processed_by = Column(String(36), ForeignKey("users.id"), nullable=True)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)
    resolved_at = Column(DateTime, nullable=True)

    report = relationship("MissingPersonReport", back_populates="deletion_requests")


class NotificationSubscription(Base):
    __tablename__ = "notification_subscriptions"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    user_id = Column(String(36), ForeignKey("users.id"), nullable=True)
    email = Column(String(255), index=True, nullable=False)
    department = Column(String(100), nullable=True)
    is_active = Column(Boolean, default=True, nullable=False)
    token_unsubscribe = Column(String(64), unique=True, nullable=False)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)

    user = relationship("User", back_populates="subscriptions")
    notifications = relationship("Notification", back_populates="subscription", cascade="all, delete-orphan")


class Notification(Base):
    __tablename__ = "notifications"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    subscription_id = Column(String(36), ForeignKey("notification_subscriptions.id"), nullable=False)
    type = Column(String(50), nullable=False)
    title = Column(String(255), nullable=False)
    content = Column(Text, nullable=False)
    sent_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)
    status = Column(String(32), default="sent", nullable=False)

    subscription = relationship("NotificationSubscription", back_populates="notifications")


class AuditLog(Base):
    __tablename__ = "audit_logs"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    user_id = Column(String(36), ForeignKey("users.id"), nullable=True)
    action = Column(String(100), index=True, nullable=False)
    entity_name = Column(String(100), nullable=False)
    entity_id = Column(String(36), nullable=False)
    ip_address = Column(String(45), nullable=True)
    user_agent = Column(String(255), nullable=True)
    details_json = Column(JSON, nullable=True)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), index=True, nullable=False)

    user = relationship("User", back_populates="audit_logs")


class AIAnalysisResult(Base):
    __tablename__ = "ai_analysis_results"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    report_id = Column(String(36), ForeignKey("missing_person_reports.id"), nullable=False)
    potential_duplicate_report_id = Column(String(36), ForeignKey("missing_person_reports.id"), nullable=True)
    similarity_score = Column(Float, nullable=True)
    suggested_tags = Column(JSON, nullable=True)
    completeness_score = Column(Float, default=1.0, nullable=False)
    summary_for_moderator = Column(Text, nullable=True)
    evaluated_by_human = Column(Boolean, default=False, nullable=False)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)

    report = relationship("MissingPersonReport", foreign_keys=[report_id], back_populates="ai_results")
