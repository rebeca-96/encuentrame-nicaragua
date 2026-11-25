import pytest
import os
from fastapi.testclient import TestClient
from app.main import app
from app.models.entities import User, MissingPersonReport, GeographicLocation, UserRole, ReportStatus
from app.core.security import get_password_hash, create_access_token
from tests.conftest import TestingSessionLocal
from datetime import datetime, timezone

client = TestClient(app)

test_admin_id = None
test_reporter_id = None
test_report_id = None

@pytest.fixture(scope="module", autouse=True)
def setup_v2_fixtures():
    global test_admin_id, test_reporter_id, test_report_id
    with TestingSessionLocal() as db:
        # Create reporter
        rep = db.query(User).filter(User.email == "v2_reporter@encuentrame.ni").first()
        if not rep:
            rep = User(
                email="v2_reporter@encuentrame.ni",
                password_hash=get_password_hash("ReportPass2026!"),
                full_name="Reporter V2 Test",
                role=UserRole.REPORTER.value,
                is_active=True,
                is_verified=True
            )
            db.add(rep)
            db.commit()
            db.refresh(rep)
        test_reporter_id = rep.id

        # Create admin
        adm = db.query(User).filter(User.email == "v2_admin@encuentrame.ni").first()
        if not adm:
            adm = User(
                email="v2_admin@encuentrame.ni",
                password_hash=get_password_hash("AdminPass2026!"),
                full_name="Admin V2 Test",
                role=UserRole.ADMIN.value,
                is_active=True,
                is_verified=True
            )
            db.add(adm)
            db.commit()
            db.refresh(adm)
        test_admin_id = adm.id

        # Create location and test report
        loc = GeographicLocation(
            department="Managua",
            municipality="Managua",
            approximate_latitude=12.1364,
            approximate_longitude=-86.2514
        )
        db.add(loc)
        db.flush()

        report = MissingPersonReport(
            case_number="EN-2026-9999",
            reporter_id=test_reporter_id,
            first_name="Carlos",
            last_name="Prueba",
            age_at_disappearance=25,
            disappearance_date=datetime.now(timezone.utc),
            location_id=loc.id,
            physical_description="Estatura 1.75m, contextura atlética",
            clothing_description="Camisa azul, pantalón negro",
            circumstances="Desaparecido al salir del trabajo",
            status=ReportStatus.APPROVED_PUBLISHED.value,
            is_public=True
        )
        db.add(report)
        db.commit()
        db.refresh(report)
        test_report_id = report.id


def test_v2_path_traversal_strictly_blocked():
    """Verifica que intentos de Path Traversal en descarga de fotos sean bloqueados con 400 o 404 (nunca 200)."""
    payloads = [
        "../../README.md",
        "..%2F..%2FREADME.md",
        "..\\..\\README.md",
        "invalid_key.txt",
        "../../../etc/passwd"
    ]
    for p in payloads:
        res = client.get(f"/api/v1/reports/photos/{p}")
        assert res.status_code in [400, 404], f"Payload {p} admitió descarga con HTTP {res.status_code}"
        assert res.status_code != 200, f"Vulnerabilidad activa: {p} entregó archivo con 200!"


def test_v2_register_rate_limiting():
    """Verifica que el registro de cuentas bloquee intentos de flooding con HTTP 429."""
    codes = []
    for i in range(5):
        res = client.post("/api/v1/auth/register", json={
            "email": f"ratetest_v2_{i}@test.com",
            "password": "Password123#",
            "confirm_password": "Password123#",
            "full_name": f"Rate User {i}",
            "role": "reporter"
        })
        codes.append(res.status_code)
    assert 429 in codes, f"No se activó rate limiting (códigos: {codes})"


def test_v2_jwt_revocation_on_logout():
    """Verifica que un token JWT sea estrictamente revocado en el servidor al cerrar sesión."""
    # Login as v2 reporter
    login_res = client.post("/api/v1/auth/login", json={
        "email": "v2_reporter@encuentrame.ni",
        "password": "ReportPass2026!"
    })
    assert login_res.status_code == 200
    token = login_res.json()["access_token"]
    
    # Verify token works before logout
    me_before = client.get("/api/v1/auth/me", headers={"Authorization": f"Bearer {token}"})
    assert me_before.status_code == 200
    
    # Logout
    logout_res = client.post("/api/v1/auth/logout", headers={"Authorization": f"Bearer {token}"})
    assert logout_res.status_code == 200
    assert "revocada" in logout_res.json()["message"]
    
    # Attempt to reuse token after logout
    me_after = client.get("/api/v1/auth/me", headers={"Authorization": f"Bearer {token}"})
    assert me_after.status_code == 401, f"Token revocado fue admitido indebidamente con HTTP {me_after.status_code}"


def test_v2_notification_subscription_flow():
    """Verifica el flujo completo de suscripción y cancelación de alertas ciudadanas."""
    test_email = "ciudadano_alertas_v2@ejemplo.ni"
    sub_res = client.post("/api/v1/notifications/subscribe", json={
        "email": test_email,
        "department": "Matagalpa"
    })
    assert sub_res.status_code == 201
    data = sub_res.json()
    assert data["email"] == test_email
    assert data["department"] == "Matagalpa"
    assert "token_unsubscribe" in data
    
    # Test unsubscribe with unique token
    unsub_token = data["token_unsubscribe"]
    unsub_res = client.get(f"/api/v1/notifications/unsubscribe/{unsub_token}")
    assert unsub_res.status_code == 200
    assert "cancelada exitosamente" in unsub_res.json()["message"]


def test_v2_deletion_request_flow_ley787():
    """Verifica la solicitud y trámite de supresión de datos conforme a la Ley N.° 787."""
    admin_token = create_access_token(subject=test_admin_id, role=UserRole.ADMIN.value)
    
    # Request deletion
    del_res = client.post(f"/api/v1/reports/{test_report_id}/request-deletion", json={
        "reason": "Persona localizada pacíficamente, se solicita retiro de datos según Ley 787"
    }, headers={"Authorization": f"Bearer {admin_token}"})
    assert del_res.status_code == 201
    req_id = del_res.json()["id"]
    
    # Admin lists deletion requests
    admin_list = client.get("/api/v1/admin/deletion-requests", headers={"Authorization": f"Bearer {admin_token}"})
    assert admin_list.status_code == 200
    matching = next((r for r in admin_list.json() if r["id"] == req_id), None)
    assert matching is not None
    
    # Admin resolves deletion request
    resolve_res = client.patch(f"/api/v1/admin/deletion-requests/{req_id}/status?action=processed", headers={"Authorization": f"Bearer {admin_token}"})
    assert resolve_res.status_code == 200
    assert resolve_res.json()["status"] == "processed"
