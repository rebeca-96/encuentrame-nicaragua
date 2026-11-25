from datetime import datetime, date, timezone, timedelta
from typing import Optional, List, Any
import re
from pydantic import BaseModel, EmailStr, Field, ConfigDict, field_validator, model_validator
from app.services.geo_service import get_departments, get_municipalities

# --- Auth & User Schemas ---
class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"
    role: str
    user_id: str
    full_name: str

class TokenPayload(BaseModel):
    sub: Optional[str] = None
    role: Optional[str] = None

class LoginRequest(BaseModel):
    email: EmailStr
    password: str

class UserRegister(BaseModel):
    email: EmailStr
    password: str = Field(..., min_length=8)
    confirm_password: Optional[str] = None
    full_name: str = Field(..., min_length=3)
    phone_number: Optional[str] = None
    role: Optional[str] = "reporter"

    @field_validator("password")
    @classmethod
    def validate_password_strength(cls, v: str) -> str:
        if not re.search(r"[A-Z]", v):
            raise ValueError("La contraseña debe contener al menos una letra mayúscula")
        if not re.search(r"[a-z]", v):
            raise ValueError("La contraseña debe contener al menos una letra minúscula")
        if not re.search(r"\d", v):
            raise ValueError("La contraseña debe contener al menos un número")
        if not re.search(r"[@$!%*?&#_.:,;-]", v):
            raise ValueError("La contraseña debe contener al menos un carácter especial (@$!%*?&#_.:,;-)")
        return v

    @model_validator(mode="after")
    def check_passwords_match(self):
        if self.confirm_password is not None and self.password != self.confirm_password:
            raise ValueError("Las contraseñas ingresadas no coinciden")
        return self

class UserResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: str
    email: EmailStr
    full_name: str
    phone_number: Optional[str] = None
    role: str
    is_active: bool
    is_verified: bool
    created_at: datetime

# --- Location Schemas ---
class LocationBase(BaseModel):
    department: str
    municipality: str
    neighborhood_zone: Optional[str] = None
    approximate_latitude: float
    approximate_longitude: float

class LocationResponse(LocationBase):
    model_config = ConfigDict(from_attributes=True)
    id: str

class MapPointItem(BaseModel):
    id: str
    case_number: str
    full_name: str
    age_at_disappearance: int
    gender: str
    department: str
    municipality: str
    disappearance_date: datetime
    approximate_latitude: float
    approximate_longitude: float
    photo_url: Optional[str] = None
    is_minor: bool
    status: str

# --- Report Schemas ---
class ConsentInput(BaseModel):
    relationship_to_victim: str = Field(..., min_length=2)
    identity_doc_number: str = Field(..., min_length=5)
    accepted_terms: bool = Field(..., description="Aceptación de términos y Ley 787 de Nicaragua")

    @field_validator("accepted_terms")
    @classmethod
    def validate_consent_accepted(cls, v: bool) -> bool:
        if not v:
            raise ValueError("Debe aceptar expresamente los términos de consentimiento informado y la Ley 787")
        return v

class ReportCreate(BaseModel):
    first_name: str = Field(..., min_length=2)
    last_name: str = Field(..., min_length=2)
    nickname: Optional[str] = None
    age_at_disappearance: int = Field(..., ge=0, le=120)
    birth_date: Optional[date] = None
    gender: str = "unspecified"
    disappearance_date: datetime
    
    # Location
    department: str
    municipality: str
    neighborhood_zone: Optional[str] = None
    approximate_latitude: Optional[float] = None
    approximate_longitude: Optional[float] = None
    
    # Descriptive features
    physical_description: str = Field(..., min_length=10)
    clothing_description: str = Field(..., min_length=5)
    medical_conditions: Optional[str] = None
    circumstances: str = Field(..., min_length=15)
    
    is_minor: Optional[bool] = False
    vulnerability_flag: Optional[bool] = False
    
    # Consent
    consent: ConsentInput

    @field_validator("disappearance_date")
    @classmethod
    def validate_disappearance_date_not_future(cls, v: datetime) -> datetime:
        now_utc = datetime.now(timezone.utc)
        target_utc = v if v.tzinfo else v.replace(tzinfo=timezone.utc)
        if target_utc > (now_utc + timedelta(minutes=5)):
            raise ValueError("La fecha de desaparición no puede ser una fecha en el futuro.")
        if target_utc < datetime(1920, 1, 1, tzinfo=timezone.utc):
            raise ValueError("La fecha de desaparición es inverosímil (anterior a 1920).")
        return v

    @field_validator("department")
    @classmethod
    def validate_department_exists(cls, v: str) -> str:
        valid_departments = get_departments()
        matching = next((d for d in valid_departments if d.lower() == v.lower().strip()), None)
        if not matching:
            raise ValueError(f"El departamento '{v}' no es un departamento válido de Nicaragua.")
        return matching

    @model_validator(mode="after")
    def validate_municipality_matches_department(self):
        valid_muns = get_municipalities(self.department)
        if not valid_muns:
            raise ValueError(f"No se encontraron municipios para el departamento '{self.department}'.")
        matching_mun = next((m for m in valid_muns if m.lower() == self.municipality.lower().strip()), None)
        if not matching_mun:
            raise ValueError(
                f"El municipio '{self.municipality}' no pertenece al departamento de '{self.department}'."
            )
        self.municipality = matching_mun
        return self

class ReportUpdate(BaseModel):
    first_name: Optional[str] = Field(None, min_length=2)
    last_name: Optional[str] = Field(None, min_length=2)
    nickname: Optional[str] = None
    age_at_disappearance: Optional[int] = Field(None, ge=0, le=120)
    physical_description: Optional[str] = Field(None, min_length=10)
    clothing_description: Optional[str] = Field(None, min_length=5)
    medical_conditions: Optional[str] = None
    circumstances: Optional[str] = Field(None, min_length=15)
    neighborhood_zone: Optional[str] = None

class ReportPhotoResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: str
    storage_key: str
    url: str
    is_primary: bool
    original_filename: str

class ReportPublicListItem(BaseModel):
    id: str
    case_number: str
    first_name: str
    last_name: str
    age_at_disappearance: int
    gender: str
    disappearance_date: datetime
    department: str
    municipality: str
    physical_description: str
    primary_photo_url: Optional[str] = None
    is_minor: bool
    status: str
    published_at: Optional[datetime] = None

class ReportDetailPublic(BaseModel):
    id: str
    case_number: str
    first_name: str
    last_name: str
    nickname: Optional[str] = None
    age_at_disappearance: int
    gender: str
    disappearance_date: datetime
    department: str
    municipality: str
    neighborhood_zone: Optional[str] = None
    approximate_latitude: float
    approximate_longitude: float
    physical_description: str
    clothing_description: str
    circumstances: str
    medical_conditions: Optional[str] = None
    is_minor: bool
    vulnerability_flag: bool
    status: str
    published_at: Optional[datetime] = None
    photos: List[ReportPhotoResponse] = []

class ReportDetailAdmin(ReportDetailPublic):
    reporter_id: str
    reporter_name: Optional[str] = None
    reporter_email: Optional[str] = None
    reporter_phone: Optional[str] = None
    relationship_to_victim: Optional[str] = None
    created_at: datetime
    updated_at: datetime
    moderation_notes: Optional[str] = None

class CloseReportRequest(BaseModel):
    reason: str = Field(..., min_length=5)
    details: Optional[str] = None

# --- Confidential Tip Schemas ---
class TipCreate(BaseModel):
    report_id: str
    description: str = Field(..., min_length=10)
    sighting_date: Optional[datetime] = None
    sighting_department: Optional[str] = None
    sighting_municipality: Optional[str] = None
    informant_contact: Optional[str] = None
    confidentiality_level: Optional[str] = "strict_anonymous"

    @field_validator("sighting_date")
    @classmethod
    def validate_sighting_date_not_future(cls, v: Optional[datetime]) -> Optional[datetime]:
        if v is not None:
            now_utc = datetime.now(timezone.utc)
            target_utc = v if v.tzinfo else v.replace(tzinfo=timezone.utc)
            if target_utc > (now_utc + timedelta(minutes=5)):
                raise ValueError("La fecha de avistamiento no puede ser una fecha en el futuro.")
        return v

class TipCreateResponse(BaseModel):
    tip_code: str
    message: str
    status: str
    created_at: datetime

class TipTrackResponse(BaseModel):
    tip_code: str
    status: str
    created_at: datetime
    message: str

class TipAdminDetail(BaseModel):
    id: str
    tip_code: str
    report_id: str
    case_number: str
    missing_person_name: str
    description: str
    sighting_date: Optional[datetime] = None
    informant_contact: Optional[str] = None
    confidentiality_level: str
    status: str
    created_at: datetime

# --- Moderation & Admin Schemas ---
class ModerationAction(BaseModel):
    decision: str = Field(..., pattern="^(approve|reject|request_changes)$")
    notes_internal: Optional[str] = None
    rejection_reason: Optional[str] = None

class AuditLogItem(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: str
    user_email: Optional[str] = None
    action: str
    entity_name: str
    entity_id: str
    ip_address: Optional[str] = None
    details_json: Optional[Any] = None
    created_at: datetime

class SystemMetricsResponse(BaseModel):
    total_reports: int
    pending_review: int
    approved_published: int
    closed_found: int
    closed_resolved: int
    rejected: int
    total_tips: int
    total_users: int

# --- AI Schemas ---
class DuplicateMatch(BaseModel):
    existing_report_id: str
    case_number: str
    full_name: str
    similarity_score: float
    reasons: List[str]

class AIDuplicateCheckResponse(BaseModel):
    report_id: str
    potential_duplicates: List[DuplicateMatch]
    has_high_confidence_duplicate: bool

class AISummaryResponse(BaseModel):
    report_id: str
    case_number: str
    summary_text: str
    completeness_score: float
    missing_or_weak_fields: List[str]
    suggested_priority: str


# --- Geographic Schemas ---
class DepartmentBase(BaseModel):
    name: str = Field(..., min_length=2, max_length=100)
    code: str = Field(..., min_length=2, max_length=10, pattern=r"^[A-Z0-9_-]+$")
    type: str = Field(default="department", pattern=r"^(department|autonomous_region)$")
    latitude: float = Field(..., ge=10.70, le=15.10, description="Latitud en territorio nicaragüense")
    longitude: float = Field(..., ge=-87.70, le=-82.50, description="Longitud en territorio nicaragüense")

class DepartmentCreate(DepartmentBase):
    pass

class DepartmentUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=2, max_length=100)
    code: Optional[str] = Field(None, min_length=2, max_length=10, pattern=r"^[A-Z0-9_-]+$")
    type: Optional[str] = Field(None, pattern=r"^(department|autonomous_region)$")
    latitude: Optional[float] = Field(None, ge=10.70, le=15.10)
    longitude: Optional[float] = Field(None, ge=-87.70, le=-82.50)
    is_active: Optional[bool] = None

class DepartmentResponse(DepartmentBase):
    model_config = ConfigDict(from_attributes=True)
    id: str
    is_active: bool
    created_at: datetime
    updated_at: Optional[datetime] = None
    municipalities_count: Optional[int] = 0

class MunicipalityBase(BaseModel):
    name: str = Field(..., min_length=2, max_length=100)
    code: str = Field(..., min_length=2, max_length=15, pattern=r"^[A-Z0-9_-]+$")
    latitude: float = Field(..., ge=10.70, le=15.10, description="Latitud en territorio nicaragüense")
    longitude: float = Field(..., ge=-87.70, le=-82.50, description="Longitud en territorio nicaragüense")

class MunicipalityCreate(MunicipalityBase):
    department_id: str

class MunicipalityUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=2, max_length=100)
    department_id: Optional[str] = None
    code: Optional[str] = Field(None, min_length=2, max_length=15, pattern=r"^[A-Z0-9_-]+$")
    latitude: Optional[float] = Field(None, ge=10.70, le=15.10)
    longitude: Optional[float] = Field(None, ge=-87.70, le=-82.50)
    is_active: Optional[bool] = None

class MunicipalityResponse(MunicipalityBase):
    model_config = ConfigDict(from_attributes=True)
    id: str
    department_id: str
    department_name: Optional[str] = None
    is_active: bool
    created_at: datetime
    updated_at: Optional[datetime] = None

class GeographicSummaryResponse(BaseModel):
    total_departments: int
    total_municipalities: int
    active_departments: int
    active_municipalities: int
    source: str = "INETER / Ley N.° 59 de División Política Administrativa"
    last_update: str = "Noviembre 2026"


# --- Notifications & Citizen Alerts Schemas ---
class NotificationSubscribeRequest(BaseModel):
    email: EmailStr
    department: Optional[str] = None

class NotificationSubscriptionResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: str
    email: EmailStr
    department: Optional[str] = None
    is_active: bool
    token_unsubscribe: str
    message: str = "Suscripción a alertas cívicas activada exitosamente."


# --- Right to be Forgotten / Data Deletion (Ley N.° 787) ---
class DeletionRequestCreate(BaseModel):
    reason: str = Field(..., min_length=10, description="Motivo de la solicitud de supresión de datos conforme a Ley 787")

class DeletionRequestResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: str
    report_id: str
    case_number: Optional[str] = None
    reason: str
    status: str
    created_at: datetime
    message: str = "Solicitud de supresión de datos recibida y en cola de procesamiento conforme a la Ley N.° 787."


