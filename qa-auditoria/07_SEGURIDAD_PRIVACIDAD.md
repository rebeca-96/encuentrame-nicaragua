# 07 — AUDITORÍA DE SEGURIDAD, OWASP Y PRIVACIDAD (LEY N.° 787)
## Proyecto: ENCUÉNTRAME NICARAGUA
### Evaluación contra OWASP Top 10 y Marco Legal de Protección de Datos Personales
**Auditor:** Senior QA Engineer & SDET  
**Fecha:** 19 de Noviembre de 2026  

---

## 1. EVALUACIÓN OWASP TOP 10 (2021 / ASVS v4.0)

### A01:2021 — Broken Access Control (Control de Acceso Roto)
- **Evaluación:** **CONFORME / ALTA SEGURIDAD**
- **Pruebas Ejecutadas:**
  - Se intentó acceder a la cola de moderación (`GET /api/v1/admin/reports/pending`) con usuarios anónimos, rol `citizen` y rol `reporter`.
  - En todos los casos el sistema rechazó la solicitud con `HTTP 401 Unauthorized` o `HTTP 403 Forbidden`.
  - Se verificó que un reporter no puede modificar ni aprobar sus propios reportes (prevención de BOLA / IDOR).

### A02:2021 — Cryptographic Failures (Fallos Criptográficos)
- **Evaluación:** **CONFORME**
- **Pruebas Ejecutadas:**
  - Contraseñas almacenadas exclusivamente mediante `bcrypt` con factor de coste estándar.
  - Firma de tokens JWT mediante `HS256` utilizando clave secreta criptográfica configurable desde variables de entorno.
  - Mecanismo de revocación inmediata de token en `POST /api/v1/auth/logout`: el token revocado es rechazado en peticiones subsiguientes (`HTTP 401: Token inválido o expirado`).

### A03:2021 — Injection (Inyecciones SQL / NoSQL / OS / Path Traversal)
- **Evaluación:** **CONFORME**
- **Pruebas Ejecutadas:**
  - Payloads de SQL Injection (`' OR '1'='1`, `'; DROP TABLE users; --`) inyectados en filtros de búsqueda, nombres y campos de texto: absorbidos de forma segura como texto plano por los parámetros vinculados de SQLAlchemy ORM.
  - Payloads de Path Traversal (`../../etc/passwd`, `..\\..\\windows\\win.ini`) en endpoints de fotos: bloqueados en `storage_service.py` (`HTTP 400 Bad Request: Nombre de archivo no permitido`).

### A04:2021 — Insecure Design (Diseño Inseguro)
- **Evaluación:** **CONFORME**
- **Hallazgo:**
  - La plataforma implementa un flujo de diseño ético y seguro: ningún reporte creado por un ciudadano se publica de forma inmediata.
  - Todo reporte recién registrado ingresa en estado `pending_review` y permanece invisible al público y a los motores de búsqueda hasta que un moderador o administrador humano revisa la veracidad del caso y el documento de consentimiento.

### A05:2021 — Security Misconfiguration (Mala Configuración de Seguridad)
- **Evaluación:** **HALLAZGO (DEF-01 / DEF-02)**
- **Hallazgo:**
  - En el entorno de hosting público (`https://creacionvaloria.tradescanner.online`), el servidor web sirve los archivos estáticos pero no está enrutando las peticiones bajo `/api/v1` hacia el puerto de FastAPI, devolviendo `HTTP 404`.
  - CORS está configurado con orígenes explícitos en `backend/app/main.py`.

### A07:2021 — Identification and Authentication Failures (Fallos de Identificación y Autenticación)
- **Evaluación:** **CONFORME**
- **Pruebas Ejecutadas:**
  - Se ejecutaron ráfagas de 7 intentos de login con contraseñas inválidas.
  - Al 6.° intento el backend activó el limitador de tasa respondiendo `HTTP 429 Too Many Requests: Límite de solicitudes excedido. Por favor intente de nuevo en 60 segundos`.

### A09:2021 — Security Logging and Monitoring Failures (Fallos de Registro y Monitoreo)
- **Evaluación:** **CONFORME**
- **Pruebas Ejecutadas:**
  - La tabla `audit_logs` registra de manera inmutable: inicio de sesión, creación de casos, aprobación/rechazo de moderación, solicitudes de baja y fecha/hora exacta con IP y User-Agent.

---

## 2. CUMPLIMIENTO DE LA LEY N.° 787 DE NICARAGUA (PROTECCIÓN DE DATOS PERSONALES)

La **Ley N.° 787** de la República de Nicaragua establece principios estrictos sobre licitud, lealtad, finalidad, proporcionalidad y confidencialidad de los datos personales.

| Artículo / Principio | Mecanismo de la Plataforma | Estado | Veredicto |
| :--- | :--- | :--- | :--- |
| **Principio de Consentimiento (Art. 5)** | Formulario exige aceptación obligatoria de declaración jurada y consentimiento informado (`consent.accepted_terms=True`). | El backend rechaza cualquier registro con `accepted_terms=False` (`HTTP 422`). | **CUMPLE** |
| **Confidencialidad del Reportante (Art. 6)** | Los datos de contacto del familiar/reportante (nombre, teléfono, cédula) no se exponen en las respuestas de la API pública (`ReportPublicResponse`). | Verificado en `GET /api/v1/reports/{id}`: omite campos privados del denunciante. | **CUMPLE** |
| **Derechos ARCO: Cancelación / Supresión (Art. 13)** | Endpoint `POST /api/v1/reports/{id}/request-deletion` permite al titular o familiar solicitar el cierre o baja del expediente. | Verificado en prueba `TC-LEY787-01`: genera solicitud formal y cambia el estado. | **CUMPLE** |
| **Protección contra Geolocalización Privada** | El mapa público (`/locations/map-aggregated`) utiliza coordenadas aproximadas a nivel de municipio y no la dirección exacta de la vivienda. | Verificado: coordenadas exactas no son transmitidas a clientes anónimos. | **CUMPLE** |
| **Purga de Metadatos EXIF en Fotografías (DEF-07)** | Al recibir una foto de una persona desaparecida, la imagen puede contener coordenadas GPS de la cámara del informante. | **DEF-07**: El procesador de imágenes debe limpiar explícitamente los metadatos EXIF al guardar para evitar fuga indirecta de ubicación del fotógrafo. | **HALLAZGO (P2)** |
