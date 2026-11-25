import os
import logging
from fastapi import FastAPI, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from sqlalchemy.exc import SQLAlchemyError
from app.core.config import settings
from app.core.database import Base, engine, SessionLocal
import app.models.entities
from app.core.seed_geography import seed_nicaragua_geography
from app.api.v1 import (
    auth, reports, search, locations, 
    tips, admin, ai_assistance, statistics,
    notifications
)

logger = logging.getLogger("encuentrame_nicaragua")
logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(name)s: %(message)s")

# Initialize database schema safely
try:
    Base.metadata.create_all(bind=engine)
except Exception as e:
    logger.warning(f"Aviso durante create_all inicial: {e}")

# Ensure geographic division catalog is seeded idempotently
try:
    with SessionLocal() as init_db:
        if init_db.query(app.models.entities.Department).count() == 0:
            seed_nicaragua_geography(init_db)
except Exception as e:
    logger.warning(f"Aviso en inicialización de catálogo geográfico: {e}")

app = FastAPI(
    title=settings.PROJECT_NAME,
    description=settings.PROJECT_DESCRIPTION,
    version=settings.VERSION,
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json"
)

# Global Exception Handlers to guarantee clean JSON errors and prevent unhandled 500s
@app.exception_handler(SQLAlchemyError)
async def sqlalchemy_exception_handler(request: Request, exc: SQLAlchemyError):
    logger.error(f"Error de base de datos en {request.method} {request.url.path}: {exc}", exc_info=True)
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "detail": "Error interno de base de datos. Verifique la conexión o contacte al administrador.",
            "code": "DATABASE_ERROR"
        }
    )

@app.exception_handler(Exception)
async def generic_exception_handler(request: Request, exc: Exception):
    logger.error(f"Excepción no controlada en {request.method} {request.url.path}: {exc}", exc_info=True)
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "detail": "Ha ocurrido un error interno en el servidor. El incidente ha sido registrado para investigación.",
            "code": "INTERNAL_SERVER_ERROR"
        }
    )

# CORS Configuration: Uses explicit authorized origins (OWASP compliant, never wildcard with credentials)
cors_origins = settings.BACKEND_CORS_ORIGINS
app.add_middleware(
    CORSMiddleware,
    allow_origins=cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Security headers middleware
@app.middleware("http")
async def add_security_headers(request: Request, call_next):
    response = await call_next(request)
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "DENY"
    response.headers["X-XSS-Protection"] = "1; mode=block"
    response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
    return response

# Include domain routers
app.include_router(auth.router, prefix=settings.API_V1_STR)
app.include_router(reports.router, prefix=settings.API_V1_STR)
app.include_router(search.router, prefix=settings.API_V1_STR)
app.include_router(locations.router, prefix=settings.API_V1_STR)
app.include_router(tips.router, prefix=settings.API_V1_STR)
app.include_router(admin.router, prefix=settings.API_V1_STR)
app.include_router(ai_assistance.router, prefix=settings.API_V1_STR)
app.include_router(statistics.router, prefix=settings.API_V1_STR)
app.include_router(notifications.router, prefix=settings.API_V1_STR)

@app.get("/health", tags=["Health"])
def health_check():
    return {
        "status": "healthy",
        "service": settings.PROJECT_NAME,
        "version": settings.VERSION,
        "environment": settings.ENVIRONMENT
    }

# Dynamic Static Frontend Mounting for Single-Port / Unified Domain Deployment
STATIC_DIR = os.getenv("FRONTEND_STATIC_DIR")
if not STATIC_DIR:
    candidate_dirs = [
        os.path.abspath(os.path.join(os.path.dirname(__file__), "../../frontend/out")),
        os.path.abspath("./frontend/out"),
        os.path.abspath("./out"),
        os.path.abspath("../frontend/out"),
        os.path.abspath("./static"),
    ]
    for c in candidate_dirs:
        if os.path.isdir(c) and os.path.isfile(os.path.join(c, "index.html")):
            STATIC_DIR = c
            break

if STATIC_DIR and os.path.isdir(STATIC_DIR):
    logger.info(f"Frontend estático detectado y montado desde: {STATIC_DIR}")

    # Mount _next static assets (CSS, JS bundles, static media)
    next_dir = os.path.join(STATIC_DIR, "_next")
    if os.path.isdir(next_dir):
        app.mount("/_next", StaticFiles(directory=next_dir), name="next_static")

    # Mount images directory
    images_dir = os.path.join(STATIC_DIR, "images")
    if os.path.isdir(images_dir):
        app.mount("/images", StaticFiles(directory=images_dir), name="images_static")

    # Mount fonts directory
    fonts_dir = os.path.join(STATIC_DIR, "fonts")
    if os.path.isdir(fonts_dir):
        app.mount("/fonts", StaticFiles(directory=fonts_dir), name="fonts_static")

    @app.get("/{full_path:path}", tags=["Frontend"])
    async def serve_frontend(full_path: str, request: Request):
        # Exclude API endpoints or technical paths
        if full_path.startswith("api/") or full_path.startswith("docs") or full_path.startswith("redoc") or full_path.startswith("openapi.json"):
            return JSONResponse(status_code=404, content={"detail": "Not Found"})

        # Si el cliente solicita explícitamente JSON en la raíz
        accept = request.headers.get("accept", "")
        if (not full_path or full_path == "") and ("application/json" in accept or "*/*" in accept) and "text/html" not in accept:
            return JSONResponse({
                "message": f"Bienvenido a la API de {settings.PROJECT_NAME}",
                "docs": "/docs",
                "health": "/health"
            })

        clean_path = full_path.strip("/")

        # 1. Exact static file match (e.g. 404.html, favicon.ico)
        target_file = os.path.join(STATIC_DIR, clean_path)
        if clean_path and os.path.isfile(target_file):
            return FileResponse(target_file)

        # 2. Clean URL match (e.g. /casos -> casos.html, /mapa -> mapa.html)
        html_target = os.path.join(STATIC_DIR, f"{clean_path}.html")
        if clean_path and os.path.isfile(html_target):
            return FileResponse(html_target)

        # 3. Directory index match (e.g. /casos/ -> casos/index.html)
        dir_index = os.path.join(STATIC_DIR, clean_path, "index.html")
        if clean_path and os.path.isfile(dir_index):
            return FileResponse(dir_index)

        # 4. Dynamic case detail match (e.g. /casos/EN-2026-0001)
        if clean_path.startswith("casos/"):
            sub_id = clean_path.split("/", 1)[1]
            case_html = os.path.join(STATIC_DIR, "casos", f"{sub_id}.html")
            if os.path.isfile(case_html):
                return FileResponse(case_html)
            placeholder_file = os.path.join(STATIC_DIR, "casos", "placeholder.html")
            if os.path.isfile(placeholder_file):
                return FileResponse(placeholder_file)

        # 5. Root index.html
        if not clean_path:
            index_file = os.path.join(STATIC_DIR, "index.html")
            if os.path.isfile(index_file):
                return FileResponse(index_file)

        # 6. Responder 404 con 404.html si existe
        not_found_file = os.path.join(STATIC_DIR, "404.html")
        if os.path.isfile(not_found_file):
            return FileResponse(not_found_file, status_code=404)

        return JSONResponse(status_code=404, content={"detail": "Página no encontrada"})
else:
    @app.get("/", tags=["Root"])
    def root():
        return {
            "message": f"Bienvenido a la API de {settings.PROJECT_NAME}",
            "docs": "/docs",
            "health": "/health"
        }
