# INFORME DE AUDITORÍA GENERAL DE CALIDAD DE SOFTWARE
## PROYECTO: ENCUÉNTRAME NICARAGUA
### Plataforma Inteligente de Búsqueda y Reunificación Familiar

**Fecha de Auditoría:** 18 de Noviembre de 2026  
**Versión del Sistema Auditado:** 1.0.0  
**Equipo Auditor:** Senior QA, Software Architect, Cybersecurity Specialist, DBA, Full Stack Senior, DevOps Engineer  
**Metodología:** Caja Blanca (inspección estática de código) y Caja Gris (ejecución de pruebas de integración y comportamiento real de API)  
**Veredicto General:** ⚠️ **APROBADO CON CONDICIONANTES — REQUIERE CORRECCIONES PREVIAS A PRODUCCIÓN (NO DEPLOYABLE TO PRODUCTION YET)**

---

## 1. OBJETIVO DEL DIAGNÓSTICO
Ejecutar una auditoría exhaustiva de calidad, estabilidad, seguridad, accesibilidad y arquitectura sobre el código fuente, la base de datos y la interfaz de la plataforma web **Encuéntrame Nicaragua**, garantizando que el sistema sea confiable, no filtre datos personales sensibles (en cumplimiento de la **Ley N.° 787 de Protección de Datos Personales** y el Código de la Niñez y la Adolescencia de Nicaragua), cuente con validaciones simétricas y esté libre de defectos críticos antes de su despliegue operativo.

---

## 2. INVENTARIO DEL STACK TECNOLÓGICO Y ARQUITECTURA

### 2.1. Backend
- **Framework:** FastAPI `0.165.0` sobre Python `3.12.10` y Starlette `1.10.0`.
- **Servidor ASGI:** Uvicorn `0.54.0`.
- **ORM & Database Toolkit:** SQLAlchemy `2.1.9` con soporte multibase (SQLite por defecto para desarrollo local / PostgreSQL nativo mediante `psycopg2-binary 2.9.13` para entornos productivos).
- **Control de Versiones de Base de Datos:** Alembic `1.20.1`.
- **Criptografía & Hashing:** Argon2 (`argon2-cffi 25.1.0`) y Bcrypt (`passlib 1.7.4`), JWT (`python-jose 3.5.0` con algoritmos criptográficos `cryptography 50.0.2`).
- **Validación de Datos:** Pydantic `2.14.3` y `pydantic-settings 2.16.3`.
- **Procesamiento de Imágenes:** Pillow `13.0.0` (sanitización de metadatos EXIF, conversión WebP, geofencing).
- **Testing:** Pytest `9.2.0`, `pytest-asyncio 1.5.0`, HTTPX `0.28.1`.

### 2.2. Frontend
- **Framework:** Next.js `14.2.35` (App Router) sobre React `18.2.0` y TypeScript `5.4.2`.
- **Estilos & Diseño:** Tailwind CSS `3.4.1`, PostCSS `8.4.38`, Lucide React `0.359.0`.
- **Sistemas de Información Geográfica (GIS):** Leaflet `1.9.4` y `@types/leaflet 1.9.8`.
- **Linter & Type Checking:** ESLint `8.57.1`, `eslint-config-next 14.2.35`.

### 2.3. Base de Datos Activa
- **Motor Actual:** SQLite `3` (`encuentrame_nicaragua.db`, 315 KB) con compatibilidad relacional estándar para PostgreSQL.
- **Tablas:** 16 tablas relacionales formalizadas.
- **Datos Territoriales:** 17 divisiones políticas oficiales (15 departamentos y 2 regiones autónomas) y 153 municipios según la **Ley N.° 59 de Nicaragua** e **INETER**.

---

## 3. INVENTARIO DE RUTAS, ENDPOINTS Y COMPONENTES

### 3.1. Rutas Frontend (10 rutas en App Router)
| Ruta | Tipo | Propósito | Estado de Implementación |
| :--- | :---: | :--- | :---: |
| `/` | Estática (SSG) | Landing page, buscador rápido, casos recientes, enlaces de emergencia | ✅ Completo |
| `/casos` | Estática (SSG) | Directorio público de casos aprobados con filtros multifactor | ✅ Completo |
| `/casos/[id]` | Dinámica (SSR) | Expediente público del caso y formulario seguro de pistas | ✅ Completo |
| `/mapa` | Estática (SSG) | Mapa interactivo GIS con datos geofiltados y panel territorial admin | ✅ Completo |
| `/pistas` | Estática (SSG) | Consulta anónima de trazabilidad de pistas mediante código | ✅ Completo |
| `/reportar` | Estática (SSG) | Formulario multipaso para registro de reporte y consentimiento Ley 787 | ⚠️ Falta feedback en subida de foto |
| `/login` | Estática (SSG) | Acceso y registro con validación RBAC | ⚠️ Falta recuperación de contraseña |
| `/admin` | Estática (SSG) | Centro de control, moderación humana, triaje de pistas y auditoría | ✅ Completo |
| `/_not-found` | Estática (SSG) | Manejador de error 404 | ✅ Completo |
| `/layout.tsx` | Global | Encabezado institucional, barra de navegación y pie de página | ✅ Completo |

### 3.2. Endpoints Backend (31 endpoints en FastAPI)
- **Autenticación (`/api/v1/auth`):**
  - `POST /login` (Rate limit 5/min, log de auditoría, JWT Argon2)
  - `POST /register` (Validación de robustez de contraseña, rol seguro por defecto)
  - `GET /me` (Consulta de perfil activo)
  - `POST /logout` (Cierre formal de sesión)
- **Reportes (`/api/v1/reports`):**
  - `GET /` (Listado público de casos aprobados/publicados con filtros)
  - `GET /my-reports` (Reportes del usuario autenticado)
  - `GET /{id_or_case}` (Detalle público con control de acceso estricto a borradores)
  - `POST /` (Creación de reporte en estado `pending_review`, hash de consentimiento Ley 787)
  - `PUT /{report_id}` (Edición controlada con reglas de estado y RBAC)
  - `POST /{report_id}/photos` (Subida de foto con remoción forzada de EXIF)
  - `GET /photos/{storage_key}` (Descarga de imagen WebP sanitizada)
  - `POST /{report_id}/request-close` (Solicitud de cierre y despublicación inmediata)
- **Búsqueda (`/api/v1/search`):**
  - `GET /` (Búsqueda multifiltro tolerante)
  - `GET /semantic` (Búsqueda asistida por rasgos físicos y señas particulares)
- **División Territorial (`/api/v1/locations`):**
  - `GET /departments` (Catálogo de 17 departamentos/regiones)
  - `GET /departments/{id}` (Detalle de departamento)
  - `POST /departments` (Creación administrativa RBAC)
  - `PATCH /departments/{id}` (Actualización/activación RBAC)
  - `GET /municipalities` (Catálogo de 153 municipios con filtro dependiente)
  - `GET /municipalities/{id}` (Detalle de municipio)
  - `POST /municipalities` (Creación administrativa RBAC)
  - `PATCH /municipalities/{id}` (Actualización/activación RBAC)
  - `GET /summary` (Consolidado territorial cuantitativo)
  - `GET /map-aggregated` (Puntos agregados aproximados para el mapa)
- **Pistas Ciudadanas (`/api/v1/tips`):**
  - `POST /` (Recepción anónima de pistas confidenciales con código aleatorio)
  - `GET /track/{tip_code}` (Consulta anónima de estado sin divulgar datos sensibles)
- **Administración & Moderación (`/api/v1/admin`):**
  - `GET /metrics` (Métricas del sistema)
  - `GET /reports/pending` (Cola de moderación de reportes pendientes)
  - `POST /reports/{report_id}/moderate` (Aprobación, rechazo o solicitud de cambios)
  - `GET /tips` (Triaje y revisión de pistas para moderadores)
  - `PATCH /tips/{tip_id}/status` (Actualización de estado de investigación de pista)
  - `GET /audit-logs` (Consulta de registros inmutables de auditoría)
- **Asistencia IA Supervisada (`/api/v1/ai`):**
  - `POST /check-duplicates/{report_id}` (Detección de posibles casos duplicados)
  - `GET /summary/{report_id}` (Resumen sintético y completitud para el moderador)
- **Notificaciones (`/api/v1/notifications`):**
  - `GET /unsubscribe/{token}` (Cancelación voluntaria de alertas)
- **Estadísticas (`/api/v1/statistics`):**
  - `GET /by-department` (Conteo público de casos por departamento)
  - `GET /summary-public` (Métricas globales públicas)

---

## 4. ESTADO DE LOS ERRORES PREVIOS REPORTADOS

### 4.1. Error 1: `TypeError: Failed to fetch` en `src/lib/api.ts`
- **Causa original:** Incompatibilidad de origen (CORS) y ausencia de URL base unificada para llamadas en navegador y llamadas de servidor.
- **Estado verificado:** ✅ **CORREGIDO TOTALMENTE**.
  - `getApiBase()` resuelve dinámicamente `/api/v1` en navegador aprovechando el proxy rewrite de Next.js (`next.config.js`), eliminando bloqueos CORS.
  - Implementación de deduplicación de consultas GET concurrentes y reintentos automáticos ante cortes transitorios.

### 4.2. Error 2: `ApiError: Error en el servidor: Error HTTP 500` en `executeFetch`
- **Causa original:** 
  1. Desreferenciación nula en `backend/app/api/v1/locations.py` al acceder a `r.location.department` en reportes con ubicación vacía.
  2. Ausencia de `db.rollback()` en `backend/app/core/database.py`, que dejaba conexiones en estado `InFailedSqlTransaction` tras cualquier fallo previo.
  3. Ausencia de manejador global de excepciones en `backend/app/main.py`.
- **Estado verificado:** ✅ **CORREGIDO EN SU ORIGEN**.
  - Coalescencia defensiva en `locations.py` (`r.location.department if r.location else "Desconocido"`).
  - Manejo preventivo de `db.rollback()` en generador `get_db()`.
  - Manejadores globales para `SQLAlchemyError` y `Exception` devolviendo respuestas estructuradas en JSON.
  - Verificado con 33 pruebas automatizadas pasando con éxito.

---

## 5. RESUMEN DE HALLAZGOS Y CALIFICACIÓN GLOBAL

| Dimensión Auditada | Calificación (1-10) | Estado | Hallazgos Críticos |
| :--- | :---: | :---: | :--- |
| **Arquitectura de Software** | 9.0 / 10 | Muy Bueno | Separación limpia de capas, ORM robusto, App Router moderno |
| **Validaciones Frontend/Backend** | 7.5 / 10 | Regular | Backend muy estricto; Frontend carece de validaciones previas al envío |
| **Ciberseguridad & OWASP** | 7.0 / 10 | Atención | Vulnerabilidad potencial de Path Traversal en fotos, fuga en mensaje de error 500 |
| **Base de Datos & Integridad** | 8.8 / 10 | Bueno | Modelos normalizados, relaciones bien definidas, tablas huérfanas en endpoints |
| **Módulo GIS y Catálogo Territorial** | 9.8 / 10 | Excelente | 17 divisiones y 153 municipios oficiales, geofencing estricto, geocodificación difusa |
| **Accesibilidad & UI/UX** | 8.0 / 10 | Bueno | Diseño responsivo y contrastado; faltan atributos `htmlFor` y optimización `next/image` |
| **Cobertura de Pruebas Automatizadas**| 7.2 / 10 | Aceptable | Backend con 33 pruebas pasando; Frontend sin suites de test unitario o E2E |

**Índice Global de Calidad (Software Quality Index):** **8.18 / 10**  
*El sistema cuenta con una arquitectura de alta calidad, pero requiere la atención inmediata de 2 vulnerabilidades de seguridad y la completación de 3 flujos funcionales antes de su puesta en producción.*
