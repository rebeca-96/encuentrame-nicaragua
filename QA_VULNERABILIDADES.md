# INFORME DE AUDITORÍA DE CIBERSEGURIDAD Y EVALUACIÓN OWASP
## PROYECTO: ENCUÉNTRAME NICARAGUA
### Evaluación contra OWASP Top 10 (2021), OWASP ASVS y Ley N.° 787 de Nicaragua

**Fecha de Evaluación:** 18 de Noviembre de 2026  
**Especialista:** Senior Cybersecurity Engineer & Application Security (AppSec)  
**Alcance:** Código backend FastAPI, componentes frontend Next.js, esquemas de base de datos, políticas de almacenamiento y manejo de tokens.

---

## 1. RESUMEN EJECUTIVO DE VULNERABILIDADES Y RIESGOS

| Identificador | Clasificación OWASP | Vulnerabilidad Detectada | Severidad | Impacto Potencial | Corrección Requerida |
| :--- | :--- | :--- | :---: | :--- | :--- |
| **VULN-01** | CWE-22 / OWASP A01 | **Ruta no saneada / Path Traversal en descarga de imágenes** | **P0 (Crítico)** | Lectura no autorizada de archivos fuera de `storage/uploads` | Forzar regex estricto `^[a-f0-9]{32}\.webp$` o validar `commonpath` |
| **VULN-02** | OWASP A05:2021 | **Fuga de información técnica en el manejador global de error 500** | **P0 (Crítico)** | Revelación de nombres de esquemas, librerías o trazas al cliente HTTP | Enmascarar mensaje hacia el cliente; logging detallado solo en servidor |
| **VULN-03** | OWASP A07:2021 | **Ausencia de Rate Limiting en endpoint de registro (`/auth/register`)** | **P1 (Alto)** | Ataques de denegación de servicio por agotamiento de almacenamiento | Aplicar limitador en memoria (máx. 3 cuentas / 10 min por IP) |
| **VULN-04** | OWASP A07:2021 | **Falta de invalidación/revocación de JWT en logout** | **P1 (Alto)** | Tokens robados utilizables hasta el vencimiento (24 horas) | Implementar lista negra de tokens revocados o reducir expiración a 60 min |
| **VULN-05** | OWASP A02:2021 | **Uso permisivo de `SECRET_KEY` de desarrollo en producción** | **P1 (Alto)** | Falsificación potencial de tokens si no se reemplaza en producción | Bloquear arranque de la aplicación si `ENVIRONMENT=production` y `SECRET_KEY` es la default |

---

## 2. ANÁLISIS DETALLADO POR CATEGORÍA OWASP TOP 10 (2021)

### A01:2021 — Broken Access Control (Control de Acceso Roto)
- **Evaluación de IDOR / BOLA:**
  - En `PUT /api/v1/reports/{report_id}` ([reports.py:307](file:///c:/Users/User/Documents/Valor%20IA/EncuentrameNicaragua/backend/app/api/v1/reports.py#L307-L325)), se verifica rigurosamente que el usuario sea el propietario (`reporter_id == current_user.id`) o cuente con rol `moderator`/`admin`. Si el caso ya fue publicado o está cerrado, los usuarios comunes no pueden modificarlo. ✅ **PROTEGIDO CONTRA IDOR**.
  - En `GET /api/v1/reports/{id_or_case}` ([reports.py:139](file:///c:/Users/User/Documents/Valor%20IA/EncuentrameNicaragua/backend/app/api/v1/reports.py#L139-L151)), los casos no publicados (`is_public=False`) solo pueden ser leídos por su autor o moderadores; usuarios anónimos o ajenos reciben HTTP 403. ✅ **PROTEGIDO**.
  - En `/api/v1/admin/tips`, el acceso está protegido con `require_moderator`. Las pistas de ciudadanos son inaccesibles para el público general. ✅ **PROTEGIDO**.
- **Vulnerabilidad CWE-22 (Path Traversal en fotos):**
  - **Ubicación:** `backend/app/api/v1/reports.py:412` y `backend/app/services/storage_service.py:84`.
  - **Análisis:** `get_photo_file(storage_key: str)` concatena directamente `os.path.join(settings.STORAGE_DIR, storage_key)` sin verificar si `storage_key` contiene secuencias `..` o separadores de directorio.
  - **Remediación Inmediata:**  
    ```python
    import re
    if not re.match(r"^[a-f0-9]{32}\.webp$", storage_key):
        raise HTTPException(status_code=400, detail="Identificador de archivo inválido.")
    ```

### A02:2021 — Cryptographic Failures (Fallos Criptográficos)
- **Almacenamiento de Contraseñas:** Se utiliza `CryptContext` con **Argon2id** (algoritmo ganador del Password Hashing Competition) con fallback a Bcrypt. No se almacenan contraseñas en texto plano. ✅ **EXCELENTE**.
- **Gestión de Cédulas y Consentimiento (Ley N.° 787):** El número de cédula del reportante se procesa con hashing criptográfico irreversibilidad SHA-256 (`identity_doc_hash`), garantizando que la base de datos no retenga números de cédula legibles en caso de volcado no autorizado. ✅ **CONFORME A LEY 787**.
- **Firma de Tokens JWT:** Algoritmo HMAC-SHA256 (`HS256`). Se requiere forzar una clave de al menos 256 bits generada con alta entropía en entornos de producción.

### A03:2021 — Injection (Inyecciones SQL / NoSQL / Command)
- **Consultas a Base de Datos:** Todas las consultas se construyen mediante el ORM SQLAlchemy con parámetros enlazados (`Parameterized Queries`). No existen consultas concatenadas con `f-strings` directas en el código de producción. ✅ **PROTEGIDO CONTRA SQLi**.
- **XSS (Cross-Site Scripting):** React y Next.js escapan automáticamente todas las cadenas de texto antes de renderizarlas en el DOM. No se detectó uso de `dangerouslySetInnerHTML`. Cabeceras de seguridad activas en FastAPI (`X-Content-Type-Options: nosniff`, `X-Frame-Options: DENY`). ✅ **PROTEGIDO CONTRA XSS**.

### A04:2021 — Insecure Design (Diseño Inseguro)
- **Privacidad por Diseño (Privacy by Design):**
  - Las coordenadas geográficas exactas de desaparición **NUNCA** se almacenan ni se devuelven al cliente. Se calculan coordenadas referenciales aproximadas mediante `get_approximate_coords` (centroides municipales con ruido deliberado).
  - Toda fotografía subida al sistema pasa por `sanitize_and_save_image()`, que destruye absolutamente todos los metadatos EXIF (coordenadas GPS del celular donde se tomó la foto, modelo de cámara, hora exacta).
  - Los casos de menores de edad (`is_minor = True`) activan banderas especiales de protección que prohíben la divulgación de direcciones domiciliarias o colegios.

### A05:2021 — Security Misconfiguration (Configuración Errónea de Seguridad)
- **Fuga de Información en Manejador 500:**
  - **Ubicación:** `backend/app/main.py:59`.
  - **Problema:** En el manejador `@app.exception_handler(Exception)`, se devuelve `detail: f"Error interno en el servidor: {str(exc)}"`. En caso de un error de infraestructura, SQLAlchemy o disco, el cliente HTTP recibe el traceback o mensaje de excepción interno.
  - **Remediación:** Devolver `"detail": "Ha ocurrido un error interno en el servidor. El incidente ha sido registrado para investigación."` y dejar `{str(exc)}` únicamente en `logger.error()`.
- **CORS:** Restringido a orígenes explícitos (`http://localhost:3000`, `http://127.0.0.1:3000`). No utiliza comodines `*` con credenciales habilitadas. ✅ **CONFORME**.

### A06:2021 — Vulnerable and Outdated Components
- Todas las librerías instaladas en el entorno virtual corresponden a versiones seguras y actualizadas (FastAPI 0.165, SQLAlchemy 2.1, Pydantic 2.14, Next.js 14.2.35, Pillow 13.0). No existen componentes obsoletos conocidos con vulnerabilidades críticas reportadas en CVEs activos.

### A07:2021 — Identification and Authentication Failures
- **Fuerza Bruta en Login:** Protegido con `rate_limit_login` (máximo 5 intentos por minuto por IP). Al exceder, responde HTTP 429 con cabecera `Retry-After`. ✅ **PROTEGIDO**.
- **Fuerza Bruta en Registro:** **Falta limitador**. Debe agregarse `rate_limit_register` en `POST /auth/register`. ⚠️ **HALLAZGO P1**.
- **Enumeración de Usuarios:** El endpoint `/auth/login` devuelve un mensaje unificado genérico: `"Credenciales incorrectas o usuario no registrado"`, impidiendo averiguar si un correo existe en la base de datos. ✅ **PROTEGIDO**.

### A08:2021 — Software and Data Integrity Failures
- Las imágenes subidas son validadas con firmas mágicas binarias (JPEG `FF D8 FF`, PNG `89 50 4E 47`, WebP `52 49 46 46`) antes de procesarlas con Pillow. Se rechazan scripts camuflados o binarios maliciosos renombrados como `.jpg`.

### A09:2021 — Security Logging and Monitoring Failures
- Toda acción crítica (creación de caso, actualización, moderación, aprobación, recepción de pista, cambio de estado, inicio de sesión) se registra de forma inmutable en la tabla `audit_logs` con `user_id`, `ip_address`, `user_agent`, `action` y timestamp UTC. Los logs de auditoría son consultables exclusivamente por el Administrador General (`require_admin`). ✅ **EXCELENTE**.

---

## 3. SALVAGUARDAS DE PROTECCIÓN DE DATOS DE PERSONAS VULNERABLES

1. **Datos de Menores de Edad:** Identificados con `is_minor=True`. Las alertas se restringen estrictamente a datos fisonómicos y de vestimenta necesarios para su localización, sin divulgar información familiar privada.
2. **Pistas Confidenciales:** Poseen un identificador aleatorio de 64 bits (`generate_tip_code()`, ej. `PISTA-9A4K-2B7Z`) generado mediante el generador criptográficamente seguro de Python (`secrets.token_hex`). No se pueden deducir ni enumerar pistas de otros usuarios.
3. **Despublicación Inmediata al Cierre:** En cuanto un caso es cerrado o la persona es localizada (`request_close_case`), el campo `is_public` pasa automáticamente a `False`, retirando la información del buscador y del mapa en milisegundos para preservar la dignidad y privacidad de la persona localizada.
