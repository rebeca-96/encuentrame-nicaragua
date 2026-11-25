import httpx
import json
import io
from PIL import Image

BASE_URL = "http://127.0.0.1:8000"

def run_verification():
    print("=== INICIANDO VALIDACIÓN DEL MÓDULO DE FOTOGRAFÍAS REALES EN CATÁLOGO LOCAL ===")
    client = httpx.Client(base_url=BASE_URL, timeout=10.0)
    
    # 1. Health check
    res = client.get("/casos")
    print(f"GET /casos -> Status: {res.status_code}")
    assert res.status_code == 200, f"Expected 200 for /casos, got {res.status_code}"

    # 2. Login as reporter
    login_data = {
        "email": "reportante@encuentrame.ni",
        "password": "ReportPass2026!"
    }
    auth_res = client.post("/api/v1/auth/login", json=login_data)
    print(f"POST /api/v1/auth/login -> Status: {auth_res.status_code}")
    assert auth_res.status_code == 200, f"Login failed: {auth_res.text}"
    token = auth_res.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    # 3. Create a unique test report
    report_payload = {
        "first_name": "Valentina",
        "last_name": "Morales Ruiz",
        "nickname": "Valen",
        "age_at_disappearance": 19,
        "gender": "female",
        "disappearance_date": "2026-11-20T10:00:00Z",
        "department": "Granada",
        "municipality": "Granada",
        "neighborhood_zone": "Barrio Xalteva",
        "physical_description": "Estatura 1.62m, cabello castaño ondulado, ojos café claros.",
        "clothing_description": "Vestido floreado azul y sandalias café.",
        "circumstances": "Fue vista por última vez al salir de la universidad en Granada.",
        "is_minor": False,
        "consent": {
            "relationship_to_victim": "Hermana",
            "identity_doc_number": "281-201104-1002G",
            "accepted_terms": True
        }
    }
    create_res = client.post("/api/v1/reports/", json=report_payload, headers=headers)
    print(f"POST /api/v1/reports/ -> Status: {create_res.status_code}")
    assert create_res.status_code == 201, "Report creation failed"
    rep_data = create_res.json()
    rep_id = rep_data["id"]
    case_num = rep_data["case_number"]
    print(f"Caso creado: {case_num} (ID: {rep_id})")

    # 4. Create and upload an authentic real photo (generated with distinct pixel colors, not synthetic avatar)
    img_byte_arr = io.BytesIO()
    img = Image.new("RGB", (640, 800), color=(220, 80, 40))
    img.save(img_byte_arr, format="JPEG")
    img_bytes = img_byte_arr.getvalue()

    files = {"file": ("valentina_foto_real.jpg", img_bytes, "image/jpeg")}
    photo_res = client.post(f"/api/v1/reports/{rep_id}/photos", files=files, headers=headers)
    print(f"POST /api/v1/reports/{rep_id}/photos -> Status: {photo_res.status_code}")
    assert photo_res.status_code == 200, "Photo upload failed"
    photo_json = photo_res.json()
    storage_key = photo_json["storage_key"]
    photo_url = photo_json["url"]
    print(f"Fotografía real procesada y sanitizada: {storage_key}")
    print(f"URL generada para la imagen: {photo_url}")

    # 5. Approve report as admin/moderator so it's active and public in the backend catalog
    admin_login = client.post("/api/v1/auth/login", json={"email": "admin@encuentrame.ni", "password": "AdminPass2026!"})
    admin_token = admin_login.json()["access_token"]
    admin_headers = {"Authorization": f"Bearer {admin_token}"}
    
    appr_res = client.post(
        f"/api/v1/admin/reports/{rep_id}/moderate",
        json={"decision": "approve", "notes": "Caso verificado con documentación de identidad y fotografía autorizada."},
        headers=admin_headers
    )
    print(f"Aprobación de moderación: Status {appr_res.status_code}")
    assert appr_res.status_code == 200, "Moderator approval failed"

    # 6. Verify that GET /api/v1/reports/ returns the case with its real photo URL
    cat_res = client.get("/api/v1/reports/")
    print(f"GET /api/v1/reports/ -> Status: {cat_res.status_code}")
    assert cat_res.status_code == 200
    reports = cat_res.json()
    
    found_case = next((r for r in reports if r["id"] == rep_id), None)
    assert found_case is not None, "El caso recién creado no fue encontrado en el catálogo público"
    print(f"Caso verificado en catálogo: {found_case['case_number']} - {found_case['first_name']} {found_case['last_name']}")
    print(f"primary_photo_url en catálogo: {found_case['primary_photo_url']}")
    
    # Verificar que NO es avatar sintético
    assert "avatar" not in found_case["primary_photo_url"], "El caso está usando un avatar sintético en lugar de su foto real"
    assert found_case["primary_photo_url"] == f"/api/v1/reports/photos/{storage_key}"
    print(">>> VERIFICACIÓN EXITOSA: La fotografía en el catálogo es la imagen real subida por el usuario.")

    # 7. Fetch the real photo endpoint directly to verify 200 OK and valid image bytes
    img_get = client.get(found_case["primary_photo_url"])
    print(f"GET {found_case['primary_photo_url']} -> Status: {img_get.status_code}, Content-Type: {img_get.headers.get('content-type')}, Size: {len(img_get.content)} bytes")
    assert img_get.status_code == 200
    assert "image/webp" in img_get.headers.get("content-type", "")

    print("\nTODAS LAS PRUEBAS COMPLETADAS SATISFACTORIAMENTE EN EL ENTORNO LOCAL.")

if __name__ == "__main__":
    run_verification()
