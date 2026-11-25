# PLAN DE CORRECCIONES Y MITIGACIÓN CONTROLADA
## Proyecto: ENCUÉNTRAME NICARAGUA

Este plan establece la secuencia ordenada de intervenciones técnicas para resolver los hallazgos de la auditoría.  
**REGLA DE ORO:** No se aplicará ninguna modificación hasta recibir la autorización expresa del usuario.

---

## 1. PRINCIPIOS DE INTERVENCIÓN
1. **Prioridad por Riesgo:** Resolver primero los hallazgos clasificados como **CRÍTICO** y **ALTO**.
2. **Defensa en Profundidad:** Las validaciones críticas se implementan en el Backend (FastAPI / Pydantic) y se replican en el Frontend (React Hook Form / Zod / HTML5).
3. **Cero Regresiones:** Cada corrección estará respaldada por una prueba automatizada específica en Pytest.
4. **Estrategia de Reversión (Rollback):** Respaldos y control de versiones por commit atómico por cada módulo intervenido.

---

## 2. ETAPAS DE IMPLEMENTACIÓN

### ETAPA 1: SEGURIDAD Y CONTROL DE TASA (CRÍTICO)
- **Objetivo:** Proteger `/api/v1/auth/login` contra ataques de fuerza bruta y `/api/v1/tips/` contra ataques de spam.
- **Acciones:**
  1. Implementar un middleware / dependency de limitación de tasa configurable en memoria / Redis (`RateLimiter`).
  2. Aplicar límite de 5 intentos por minuto en `/auth/login` y 10 envíos por hora en `/tips/`.
  3. Retornar cabeceras estándar `Retry-After` y código `HTTP 429 Too Many Requests`.
- **Archivos a Modificar:**
  - `backend/app/core/rate_limit.py` (Nuevo)
  - `backend/app/api/v1/auth.py`
  - `backend/app/api/v1/tips.py`
  - `backend/app/main.py`
- **Prueba Asociada:** `test_rate_limiting_login_and_tips` en `backend/tests/test_audit_fixes.py`.

---

### ETAPA 2: VALIDACIONES ROBUSTAS DE ARCHIVOS Y METADATOS (ALTO)
- **Objetivo:** Prevenir errores HTTP 500 y denegación de servicio por subida de archivos binarios corruptos o no autorizados.
- **Acciones:**
  1. Validar `Content-Type` de la imagen contra la lista permitida (`image/jpeg`, `image/png`, `image/webp`).
  2. Validar los primeros bytes (magic numbers) del archivo.
  3. Envolver `Image.open` en `storage_service.py` con manejo explícito de `UnidentifiedImageError`, retornando una excepción HTTP 400 limpia con mensaje comprensible: *"El archivo proporcionado no es una imagen válida o está dañado"*.
- **Archivos a Modificar:**
  - `backend/app/services/storage_service.py`
  - `backend/app/api/v1/reports.py`
- **Prueba Asociada:** `test_upload_invalid_image_returns_400` en `backend/tests/test_audit_fixes.py`.

---

### ETAPA 3: INTEGRIDAD TEMPORAL Y GEOGRÁFICA EN REPORTES (ALTO)
- **Objetivo:** Prohibir reportes con fechas futuras o combinaciones geográficas inexistentes en Nicaragua.
- **Acciones:**
  1. En `ReportCreate`, añadir `@field_validator("disappearance_date")` asegurando que la fecha sea `<= datetime.now(timezone.utc)`.
  2. Añadir validador de correspondencia departamento-municipio: comprobar que `municipality in get_municipalities(department)`.
  3. En `TipCreate`, validar que `sighting_date <= datetime.now(timezone.utc)`.
  4. Validar que no se puedan enviar pistas a reportes en estado `CLOSED_FOUND` o `CLOSED_RESOLVED`.
- **Archivos a Modificar:**
  - `backend/app/schemas/schemas.py`
  - `backend/app/api/v1/reports.py`
  - `backend/app/api/v1/tips.py`
- **Prueba Asociada:** `test_future_date_rejected` y `test_inconsistent_municipality_rejected`.

---

### ETAPA 4: INTERFAZ DE REGISTRO DE USUARIOS Y ENDPOINTS FALTANTES (ALTO)
- **Objetivo:** Permitir que los familiares se registren desde el frontend e implementar `PUT /reports/{id}`.
- **Acciones:**
  1. En `frontend/src/app/login/page.tsx`, agregar pestaña o interruptor para alternar entre "Iniciar Sesión" y "Registrarse como Reportante", con validación de contraseña robusta.
  2. En `backend/app/api/v1/reports.py`, implementar `PUT /api/v1/reports/{id}` permitiendo modificar datos a su autor (si está en borrador o revisión) o al moderador.
  3. En `backend/app/schemas/schemas.py`, robustecer `UserRegister` con validador de complejidad de clave.
  4. Corregir URLs absolutas hardcodeadas en componentes frontend sustituyéndolas por rutas relativas o basadas en `NEXT_PUBLIC_API_URL`.
- **Archivos a Modificar:**
  - `frontend/src/app/login/page.tsx`
  - `frontend/src/components/reports/ReportCard.tsx`
  - `frontend/src/app/casos/[id]/page.tsx`
  - `frontend/src/app/reportar/page.tsx`
  - `backend/app/api/v1/reports.py`
  - `backend/app/schemas/schemas.py`

---

### ETAPA 5: AJUSTES DE CALIDAD, LINTING Y DESUSCRIPCIÓN (MEDIO/BAJO)
- **Objetivo:** Completar tooling de CI/CD y módulos auxiliares.
- **Acciones:**
  1. Crear `frontend/.eslintrc.json` con `extends: ["next/core-web-vitals"]`.
  2. Implementar `backend/app/api/v1/notifications.py` con endpoint `/unsubscribe/{token}`.
  3. Crear `backend/pytest.ini` para silenciar advertencias de `pytest-asyncio`.
- **Archivos a Modificar:**
  - `frontend/.eslintrc.json`
  - `backend/app/api/v1/notifications.py`
  - `backend/app/main.py`
  - `backend/pytest.ini`

---

## 3. PLAN DE REVERSIÓN (ROLLBACK)
- En caso de presentarse una regresión durante la aplicación de cualquiera de las etapas, los archivos modificados pueden ser revertidos inmediatamente mediante git o restauración de respaldo, manteniendo intacto el estado funcional actual verificado.
