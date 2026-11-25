# AUDITORÍA TÉCNICA Y DIAGNÓSTICO INTEGRAL
## Proyecto: ENCUÉNTRAME NICARAGUA
### Plataforma Inteligente de Búsqueda y Reunificación Familiar

**Fecha de Auditoría:** 18 de Noviembre de 2026  
**Equipo Auditor:** QA Senior, Arquitecto de Software, Especialista en Ciberseguridad OWASP, DBA y Especialista UI/UX.  
**Estado:** Diagnóstico Inicial y Plan de Corrección Completado (Fase Pre-Autorización).

---

## 1. ARQUITECTURA REAL Y STACK TECNOLÓGICO IDENTIFICADO

A través de la inspección del código fuente y entorno de ejecución, se constata la siguiente arquitectura real:

| Componente | Tecnología Identificada | Versión | Estado Operativo |
| :--- | :--- | :--- | :--- |
| **Entorno de Ejecución** | Node.js / Python | Node v24.19.0 / Python 3.12.10 | Operativo |
| **Frontend Framework** | Next.js (App Router) | 14.2.35 | Operativo (Compila en producción) |
| **Librería UI** | React / React DOM | 18.2.0 | Operativo |
| **Estilos & Iconos** | Tailwind CSS / Lucide React | Tailwind 3.4.1 / Lucide 0.359.0 | Operativo |
| **Mapas Geoespaciales** | Leaflet / OpenStreetMap | Leaflet 1.9.4 | Operativo con carga dinámica SSR |
| **Backend Framework** | FastAPI (Python) | 0.165.0 | Operativo |
| **Servidor ASGI** | Uvicorn | 0.54.0 | Operativo |
| **Validación de Datos** | Pydantic / Pydantic Settings | 2.14.3 / 2.16.3 | Operativo |
| **ORM & Persistencia** | SQLAlchemy / Alembic | 2.1.9 / 1.20.1 | Operativo |
| **Motor de Base de Datos** | SQLite (desarrollo local) / PostGIS (Docker) | SQLite 3 / PostgreSQL 16 PostGIS 3.4 | Operativo |
| **Criptografía de Claves** | Argon2id (argon2-cffi / passlib) | 25.1.0 | Operativo |
| **Tokens & Sesiones** | Python-Jose (JWT HS256) | 3.5.0 | Operativo |
| **Procesamiento de Fotos** | Pillow (PIL) | 13.0.0 | Operativo (con vulnerabilidad de excepción) |

---

## 2. DIAGNÓSTICO GENERAL POR DIMENSIONES

### 2.1 Frontend
- **Compilación de producción:** Exitosa (`npm run build` genera las 10 rutas sin errores de tipado).
- **Rutas implementadas:** `/`, `/casos`, `/casos/[id]`, `/mapa`, `/reportar`, `/pistas`, `/admin`, `/login`.
- **Hallazgos:**
  1. **Ausencia de Interfaz de Registro (`/register`):** La página de login (`/login`) no cuenta con formulario ni enlace para que un ciudadano o reportante nuevo se registre, obligando a usar la API directamente.
  2. **URLs Absolutas Hardcodeadas (`http://127.0.0.1:8000`):** En `ReportCard.tsx`, `casos/[id]/page.tsx` y `reportar/page.tsx` existen llamadas y rutas de imagen que apuntan a `http://127.0.0.1:8000` en lugar de utilizar variables de entorno (`NEXT_PUBLIC_API_URL`) o rutas relativas, lo cual fallará en producción o despliegues en red.
  3. **Ausencia de Configuración ESLint:** El script `npm run lint` se detiene solicitando configuración interactiva por falta de `.eslintrc.json`.

### 2.2 Backend & API REST
- **Endpoints funcionales y testeados:** 10/10 pruebas unitarias pasan exitosamente en 2.07 segundos.
- **Hallazgos:**
  1. **Falta de Rate Limiting (Límites de Solicitud):** Los endpoints sensibles como `POST /api/v1/auth/login` y `POST /api/v1/tips/` carecen de limitadores de peticiones por IP o sesión, dejándolos vulnerables a ataques de fuerza bruta y denegación de servicio / spam de pistas falsas.
  2. **Excepción No Controlada en Subida de Archivos:** En `POST /api/v1/reports/{id}/photos`, si se envía un archivo no gráfico o corrupto, Pillow lanza `UnidentifiedImageError` no capturado, generando un HTTP 500 (Internal Server Error) en lugar de un HTTP 400 limpio.
  3. **Falta de Endpoint de Actualización (`PUT /api/v1/reports/{id}`):** Requerido para corregir borradores o actualizar datos por el autor o moderador.
  4. **Falta de Router de Notificaciones y Cancelación de Suscripción:** La entidad `NotificationSubscription` posee `token_unsubscribe`, pero no existe el endpoint público `/api/v1/notifications/unsubscribe/{token}`.
  5. **CORS Permisivo:** `allow_origins=["*"]` en `main.py` debe restringirse a orígenes autorizados para entornos de producción.

### 2.3 Validaciones de Formularios
- **Fechas Futuras:** `ReportCreate` no valida que la fecha de desaparición sea igual o anterior a la fecha actual. Se comprobó empíricamente que una fecha en el año 2099 fue admitida.
- **Inconsistencia Geográfica:** El modelo no valida que el municipio enviado pertenezca efectivamente al departamento seleccionado (ej. Departamento Managua con Municipio Sébaco fue admitido con HTTP 201).
- **Contraseñas Débiles:** En `UserRegister`, solo se valida `min_length=8`, permitiendo contraseñas sin requerimientos de complejidad (mayúsculas, números, caracteres especiales).
- **Fechas en Pistas:** `TipCreate` no valida que `sighting_date` sea coherente (no futura y posterior a la fecha de desaparición del caso).

### 2.4 Base de Datos y Modelo de Datos
- **Integridad Referencial:** 14 entidades mapeadas correctamente con SQLAlchemy 2.0.
- **Cascadas de Eliminación:** Definidas correctamente en reportes para fotos, consentimientos, historial y pistas.
- **Índices Faltantes:** Claves foráneas como `location_id` y `reporter_id` en `missing_person_reports` carecen de `index=True`, lo que puede degradar consultas de agregación en bases de datos PostgreSQL con miles de registros.

### 2.5 Seguridad OWASP Top 10
- **A01:2021 (Broken Access Control):** Buen aislamiento de pistas confidenciales (protegidas por token de moderador/admin). No obstante, la ausencia de rate limiting facilita la enumeración de identificadores.
- **A02:2021 (Cryptographic Failures):** Contraseñas hasheadas robustamente con Argon2id. Sin embargo, en `config.py` la clave `SECRET_KEY` tiene un valor por defecto que debe forzarse como obligatorio en producción.
- **A04:2021 (Insecure Design):** Admisión de fechas futuras y archivos no verificados a nivel de bytes (magic numbers).
- **A07:2021 (Identification and Authentication Failures):** Sin protección contra ataques de diccionario en `/login`.
