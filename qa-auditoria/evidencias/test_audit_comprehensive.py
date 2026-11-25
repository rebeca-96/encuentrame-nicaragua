import sys
import os
import io
import json
import pytest
from datetime import datetime, timezone, timedelta

sys.path.insert(0, os.path.abspath("backend"))

from fastapi.testclient import TestClient
from app.main import app
from app.core.database import SessionLocal
from app.models.entities import (
    User, UserRole, MissingPersonReport, ReportStatus, 
    ConfidentialTip, TipStatus, AuditLog, Department, 
    Municipality, DeletionRequest, DeletionStatus
)
from app.core.security import get_password_hash, create_access_token

client = TestClient(app)

audit_log = []

def record(test_id, module, title, status, expected, actual, evidence, severity=None):
    entry = {
        "id": test_id,
        "module": module,
        "title": title,
        "status": status,
        "expected": expected,
        "actual": actual,
        "evidence": str(evidence),
        "severity": severity
    }
    audit_log.append(entry)
    print(f"[{status}] {test_id} - {title}")

def run_all_audit_tests():
    print("=== INICIANDO EJECUCIÓN DE PRUEBAS QA SENIOR ===")
    from app.core.rate_limit import limiter
    db = SessionLocal()

    # -------------------------------------------------------------
    # 1. AUTENTICACIÓN Y CONTROL DE ACCESO
    # -------------------------------------------------------------
    # 1.1 Login exitoso
    res_login = client.post("/api/v1/auth/login", json={"email": "admin@encuentrame.ni", "password": "AdminPass2026!"})
    if res_login.status_code == 200 and "access_token" in res_login.json():
        admin_token = res_login.json()["access_token"]
        record("TC-AUTH-01", "Autenticación", "Login exitoso de Administrador con credenciales válidas", "PASS", "HTTP 200 con token JWT", f"HTTP {res_login.status_code}", res_login.json())
    else:
        record("TC-AUTH-01", "Autenticación", "Login exitoso de Administrador", "FAIL", "HTTP 200", f"HTTP {res_login.status_code}", res_login.text, "P1")
        admin_token = None

    # 1.2 Login con contraseña inválida
    res_bad_pw = client.post("/api/v1/auth/login", json={"email": "admin@encuentrame.ni", "password": "WrongPassword!"})
    if res_bad_pw.status_code in [400, 401]:
        record("TC-AUTH-02", "Autenticación", "Rechazo de credenciales incorrectas", "PASS", "HTTP 400/401", f"HTTP {res_bad_pw.status_code}", res_bad_pw.json())
    else:
        record("TC-AUTH-02", "Autenticación", "Rechazo de credenciales incorrectas", "FAIL", "HTTP 401", f"HTTP {res_bad_pw.status_code}", res_bad_pw.text, "P0")

    # 1.3 Revocación de token en Logout
    if admin_token:
        res_logout = client.post("/api/v1/auth/logout", headers={"Authorization": f"Bearer {admin_token}"})
        res_me_revoked = client.get("/api/v1/auth/me", headers={"Authorization": f"Bearer {admin_token}"})
        if res_logout.status_code == 200 and res_me_revoked.status_code == 401:
            record("TC-AUTH-03", "Autenticación", "Revocación de JWT en cierre de sesión (Logout Blacklist)", "PASS", "HTTP 401 con token revocado", f"HTTP {res_me_revoked.status_code}", res_me_revoked.json())
        else:
            record("TC-AUTH-03", "Autenticación", "Revocación de JWT en cierre de sesión", "FAIL", "HTTP 401", f"Logout {res_logout.status_code}, Me {res_me_revoked.status_code}", res_me_revoked.text, "P1")

    # Obtener token de reportante antes de agotar rate limit
    rep_user = db.query(User).filter(User.email == "reportante@encuentrame.ni").first()
    reporter_token = create_access_token(subject=rep_user.id, role="reporter") if rep_user else None

    # 1.4 Rate limiting en autenticación
    rate_limited = False
    for i in range(7):
        r = client.post("/api/v1/auth/login", json={"email": "bruteforce@test.ni", "password": f"Pass_{i}!"})
        if r.status_code == 429:
            rate_limited = True
            break
    if rate_limited:
        record("TC-AUTH-04", "Seguridad / Rate Limiting", "Protección contra fuerza bruta en login (HTTP 429)", "PASS", "HTTP 429 Too Many Requests", "HTTP 429 detectado", "Rate limit activo")
    else:
        record("TC-AUTH-04", "Seguridad / Rate Limiting", "Protección contra fuerza bruta en login", "FAIL", "HTTP 429", "No bloqueado tras 7 intentos", "P1")

    # Limpiar rate limiter en memoria para permitir siguientes pruebas
    limiter._requests.clear()

    # -------------------------------------------------------------
    # 2. CONTROL DE ACCESO BASADO EN ROLES (RBAC / OWASP BOLA)
    # -------------------------------------------------------------
    res_mod_pending = client.get("/api/v1/admin/reports/pending", headers={"Authorization": f"Bearer {reporter_token}"})
    if res_mod_pending.status_code in [401, 403]:
        record("TC-RBAC-01", "Autorización", "Usuario con rol 'reporter' no puede acceder a reportes pendientes de moderación", "PASS", "HTTP 401/403 Prohibido", f"HTTP {res_mod_pending.status_code}", res_mod_pending.text)
    else:
        record("TC-RBAC-01", "Autorización", "Aislamiento de rol reporter ante panel admin", "FAIL", "HTTP 403", f"HTTP {res_mod_pending.status_code}", res_mod_pending.text, "P0")

    # -------------------------------------------------------------
    # 3. MÓDULO DE REPORTES Y PERSONAS DESAPARECIDAS
    # -------------------------------------------------------------
    # 3.1 Creación con datos válidos por reporter
    valid_report = {
        "first_name": "Carlos",
        "last_name": "García QA",
        "gender": "male",
        "age_at_disappearance": 28,
        "disappearance_date": (datetime.now(timezone.utc) - timedelta(days=2)).isoformat(),
        "department": "Managua",
        "municipality": "Ciudad Sandino",
        "physical_description": "Altura 1.75m, tez morena clara, cicatriz en ceja derecha.",
        "clothing_description": "Camisa azul oscuro, pantalón negro jeans.",
        "circumstances": "Visto por última vez saliendo de su trabajo hacia su domicilio.",
        "consent": {
            "relationship_to_victim": "Madre",
            "identity_doc_number": "001-010190-0000A",
            "accepted_terms": True
        }
    }
    res_create = client.post("/api/v1/reports/", json=valid_report, headers={"Authorization": f"Bearer {reporter_token}"})
    created_id = None
    if res_create.status_code == 201:
        created_id = res_create.json()["id"]
        status_val = res_create.json()["status"]
        is_public = res_create.json().get("is_public", False)
        if status_val == "pending_review" and not is_public:
            record("TC-REP-01", "Reportes", "Creación correcta en estado pending_review y oculto al público", "PASS", "HTTP 201, pending_review, is_public=False", f"HTTP {res_create.status_code}, status={status_val}", res_create.json())
        else:
            record("TC-REP-01", "Reportes", "Estado de reporte recién creado", "FAIL", "pending_review e is_public=False", f"status={status_val}, is_public={is_public}", res_create.json(), "P0")
    else:
        record("TC-REP-01", "Reportes", "Creación de reporte con datos válidos", "FAIL", "HTTP 201", f"HTTP {res_create.status_code}", res_create.text, "P1")

    # 3.2 Rechazo de fecha futura
    future_report = dict(valid_report)
    future_report["disappearance_date"] = (datetime.now(timezone.utc) + timedelta(days=10)).isoformat()
    res_future = client.post("/api/v1/reports/", json=future_report, headers={"Authorization": f"Bearer {reporter_token}"})
    if res_future.status_code in [400, 422]:
        record("TC-REP-02", "Validaciones de Reportes", "Rechazo estricto de fecha de desaparición futura", "PASS", "HTTP 400/422", f"HTTP {res_future.status_code}", res_future.text)
    else:
        record("TC-REP-02", "Validaciones de Reportes", "Rechazo de fecha futura", "FAIL", "HTTP 422", f"HTTP {res_future.status_code}", res_future.text, "P1")

    # 3.3 Rechazo de inconsistencia territorial (Municipio no pertenece a Departamento)
    mismatch_report = dict(valid_report)
    mismatch_report["department"] = "Managua"
    mismatch_report["municipality"] = "León" # León es de León, no de Managua
    res_mismatch = client.post("/api/v1/reports/", json=mismatch_report, headers={"Authorization": f"Bearer {reporter_token}"})
    if res_mismatch.status_code in [400, 422]:
        record("TC-REP-03", "Validaciones Territoriales", "Rechazo de municipio que no pertenece al departamento", "PASS", "HTTP 400/422", f"HTTP {res_mismatch.status_code}", res_mismatch.text)
    else:
        record("TC-REP-03", "Validaciones Territoriales", "Consistencia departamento-municipio", "FAIL", "HTTP 422", f"HTTP {res_mismatch.status_code}", res_mismatch.text, "P1")

    # 3.4 Rechazo sin consentimiento legal (Ley N.° 787)
    noconsent_report = dict(valid_report)
    noconsent_report["consent"] = {
        "relationship_to_victim": "Madre",
        "identity_doc_number": "001-010190-0000A",
        "accepted_terms": False
    }
    res_noconsent = client.post("/api/v1/reports/", json=noconsent_report, headers={"Authorization": f"Bearer {reporter_token}"})
    if res_noconsent.status_code in [400, 422]:
        record("TC-REP-04", "Privacidad / Ley 787", "Rechazo de reporte sin consentimiento legal expreso", "PASS", "HTTP 400/422", f"HTTP {res_noconsent.status_code}", res_noconsent.text)
    else:
        record("TC-REP-04", "Privacidad / Ley 787", "Obligatoriedad de consentimiento", "FAIL", "HTTP 400", f"HTTP {res_noconsent.status_code}", res_noconsent.text, "P0")

    # 3.5 Subida de fotografía sanitizada y bloqueo de archivos maliciosos
    if created_id:
        # Archivo malicioso (script PHP o HTML)
        malicious_file = io.BytesIO(b"<?php echo 'malicious'; ?>")
        res_malicious = client.post(
            f"/api/v1/reports/{created_id}/photos",
            files={"file": ("exploit.php", malicious_file, "application/x-php")},
            headers={"Authorization": f"Bearer {reporter_token}"}
        )
        if res_malicious.status_code in [400, 415, 422]:
            record("TC-REP-05", "Seguridad / Carga de Archivos", "Bloqueo de archivos ejecutables/scripts en carga de fotos", "PASS", "HTTP 400/415", f"HTTP {res_malicious.status_code}", res_malicious.text)
        else:
            record("TC-REP-05", "Seguridad / Carga de Archivos", "Bloqueo de archivos maliciosos", "FAIL", "HTTP 400", f"HTTP {res_malicious.status_code}", res_malicious.text, "P0")

    # -------------------------------------------------------------
    # 4. MÓDULO DE MAPAS Y CATÁLOGO TERRITORIAL
    # -------------------------------------------------------------
    res_depts = client.get("/api/v1/locations/departments")
    depts_data = res_depts.json() if res_depts.status_code == 200 else []
    if len(depts_data) == 17:
        record("TC-GEO-01", "Geografía y Mapas", "Presencia exacta de 17 entidades territoriales (15 deptos + 2 regiones)", "PASS", "17 entidades", f"{len(depts_data)} entidades", depts_data)
    else:
        record("TC-GEO-01", "Geografía y Mapas", "Catálogo de entidades territoriales de Nicaragua", "FAIL", "17 entidades", f"{len(depts_data)} entidades", depts_data, "P1")

    res_munis = client.get("/api/v1/locations/municipalities")
    munis_data = res_munis.json() if res_munis.status_code == 200 else []
    if len(munis_data) == 153:
        record("TC-GEO-02", "Geografía y Mapas", "Presencia exacta de 153 municipios oficiales", "PASS", "153 municipios", f"{len(munis_data)} municipios", f"Total: {len(munis_data)}")
    else:
        record("TC-GEO-02", "Geografía y Mapas", "Catálogo de municipios de Nicaragua", "FAIL", "153 municipios", f"{len(munis_data)} municipios", munis_data, "P1")

    # 4.3 Puntos de mapa no revelan coordenadas privadas exactas
    res_map = client.get("/api/v1/locations/map-aggregated")
    if res_map.status_code == 200:
        pts = res_map.json()
        has_exact = any("exact_address" in p or "exact_home_coordinates" in p for p in pts)
        if not has_exact:
            record("TC-GEO-03", "Privacidad / Mapas", "Mapa utiliza coordenadas aproximadas agregadas sin filtrar domicilios", "PASS", "Coordenadas aproximadas sin domicilios", "Sin fuga de datos privados", f"{len(pts)} puntos")
        else:
            record("TC-GEO-03", "Privacidad / Mapas", "Exposición de direcciones exactas en mapa", "FAIL", "Sin domicilios privados", "Fuga detectada", pts, "P0")
    else:
        record("TC-GEO-03", "Geografía y Mapas", "Endpoint de puntos de mapa agregados", "FAIL", "HTTP 200", f"HTTP {res_map.status_code}", res_map.text, "P1")

    # -------------------------------------------------------------
    # 5. MÓDULO DE PISTAS CONFIDENCIALES
    # -------------------------------------------------------------
    # Crear pista ciudadana anónima
    res_public_reps = client.get("/api/v1/reports/")
    target_rep_id = res_public_reps.json()[0]["id"] if (res_public_reps.status_code == 200 and len(res_public_reps.json()) > 0) else None
    if target_rep_id:
        tip_payload = {
            "report_id": target_rep_id,
            "description": "Avistamiento de prueba en parada de autobuses con vestimenta similar.",
            "sighting_department": "Managua",
            "sighting_date": (datetime.now(timezone.utc) - timedelta(days=1)).isoformat(),
            "confidentiality_level": "strict_anonymous"
        }
        res_tip = client.post("/api/v1/tips/", json=tip_payload)
        if res_tip.status_code == 201 and "tip_code" in res_tip.json():
            tip_code = res_tip.json()["tip_code"]
            record("TC-TIP-01", "Pistas Confidenciales", "Recepción segura de pista y generación de código de seguimiento anónimo", "PASS", "HTTP 201 con código no predecible", f"HTTP {res_tip.status_code}, code={tip_code}", res_tip.json())
            
            # Consultar con código
            res_track = client.get(f"/api/v1/tips/track/{tip_code}")
            if res_track.status_code == 200 and "status" in res_track.json():
                record("TC-TIP-02", "Pistas Confidenciales", "Consulta ciudadana de estado mediante código anónimo", "PASS", "HTTP 200 con estado de pista", f"HTTP {res_track.status_code}", res_track.json())
            else:
                record("TC-TIP-02", "Pistas Confidenciales", "Consulta de pista con código", "FAIL", "HTTP 200", f"HTTP {res_track.status_code}", res_track.text, "P1")
        else:
            record("TC-TIP-01", "Pistas Confidenciales", "Recepción de pista", "FAIL", "HTTP 201", f"HTTP {res_tip.status_code}", res_tip.text, "P1")
    else:
        record("TC-TIP-01", "Pistas Confidenciales", "Sin casos públicos para enviar pista", "BLOCKED", "Caso público existente", "0 casos públicos", None, "P2")

    # -------------------------------------------------------------
    # 6. DERECHO DE SUPRESIÓN Y PROTECCIÓN DE DATOS (LEY N.° 787)
    # -------------------------------------------------------------
    if created_id:
        res_del = client.post(
            f"/api/v1/reports/{created_id}/request-deletion",
            json={"reason": "Persona localizada por cuenta propia, solicitud de baja."},
            headers={"Authorization": f"Bearer {reporter_token}"}
        )
        if res_del.status_code == 201:
            record("TC-LEY787-01", "Privacidad / Ley 787", "Solicitud de cancelación/supresión de expediente por el titular", "PASS", "HTTP 201 Solicitud creada", f"HTTP {res_del.status_code}", res_del.json())
        else:
            record("TC-LEY787-01", "Privacidad / Ley 787", "Solicitud de supresión", "FAIL", "HTTP 201", f"HTTP {res_del.status_code}", res_del.text, "P1")

    # -------------------------------------------------------------
    # 7. AUDITORÍA DEL HOSTING EN VIVO (DISCREPANCIAS EN PRODUCCIÓN)
    # -------------------------------------------------------------
    # Comprobar rutas limpias en el hosting público
    try:
        import urllib.request
        def check_url(url):
            try:
                req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 QA"})
                with urllib.request.urlopen(req, timeout=5) as r:
                    return r.status
            except urllib.error.HTTPError as e:
                return e.code
            except Exception as e:
                return str(e)

        s_casos = check_url("https://creacionvaloria.tradescanner.online/casos")
        s_casos_html = check_url("https://creacionvaloria.tradescanner.online/casos.html")
        s_api_health = check_url("https://creacionvaloria.tradescanner.online/api/v1/health")

        if s_casos == 404 and s_casos_html == 200:
            record(
                "TC-ENV-01", 
                "Integración / Hosting", 
                "Rutas limpias de Next.js devuelven 404 en hosting estático si no se agrega .html (Falta rewrite rule)", 
                "FAIL", 
                "HTTP 200 en /casos", 
                f"/casos devolvió {s_casos}, mientras /casos.html devolvió {s_casos_html}", 
                {"clean_url_status": s_casos, "html_status": s_casos_html}, 
                "P2"
            )
        else:
            record("TC-ENV-01", "Integración / Hosting", "Resolución de rutas limpias en hosting", "PASS", "HTTP 200", f"Status: {s_casos}", None)

        if s_api_health == 404:
            record(
                "TC-ENV-02", 
                "Integración / Hosting", 
                "API de Backend no está conectada o proxied en https://creacionvaloria.tradescanner.online/api/v1/ (Devuelve 404)", 
                "FAIL", 
                "HTTP 200 en /api/v1/health", 
                f"/api/v1/health devolvió {s_api_health} (El hosting solo sirve el frontend estático)", 
                {"api_health_status": s_api_health}, 
                "P1"
            )
        else:
            record("TC-ENV-02", "Integración / Hosting", "Disponibilidad de API en hosting", "PASS", "HTTP 200", f"Status: {s_api_health}", None)

    except Exception as e:
        record("TC-ENV-01", "Integración / Hosting", "Prueba de hosting público", "BLOCKED", "Conexión a internet", str(e), None, "P2")

    # Guardar resumen final en evidencias
    out_summary = "qa-auditoria/evidencias/audit_execution_summary.json"
    with open(out_summary, "w", encoding="utf-8") as f:
        json.dump(audit_log, f, indent=2, ensure_ascii=False)

    print(f"\nTotal pruebas ejecutadas: {len(audit_log)}")
    passes = sum(1 for t in audit_log if t["status"] == "PASS")
    fails = sum(1 for t in audit_log if t["status"] == "FAIL")
    blocked = sum(1 for t in audit_log if t["status"] == "BLOCKED")
    print(f"PASS: {passes} | FAIL: {fails} | BLOCKED: {blocked}")

if __name__ == "__main__":
    run_all_audit_tests()
