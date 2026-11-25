import pytest
import os
import sys
import io
from datetime import datetime, timedelta, timezone
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
os.environ["DATABASE_URL"] = "sqlite:///./test_fixes.db"

from app.main import app
from app.core.database import Base, get_db
from app.core.security import create_access_token, get_password_hash
from app.core.rate_limit import limiter
from app.models.entities import (
    User, UserRole, MissingPersonReport, GeographicLocation, 
    ReportStatus, NotificationSubscription
)
from tests.conftest import TestingSessionLocal

client = TestClient(app)

@pytest.fixture(scope="module", autouse=True)
def setup_test_db():
    db = TestingSessionLocal()
    
    existing = db.query(User).filter(User.email == "reporter_fix@encuentrame.ni").first()
    if not existing:
        reporter1 = User(
            email="reporter_fix@encuentrame.ni",
            password_hash=get_password_hash("Pass1234!Strong"),
            full_name="Reporter Fix",
            role=UserRole.REPORTER.value,
            is_active=True,
            is_verified=True
        )
        reporter2 = User(
            email="reporter_other@encuentrame.ni",
            password_hash=get_password_hash("Pass1234!Strong"),
            full_name="Reporter Other",
            role=UserRole.REPORTER.value,
            is_active=True,
            is_verified=True
        )
        moderator = User(
            email="mod_fix@encuentrame.ni",
            password_hash=get_password_hash("Pass1234!Strong"),
            full_name="Mod Fix",
            role=UserRole.MODERATOR.value,
            is_active=True,
            is_verified=True
        )
        db.add_all([reporter1, reporter2, moderator])
        db.commit()
    db.close()
    
    yield

def get_auth_header(email: str, role: str) -> dict:
    db = TestingSessionLocal()
    user = db.query(User).filter(User.email == email).first()
    token = create_access_token(subject=user.id, role=role)
    db.close()
    return {"Authorization": f"Bearer {token}"}

# 1. Test: Fechas futuras en disappearance_date son estrictamente rechazadas (ERR-04)
def test_future_date_rejected():
    headers = get_auth_header("reporter_fix@encuentrame.ni", UserRole.REPORTER.value)
    future_date = (datetime.now(timezone.utc) + timedelta(days=30)).isoformat()
    
    payload = {
        "first_name": "Ernesto",
        "last_name": "Futuro",
        "age_at_disappearance": 25,
        "disappearance_date": future_date,
        "department": "Managua",
        "municipality": "Managua",
        "physical_description": "Estatura 1.70m, tez trigueña clara.",
        "clothing_description": "Camisa azul con botones, jeans.",
        "circumstances": "Circunstancias de prueba de quince caracteres.",
        "consent": {
            "relationship_to_victim": "Hermano",
            "identity_doc_number": "001-000000-0000A",
            "accepted_terms": True
        }
    }
    res = client.post("/api/v1/reports/", json=payload, headers=headers)
    assert res.status_code == 422 # Pydantic validation error
    err_text = str(res.json()).lower()
    assert "futuro" in err_text

# 2. Test: Inconsistencia entre Departamento y Municipio es estrictamente rechazada (ERR-05)
def test_inconsistent_municipality_rejected():
    headers = get_auth_header("reporter_fix@encuentrame.ni", UserRole.REPORTER.value)
    past_date = (datetime.now(timezone.utc) - timedelta(days=2)).isoformat()
    
    # Sébaco belongs to Matagalpa, not Managua!
    payload = {
        "first_name": "Luis",
        "last_name": "Inconsistente",
        "age_at_disappearance": 30,
        "disappearance_date": past_date,
        "department": "Managua",
        "municipality": "Sébaco",
        "physical_description": "Estatura 1.70m, tez trigueña clara.",
        "clothing_description": "Camisa azul con botones, jeans.",
        "circumstances": "Circunstancias de prueba de quince caracteres.",
        "consent": {
            "relationship_to_victim": "Hermano",
            "identity_doc_number": "001-000000-0000A",
            "accepted_terms": True
        }
    }
    res = client.post("/api/v1/reports/", json=payload, headers=headers)
    assert res.status_code == 422
    err_text = str(res.json()).lower()
    assert "no pertenece al departamento" in err_text

# 3. Test: Subida de archivo no imagen o corrupto devuelve HTTP 400 limpio, no 500 (ERR-03)
def test_invalid_image_upload_returns_400():
    headers = get_auth_header("reporter_fix@encuentrame.ni", UserRole.REPORTER.value)
    past_date = (datetime.now(timezone.utc) - timedelta(days=1)).isoformat()
    
    # First create a valid report
    create_res = client.post("/api/v1/reports/", json={
        "first_name": "Claudia",
        "last_name": "Vargas",
        "age_at_disappearance": 21,
        "disappearance_date": past_date,
        "department": "Matagalpa",
        "municipality": "Sébaco",
        "physical_description": "Estatura 1.60m, piel clara, contextura delgada.",
        "clothing_description": "Blusa blanca, pantalón negro.",
        "circumstances": "Salió hacia sus clases en horas matutinas.",
        "consent": {
            "relationship_to_victim": "Madre",
            "identity_doc_number": "441-100295-0001B",
            "accepted_terms": True
        }
    }, headers=headers)
    assert create_res.status_code == 201
    rep_id = create_res.json()["id"]
    
    # Upload binary corrupt file / text disguised as photo
    fake_file = io.BytesIO(b"MALICIOUS_EXE_OR_CORRUPT_DATA_NOT_IMAGE")
    res = client.post(
        f"/api/v1/reports/{rep_id}/photos",
        files={"file": ("malicious.exe", fake_file, "application/octet-stream")},
        headers=headers
    )
    assert res.status_code == 400
    assert "no permitido" in res.json()["detail"].lower() or "no es una imagen" in res.json()["detail"].lower()

# 4. Test: Endpoint PUT /api/v1/reports/{id} con control de acceso por recurso (ERR-07)
def test_put_report_update_authorization():
    r1_headers = get_auth_header("reporter_fix@encuentrame.ni", UserRole.REPORTER.value)
    r2_headers = get_auth_header("reporter_other@encuentrame.ni", UserRole.REPORTER.value)
    mod_headers = get_auth_header("mod_fix@encuentrame.ni", UserRole.MODERATOR.value)
    
    db = TestingSessionLocal()
    rep = db.query(MissingPersonReport).filter(MissingPersonReport.first_name == "Claudia").first()
    rep_id = rep.id
    db.close()
    
    # Reporter 2 cannot edit Reporter 1's report
    unauth_res = client.put(f"/api/v1/reports/{rep_id}", json={
        "nickname": "Clau"
    }, headers=r2_headers)
    assert unauth_res.status_code == 403
    
    # Reporter 1 (Author) can update while in pending_review
    auth_res = client.put(f"/api/v1/reports/{rep_id}", json={
        "nickname": "Clau",
        "clothing_description": "Blusa blanca con suéter gris, pantalón negro."
    }, headers=r1_headers)
    assert auth_res.status_code == 200
    assert "actualizado" in auth_res.json()["message"].lower()
    
    # Moderator can also update
    mod_res = client.put(f"/api/v1/reports/{rep_id}", json={
        "medical_conditions": "Alergia a penicilina"
    }, headers=mod_headers)
    assert mod_res.status_code == 200

# 5. Test: Complejidad de contraseñas en registro de usuarios (ERR-08)
def test_password_complexity_required():
    # Trivial password without uppercase or symbols
    weak_res = client.post("/api/v1/auth/register", json={
        "email": "nuevo@encuentrame.ni",
        "password": "solominisculas",
        "confirm_password": "solominisculas",
        "full_name": "Usuario Débil"
    })
    assert weak_res.status_code == 422
    
    # Passwords do not match
    mismatch_res = client.post("/api/v1/auth/register", json={
        "email": "nuevo2@encuentrame.ni",
        "password": "PassRobust123!",
        "confirm_password": "PassDiferente456!",
        "full_name": "Usuario Descuadrado"
    })
    assert mismatch_res.status_code == 422
    
    # Valid robust password
    valid_res = client.post("/api/v1/auth/register", json={
        "email": "valido@encuentrame.ni",
        "password": "PassRobust123!",
        "confirm_password": "PassRobust123!",
        "full_name": "Usuario Robusto",
        "role": "reporter"
    })
    assert valid_res.status_code == 201

# 6. Test: Rate Limiting en Login devuelve HTTP 429 tras exceder límite (ERR-01)
def test_rate_limiting_login_returns_429():
    limiter._requests.clear()
    
    # Make 5 attempts (allowed)
    for _ in range(5):
        r = client.post("/api/v1/auth/login", json={
            "email": "reporter_fix@encuentrame.ni",
            "password": "WrongPassword123!"
        })
        assert r.status_code in [401, 200]
        
    # 6th attempt must be blocked by rate limiter with HTTP 429
    r_blocked = client.post("/api/v1/auth/login", json={
        "email": "reporter_fix@encuentrame.ni",
        "password": "WrongPassword123!"
    })
    assert r_blocked.status_code == 429
    assert "límite" in r_blocked.json()["detail"].lower()
    
    limiter._requests.clear()

# 7. Test: Rechazo de pistas para casos cerrados/resueltos
def test_tip_rejected_on_closed_case():
    headers = get_auth_header("reporter_fix@encuentrame.ni", UserRole.REPORTER.value)
    past_date = (datetime.now(timezone.utc) - timedelta(days=2)).isoformat()
    
    # Create dedicated case to close
    create_res = client.post("/api/v1/reports/", json={
        "first_name": "Caso",
        "last_name": "Cerrado",
        "age_at_disappearance": 40,
        "disappearance_date": past_date,
        "department": "Granada",
        "municipality": "Granada",
        "physical_description": "Estatura 1.70m, piel morena clara.",
        "clothing_description": "Camisa blanca, jeans.",
        "circumstances": "Circunstancias de prueba de quince caracteres.",
        "consent": {
            "relationship_to_victim": "Hermano",
            "identity_doc_number": "001-000000-0000A",
            "accepted_terms": True
        }
    }, headers=headers)
    rep_id = create_res.json()["id"]

    db = TestingSessionLocal()
    rep = db.query(MissingPersonReport).filter(MissingPersonReport.id == rep_id).first()
    rep.status = ReportStatus.CLOSED_FOUND.value
    db.commit()
    db.close()
    
    res = client.post("/api/v1/tips/", json={
        "report_id": rep_id,
        "description": "Informacion sobre caso ya resuelto",
        "sighting_department": "Granada"
    })
    assert res.status_code == 400
    assert "cerrado" in res.json()["detail"].lower()

# 8. Test: Desuscripción voluntaria de alertas (ERR-10)
def test_notification_unsubscribe_flow():
    db = TestingSessionLocal()
    sub = NotificationSubscription(
        email="baja@encuentrame.ni",
        department="Managua",
        is_active=True,
        token_unsubscribe="TOKEN-UNSUB-TEST-99"
    )
    db.add(sub)
    db.commit()
    db.close()
    
    res = client.get("/api/v1/notifications/unsubscribe/TOKEN-UNSUB-TEST-99")
    assert res.status_code == 200
    assert "cancelada" in res.json()["message"].lower()
    
    # Check DB state
    db = TestingSessionLocal()
    sub_after = db.query(NotificationSubscription).filter(
        NotificationSubscription.token_unsubscribe == "TOKEN-UNSUB-TEST-99"
    ).first()
    assert sub_after.is_active is False
    db.close()
