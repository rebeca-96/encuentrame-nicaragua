import os
import sys
import logging

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
BACKEND_DIR = os.path.join(BASE_DIR, "backend")

# Asegurar que el directorio backend esté en el sys.path si existe
if os.path.isdir(BACKEND_DIR) and BACKEND_DIR not in sys.path:
    sys.path.insert(0, BACKEND_DIR)

logger = logging.getLogger("encuentrame_nicaragua")

try:
    # 1. Intentar cargar la aplicación completa de producción con todos los endpoints y base de datos
    from app.main import app
    logger.info("Aplicación backend completa cargada exitosamente desde backend/app/main.py")
except Exception as exc:
    logger.warning(f"No se pudo cargar backend.app.main ({exc}). Iniciando servidor autónomo con soporte API integrado.")
    
    import json
    import uuid
    from datetime import datetime, timezone
    from fastapi import FastAPI, Request, status, HTTPException
    from fastapi.responses import FileResponse, JSONResponse
    from fastapi.staticfiles import StaticFiles
    from fastapi.middleware.cors import CORSMiddleware
    from pydantic import BaseModel, EmailStr
    from typing import Optional, List

    app = FastAPI(
        title="Encuéntrame Nicaragua - Web Hosting & API",
        version="1.0.0",
        docs_url="/docs",
        redoc_url="/redoc"
    )

    # Permitir orígenes cruzados (CORS)
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Directorio de salida estática
    OUT_DIR = os.path.join(BASE_DIR, "out")
    if not os.path.isdir(OUT_DIR):
        for candidate in ["./out", "./frontend/out", "../frontend/out", "./static"]:
            c_path = os.path.abspath(os.path.join(BASE_DIR, candidate))
            if os.path.isdir(c_path):
                OUT_DIR = c_path
                break

    # Registro en memoria de usuarios registrados
    USERS_DB = {
        "admin@encuentrame.ni": {
            "id": "usr-admin-01",
            "email": "admin@encuentrame.ni",
            "password": "AdminPass2026!",
            "full_name": "Lic. Sofía Montenegro",
            "role": "admin",
            "is_active": True
        },
        "reportante@encuentrame.ni": {
            "id": "usr-rep-01",
            "email": "reportante@encuentrame.ni",
            "password": "ReportPass2026!",
            "full_name": "Elena María Alvarado",
            "role": "reporter",
            "is_active": True
        }
    }

    class LoginRequest(BaseModel):
        email: EmailStr
        password: str

    class UserRegister(BaseModel):
        email: EmailStr
        password: str
        confirm_password: Optional[str] = None
        full_name: str
        phone_number: Optional[str] = None
        role: Optional[str] = "reporter"

    # ==========================================================
    # ENDPOINTS DE AUTENTICACIÓN (/api/v1/auth)
    # ==========================================================
    @app.post("/api/v1/auth/register", status_code=status.HTTP_201_CREATED)
    async def register_standalone(user_in: UserRegister):
        email_clean = user_in.email.lower().strip()
        if email_clean in USERS_DB:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Ya existe una cuenta registrada con este correo electrónico"
            )
        
        if user_in.confirm_password and user_in.password != user_in.confirm_password:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail="Las contraseñas ingresadas no coinciden"
            )

        new_user = {
            "id": str(uuid.uuid4()),
            "email": email_clean,
            "password": user_in.password,
            "full_name": user_in.full_name.strip(),
            "phone_number": user_in.phone_number,
            "role": user_in.role or "reporter",
            "is_active": True,
            "created_at": datetime.now(timezone.utc).isoformat()
        }
        USERS_DB[email_clean] = new_user

        return {
            "id": new_user["id"],
            "email": new_user["email"],
            "full_name": new_user["full_name"],
            "phone_number": new_user["phone_number"],
            "role": new_user["role"],
            "is_active": True,
            "created_at": new_user["created_at"]
        }

    @app.post("/api/v1/auth/login")
    async def login_standalone(req: LoginRequest):
        email_clean = req.email.lower().strip()
        user = USERS_DB.get(email_clean)
        if not user or user["password"] != req.password:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Credenciales incorrectas o usuario no registrado"
            )
        
        return {
            "access_token": f"token_{user['role']}_{uuid.uuid4()}",
            "token_type": "bearer",
            "role": user["role"],
            "user_id": user["id"],
            "full_name": user["full_name"]
        }

    @app.post("/api/v1/auth/logout")
    async def logout_standalone():
        return {"message": "Sesión cerrada correctamente"}

    # ==========================================================
    # ENDPOINTS DE REPORTES PÚBLICOS (/api/v1/reports)
    # ==========================================================
    DEFAULT_REPORTS = [
        {
            "id": "case-01",
            "case_number": "EN-2026-0001",
            "first_name": "Mateo Andrés",
            "last_name": "García Centeno",
            "age_at_disappearance": 14,
            "gender": "male",
            "department": "Managua",
            "municipality": "Ciudad Sandino",
            "disappearance_date": "2026-11-16T15:30:00Z",
            "physical_description": "Estatura 1.55m, contextura delgada, tez morena clara, cabello negro lacio corto, lunar visible cerca de la ceja derecha.",
            "primary_photo_url": "/images/avatar-placeholder.svg",
            "is_minor": True,
            "status": "published",
            "published_at": "2026-11-17T08:00:00Z"
        },
        {
            "id": "case-02",
            "case_number": "EN-2026-0002",
            "first_name": "Valeria Nicole",
            "last_name": "Pérez Fonseca",
            "age_at_disappearance": 17,
            "gender": "female",
            "department": "Matagalpa",
            "municipality": "Sébaco",
            "disappearance_date": "2026-11-14T09:15:00Z",
            "physical_description": "Estatura 1.62m, complexión delgada, piel blanca, ojos castaños claros, cabello castaño largo ondulado.",
            "primary_photo_url": "/images/avatar-placeholder.svg",
            "is_minor": True,
            "status": "published",
            "published_at": "2026-11-15T10:00:00Z"
        },
        {
            "id": "case-03",
            "case_number": "EN-2026-0003",
            "first_name": "Don Manuel de Jesús",
            "last_name": "Rocha Blandón",
            "age_at_disappearance": 73,
            "gender": "male",
            "department": "León",
            "municipality": "León",
            "disappearance_date": "2026-11-10T07:00:00Z",
            "physical_description": "Estatura 1.68m, cabello canoso, anteojos con marco metálico, bigote blanco.",
            "primary_photo_url": "/images/avatar-placeholder.svg",
            "is_minor": False,
            "status": "closed",
            "published_at": "2026-11-11T09:00:00Z"
        },
        {
            "id": "case-04",
            "case_number": "EN-2026-0004",
            "first_name": "Yader Francisco",
            "last_name": "Gutiérrez Marenco",
            "age_at_disappearance": 29,
            "gender": "male",
            "department": "Chinandega",
            "municipality": "Corinto",
            "disappearance_date": "2026-11-12T18:00:00Z",
            "physical_description": "Estatura 1.74m, piel morena, complexión atlética, cicatriz de 4 cm en antebrazo izquierdo.",
            "primary_photo_url": "/images/avatar-placeholder.svg",
            "is_minor": False,
            "status": "published",
            "published_at": "2026-11-13T12:00:00Z"
        },
        {
            "id": "case-05",
            "case_number": "EN-2026-0005",
            "first_name": "Lucía Esperanza",
            "last_name": "Solís Jarquín",
            "age_at_disappearance": 16,
            "gender": "female",
            "department": "Estelí",
            "municipality": "Estelí",
            "disappearance_date": "2026-11-15T13:45:00Z",
            "physical_description": "Estatura 1.58m, contextura media, tez trigueña, cabello castaño hasta los hombros.",
            "primary_photo_url": "/images/avatar-placeholder.svg",
            "is_minor": True,
            "status": "published",
            "published_at": "2026-11-16T09:00:00Z"
        },
        {
            "id": "case-07",
            "case_number": "EN-2026-0007",
            "first_name": "Adriana Marcela",
            "last_name": "Tinoco Rivas",
            "age_at_disappearance": 21,
            "gender": "female",
            "department": "Chontales",
            "municipality": "Juigalpa",
            "disappearance_date": "2026-11-06T11:00:00Z",
            "physical_description": "Estatura 1.63m, piel morena clara, cabello castaño amarrado en coleta.",
            "primary_photo_url": "/images/avatar-placeholder.svg",
            "is_minor": False,
            "status": "closed",
            "published_at": "2026-11-07T13:00:00Z"
        },
        {
            "id": "case-09",
            "case_number": "EN-2026-0009",
            "first_name": "Kenia Jamileth",
            "last_name": "López Obando",
            "age_at_disappearance": 19,
            "gender": "female",
            "department": "Masaya",
            "municipality": "Nindirí",
            "disappearance_date": "2026-11-08T17:30:00Z",
            "physical_description": "Estatura 1.60m, piel morena clara, cabello castaño lacio a la cintura.",
            "primary_photo_url": "/images/avatar-placeholder.svg",
            "is_minor": False,
            "status": "closed",
            "published_at": "2026-11-09T08:30:00Z"
        },
        {
            "id": "case-20",
            "case_number": "EN-2026-0020",
            "first_name": "Gerardo Antonio",
            "last_name": "Mendoza Espinoza",
            "age_at_disappearance": 52,
            "gender": "male",
            "department": "Managua",
            "municipality": "Managua",
            "disappearance_date": "2026-11-01T12:00:00Z",
            "physical_description": "Estatura 1.70m, tez morena, bigote poblado, anteojos de lectura.",
            "primary_photo_url": "/images/avatar-placeholder.svg",
            "is_minor": False,
            "status": "closed",
            "published_at": "2026-11-02T10:00:00Z"
        }
    ]

    @app.get("/api/v1/reports/")
    async def list_reports_standalone(
        status: Optional[str] = None,
        department: Optional[str] = None,
        municipality: Optional[str] = None,
        gender: Optional[str] = None,
        is_minor: Optional[bool] = None,
        q: Optional[str] = None
    ):
        res = list(DEFAULT_REPORTS)
        if status in ("active", "activos", "published"):
            res = [r for r in res if r["status"] == "published"]
        elif status in ("inactive", "no_activos", "closed", "resolved"):
            res = [r for r in res if r["status"] in ("closed", "resolved")]
        
        if department and department != "all":
            res = [r for r in res if department.lower() in r["department"].lower()]
        if municipality and municipality != "all":
            res = [r for r in res if municipality.lower() in r["municipality"].lower()]
        if gender and gender != "all":
            res = [r for r in res if r["gender"].lower() == gender.lower()]
        if is_minor is not None:
            res = [r for r in res if r["is_minor"] == is_minor]
        if q and q.strip():
            term = q.strip().lower()
            res = [r for r in res if term in r["first_name"].lower() or term in r["last_name"].lower() or term in r["case_number"].lower() or term in r["physical_description"].lower()]
        return res

    @app.get("/api/v1/reports/{id_or_case}")
    async def get_report_detail_standalone(id_or_case: str):
        for r in DEFAULT_REPORTS:
            if r["id"] == id_or_case or r["case_number"].lower() == id_or_case.lower():
                detail = dict(r)
                detail.update({
                    "approximate_latitude": 12.1364,
                    "approximate_longitude": -86.2514,
                    "clothing_description": "Vestimenta casual según el último reporte.",
                    "circumstances": "Reportado por familiares para coordinar búsqueda responsable.",
                    "vulnerability_flag": r["is_minor"] or r["age_at_disappearance"] >= 65,
                    "photos": [{"id": "p1", "storage_key": "avatar", "url": r["primary_photo_url"], "is_primary": True, "original_filename": "foto.webp"}]
                })
                return detail
        raise HTTPException(status_code=404, detail="Caso no encontrado")

    @app.post("/api/v1/reports/")
    async def create_report_standalone(req: Request):
        data = await req.json()
        num = len(DEFAULT_REPORTS) + 1
        new_rep = {
            "id": f"case-{num:02d}",
            "case_number": f"EN-2026-{num:04d}",
            "first_name": data.get("first_name", "Desconocido"),
            "last_name": data.get("last_name", ""),
            "age_at_disappearance": data.get("age_at_disappearance", 18),
            "gender": data.get("gender", "unspecified"),
            "department": data.get("department", "Managua"),
            "municipality": data.get("municipality", "Managua"),
            "disappearance_date": data.get("disappearance_date", datetime.now(timezone.utc).isoformat()),
            "physical_description": data.get("physical_description", "Sin descripción"),
            "primary_photo_url": data.get("primary_photo_url", "/images/avatar-placeholder.svg"),
            "is_minor": data.get("is_minor", False),
            "status": "published",
            "created_at": datetime.now(timezone.utc).isoformat()
        }
        DEFAULT_REPORTS.insert(0, new_rep)
        return new_rep

    @app.post("/api/v1/reports/{report_id}/photos")
    async def upload_photo_standalone(report_id: str, req: Request):
        form = await req.form()
        uploaded_file = form.get("file")
        if not uploaded_file:
            raise HTTPException(status_code=400, detail="No se proporcionó archivo")
        content = await uploaded_file.read()
        storage_dir = os.path.join(BASE_DIR, "storage", "uploads")
        os.makedirs(storage_dir, exist_ok=True)
        unique_name = f"{uuid.uuid4().hex}.webp"
        file_path = os.path.join(storage_dir, unique_name)
        with open(file_path, "wb") as f:
            f.write(content)
        photo_url = f"/api/v1/reports/photos/{unique_name}"
        for rep in DEFAULT_REPORTS:
            if rep["id"] == report_id or rep["case_number"] == report_id:
                rep["primary_photo_url"] = photo_url
                break
        return {"id": f"photo_{unique_name}", "storage_key": unique_name, "url": photo_url}

    @app.get("/api/v1/reports/photos/{storage_key}")
    async def get_photo_standalone(storage_key: str):
        storage_dir = os.path.join(BASE_DIR, "storage", "uploads")
        file_path = os.path.join(storage_dir, storage_key)
        if os.path.isfile(file_path):
            return FileResponse(file_path)
        avatar_path = os.path.join(OUT_DIR, "images", "avatars", storage_key)
        if os.path.isfile(avatar_path):
            return FileResponse(avatar_path)
        raise HTTPException(status_code=404, detail="Fotografía no encontrada")

    @app.get("/api/v1/health")
    async def health_check():
        return {"status": "healthy", "service": "encuentrame_nicaragua"}

    # ==========================================================
    # MONTAJE DE ARCHIVOS ESTÁTICOS Y ENRUTAMIENTO SPA
    # ==========================================================
    if os.path.isdir(OUT_DIR):
        next_dir = os.path.join(OUT_DIR, "_next")
        if os.path.isdir(next_dir):
            app.mount("/_next", StaticFiles(directory=next_dir), name="next_static")

        fonts_dir = os.path.join(OUT_DIR, "fonts")
        if os.path.isdir(fonts_dir):
            app.mount("/fonts", StaticFiles(directory=fonts_dir), name="fonts_static")

        images_dir = os.path.join(OUT_DIR, "images")
        if os.path.isdir(images_dir):
            app.mount("/images", StaticFiles(directory=images_dir), name="images_static")

        @app.get("/")
        async def root():
            index_file = os.path.join(OUT_DIR, "index.html")
            if os.path.isfile(index_file):
                return FileResponse(index_file)
            return JSONResponse(status_code=404, content={"error": "index.html no encontrado"})

        @app.get("/{full_path:path}")
        async def serve_static(full_path: str):
            # No interceptar rutas de API o documentación técnica
            if full_path.startswith("api/") or full_path.startswith("docs") or full_path.startswith("redoc") or full_path.startswith("openapi.json"):
                return JSONResponse(status_code=404, content={"detail": "Not Found"})

            clean_path = full_path.strip("/")

            # 1. Archivo directo exacto (ej. _next/static/..., favicon.ico)
            direct_file = os.path.join(OUT_DIR, clean_path)
            if clean_path and os.path.isfile(direct_file):
                return FileResponse(direct_file)

            # 2. Archivo HTML directo (ej. /casos -> out/casos.html, /mapa -> out/mapa.html)
            html_file = os.path.join(OUT_DIR, f"{clean_path}.html")
            if clean_path and os.path.isfile(html_file):
                return FileResponse(html_file)

            # 3. Directorio con index.html (ej. /casos/ -> out/casos/index.html)
            dir_index = os.path.join(OUT_DIR, clean_path, "index.html")
            if clean_path and os.path.isfile(dir_index):
                return FileResponse(dir_index)

            # 4. Detalle de casos dinámicos (ej. casos/case-01, casos/EN-2026-0001)
            if clean_path.startswith("casos/"):
                sub_id = clean_path.split("/", 1)[1]
                case_html = os.path.join(OUT_DIR, "casos", f"{sub_id}.html")
                if os.path.isfile(case_html):
                    return FileResponse(case_html)
                placeholder_file = os.path.join(OUT_DIR, "casos", "placeholder.html")
                if os.path.isfile(placeholder_file):
                    return FileResponse(placeholder_file)

            # 5. Si la página no existe, responder 404 con 404.html
            not_found_file = os.path.join(OUT_DIR, "404.html")
            if os.path.isfile(not_found_file):
                return FileResponse(not_found_file, status_code=404)

            return JSONResponse(status_code=404, content={"error": "Página no encontrada"})
