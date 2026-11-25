import pytest
import os
import sys
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Setup test environment
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
os.environ["DATABASE_URL"] = "sqlite:///./test_encuentrame.db"

from app.main import app
from app.core.database import Base, get_db
from app.core.security import create_access_token, get_password_hash
from app.models.entities import (
    User, UserRole, MissingPersonReport, GeographicLocation, 
    ReportStatus, ConfidentialTip, TipStatus, AuditLog
)
from tests.conftest import TestingSessionLocal

client = TestClient(app)

@pytest.fixture(scope="module", autouse=True)
def setup_test_db():
    db = TestingSessionLocal()
    
    # Create test users if not present
    existing = db.query(User).filter(User.email == "admin_test@encuentrame.ni").first()
    if not existing:
        admin = User(
            email="admin_test@encuentrame.ni",
            password_hash=get_password_hash("SecretPass123!"),
            full_name="Admin Test",
            role=UserRole.ADMIN.value,
            is_active=True,
            is_verified=True
        )
        moderator = User(
            email="mod_test@encuentrame.ni",
            password_hash=get_password_hash("SecretPass123!"),
            full_name="Mod Test",
            role=UserRole.MODERATOR.value,
            is_active=True,
            is_verified=True
        )
        reporter1 = User(
            email="reporter1_test@encuentrame.ni",
            password_hash=get_password_hash("SecretPass123!"),
            full_name="Reporter One",
            role=UserRole.REPORTER.value,
            is_active=True,
            is_verified=True
        )
        reporter2 = User(
            email="reporter2_test@encuentrame.ni",
            password_hash=get_password_hash("SecretPass123!"),
            full_name="Reporter Two",
            role=UserRole.REPORTER.value,
            is_active=True,
            is_verified=True
        )
        citizen = User(
            email="citizen_test@encuentrame.ni",
            password_hash=get_password_hash("SecretPass123!"),
            full_name="Citizen Test",
            role=UserRole.CITIZEN.value,
            is_active=True,
            is_verified=True
        )
        db.add_all([admin, moderator, reporter1, reporter2, citizen])
        db.commit()
    db.close()
    
    yield

def get_auth_header(email: str, role: str) -> dict:
    db = TestingSessionLocal()
    user = db.query(User).filter(User.email == email).first()
    token = create_access_token(subject=user.id, role=role)
    db.close()
    return {"Authorization": f"Bearer {token}"}

# 1. Test: Un reporte nuevo no se publica sin aprobación (ingresa como pending_review y is_public=False)
def test_1_new_report_not_published_without_moderator_approval():
    headers = get_auth_header("reporter1_test@encuentrame.ni", UserRole.REPORTER.value)
    payload = {
        "first_name": "Gabriel",
        "last_name": "Salmerón",
        "nickname": "Gabo",
        "age_at_disappearance": 16,
        "gender": "male",
        "disappearance_date": "2026-11-10T14:30:00Z",
        "department": "Managua",
        "municipality": "Tipitapa",
        "neighborhood_zone": "Barrio San Juan",
        "physical_description": "Estatura 1.68m, contextura delgada, tez morena clara.",
        "clothing_description": "Camisa polo blanca, jeans azules, tenis negros.",
        "circumstances": "Salió en horas de la tarde hacia la terminal y no regresó.",
        "is_minor": True,
        "consent": {
            "relationship_to_victim": "Madre",
            "identity_doc_number": "001-120590-0004M",
            "accepted_terms": True
        }
    }
    response = client.post("/api/v1/reports/", json=payload, headers=headers)
    assert response.status_code == 201
    data = response.json()
    assert data["status"] == ReportStatus.PENDING_REVIEW.value
    report_id = data["id"]
    
    # Verify it does NOT appear in public catalog
    public_res = client.get("/api/v1/reports/")
    assert public_res.status_code == 200
    public_reports = public_res.json()
    assert not any(r["id"] == report_id for r in public_reports)

# 2. Test: Un ciudadano anónimo o regular no puede acceder a la lista de pistas confidenciales
def test_2_citizen_cannot_access_confidential_tips():
    # Anonymous citizen
    anon_res = client.get("/api/v1/admin/tips")
    assert anon_res.status_code == 401

    # Regular citizen token
    citizen_headers = get_auth_header("citizen_test@encuentrame.ni", UserRole.CITIZEN.value)
    cit_res = client.get("/api/v1/admin/tips", headers=citizen_headers)
    assert cit_res.status_code == 403

    # Reporter token
    reporter_headers = get_auth_header("reporter1_test@encuentrame.ni", UserRole.REPORTER.value)
    rep_res = client.get("/api/v1/admin/tips", headers=reporter_headers)
    assert rep_res.status_code == 403

    # Authorized moderator token
    mod_headers = get_auth_header("mod_test@encuentrame.ni", UserRole.MODERATOR.value)
    mod_res = client.get("/api/v1/admin/tips", headers=mod_headers)
    assert mod_res.status_code == 200

# 3. Test: Un usuario no puede modificar ni cerrar reportes ajenos
def test_3_user_cannot_modify_or_close_others_reports():
    # Reporter 1 creates a report
    r1_headers = get_auth_header("reporter1_test@encuentrame.ni", UserRole.REPORTER.value)
    res = client.post("/api/v1/reports/", json={
        "first_name": "Roberto",
        "last_name": "Silva",
        "age_at_disappearance": 34,
        "disappearance_date": "2026-11-05T10:00:00Z",
        "department": "Masaya",
        "municipality": "Masaya",
        "physical_description": "Estatura 1.75m, tez morena, cicatriz en ceja derecha.",
        "clothing_description": "Camisa azul con botones, jeans negros.",
        "circumstances": "Viajó a Masaya por motivos laborales.",
        "consent": {
            "relationship_to_victim": "Hermano",
            "identity_doc_number": "401-200388-0002A",
            "accepted_terms": True
        }
    }, headers=r1_headers)
    report_id = res.json()["id"]

    # Reporter 2 attempts to request closure on Reporter 1's report
    r2_headers = get_auth_header("reporter2_test@encuentrame.ni", UserRole.REPORTER.value)
    close_res = client.post(f"/api/v1/reports/{report_id}/request-close", json={
        "reason": "Persona localizada con bien"
    }, headers=r2_headers)
    assert close_res.status_code == 403

# 4. Test: Los filtros devuelven resultados correctos y no mezclan estados
def test_4_search_filters_return_correct_results():
    # Approve Reporter 1's report by moderator
    mod_headers = get_auth_header("mod_test@encuentrame.ni", UserRole.MODERATOR.value)
    db = TestingSessionLocal()
    rep = db.query(MissingPersonReport).filter(MissingPersonReport.first_name == "Roberto").first()
    db.close()
    
    mod_res = client.post(f"/api/v1/admin/reports/{rep.id}/moderate", json={
        "decision": "approve",
        "notes_internal": "Documentación de parentesco validada"
    }, headers=mod_headers)
    assert mod_res.status_code == 200
    
    # Search by department
    search_dept = client.get("/api/v1/search/?department=Masaya")
    assert search_dept.status_code == 200
    results = search_dept.json()
    assert len(results) >= 1
    assert any(r["first_name"] == "Roberto" for r in results)
    
    # Search for non-existent department
    search_empty = client.get("/api/v1/search/?department=AtlantidaInexistente")
    assert search_empty.status_code == 200
    assert len(search_empty.json()) == 0

# 5. Test: Los datos geográficos no revelan ubicaciones sensibles ni domicilios exactos
def test_5_geographic_data_does_not_reveal_sensitive_coordinates():
    res = client.get("/api/v1/locations/map-aggregated")
    assert res.status_code == 200
    points = res.json()
    for pt in points:
        # Check that no street address or sensitive fields are returned in public map point item
        assert "exact_address" not in pt
        assert "home_address" not in pt
        assert "shelter_location" not in pt
        assert "reporter_phone" not in pt
        assert pt["approximate_latitude"] is not None
        assert pt["approximate_longitude"] is not None

# 6. Test: Los cambios administrativos y de moderación quedan auditados inmutablemente
def test_6_administrative_actions_are_audit_logged():
    admin_headers = get_auth_header("admin_test@encuentrame.ni", UserRole.ADMIN.value)
    audit_res = client.get("/api/v1/admin/audit-logs", headers=admin_headers)
    assert audit_res.status_code == 200
    logs = audit_res.json()
    assert len(logs) > 0
    actions = [l["action"] for l in logs]
    assert any("REPORT_MODERATED_APPROVE" in a or "REPORT_CREATED" in a for a in actions)

# 7. Test: El cierre formal de caso es procesable y despublica el reporte inmediatamente
def test_7_case_closure_is_processable_and_depublishes_case():
    r1_headers = get_auth_header("reporter1_test@encuentrame.ni", UserRole.REPORTER.value)
    db = TestingSessionLocal()
    rep = db.query(MissingPersonReport).filter(MissingPersonReport.first_name == "Roberto").first()
    db.close()
    
    close_res = client.post(f"/api/v1/reports/{rep.id}/request-close", json={
        "reason": "Persona localizada con buen estado de salud"
    }, headers=r1_headers)
    assert close_res.status_code == 200
    
    # Verify it is no longer listed in public searches
    public_res = client.get("/api/v1/reports/")
    assert not any(r["id"] == rep.id for r in public_res.json())

# 8. Test: Manejo correcto de errores ante cargas inválidas y falta de consentimiento
def test_8_error_handling_for_invalid_input_and_missing_consent():
    r1_headers = get_auth_header("reporter1_test@encuentrame.ni", UserRole.REPORTER.value)
    # Attempt report without accepting consent terms
    invalid_payload = {
        "first_name": "Test",
        "last_name": "Invalido",
        "age_at_disappearance": 25,
        "disappearance_date": "2026-11-01T00:00:00Z",
        "department": "Managua",
        "municipality": "Managua",
        "physical_description": "Descripcion de prueba valida.",
        "clothing_description": "Ropa de prueba valida.",
        "circumstances": "Circunstancias de prueba validas.",
        "consent": {
            "relationship_to_victim": "Amigo",
            "identity_doc_number": "001-000000-0000A",
            "accepted_terms": False # REJECTED!
        }
    }
    res = client.post("/api/v1/reports/", json=invalid_payload, headers=r1_headers)
    assert res.status_code in [400, 422]
    assert "consentimiento" in str(res.json()).lower()

# 9. Test: La IA actúa como asesora sin modificar estados ni publicar de forma autónoma
def test_9_ai_acts_strictly_as_advisor_without_autonomous_state_changes():
    mod_headers = get_auth_header("mod_test@encuentrame.ni", UserRole.MODERATOR.value)
    db = TestingSessionLocal()
    rep = db.query(MissingPersonReport).first()
    initial_status = rep.status
    initial_public = rep.is_public
    db.close()
    
    # Run AI duplicate check
    ai_dup_res = client.post(f"/api/v1/ai/check-duplicates/{rep.id}", headers=mod_headers)
    assert ai_dup_res.status_code == 200
    
    # Run AI summary
    ai_sum_res = client.get(f"/api/v1/ai/summary/{rep.id}", headers=mod_headers)
    assert ai_sum_res.status_code == 200
    
    # Verify report state remained completely unchanged
    db2 = TestingSessionLocal()
    rep_after = db2.query(MissingPersonReport).filter(MissingPersonReport.id == rep.id).first()
    assert rep_after.status == initial_status
    assert rep_after.is_public == initial_public
    db2.close()

# 10. Test: Recepción y rastreo seguro de pistas con código no adivinable
def test_10_secure_tip_submission_and_unpredictable_code():
    db = TestingSessionLocal()
    rep = db.query(MissingPersonReport).filter(
        MissingPersonReport.status.in_([
            ReportStatus.PENDING_REVIEW.value,
            ReportStatus.APPROVED_PUBLISHED.value,
            ReportStatus.UNDER_INVESTIGATION.value
        ])
    ).first()
    rep_id = rep.id
    db.close()
    
    tip_res = client.post("/api/v1/tips/", json={
        "report_id": rep_id,
        "description": "Se vio una persona con vestimenta similar en la parada del mercado.",
        "sighting_department": "Managua",
        "sighting_municipality": "Ciudad Sandino",
        "confidentiality_level": "strict_anonymous"
    })
    assert tip_res.status_code == 201
    tip_data = tip_res.json()
    assert "tip_code" in tip_data
    assert tip_data["tip_code"].startswith("PISTA-")
    
    # Track tip anonymously
    track_res = client.get(f"/api/v1/tips/track/{tip_data['tip_code']}")
    assert track_res.status_code == 200
    assert track_res.json()["status"] == TipStatus.RECEIVED.value
