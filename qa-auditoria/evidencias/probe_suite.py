import os
import sys
import json
import urllib.request
import urllib.error

# Ensure backend can be imported
sys.path.insert(0, os.path.abspath("backend"))

from fastapi.testclient import TestClient
from app.main import app
from app.core.config import settings
from app.models.entities import User, MissingPersonReport, ConfidentialTip, AuditLog, ReportPhoto, Department, Municipality
from app.core.security import create_access_token, get_password_hash
from sqlalchemy import create_engine, inspect
from sqlalchemy.orm import sessionmaker

client = TestClient(app)

results = {
    "live_hosting": {},
    "endpoints": {},
    "validations": {},
    "security": {},
    "database": {},
    "findings": []
}

# 1. Probing Live Hosting
live_base = "https://creacionvaloria.tradescanner.online"
live_urls = [
    "/",
    "/index.html",
    "/casos.html",
    "/mapa.html",
    "/reportar.html",
    "/pistas.html",
    "/login.html",
    "/admin.html",
    "/Personas_Desaparecidas_Nicaragua.mp4",
    "/_next/static/css/258f9f5fa0e5b894.css",
    "/fonts/Inter-Regular.woff2",
    "/images/avatar-placeholder.svg",
    "/api/v1/health",
    "/api/v1/locations/departments",
    "/api/v1/reports/",
    "/casos",
    "/mapa",
    "/reportar",
    "/pistas",
    "/login",
    "/admin"
]

print("--- 1. PROBING LIVE HOSTING ---")
for path in live_urls:
    url = f"{live_base}{path}"
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 QA-Auditor"})
    try:
        with urllib.request.urlopen(req, timeout=5) as r:
            status = r.status
            ctype = r.headers.get("Content-Type", "")
            clen = r.headers.get("Content-Length", len(r.read()))
            results["live_hosting"][path] = {"status": status, "content_type": ctype, "size": int(clen)}
            print(f"LIVE {path} -> {status} ({ctype})")
    except urllib.error.HTTPError as e:
        results["live_hosting"][path] = {"status": e.code, "error": str(e)}
        print(f"LIVE {path} -> {e.code} (ERROR)")
    except Exception as e:
        results["live_hosting"][path] = {"status": "FAILED", "error": str(e)}
        print(f"LIVE {path} -> FAILED: {e}")

# 2. Local Backend Endpoint Exploration
print("\n--- 2. LOCAL BACKEND EXPLORATION ---")
# Health & Root
r_health = client.get("/health")
results["endpoints"]["GET /health"] = {"status": r_health.status_code, "data": r_health.json()}

r_root = client.get("/", headers={"Accept": "application/json"})
results["endpoints"]["GET / (JSON)"] = {"status": r_root.status_code, "data": r_root.json()}

# Locations catalog
r_depts = client.get("/api/v1/locations/departments")
results["endpoints"]["GET /api/v1/locations/departments"] = {"status": r_depts.status_code, "count": len(r_depts.json()) if r_depts.status_code == 200 else 0}

r_munis = client.get("/api/v1/locations/municipalities")
results["endpoints"]["GET /api/v1/locations/municipalities"] = {"status": r_munis.status_code, "count": len(r_munis.json()) if r_munis.status_code == 200 else 0}

# Public reports
r_reports = client.get("/api/v1/reports/")
results["endpoints"]["GET /api/v1/reports/"] = {"status": r_reports.status_code, "count": len(r_reports.json()) if r_reports.status_code == 200 else 0}

# Search map points
r_map = client.get("/api/v1/search/map-points")
results["endpoints"]["GET /api/v1/search/map-points"] = {"status": r_map.status_code, "count": len(r_map.json()) if r_map.status_code == 200 else 0}

# 3. Security & Validation Probes
print("\n--- 3. SECURITY & BOUNDARY TESTS ---")

# A. Unauthenticated Admin Endpoints (OWASP Broken Access Control)
admin_endpoints = [
    ("GET", "/api/v1/admin/reports/pending"),
    ("GET", "/api/v1/admin/tips"),
    ("GET", "/api/v1/admin/audit-logs"),
    ("GET", "/api/v1/admin/deletion-requests")
]
for method, ep in admin_endpoints:
    res = client.request(method, ep)
    results["security"][f"Unauth {method} {ep}"] = {
        "status": res.status_code,
        "blocked": res.status_code in [401, 403]
    }
    print(f"Security: Unauth {method} {ep} -> {res.status_code} (Blocked: {res.status_code in [401, 403]})")

# B. Citizen Token on Admin Endpoints (Privilege Escalation)
citizen_token = create_access_token("test_citizen@encuentrame.ni", role="citizen")
for method, ep in admin_endpoints:
    res = client.request(method, ep, headers={"Authorization": f"Bearer {citizen_token}"})
    results["security"][f"Citizen Role on {method} {ep}"] = {
        "status": res.status_code,
        "blocked": res.status_code in [401, 403]
    }
    print(f"Security: Citizen Role {method} {ep} -> {res.status_code} (Blocked: {res.status_code in [401, 403]})")

# C. Path Traversal on Photos
traversal_payloads = [
    "../../../../etc/passwd",
    "..\\..\\..\\..\\Windows\\win.ini",
    "%2e%2e%2fREADME.md",
    "invalid_key_name"
]
for p in traversal_payloads:
    res = client.get(f"/api/v1/reports/photos/{p}")
    results["security"][f"Traversal {p}"] = {
        "status": res.status_code,
        "safe": res.status_code in [400, 404]
    }

# D. Input Validations on /reports/ (Future Dates, Boundary Strings, Territory Mismatch)
# Future date
bad_date_payload = {
    "first_name": "Test",
    "last_name": "Future",
    "gender": "male",
    "age_at_disappearance": 25,
    "disappearance_date": "2099-01-01T00:00:00",
    "department": "Managua",
    "municipality": "Managua",
    "physical_description": "Persona de prueba para validaciones",
    "clothing_description": "Ropa de prueba",
    "circumstances": "Circunstancias de prueba",
    "reporting_person_name": "Familiar Test",
    "reporting_person_phone": "+50588888888",
    "legal_consent_accepted": True
}
res_future = client.post("/api/v1/reports/", json=bad_date_payload)
results["validations"]["Future Date Rejection"] = {
    "status": res_future.status_code,
    "rejected": res_future.status_code == 422
}

# Territory mismatch (Municipality not in Department)
bad_geo_payload = dict(bad_date_payload)
bad_geo_payload["disappearance_date"] = "2024-01-01T00:00:00"
bad_geo_payload["department"] = "Managua"
bad_geo_payload["municipality"] = "Matagalpa" # Belongs to Matagalpa, not Managua!
res_geo = client.post("/api/v1/reports/", json=bad_geo_payload)
results["validations"]["Territorial Inconsistency Rejection"] = {
    "status": res_geo.status_code,
    "rejected": res_geo.status_code == 422
}

# Negative age
bad_age_payload = dict(bad_geo_payload)
bad_age_payload["municipality"] = "Managua"
bad_age_payload["age_at_disappearance"] = -5
res_age = client.post("/api/v1/reports/", json=bad_age_payload)
results["validations"]["Negative Age Rejection"] = {
    "status": res_age.status_code,
    "rejected": res_age.status_code == 422
}

# Missing legal consent
no_consent_payload = dict(bad_geo_payload)
no_consent_payload["municipality"] = "Managua"
no_consent_payload["legal_consent_accepted"] = False
res_consent = client.post("/api/v1/reports/", json=no_consent_payload)
results["validations"]["Missing Consent Rejection"] = {
    "status": res_consent.status_code,
    "rejected": res_consent.status_code in [400, 422]
}

# E. Database Schema Inspection
print("\n--- 4. DATABASE SCHEMA INSPECTION ---")
from app.core.database import engine
inspector = inspect(engine)
tables = inspector.get_table_names()
results["database"]["tables"] = tables
print("Tables found:", tables)

for t in tables:
    columns = [c["name"] for c in inspector.get_columns(t)]
    fks = inspector.get_foreign_keys(t)
    results["database"][t] = {
        "columns": columns,
        "foreign_keys": fks
    }

# Save findings
out_file = "qa-auditoria/evidencias/probe_results.json"
with open(out_file, "w", encoding="utf-8") as f:
    json.dump(results, f, indent=2, ensure_ascii=False)

print(f"\nResultados guardados exitosamente en: {out_file}")
