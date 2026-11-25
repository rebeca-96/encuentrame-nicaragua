# 01 — INVENTARIO FUNCIONAL COMPLETO
## Proyecto: ENCUÉNTRAME NICARAGUA
### Plataforma Cívica para la Búsqueda y Localización Responsable de Personas Desaparecidas
**Auditor:** Senior QA Engineer & SDET  
**Fecha:** 19 de Noviembre de 2026  
**Versión:** 1.0.0-AUDIT  

---

## 1. RESUMEN DE LA ARQUITECTURA DETECTADA

| Capa | Tecnología Detectada | Versión / Detalle |
| :--- | :--- | :--- |
| **Frontend** | Next.js (App Router), React, TypeScript, Tailwind CSS, Lucide Icons | Next.js 15.x / React 19, compilación estática SSG (`next export` / `output: 'export'`) |
| **Backend** | Python, FastAPI, Pydantic v2, SQLAlchemy ORM, Uvicorn | Python 3.12, FastAPI 0.115+, arquitectura RESTful modular |
| **Base de Datos** | SQLite3 (desarrollo/staging local) / PostgreSQL (arquitectura compatible) | Modelo relacional con 13 entidades normalizadas y auditoría |
| **Geografía / Mapas**| Leaflet / React-Leaflet + Catálogo Territorial Oficial de Nicaragua | 15 Departamentos, 2 Regiones Autónomas (RACCN, RACCS) y 153 Municipios |
| **Almacenamiento** | Sistema de archivos local (`backend/storage/photos`) con verificación MIME | WebP / JPEG / PNG con hashing SHA-256 |
| **Autenticación** | JWT (HMAC-SHA256) con lista negra en memoria / DB + Password Hashing Bcrypt | 4 roles definidos: `admin`, `moderator`, `reporter`, `citizen` |

---

## 2. INVENTARIO DE PÁGINAS Y RUTAS (FRONTEND)

| ID | Ruta Frontend | Tipo | Rol Requerido | Dependencias de Backend | Estado Observado |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **PAG-01** | `/` | Pública | Anónimo | `GET /api/v1/reports/recent`, `GET /api/v1/statistics/summary`, `GET /api/v1/locations/departments` | Funcional en local; en hosting estático no conecta a la API. |
| **PAG-02** | `/casos` | Pública | Anónimo | `GET /api/v1/reports/`, `GET /api/v1/locations/departments`, `GET /api/v1/locations/municipalities` | En hosting falla si se ingresa sin `.html` (DEF-02). |
| **PAG-03** | `/casos/[id]` | Pública | Anónimo | `GET /api/v1/reports/{id}`, `GET /api/v1/reports/{id}/photos` | Funcional con export dinámico. En hosting requiere rewrite. |
| **PAG-04** | `/mapa` | Pública | Anónimo | `GET /api/v1/locations/map-aggregated`, `GET /api/v1/locations/departments` | Funcional en local con Leaflet; requiere proxy de API. |
| **PAG-05** | `/reportar` | Protegida | `reporter`, `moderator`, `admin` | `POST /api/v1/reports/`, `POST /api/v1/reports/{id}/photos`, `GET /api/v1/locations/...` | Flujo de 4 pasos implementado; requiere sesión activa. |
| **PAG-06** | `/pistas` | Pública / Mixta | Anónimo / Ciudadano | `POST /api/v1/tips/`, `GET /api/v1/tips/track/{tracking_code}` | Permite aporte confidencial anónimo y consulta con código. |
| **PAG-07** | `/admin` | Privada | `moderator`, `admin` | `GET /api/v1/admin/reports/pending`, `POST /api/v1/admin/reports/{id}/review`, `GET /api/v1/admin/audit-logs` | Panel de control, moderación de casos y pistas. |
| **PAG-08** | `/auth/login` | Pública | Anónimo | `POST /api/v1/auth/login` | Formulario con validación de credenciales y redirección por rol. |
| **PAG-09** | `/auth/registro` | Pública | Anónimo | `POST /api/v1/auth/register` | Registro ciudadano con consentimiento y verificación de teléfono. |
| **PAG-10** | `/privacidad` | Pública | Anónimo | Ninguna (Contenido estático Ley N.° 787) | Informativo institucional sobre derechos ARCO y confidencialidad. |
| **PAG-11** | `/contacto` | Pública | Anónimo | `POST /api/v1/notifications/feedback` | Formulario de atención ciudadana y números de emergencia (118). |

---

## 3. INVENTARIO DE ENDPOINTS DE BACKEND (REST API)

### 3.1 Módulo Autenticación (`/api/v1/auth`)
| Endpoint | Método | Autenticación | Rol | Descripción | Estado Observado |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `/api/v1/auth/login` | POST | No | Público | Autenticación con email y contraseña, emite JWT. | Rate limiting activo (5 req/min). |
| `/api/v1/auth/register` | POST | No | Público | Registro de nuevos usuarios ciudadanos / reportantes. | Rate limiting activo (3 req/10 min). |
| `/api/v1/auth/logout` | POST | Bearer JWT | Cualquier rol | Invalida el JWT actual en blacklist. | Verificado OK (HTTP 200). |
| `/api/v1/auth/me` | GET | Bearer JWT | Cualquier rol | Devuelve el perfil del usuario autenticado. | Protegido OK (HTTP 401 sin token). |

### 3.2 Módulo de Reportes de Personas Desaparecidas (`/api/v1/reports`)
| Endpoint | Método | Autenticación | Rol | Descripción | Estado Observado |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `/api/v1/reports/` | GET | No | Público | Lista casos públicos verificados (`status=published`). | Filtros por depto, municipio, género, edad. |
| `/api/v1/reports/recent` | GET | No | Público | Últimos 6 casos publicados para portada. | Funcional, orden descendente. |
| `/api/v1/reports/{id}` | GET | No | Público | Detalle de caso público (omite datos sensibles Ley 787). | 404 si no existe o no está publicado. |
| `/api/v1/reports/` | POST | Bearer JWT | `reporter`, `moderator`, `admin` | Crea un nuevo reporte de persona desaparecida. | Pasa a estado `pending_review`. |
| `/api/v1/reports/{id}` | PUT | Bearer JWT | Propietario o Staff | Actualiza datos descriptivos del reporte. | Auditoría de cambios registrada. |
| `/api/v1/reports/{id}/photos` | POST | Bearer JWT | Propietario o Staff | Carga fotografía de la persona desaparecida. | Validación MIME y tamaño máximo 5MB. |
| `/api/v1/reports/{id}/request-deletion`| POST | Bearer JWT | Propietario o Staff | Solicitud formal de cancelación por Ley 787. | Registra evento y pasa a revisión de baja. |

### 3.3 Módulo de Pistas Confidenciales (`/api/v1/tips`)
| Endpoint | Método | Autenticación | Rol | Descripción | Estado Observado |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `/api/v1/tips/` | POST | No | Anónimo / Ciudadano | Envío seguro de información o avistamiento. | Genera código `PISTA-XXXX-XXXX`. |
| `/api/v1/tips/track/{code}` | GET | No | Anónimo (con código) | Consulta el estado de verificación de la pista. | Oculta identidad del informante. |
| `/api/v1/tips/{id}/review` | POST | Bearer JWT | `moderator`, `admin` | Moderador valida o descarta la pista. | Registra notas de investigación interna. |

### 3.4 Módulo Geográfico y Mapas (`/api/v1/locations`)
| Endpoint | Método | Autenticación | Rol | Descripción | Estado Observado |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `/api/v1/locations/departments` | GET | No | Público | Catálogo de 17 entidades (15 deptos + 2 regiones). | Verificado completo con códigos ISO/INEC. |
| `/api/v1/locations/municipalities` | GET | No | Público | Lista los 153 municipios filtrables por departamento. | Relación jerárquica exacta verificada. |
| `/api/v1/locations/map-aggregated` | GET | No | Público | Puntos geográficos agregados para el mapa cívico. | Coordenadas aproximadas sin vulnerar privacidad. |

### 3.5 Módulo de Administración y Auditoría (`/api/v1/admin`)
| Endpoint | Método | Autenticación | Rol | Descripción | Estado Observado |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `/api/v1/admin/reports/pending` | GET | Bearer JWT | `moderator`, `admin` | Cola de expedientes pendientes de moderación. | Bloqueado para reporter/citizen (HTTP 403). |
| `/api/v1/admin/reports/{id}/review` | POST | Bearer JWT | `moderator`, `admin` | Aprobar (`published`) o Rechazar (`rejected`) caso. | Genera historial inmutable en DB. |
| `/api/v1/admin/audit-logs` | GET | Bearer JWT | `admin` | Bitácora de accesos, modificaciones y cierres. | Restringido exclusivamente al Administrador. |
| `/api/v1/admin/stats` | GET | Bearer JWT | `moderator`, `admin` | Métricas operativas y tiempos de respuesta. | Agregaciones estadísticas en tiempo real. |

---

## 4. INVENTARIO DE COMPONENTES DE INTERFAZ (UI)

1. **Barra de Navegación Principal (`Navbar.tsx`):**
   - Logotipo institucional y lema cívico.
   - Enlaces de navegación: Inicio, Casos Activos, Mapa Nacional, Aportar Pista, Reportar Caso.
   - Indicador de estado de sesión (Botón Ingresar / Avatar con menú desplegable).
   - Menú responsive colapsable tipo hamburguesa para resoluciones móviles.

2. **Pie de Página (`Footer.tsx`):**
   - Enlaces institucionales, marco legal (Ley N.° 787 de Protección de Datos Personales).
   - Canales oficiales de emergencia de Nicaragua (Policía Nacional 118, Bomberos 115, Cruz Blanca).
   - Declaración de uso ético y no monetización.

3. **Buscador y Filtros Avanzados (`CaseFilter.tsx`):**
   - Input de texto con debounce para búsqueda por nombre, alias o número de expediente.
   - Select dinámico en cascada: Departamento -> Municipios pertenecientes.
   - Filtros por rango de edad y género.

4. **Visor de Mapa Interactivo (`NationalMap.tsx`):**
   - Integración con OpenStreetMap vía Leaflet.
   - Clusters de marcadores geográficos aproximados por municipio.
   - Popups con resumen del caso y enlace al expediente completo.

5. **Asistente de Reporte en Pasos (`ReportWizard.tsx`):**
   - Paso 1: Datos de identidad de la persona no localizada.
   - Paso 2: Ubicación geográfica y circunstancias de la desaparición.
   - Paso 3: Fotografía reciente y señas particulares.
   - Paso 4: Declaración jurada, representación legal y consentimiento Ley 787.

6. **Módulo de Pistas Anónimas (`TipForm.tsx`):**
   - Formulario de avistamiento con campos opcionales de contacto.
   - Generador y protector de código alfanumérico único para seguimiento ciudadano.
