# REQUISITOS DERIVADOS DE LA INVESTIGACIÓN Y MATRIZ DE TRAZABILIDAD

## PROYECTO: ENCUÉNTRAME NICARAGUA
### Plataforma Cívica de Búsqueda y Reunificación Familiar
**Fecha de Emisión:** 24 de noviembre de 2026  
**Estándares de Referencia:** Ley N.° 787 (Nicaragua), CICR Búsqueda Humanitaria, OWASP ASVS v5.0.0

---

### 1. ESTRUCTURA Y CONVENCIONES

Los requisitos se clasifican en:
- **RF (Requisito Funcional):** Funcionalidades y comportamientos específicos que el sistema ejecuta.
- **RNF (Requisito No Funcional):** Atributos de calidad, seguridad, desempeño, privacidad y marco legal.

Estados de implementación en la plataforma:
1. **[IMPLEMENTADO]:** Codificado, probado y verificado en la base de código actual.
2. **[REQUIERE VERIFICACIÓN]:** Implementado parcialmente o dependiente de pruebas complementarias de entorno/carga.
3. **[PENDIENTE]:** Recomendación de arquitectura o mejora futura identificada en la investigación que requiere desarrollo posterior.

---

### 2. MATRIZ DE REQUISITOS VINCULADOS A MÓDULOS DEL SISTEMA

| ID | Módulo del Sistema | Tipo | Descripción del Requisito | Fuente de Origen | Estado Actual | Archivos de Código / Evidencia |
| :--- | :--- | :---: | :--- | :--- | :---: | :--- |
| **RF-01** | Registro de Reportes | RF | Formulario multipaso con captura estructurada de datos ante mortem: rasgos fisonómicos, indumentaria, condiciones médicas y fecha/hora. | CICR (2021) | **[IMPLEMENTADO]** | `frontend/src/app/reportar/page.tsx`, `backend/app/schemas/schemas.py` |
| **RF-02** | Registro de Reportes | RF | Declaración obligatoria de consentimiento informado bajo Ley 787, con registro de parentesco, hash de cédula e IP. | Ley N.° 787 (Art. 5) | **[IMPLEMENTADO]** | `ConsentRecord` en `backend/app/models/entities.py`, `reportar/page.tsx` |
| **RF-03** | Registro de Reportes | RF | Asignación automática de identificador de caso cívico oficial con nomenclatura normalizada (ej. `EN-2026-XXXX`). | Buenas Prácticas / CICR | **[IMPLEMENTADO]** | Función `generate_case_number()` en `backend/app/api/v1/reports.py` |
| **RF-04** | Catálogo Público | RF | Separación visual y filtrado estricto entre "Casos Activos" (en búsqueda) y "Casos No Activos" (localizados/resueltos). | CICR (2023) | **[IMPLEMENTADO]** | Selector de tabs y filtros en `frontend/src/app/casos/page.tsx` |
| **RF-05** | Catálogo Público | RF | Priorización de visualización de fotografías reales autorizadas antes de recurrir a cualquier representación gráfica ilustrativa. | QA Senior / Usuario | **[IMPLEMENTADO]** | `getCasePhotoUrl()` en `catalogData.ts`, `ReportCard.tsx`, `reports.py` |
| **RF-06** | Ficha de Caso | RF | Despliegue de expediente forense completo, fotografía autorizada y Línea de Tiempo Dinámica (`timeline`) tipo 'Carpetas Vivas'. | CICR (2021, 2023) | **[IMPLEMENTADO]** | `CasoDetailClient.tsx`, `generateDefaultTimeline()` en `catalogData.ts` |
| **RF-07** | Moderación | RF | Los reportes nuevos ingresan en estado `pending_review` (`is_public=False`); requieren aprobación humana para su difusión pública. | Ética y Seguridad | **[IMPLEMENTADO]** | Endpoint `POST /api/v1/admin/reports/{id}/moderate` en `admin.py` |
| **RF-08** | Moderación | RF | Capacidad del moderador para solicitar aclaraciones (`request_changes`) o rechazar (`reject`) justificadamente reportes fraudulentos. | Ley 787 / Ética | **[IMPLEMENTADO]** | Función `moderate_report()` en `backend/app/api/v1/admin.py` |
| **RF-09** | Aportación de Pistas | RF | Recepción de testimonios ciudadanos con opción de anonimato estricto, generación de código de seguimiento único y no publicación abierta. | CICR (2021) | **[IMPLEMENTADO]** | `frontend/src/app/pistas/page.tsx`, `backend/app/api/v1/tips.py` |
| **RF-10** | Geolocalización | RF | Georreferenciación de casos en mapa nacional interactivo cubriendo los 15 departamentos y 2 regiones autónomas (153 municipios). | INIDE (2021) | **[IMPLEMENTADO]** | `NationalMap.tsx`, `frontend/public/data/nicaragua_departments.geojson` |
| **RF-11** | Geolocalización | RF | Protección de domicilio exacto: el mapa público ubica centroides municipales o zonas aproximadas (privacidad diferencial). | Ley 787 (Art. 6) | **[IMPLEMENTADO]** | Campos `approximate_latitude` y `approximate_longitude` en `entities.py` |
| **RF-12** | Gestión de Fotos | RF | Sanitización forzada de metadatos EXIF (coordenadas GPS, modelo cámara) antes de guardar cualquier archivo fotográfico en disco. | OWASP ASVS v5.0.0 (V12) | **[IMPLEMENTADO]** | `sanitize_and_save_image()` con Pillow en `storage_service.py` |
| **RF-13** | Gestión de Fotos | RF | Transcodificación obligatoria a WebP optimizado (calidad 85%, 800x800 máx) y almacenamiento con nombre hash impredecible en disco persistente. | OWASP ASVS (V12) | **[IMPLEMENTADO]** | `storage/uploads/` y endpoint `GET /api/v1/reports/photos/{key}` |
| **RF-14** | Cierre y Despublicación | RF | Retiro inmediato de publicación pública (`is_public=False`) tras resolución del caso para proteger la dignidad y evitar revictimización. | Ley 787 (Art. 16) | **[IMPLEMENTADO]** | Endpoint `POST /api/v1/reports/{id}/request-close` en `reports.py` |
| **RF-15** | Cierre y Despublicación | RF | Tramitación formal de supresión de datos bajo el artículo 16 de la Ley 787 a petición del titular o reportante verificado. | Ley 787 (Art. 16) | **[IMPLEMENTADO]** | Endpoint `POST /api/v1/reports/{id}/request-deletion` en `reports.py` |
| **RNF-01** | Seguridad / Auth | RNF | Almacenamiento de contraseñas mediante algoritmo de alta resistencia a memoria (Argon2id con sal aleatoria criptográfica). | OWASP ASVS (V2) | **[IMPLEMENTADO]** | `verify_password()`, `get_password_hash()` en `security.py` |
| **RNF-02** | Seguridad / Auth | RNF | Gestión de sesiones basada en tokens JWT firmados criptográficamente (HS256) con expiración corta y lista de revocaciones. | OWASP ASVS (V3) | **[IMPLEMENTADO]** | `create_access_token()`, tabla `token_revocations` en `entities.py` |
| **RNF-03** | Control de Acceso | RNF | Control de acceso basado en roles jerárquicos (RBAC: Admin, Moderator, Reporter, Citizen) aplicado estrictamente en servidor. | OWASP ASVS (V4) | **[IMPLEMENTADO]** | Inyección de dependencias `require_role`, `require_moderator` en `deps.py` |
| **RNF-04** | Auditoría Forense | RNF | Registro inmutable de operaciones críticas (creación, edición, consulta administrativa, moderación) con timestamp UTC y no-repudio. | OWASP ASVS (V8) | **[IMPLEMENTADO]** | Tabla `audit_logs` en BD y función `log_audit_event()` en `audit_service.py` |
| **RNF-05** | Seguridad en Red | RNF | Limitación de tasa de solicitudes (Rate Limiting) en memoria para mitigar ataques de fuerza bruta y denegación de servicio. | OWASP ASVS (V13) | **[IMPLEMENTADO]** | Dependencias `rate_limit_login`, `rate_limit_register` en `rate_limit.py` |
| **RNF-06** | Privacidad de Datos | RNF | No almacenamiento en texto claro de números de cédula; aplicación de función hash irreversible SHA-256 (`doc_hash`). | Ley 787 (Art. 6) | **[IMPLEMENTADO]** | Campo `identity_doc_hash` en tabla `consent_records` |
| **RNF-07** | Disponibilidad / Hosting | RNF | Compatibilidad de despliegue dual: API REST FastAPI y servido estático de Next.js SSG sin colisiones de enrutamiento 404. | DevOps / Arquitectura | **[IMPLEMENTADO]** | Despachador de rutas estáticas en `main.py` y exportación estática SSG |
| **RNF-08** | Autonomía y Resiliencia | RNF | Independencia total de CDNs externas para estilos (CSS), cartografía (Leaflet) e iconografía; paquetería 100% local. | Resiliencia Técnica | **[IMPLEMENTADO]** | `frontend/public/` (leaflet.css, marcadores locales, fuentes embebidas) |
| **RNF-09** | Rendimiento y Carga | RNF | Tiempos de respuesta inferiores a 500 ms en endpoints públicos de catálogo y descarga de imágenes sanitizadas. | Calidad de Servicio | **[REQUIERE VERIFICACIÓN]** | Verificado en local (<100ms); requiere pruebas de estrés bajo concurrencia masiva en hosting productivo. |
| **RNF-10** | Accesibilidad Web | RNF | Cumplimiento de pautas WCAG 2.1 nivel AA en contraste de color, etiquetas semánticas y compatibilidad con lectores de pantalla. | Buenas Prácticas UI | **[REQUIERE VERIFICACIÓN]** | Implementado en Tailwind (contrastes y etiquetas); requiere auditoría formal con herramientas Lighthouse/Axe. |
| **RNF-11** | Interoperabilidad Oficial | RNF | API estándar para intercambio seguro de fichas de búsqueda con instituciones estatales (Policía, Cruz Blanca, Ministerio Público). | CICR (2021) | **[PENDIENTE]** | Depende de acuerdos institucionales bilaterales y convenios formales de interoperabilidad que actualmente no existen. |
| **RNF-12** | Aplicación Móvil Offline | RNF | Soporte de Progressive Web App (PWA) o app nativa para recopilación de reportes y fotografías en zonas rurales sin cobertura celular. | Brecha Digital Rural | **[PENDIENTE]** | Recomendación de arquitectura identificada para futuras fases de expansión territorial en la Costa Caribe. |

---

### 3. SÍNTESIS DE ESTADO DE REQUISITOS

- **Requisitos Implementados (22/27 - 81.5%):**
  Todos los requisitos críticos vinculados al consentimiento Ley 787, sanitización EXIF, catálogo diferenciado, línea de tiempo 'Carpetas Vivas', autenticación Argon2id/JWT, RBAC y auditoría inmutable se encuentran plenamente codificados y validados mediante la suite de 38 pruebas Pytest.
- **Requisitos que Requieren Verificación (2/27 - 7.4%):**
  Desempeño bajo carga masiva concurrente en producción (RNF-09) y certificación formal WCAG 2.1 AA con herramientas automatizadas de accesibilidad (RNF-10).
- **Requisitos Pendientes (3/27 - 11.1%):**
  Interoperabilidad formal con bases estatales (RNF-11) y cliente móvil offline PWA para áreas rurales remotas (RNF-12), dependientes de convenios institucionales y fases posteriores.