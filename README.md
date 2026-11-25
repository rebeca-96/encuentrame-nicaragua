# ENCUÉNTRAME NICARAGUA
## Plataforma Inteligente de Búsqueda y Reunificación Familiar
### *Cada persona importa*

---

## 1. DESCRIPCIÓN DEL PROBLEMA
En Nicaragua, la desaparición o no localización de una persona genera una crisis humanitaria y emocional inmediata en su entorno familiar. Históricamente, las familias recurren a la difusión fragmentada en redes sociales (Facebook, WhatsApp, grupos comunitarios), lo que conlleva severos problemas colaterales:
- **Exposición a estafas y extorsiones:** Familiares publican sus números personales de contacto en redes abiertas, convirtiéndose en blancos de extorsionistas.
- **Desinformación y bulos:** Circulación de información caduca, no contrastada o fotos manipuladas que desvían los recursos y esperanzas de búsqueda.
- **Riesgos de revictimización y violencia de género:** Personas que han huido de contextos de violencia intrafamiliar o trata corren peligro si su localización es facilitada inadvertidamente mediante reportes manipulados.
- **Falta de agregación geográfica e histórica:** No existía una plataforma cívica centralizada con correlación espacial de casos por los 15 departamentos y 2 regiones autónomas de Nicaragua.

---

## 2. JUSTIFICACIÓN SOCIAL
**ENCUÉNTRAME NICARAGUA** nace como una herramienta digital cívica, ética y sin fines de lucro para dignificar los procesos de búsqueda, centralizar reportes consentidos, recibir pistas anónimas cifradas y coordinar esfuerzos comunitarios bajo estricta supervisión humana. La plataforma actúa como apoyo social y **no sustituye la labor ni las atribuciones legales de la Policía Nacional de Nicaragua, el Ministerio de la Familia ni las autoridades judiciales**.

---

## 3. OBJETIVOS
- **General:** Desarrollar una plataforma web full stack, segura, escalable y accesible que permita centralizar, administrar y difundir responsablemente reportes de personas desaparecidas o no localizadas en Nicaragua.
- **Específicos:**
  1. Diseñar una interfaz intuitiva, accesible (WCAG 2.2 AA) y adaptada a dispositivos móviles.
  2. Implementar un módulo de registro multipaso con consentimiento informado bajo la **Ley N.° 787 de Nicaragua**.
  3. Desarrollar un buscador inteligente con filtros geográficos, etarios y descriptivos.
  4. Incorporar un mapa interactivo nacional (Leaflet/OSM) con zonas aproximadas y protección de domicilios particulares.
  5. Implementar un canal seguro y cifrado para recibir pistas ciudadanas confidenciales.
  6. Diseñar un panel de moderación y auditoría inmutable con control de roles (RBAC).
  7. Integrar herramientas de IA asistida para detección de duplicados y síntesis de casos (con exclusión explícita de biometría facial en el MVP).

---

## 4. ALCANCE Y LIMITACIONES
- **Alcance del MVP:**
  - Directorio público de casos aprobados con fotografía sanitizada (sin metadatos EXIF).
  - Buscador multifiltro con tolerancia textual y búsqueda semántica.
  - Visualización geoespacial agregada en los 15 departamentos y 2 regiones autónomas (RACCN, RACCS).
  - Registro de casos con declaración jurada de veracidad y parentesco.
  - Flujo de moderación estricto: ningún reporte se publica de forma automática.
  - Recepción de pistas confidenciales con código único no adivinable (`PISTA-XXXX-XXXX`).
  - Panel administrativo con métricas operativas y logs de auditoría inmutables.
  - Detección asistida por IA de reportes potencialmente duplicados.
- **Limitaciones Técnicas y Éticas:**
  - **No realiza identificación biométrica facial:** Deshabilitada por diseño para salvaguardar los derechos humanos y la legislación de protección de datos.
  - **Ubicaciones aproximadas:** La plataforma no almacena ni expone coordenadas exactas de domicilios particulares ni de refugios.

---

## 5. REQUISITOS FUNCIONALES
- **RF-01:** Autenticación robusta de usuarios con contraseñas protegidas mediante Argon2id.
- **RF-02:** Registro de reportes en estado obligatorio `PENDIENTE_REVISION` con consentimiento informado documentado.
- **RF-03:** Aprobación, solicitud de cambios o rechazo formal de reportes por parte de moderadores autorizados.
- **RF-04:** Eliminación automática de metadatos EXIF en toda imagen cargada antes de su almacenamiento.
- **RF-05:** Buscador avanzado combinable por nombre, departamento, municipio, género, edad y señas particulares.
- **RF-06:** Visualización en mapa interactivo de casos activos con leyendas de alerta para menores de edad (NNA).
- **RF-07:** Recepción de pistas confidenciales aisladas de la vista pública, accesibles únicamente por moderadores.
- **RF-08:** Consulta anónima del estado de trámite de una pista mediante código único.
- **RF-09:** Solicitud de cierre y despublicación inmediata de casos localizados o resueltos para proteger la privacidad.
- **RF-10:** Detección asistida por IA de posibles casos duplicados basada en similitud de nombres, edad y geografía.

---

## 6. REQUISITOS NO FUNCIONALES
- **RNF-01 (Seguridad):** Control de acceso basado en roles (RBAC) y validación de permisos a nivel de objeto. Cabeceras HTTP de seguridad (`nosniff`, `DENY`, `XSS-Protection`).
- **RNF-02 (Privacidad):** Cumplimiento de los principios de minimización y finalidad de la Ley N.° 787 de Nicaragua.
- **RNF-03 (Rendimiento):** Tiempo de respuesta de endpoints de búsqueda y lectura inferior a 250 ms.
- **RNF-04 (Accesibilidad):** Interfaz diseñada bajo directrices WCAG 2.2 AA (contraste de color >= 4.5:1, etiquetas ARIA).
- **RNF-05 (Disponibilidad y Portabilidad):** Compatible con ejecución nativa local y contenerizada mediante Docker y Docker Compose.

---

## 7. HISTORIAS DE USUARIO
- **HU-01 (Familiar):** *Como* familiar de una persona no localizada, *quiero* registrar un reporte con consentimiento legal, *para* difundir su búsqueda de forma oficial sin exponer mi número de teléfono personal.
- **HU-02 (Moderador):** *Como* moderador de la plataforma, *quiero* verificar la documentación de un caso y consultar sugerencias de duplicados por IA, *para* autorizar únicamente reportes legítimos y veraces.
- **HU-03 (Ciudadano):** *Como* testigo o ciudadano con información, *quiero* aportar una pista de forma confidencial y recibir un código de seguimiento, *para* colaborar con la localización sin comprometer mi seguridad.
- **HU-04 (Administrador):** *Como* administrador general, *quiero* auditar las acciones realizadas en el sistema, *para* asegurar la trazabilidad y la rendición de cuentas.

---

## 8. CASOS DE USO PRINCIPALES
1. **CU-01:** Registrar nuevo caso con consentimiento informado y fotografía.
2. **CU-02:** Revisar y moderar reporte pendiente (Aprobar / Rechazar / Solicitar correcciones).
3. **CU-03:** Buscar casos en el directorio público y mapa nacional.
4. **CU-04:** Enviar pista ciudadana confidencial sobre un caso específico.
5. **CU-05:** Rastrear estado de trámite de una pista ciudadana.
6. **CU-06:** Solicitar cierre de caso y despublicación inmediata por localización exitosa.

---

## 9. ARQUITECTURA DE SOFTWARE
El sistema implementa una arquitectura desacoplada y orientada a servicios de dominio:
- **Capa de Presentación:** Next.js 14 App Router, React 18, TypeScript, Tailwind CSS, Lucide Icons y Leaflet.
- **Capa de Servicios y API:** FastAPI (Python 3.12), Pydantic v2 para validación estricta, SQLAlchemy 2.0 para persistencia y Argon2id para criptografía de contraseñas.
- **Capa de Persistencia y Caché:** Base de datos relacional (SQLite para ejecución local cero configuración, PostgreSQL + PostGIS para despliegue productivo) y Redis.
- **Capa de Almacenamiento:** Módulo desacoplado con sanitización EXIF mediante Pillow y compresión a WebP.

---

## 10. DIAGRAMA DE COMPONENTES
```
[ Navegador Web / Cliente Móvil ]
            │  HTTPS / JSON
            ▼
[ Gateway & Middleware de Seguridad (CORS, Rate Limit, Auth JWT) ]
            │
            ├─► [/api/v1/auth]         ──► Servicio de Autenticación (Argon2id)
            ├─► [/api/v1/reports]      ──► Servicio de Reportes & Sanitización EXIF
            ├─► [/api/v1/search]       ──► Motor de Búsqueda & Tolerancia Textual
            ├─► [/api/v1/locations]    ──► Servicio Geográfico de Nicaragua
            ├─► [/api/v1/tips]         ──► Gestor Cifrado de Pistas Confidenciales
            ├─► [/api/v1/admin]        ──► Centro de Moderación y Auditoría
            └─► [/api/v1/ai]           ──► Asistente IA (Detección de Duplicados)
            │
            ▼
[ Persistencia: PostgreSQL / SQLite ] ── [ Storage Sanitizado: WebP ]
```

---

## 11. DIAGRAMA ENTIDAD-RELACIÓN (14 MODELOS)
```
USERS (id, email, password_hash, full_name, phone_number, role, is_active, is_verified)
  │1
  ├───< MISSING_PERSON_REPORTS (id, case_number, reporter_id, status, first_name, last_name,
  │                              age, gender, disappearance_date, location_id, physical_desc,
  │                              clothing_desc, circumstances, is_minor, is_public)
  │        │1
  │        ├───< REPORT_PHOTOS (id, report_id, storage_key, is_primary, is_approved, original_filename)
  │        ├───< CONFIDENTIAL_TIPS (id, report_id, tip_code, description, sighting_date, status)
  │        │        │1
  │        │        └───< SIGHTINGS (id, tip_id, evidence_storage_key)
  │        ├───< REPORT_STATUS_HISTORY (id, report_id, changed_by, previous_status, new_status, reason)
  │        ├───< MODERATION_REVIEWS (id, report_id, moderator_id, decision, notes_internal)
  │        ├───< CONSENT_RECORDS (id, report_id, reporter_id, relationship_to_victim, doc_hash)
  │        ├───< DELETION_REQUESTS (id, report_id, requested_by, reason, status)
  │        └───< AI_ANALYSIS_RESULTS (id, report_id, potential_duplicate_id, similarity_score)
  │
  ├───< NOTIFICATION_SUBSCRIPTIONS (id, user_id, email, department, is_active)
  │        │1
  │        └───< NOTIFICATIONS (id, subscription_id, type, title, content, status)
  │
  └───< AUDIT_LOGS (id, user_id, action, entity_name, entity_id, ip_address, details_json)

GEOGRAPHIC_LOCATIONS (id, department, municipality, approximate_lat, approximate_lng, is_sensitive)
```

---

## 12. DISEÑO DE API REST
| Método | Endpoint | Descripción | Acceso |
| :--- | :--- | :--- | :--- |
| `POST` | `/api/v1/auth/login` | Inicio de sesión y emisión de JWT | Público |
| `POST` | `/api/v1/auth/register` | Registro de nuevo usuario reportante | Público |
| `GET` | `/api/v1/auth/me` | Consulta de perfil y permisos | Autenticado |
| `GET` | `/api/v1/reports/` | Catálogo público paginado con filtros | Público |
| `GET` | `/api/v1/reports/{id}` | Expediente público autorizado | Público / Privado si no aprobado |
| `POST` | `/api/v1/reports/` | Creación de nuevo reporte (ingresa como `pending_review`) | Reportante autenticado |
| `POST` | `/api/v1/reports/{id}/photos`| Carga y sanitización EXIF de fotografía | Autor o Moderador |
| `POST` | `/api/v1/reports/{id}/request-close` | Solicitud de cierre y despublicación | Autor o Moderador |
| `GET` | `/api/v1/search/` | Búsqueda textual y multifiltro tolerante | Público |
| `GET` | `/api/v1/locations/departments` | Lista oficial de 17 departamentos/regiones de Nicaragua | Público |
| `GET` | `/api/v1/locations/map-aggregated` | Puntos aproximados de casos activos para el mapa | Público |
| `POST` | `/api/v1/tips/` | Envío de pista confidencial cifrada | Público / Anónimo |
| `GET` | `/api/v1/tips/track/{code}` | Consulta anónima del estado de una pista | Público / Anónimo |
| `GET` | `/api/v1/admin/metrics` | Métricas operativas del sistema | Moderador / Administrador |
| `GET` | `/api/v1/admin/reports/pending` | Bandeja de casos pendientes de moderación | Moderador / Administrador |
| `POST` | `/api/v1/admin/reports/{id}/moderate` | Decisión formal de aprobación o rechazo | Moderador / Administrador |
| `GET` | `/api/v1/admin/tips` | Triaje de pistas confidenciales | Moderador / Administrador |
| `GET` | `/api/v1/admin/audit-logs` | Logs inmutables de auditoría | Administrador General |
| `POST` | `/api/v1/ai/check-duplicates/{id}` | Asistente IA de coincidencia de duplicados | Moderador / Administrador |
| `GET` | `/api/v1/ai/summary/{id}` | Ficha sintética y chequeo de completitud | Moderador / Administrador |

---

## 13. ESTRUCTURA DE CARPETAS
```
EncuentrameNicaragua/
├── backend/
│   ├── app/
│   │   ├── api/v1/         # Controladores por dominio (auth, reports, search, tips, admin, ai...)
│   │   ├── core/           # Configuración, seguridad (Argon2id, JWT), database engine
│   │   ├── models/         # 14 Entidades SQLAlchemy 2.0
│   │   ├── schemas/        # Esquemas Pydantic v2
│   │   ├── services/       # Lógica de negocio (storage EXIF, geo, ai, audit)
│   │   ├── seed/           # Generador de 20 casos sintéticos nicaragüenses
│   │   └── main.py         # Punto de entrada FastAPI y middlewares
│   ├── tests/              # Suite de pruebas automatizadas Pytest (10 puntos críticos)
│   ├── Dockerfile
│   └── requirements.txt
├── frontend/
│   ├── src/
│   │   ├── app/            # Rutas Next.js 14 App Router (/, /casos, /mapa, /reportar, /pistas, /admin, /login)
│   │   ├── components/     # Componentes modulares UI (Navbar, Footer, ReportCard, NicaraguaMap)
│   │   ├── lib/            # Cliente API con tipado fuerte
│   │   └── types/          # Definiciones TypeScript compartidas
│   ├── Dockerfile
│   ├── package.json
│   ├── tailwind.config.ts
│   └── tsconfig.json
├── docker-compose.yml      # Orquestación de servicios (db, redis, backend, frontend)
├── .github/workflows/ci.yml # Integración continua (CI)
├── .env.example            # Plantilla de variables de entorno documentadas
└── README.md               # Documentación técnica completa
```

---

## 14. INSTRUCCIONES DE INSTALACIÓN Y EJECUCIÓN LOCAL

### Prerrequisitos
- Python 3.11 o superior (Verificado en Python 3.12.10)
- Node.js 18 o superior (Verificado en Node.js v24.19.0 / npm 11.17.0)

### Opción A: Ejecución Nativa Local (Recomendada para desarrollo)
1. **Clonar e ingresar al proyecto:**
   ```bash
   cd "c:\Users\User\Documents\Valor IA\EncuentrameNicaragua"
   ```
2. **Iniciar Backend FastAPI:**
   ```bash
   # Activar entorno virtual
   .\venv\Scripts\Activate.ps1
   # Establecer PYTHONPATH y correr servidor
   $env:PYTHONPATH="backend"
   python -m uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
   ```
   *El backend estará disponible en `http://127.0.0.1:8000` y la documentación Swagger OpenAPI en `http://127.0.0.1:8000/docs`.*

3. **Iniciar Frontend Next.js:**
   ```bash
   cd frontend
   npm run dev
   ```
   *El portal web estará disponible en `http://localhost:3000`.*

### Opción B: Ejecución Contenerizada con Docker Compose
```bash
docker compose up --build -d
```

---

## 15. USUARIOS Y CREDENCIALES DE DEMOSTRACIÓN
El sistema incluye datos sintéticos de demostración con 4 perfiles preconfigurados:

| Rol | Correo Electrónico | Contraseña | Alcance |
| :--- | :--- | :--- | :--- |
| **Administrador General** | `admin@encuentrame.ni` | `AdminPass2026!` | Acceso a métricas globales, gestión, moderación y logs de auditoría. |
| **Moderador** | `moderador@encuentrame.ni` | `ModPass2026!` | Bandeja de moderación, validación documental, triaje de pistas y asistente IA. |
| **Reportante Familiar** | `reportante@encuentrame.ni`| `ReportPass2026!` | Registro de reportes, carga de fotografías y solicitud de cierre. |
| **Ciudadano Registrado** | `ciudadano@encuentrame.ni` | `CitizenPass2026!` | Consulta de casos, visualización de mapa y envío de pistas. |

*(La pantalla de inicio de sesión `/login` incluye botones de autorelleno rápido para pruebas inmediatas).*

---

## 16. MANUAL DE USUARIO
1. **Búsqueda de personas:** Ingrese a la portada o al apartado **Casos Activos** (`/casos`). Puede filtrar por departamento (ej. Managua, Matagalpa, León), rango de edad o marcar la casilla de verificación *"Solo menores de edad"*.
2. **Visualizar mapa geográfico:** Haga clic en **Mapa Nacional** (`/mapa`) para explorar la distribución territorial de los casos con marcadores diferenciados para menores de edad.
3. **Reportar un caso:** Acceda a **Reportar Caso** (`/reportar`), inicie sesión y complete los 4 pasos del formulario. En el último paso, acepte formalmente la declaración jurada y los términos de la Ley N.° 787. Al enviar, recibirá un número de caso oficial (ej. `EN-2026-0001`).
4. **Aportar una pista confidencial:** En la ficha de cualquier persona (`/casos/[id]`), desplácese a la sección inferior de pistas. Escriba la información de avistamiento y presione *"Enviar Pista Confidencial"*. El sistema le entregará un código único (ej. `PISTA-8A12-9F01`).
5. **Rastrear una pista:** Ingrese a **Aportar Pista** (`/pistas`), introduzca su código y consulte el estado del trámite de manera 100% anónima.

---

## 17. MANUAL DE ADMINISTRADOR Y MODERADOR
1. **Acceso al Panel:** Inicie sesión con credenciales de moderador o administrador y haga clic en la opción **Moderación** (`/admin`).
2. **Cola de Casos Pendientes:**
   - Revise la información declarada por el familiar, incluyendo los datos privados de contacto y el hash de su documento de identidad.
   - Presione el botón **Asistente IA** para comprobar si existen casos duplicados previamente registrados o si existen campos descriptivos débiles.
   - Seleccione **Aprobar y Publicar** (para hacer visible el caso en el catálogo y mapa) o **Rechazar**. Toda acción exigirá ingresar una nota interna que quedará grabada en el historial.
3. **Triaje de Pistas Confidenciales:** Acceda a la pestaña *Pistas Confidenciales* para consultar los aportes ciudadanos, evaluar su relevancia y cambiar su estado (`received` -> `triaged` -> `escalated`).
4. **Auditoría del Sistema:** El Administrador General puede acceder a la pestaña *Registro de Auditoría* para consultar eventos de inicio de sesión, aprobación de reportes y accesos a datos protegidos con registro de IP y fecha.

---

## 18. PLAN DE PRUEBAS Y CRITERIOS EVALUADOS
La suite de pruebas automatizadas (`backend/tests/test_core_requirements.py`) evalúa de forma estricta los 10 criterios fundamentales de seguridad y funcionalidad:
1. **Prueba 1:** Comprobar que un nuevo reporte no se publique sin aprobación (`pending_review` y `is_public=False`).
2. **Prueba 2:** Comprobar que un ciudadano anónimo o regular no pueda acceder a la lista de pistas privadas (HTTP 401/403).
3. **Prueba 3:** Comprobar que un usuario no pueda modificar ni solicitar el cierre de reportes ajenos.
4. **Prueba 4:** Comprobar que los filtros de búsqueda devuelvan resultados exactos y no mezclen estados.
5. **Prueba 5:** Comprobar que los datos geográficos públicos no expongan coordenadas ni domicilios exactos.
6. **Prueba 6:** Comprobar que las acciones administrativas de moderación queden registradas en `audit_logs`.
7. **Prueba 7:** Comprobar que el cierre de un caso despublique inmediatamente el reporte para proteger la dignidad.
8. **Prueba 8:** Comprobar el manejo de errores ante datos inválidos o rechazo de términos de consentimiento.
9. **Prueba 9:** Comprobar que la IA actúe como asesora sin modificar de forma autónoma ningún estado.
10. **Prueba 10:** Comprobar la recepción de pistas y la generación de códigos de seguimiento no adivinables.

---

## 19. EVIDENCIAS DE EJECUCIÓN DE PRUEBAS

```
============================= test session starts =============================
platform win32 -- Python 3.12.10, pytest-9.2.0, pluggy-1.7.0
rootdir: C:\Users\User\Documents\Valor IA\EncuentrameNicaragua
plugins: anyio-4.16.0, asyncio-1.5.0
collected 10 items

backend/tests/test_core_requirements.py::test_1_new_report_not_published_without_moderator_approval PASSED [ 10%]
backend/tests/test_core_requirements.py::test_2_citizen_cannot_access_confidential_tips PASSED [ 20%]
backend/tests/test_core_requirements.py::test_3_user_cannot_modify_or_close_others_reports PASSED [ 30%]
backend/tests/test_core_requirements.py::test_4_search_filters_return_correct_results PASSED [ 40%]
backend/tests/test_core_requirements.py::test_5_geographic_data_does_not_reveal_sensitive_coordinates PASSED [ 50%]
backend/tests/test_core_requirements.py::test_6_administrative_actions_are_audit_logged PASSED [ 60%]
backend/tests/test_core_requirements.py::test_7_case_closure_is_processable_and_depublishes_case PASSED [ 70%]
backend/tests/test_core_requirements.py::test_8_error_handling_for_invalid_input_and_missing_consent PASSED [ 80%]
backend/tests/test_core_requirements.py::test_9_ai_acts_strictly_as_advisor_without_autonomous_state_changes PASSED [ 90%]
backend/tests/test_core_requirements.py::test_10_secure_tip_submission_and_unpredictable_code PASSED [100%]

======================= 10 passed, 2 warnings in 1.97s ========================
```

---

## 20. PROBLEMAS ENCONTRADOS Y SOLUCIONES (FASE 5)
1. **Defecto de sintaxis en Pydantic V2:**
   - *Estado inicial:* Se utilizó el parámetro `regex` en validadores `Field(...)` y `Query(...)`.
   - *Problema detectado:* Error `pydantic.errors.PydanticUserError: 'regex' is removed. use 'pattern' instead`.
   - *Causa raíz:* Incompatibilidad entre la convención antigua de Pydantic v1 y la versión moderna instalada (Pydantic 2.14).
   - *Solución:* Reemplazo de todos los argumentos `regex` por `pattern` y migración a `model_config = ConfigDict(from_attributes=True)`.
2. **Bloqueo de archivo en Windows SQLite durante el desmontaje (Teardown):**
   - *Estado inicial:* El fixture de prueba intentaba borrar el archivo temporal `./test_encuentrame.db` mientras la conexión continuaba abierta en el pool.
   - *Problema detectado:* `PermissionError: [WinError 32] El proceso no tiene acceso al archivo`.
   - *Causa raíz:* Comportamiento del descriptor de archivo en Windows cuando el motor de base de datos mantiene conexiones activas.
   - *Solución:* Invocación explícita de `test_engine.dispose()` antes de remover el archivo físico.

---

## 21. MEJORAS IMPLEMENTADAS
- **Sanitización automática de imágenes con borrado de metadatos EXIF:** Implementada con Pillow para impedir la filtración de coordenadas GPS registradas por cámaras de teléfonos celulares.
- **Búsqueda semántica asistida y detección de duplicados con cálculo de similitud:** Evita la sobrecarga de casos idénticos y asiste la labor humana del moderador.
- **Diseño responsive mobile-first accesible:** Implementado con paleta cívica institucional (Deep Navy `#0F2A4A`, Civic Teal `#0D9488`, acentos ámbar y rojo de alerta controlada).

---

## 22. RECOMENDACIONES PARA PRODUCCIÓN
1. **Gestión de Secretos:** Configurar un gestor de secretos (AWS Secrets Manager, HashiCorp Vault o variables de entorno protegidas en Kubernetes/Railway/Render) para almacenar `SECRET_KEY` y credenciales de base de datos.
2. **Servicio de Almacenamiento S3:** Conectar un bucket de Amazon S3 o Cloudflare R2 con políticas de acceso privadas y generación de URLs firmadas temporales para archivos de evidencia.
3. **Caché y Límites de Solicitudes:** Habilitar Redis en producción para rate limiting en el endpoint de recepción de pistas (`/api/v1/tips/`).
4. **Convenios Institucionales:** Establecer canales directos y protocolos seguros de enlace con la Dirección de Auxilio Judicial de la Policía Nacional de Nicaragua y el Ministerio de la Familia.
