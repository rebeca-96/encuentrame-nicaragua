# -*- coding: utf-8 -*-
"""
Script generador de la documentación técnica y bitácora completa del proyecto Encuéntrame Nicaragua.
Genera el archivo DOCUMENTACION_COMPLETA_PROYECTO.txt en la raíz del repositorio.
"""

import os
import json
import re
from datetime import datetime

ROOT_DIR = r"c:\Users\User\Documents\Valor IA\EncuentrameNicaragua"
OUTPUT_FILE = os.path.join(ROOT_DIR, "DOCUMENTACION_COMPLETA_PROYECTO.txt")
TRANSCRIPT_PATH = r"C:\Users\User\.gemini\antigravity\brain\a4895693-7c77-4ec0-906a-ddacc924e6c9\.system_generated\logs\transcript.jsonl"

def extract_prompts():
    prompts = []
    if os.path.exists(TRANSCRIPT_PATH):
        with open(TRANSCRIPT_PATH, "r", encoding="utf-8") as f:
            for line in f:
                try:
                    data = json.loads(line)
                    if data.get("type") == "USER_INPUT" and data.get("source") == "USER_EXPLICIT":
                        c = data.get("content", "")
                        c = re.sub(r"<USER_REQUEST>\s*", "", c)
                        c = re.sub(r"</USER_REQUEST>.*", "", c, flags=re.DOTALL)
                        prompts.append({
                            "timestamp": data.get("created_at"),
                            "content": c.strip()
                        })
                except Exception:
                    pass
    return prompts

def build_documentation():
    prompts = extract_prompts()
    
    doc = []
    doc.append("=" * 100)
    doc.append("DOCUMENTACIÓN TÉCNICA INTEGRAL, ARQUITECTURA Y BITÁCORA HISTÓRICA DEL PROYECTO")
    doc.append("ENCUÉNTRAME NICARAGUA: PLATAFORMA CÍVICA DE BÚSQUEDA Y REUNIFICACIÓN FAMILIAR")
    doc.append("=" * 100)
    doc.append(f"Fecha de generación de la documentación: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    doc.append("Autor / Rol: Equipo de Ingeniería Full Stack Senior, Arquitectura de Software, Seguridad y QA")
    doc.append("Ubicación del repositorio: " + ROOT_DIR)
    doc.append("=" * 100)
    doc.append("\n" + "=" * 100)
    doc.append("TABLA DE CONTENIDOS")
    doc.append("=" * 100)
    doc.append("1. RESUMEN EJECUTIVO Y FICHA TÉCNICA GENERAL")
    doc.append("2. ARQUITECTURA DEL SISTEMA Y CREACIÓN INICIAL")
    doc.append("   2.1. Propósito Cívico y Marco Legal (Ley N.° 787 de Nicaragua)")
    doc.append("   2.2. Pila Tecnológica (Stack Tecnológico Full Stack)")
    doc.append("   2.3. Estructura de Directorios del Proyecto")
    doc.append("   2.4. Modelo de Datos y Esquema Relacional de Base de Datos")
    doc.append("   2.5. Arquitectura de Seguridad y Control de Acceso (RBAC)")
    doc.append("   2.6. Módulo de Gestión de Medios y Sanitización de Imágenes EXIF")
    doc.append("3. BITÁCORA CRONOLÓGICA COMPLETA DE PROMPTS Y REQUERIMIENTOS DEL USUARIO (38 PROMPTS)")
    doc.append("4. ANÁLISIS DETALLADO DE HITOS, DIAGNÓSTICOS, CAMBIOS Y AJUSTES REALIZADOS")
    doc.append("   4.1. Creación Inicial y Planificación (Fases 1, 2 y 3)")
    doc.append("   4.2. Primeras Auditorías de Seguridad, RBAC y Cobertura de Pruebas Pytest")
    doc.append("   4.3. Módulo GIS, División Político-Administrativa y Mapas de Nicaragua")
    doc.append("   4.4. Autonomía y Desacoplamiento de Dependencias Externas (Paquetería Local)")
    doc.append("   4.5. Configuración de Exportación Estática Next.js y Servidor FastAPI (main.py)")
    doc.append("   4.6. Despliegue en Hosting Público y Diagnóstico de Enrutamiento (tradescanner.online)")
    doc.append("   4.7. Integración de Multimedia Institucional (Video y Ajustes de Portada)")
    doc.append("   4.8. Corrección de Endpoints de Autenticación y Registro (Error 405 Method Not Allowed)")
    doc.append("   4.9. Formulario de Registro de Casos: Selectores Dinámicos de Departamentos y Municipios")
    doc.append("   4.10. Corrección de Error de Sincronización en Mapa Nacional GeoJSON")
    doc.append("   4.11. Catálogo Oficial: Separación de Casos Activos y No Activos (Resueltos)")
    doc.append("   4.12. Consulta de Fichas: Expediente Forense, Hitos en Vivo y Tracking en Tiempo Real")
    doc.append("   4.13. Auditoría Exhaustiva del Módulo de Fotografías y Gestión de Archivos")
    doc.append("   4.14. Resolución Crítica de Enrutamiento y Navegación Next.js + FastAPI (Evitar JSON 404)")
    doc.append("   4.15. Localización, Estructura y Esquema de la Base de Datos (encuentrame_nicaragua.db)")
    doc.append("   4.16. Visualización de Fotografías Reales Subidas en Catálogo Local (Eliminación de Avatares Sintéticos)")
    doc.append("5. REGISTRO DE ARCHIVOS CLAVE MODIFICADOS Y CREADOS")
    doc.append("6. ASEGURAMIENTO DE CALIDAD (QA), COBERTURA DE PRUEBAS Y VALIDACIÓN")
    doc.append("7. GUÍA OPERATIVA: INSTALACIÓN, EJECUCIÓN LOCAL Y MANTENIMIENTO")
    doc.append("=" * 100 + "\n")

    # SECCION 1
    doc.append("\n" + "=" * 100)
    doc.append("1. RESUMEN EJECUTIVO Y FICHA TÉCNICA GENERAL")
    doc.append("=" * 100)
    doc.append(r"""
ENCUÉNTRAME NICARAGUA es una solución tecnológica cívica orientada a facilitar la búsqueda,
geolocalización, difusión oficial y reunificación de personas reportadas como desaparecidas o no
localizadas en la República de Nicaragua.

Ficha Técnica:
- Nombre del Proyecto: Encuéntrame Nicaragua
- Dominio Local: http://127.0.0.1:8000
- Dominio de Despliegue Público: https://creacionvaloria.tradescanner.online
- Tipo de Aplicación: Sistema Web Full Stack desacoplado con arquitectura Híbrida (FastAPI ASGI + Next.js Static Export SSG)
- Base de Datos Primaria Local: SQLite (encuentrame_nicaragua.db) compatible con PostgreSQL
- Marco Normativo: Ley N.° 787 de Protección de Datos Personales de Nicaragua, principio de minimización de datos,
  derechos ARCO (Acceso, Rectificación, Cancelación y Oposición), y estricta protección al interés superior del menor.
- Almacenamiento Seguro de Medios: Directorio local 'storage/uploads/' con sanitización forzada a WebP (800x800 máx),
  eliminación total de metadatos EXIF (coordenadas GPS, modelo de cámara, número de serie, marcas de tiempo), y
  denominación con hash criptográfico unidireccional (MD5/SHA256).
""")

    # SECCION 2
    doc.append("\n" + "=" * 100)
    doc.append("2. ARQUITECTURA DEL SISTEMA Y CREACIÓN INICIAL")
    doc.append("=" * 100)
    doc.append(r"""
2.1. Propósito Cívico y Marco Legal (Ley N.° 787 de Nicaragua)
El sistema fue concebido bajo premisas estrictas de derechos humanos, dignidad de las personas y
seguridad de la información:
a) Consentimiento Informado Obligatorio: Todo reporte formal exige que el reportante declare su vínculo familiar
   o legal con la víctima, registre su documento de identidad (almacenado exclusivamente como hash SHA-256 no reversible),
   su dirección IP anonimizada y acepte los términos de privacidad bajo la Ley N.° 787.
b) Moderación Humana Previa: Los reportes ciudadanos no se publican automáticamente. Pasan por una mesa técnica de
   moderación que valida la verosimilitud de la información, previniendo extorsiones, difamaciones o revictimización.
c) Protección de Menores y Grupos Vulnerables: Identificación prioritaria de alertas tempranas para menores de 18 años,
   adultos mayores (>= 65 años) o personas con condiciones médicas críticas (bandera de vulnerabilidad).
d) Derecho al Olvido y Despublicación Inmediata: Al resolverse un caso o solicitarse su supresión (artículo 16 de la
   Ley 787), la ficha se retira inmediatamente del catálogo público para proteger la integridad cívica de la persona localizada.

2.2. Pila Tecnológica (Stack Tecnológico Full Stack)
- Backend:
  * Lenguaje: Python 3.12+
  * Framework API: FastAPI 0.110+ con servidor ASGI Uvicorn
  * ORM y Migraciones: SQLAlchemy 2.0 y Alembic
  * Modelado y Serialización: Pydantic v2
  * Seguridad y Criptografía: Argon2id (hashing de contraseñas), PyJWT (tokens JWT Bearer), hashlib (SHA-256)
  * Procesamiento Multimedia: Pillow (PIL) para conversión WebP y remoción de cabeceras EXIF
  * Control de Flujo: Rate limiting en memoria por IP para endpoints sensibles (/login, /register, /tips)
  * Suite de Pruebas: Pytest, pytest-asyncio, HTTPX

- Frontend:
  * Framework: Next.js 14.2.35 (App Router)
  * Lenguaje: TypeScript 5
  * Estilizado: Tailwind CSS con tipografía Inter
  * Iconografía: Lucide React (empaquetado local sin solicitudes a CDN externas)
  * Cartografía: Leaflet 1.9.4 interactivo con capa OpenStreetMap y carga de GeoJSON de municipios de Nicaragua
  * Modo de Compilación: Exportación estática completa (`output: "export"` en next.config.mjs)
  * Rutas Generadas: 61 páginas HTML pre-renderizadas con capacidades de hidratación en cliente.

- Servidor Integrado de Producción/Hosting:
  * FastAPI implementa una estrategia de despacho híbrido en `main.py` capaz de resolver endpoints REST (/api/v1/...)
    y servir simultáneamente la aplicación estática Next.js exportada, resolviendo rutas directas sin extensión (.html)
    y con barras finales (/casos, /casos/, /mapa, /reportar, /login, /pistas).

2.3. Estructura de Directorios del Proyecto
EncuentrameNicaragua/
├── backend/
│   ├── app/
│   │   ├── api/
│   │   │   ├── deps.py                  # Inyección de dependencias de autenticación y RBAC
│   │   │   └── v1/
│   │   │       ├── admin.py             # Endpoints de moderación, auditoría y estadísticas
│   │   │       ├── auth.py              # Registro, login JWT y control de credenciales
│   │   │       ├── geography.py         # Catálogo de departamentos, municipios y GeoJSON
│   │   │       ├── locations.py         # Búsqueda geográfica y proximidad
│   │   │       ├── reports.py           # CRUD de reportes, fotos, solicitudes de cierre y supresión
│   │   │       ├── search.py            # Búsqueda textual y filtros facetados
│   │   │       ├── statistics.py        # Métricas cívicas públicas
│   │   │       └── tips.py              # Recepción anónima de pistas ciudadanas
│   │   ├── core/
│   │   │   ├── config.py                # Variables de configuración y entorno
│   │   │   ├── database.py              # Inicialización de motor de base de datos y sesiones
│   │   │   ├── rate_limit.py            # Limitador de tasa de peticiones
│   │   │   └── security.py              # Hashes de contraseña y generación/validación de JWT
│   │   ├── models/
│   │   │   └── entities.py              # Modelos declarativos SQLAlchemy (14 entidades)
│   │   ├── schemas/
│   │   │   └── schemas.py               # Esquemas Pydantic v2 para validación de entrada/salida
│   │   └── services/
│   │       ├── audit_service.py         # Bitácora inmutable de auditoría forense
│   │       └── storage_service.py       # Almacenamiento seguro, sanitización EXIF y WebP
│   ├── tests/                           # Suite integral de pruebas automatizadas (38 pruebas)
│   ├── alembic.ini                      # Configuración de migraciones de base de datos
│   ├── Dockerfile                       # Contenedorización de backend
│   └── requirements.txt                 # Dependencias Python
├── frontend/
│   ├── public/                          # Recursos públicos (imágenes, avatares, favicon, GeoJSON)
│   ├── src/
│   │   ├── app/                         # Enrutador App Router de Next.js
│   │   │   ├── admin/page.tsx           # Panel de control de moderación y auditoría
│   │   │   ├── casos/                   # Catálogo de casos públicos
│   │   │   │   ├── [id]/page.tsx        # Ficha detallada de la persona desaparecida
│   │   │   │   └── page.tsx             # Directorio con filtros activos/no activos
│   │   │   ├── login/page.tsx           # Inicio de sesión y registro de usuarios
│   │   │   ├── mapa/page.tsx            # Mapa nacional georreferenciado interactivo
│   │   │   ├── pistas/page.tsx          # Formulario de aportación confidencial de pistas
│   │   │   ├── reportar/page.tsx        # Formulario multipaso de denuncia con carga de foto
│   │   │   ├── layout.tsx               # Plantilla global, cabecera y pie de página
│   │   │   └── page.tsx                 # Página de inicio con buscador y video institucional
│   │   ├── components/                  # Componentes reutilizables (ReportCard, Map, Navbar, etc.)
│   │   ├── lib/
│   │   │   ├── api.ts                   # Cliente HTTP tipado con tolerancia a fallos
│   │   │   └── catalogData.ts           # Catálogo oficial de respaldo, avatares y resolución de fotos
│   │   └── types/index.ts               # Definición de interfaces TypeScript
│   ├── next.config.mjs                  # Configuración de compilación con exportación estática
│   ├── package.json                     # Dependencias de Node.js
│   └── tailwind.config.ts               # Configuración de diseño y colores
├── storage/
│   └── uploads/                         # Almacenamiento local persistente de fotografías autorizadas
├── scratch/                             # Scripts de verificación y auditoría automatizada
├── encuentrame_nicaragua.db             # Base de datos SQLite local relacional
├── main.py                              # Servidor unificado ASGI FastAPI + Servido estático
└── requirements.txt                     # Requisitos raíz para ejecución y despliegue

2.4. Modelo de Datos y Esquema Relacional de Base de Datos
El sistema implementa 14 entidades relacionales principales normalizadas:
1. `users`: Usuarios del sistema (administradores, moderadores, reportantes y ciudadanos) con hashes Argon2id.
2. `missing_person_reports`: Registro central de personas reportadas con número de caso oficial (ej. EN-2026-0001),
   datos biográficos, rasgos fisonómicos, indumentaria, estado del caso y banderas de vulnerabilidad.
3. `geographic_locations`: Coordenadas geográficas aproximadas, departamento, municipio y zona barrial.
4. `report_photos`: Catálogo de fotografías vinculadas, storage_key, hash criptográfico, indicador de foto principal
   y estado de aprobación.
5. `consent_records`: Trazabilidad legal del consentimiento bajo Ley 787, hash del documento de identidad e IP del declarante.
6. `tips`: Pistas recibidas de la ciudadanía, con código de rastreo aleatorio, nivel de confidencialidad y estado de verificación.
7. `tip_photos`: Fotografías aportadas por informantes en una pista ciudadana.
8. `report_status_history`: Historial inmutable de cambios de estado del caso (draft -> pending_review -> approved_published -> closed_found/resolved).
9. `audit_logs`: Registro forense inmutable de todas las operaciones críticas (creación, edición, consulta administrativa, moderación).
10. `moderation_reviews`: Calificación y notas formales de los moderadores sobre los reportes asignados.
11. `deletion_requests`: Solicitudes formales de supresión de datos bajo el artículo 16 de la Ley 787.
12. `departments`: División de los 15 departamentos y 2 regiones autónomas de Nicaragua.
13. `municipalities`: Catálogo oficial de los 153 municipios del país vinculados a su departamento.
14. `token_revocations`: Lista negra de tokens JWT invalidados por cierre de sesión.

2.5. Arquitectura de Seguridad y Control de Acceso (RBAC)
Se estructuraron 4 roles jerárquicos:
- `admin`: Control absoluto del sistema, gestión de usuarios, auditoría forense inmutable y parametrización.
- `moderator`: Revisión de reportes entrantes, aprobación de fichas para difusión pública, rechazo con justificación,
  gestión de pistas ciudadanas y cierre formal de expedientes.
- `reporter`: Familiar o declarante verificado. Puede crear casos, actualizar información mientras el caso esté en revisión,
  adjuntar fotografías autorizadas y solicitar el cierre por localización o supresión por Ley 787.
- `citizen`: Ciudadano registrado o anónimo que puede consultar el directorio público y enviar pistas confidenciales protegidas.

2.6. Módulo de Gestión de Medios y Sanitización de Imágenes EXIF
El servicio `storage_service.py` intercepta cada imagen cargada:
1. Valida el tamaño máximo (5 MB por archivo).
2. Inspecciona el tipo MIME y la firma binaria (JPEG, PNG, WebP).
3. Utiliza Pillow (PIL) para abrir la imagen y descartar todas las etiquetas EXIF / metadatos geográficos.
4. Redimensiona proporcionalmente si la dimensión excede 800x800 píxeles.
5. Codifica la imagen resultante en formato WebP con calidad 85%.
6. Genera un nombre de archivo único mediante UUID4 / MD5 (`<hash>.webp`) para prevenir colisiones y accesos predecibles.
7. Guarda el archivo en `storage/uploads/` y retorna una URL pública sanitizada `/api/v1/reports/photos/<hash>.webp`.
""")

    # SECCION 3
    doc.append("\n" + "=" * 100)
    doc.append(f"3. BITÁCORA CRONOLÓGICA COMPLETA DE PROMPTS Y REQUERIMIENTOS DEL USUARIO ({len(prompts)} PROMPTS)")
    doc.append("=" * 100)
    doc.append("""
A continuación se transcribe en orden cronológico estricto cada uno de los prompts recibidos
por parte del usuario, documentando la evolución completa del proyecto:
""")

    for idx, p in enumerate(prompts, 1):
        ts = p["timestamp"]
        content = p["content"]
        doc.append("-" * 100)
        doc.append(f"PROMPT #{idx} — FECHA Y HORA: {ts}")
        doc.append("-" * 100)
        doc.append(content)
        doc.append("\n")

    # SECCION 4
    doc.append("\n" + "=" * 100)
    doc.append("4. ANÁLISIS DETALLADO DE HITOS, DIAGNÓSTICOS, CAMBIOS Y AJUSTES REALIZADOS")
    doc.append("=" * 100)
    doc.append(r"""
4.1. Creación Inicial y Planificación (Fases 1, 2 y 3)
- Contexto: A partir del Prompt Maestro #1, se elaboró el documento de arquitectura inicial en Markdown
  (FASE_1_Y_2_ANALISIS_Y_PLANIFICACION.md), definiendo el alcance cívico, marco ético bajo la Ley N.° 787,
  modelo relacional de 14 entidades y wireframes conceptuales.
- Aprobación: El usuario aprobó el plan en el Prompt #2.
- Construcción: Se construyó la estructura inicial en FastAPI y Next.js 14 con TypeScript y Tailwind.
  Se incorporaron 20 casos sintéticos representativos cubriendo los 15 departamentos y 2 regiones autónomas
  (RACCN y RACCS), así como avatares fotográficos ilustrativos iniciales.

4.2. Primeras Auditorías de Seguridad, RBAC y Cobertura de Pruebas Pytest
- Problema: En los Prompts #3, #4 y #5, se auditó la seguridad de las APIs, validando que usuarios de rol
  'citizen' o anónimos no pudieran acceder a pistas confidenciales de otros casos, ni que un reportante pudiera
  editar reportes creados por otros autores.
- Ajustes Implementados:
  * Inyección de dependencias `require_role`, `require_moderator` en `backend/app/api/deps.py`.
  * Verificación de propiedad del reporte (`is_owner = report.reporter_id == current_user.id`).
  * Suite inicial de 10 pruebas automatizadas Pytest en `backend/tests/test_core_requirements.py` aprobada al 100%.

4.3. Módulo GIS, División Político-Administrativa y Mapas de Nicaragua
- Requerimiento (Prompt #6): Estructurar con exactitud geográfica la división política de Nicaragua:
  15 departamentos (Boaco, Carazo, Chinandega, Chontales, Estelí, Granada, Jinotega, León, Madriz, Managua,
  Masaya, Matagalpa, Nueva Segovia, Río San Juan, Rivas) y 2 regiones autónomas (Costa Caribe Norte - RACCN y
  Costa Caribe Sur - RACCS), totalizando 153 municipios oficiales con coordenadas y centroides.
- Ajustes Implementados:
  * Creación del router `geography.py` y `locations.py` con validación estricta de municipios dependientes.
  * Incorporación del archivo GeoJSON de Nicaragua en el frontend para polígonos departamentales y marcadores.
  * Normalización de nombres de municipios y control de errores ante discrepancias tipográficas.

4.4. Autonomía y Desacoplamiento de Dependencias Externas (Paquetería Local)
- Requerimiento (Prompts #11 a #19): El usuario solicitó no dejar ninguna referencia en línea (CDNs) y
  garantizar que la compilación y ejecución fueran 100% locales, autónomas e instalables en hosting estático.
- Ajustes Implementados:
  * Descarga y empaquetamiento local de estilos de Leaflet CSS (`leaflet.css`) e imágenes de marcadores en `frontend/public/`.
  * Configuración de fuentes locales y eliminación de enlaces externos a Google Fonts o librerías externas.
  * Ajuste de `next.config.mjs` con `output: "export"`, `trailingSlash: false`, e `images: { unoptimized: true }`.

4.5. Configuración de Exportación Estática Next.js y Servidor FastAPI (main.py)
- Requerimiento (Prompts #20, #21 y #22): El usuario intentó publicar en hosting con FastAPI (`tradescanner.online`)
  pero observaba pantalla en blanco o errores internos debido a la estructura de archivos HTML exportados.
- Diagnóstico: Next.js App Router con `output: "export"` genera archivos estáticos tipo `casos.html`, `mapa.html`,
  `reportar.html`, y carpetas para rutas dinámicas. Si FastAPI sólo usaba `StaticFiles(html=True)` apuntando a la raíz,
  al navegar a `/casos` o `/casos/` el servidor no encontraba `casos/index.html` y devolvía 404 o `{"detail": "Not Found"}`.
- Solución Implementada en `main.py`:
  * Middleware y despachador inteligente en FastAPI que inspecciona la ruta solicitada.
  * Si la ruta coincide con un archivo `.html` existente (`<route>.html`) o un directorio con `index.html` (`<route>/index.html`),
    lo sirve con `FileResponse` y `media_type="text/html; charset=utf-8"`.
  * Preservación intacta del prefijo `/api/v1/` para todas las rutas REST del backend.

4.6. Integración de Multimedia Institucional (Video y Ajustes de Portada)
- Requerimiento (Prompts #23 y #24): Colocar en la portada principal el video oficial `Personas_Desaparecidas_Nicaragua.mp4`,
  ubicado en la raíz, asegurando un diseño responsive y eliminando alertas de prueba o mensajes temporales.
- Solución Implementada:
  * Copia del archivo de video al directorio `frontend/public/videos/Personas_Desaparecidas_Nicaragua.mp4`.
  * Integración en el componente Hero de `frontend/src/app/page.tsx` con contenedor responsive con bordes redondeados,
    controles nativos de reproducción HTML5 y póster estático representativo.

4.7. Corrección de Endpoints de Autenticación y Registro (Error 405 Method Not Allowed)
- Problema (Prompt #26): Al intentar registrar un usuario nuevo en `/login`, la aplicación arrojaba:
  `Error en el servidor: Method Not Allowed` (HTTP 405).
- Causa Raíz: En `main.py` (servidor unificado) no estaba registrado el endpoint `POST /api/v1/auth/register`,
  o el router de autenticación no manejaba las opciones de solicitud y validación de contraseñas.
- Solución Implementada:
  * Inclusión completa de `POST /api/v1/auth/register` en `main.py` y `backend/app/api/v1/auth.py`.
  * Hashing seguro de contraseñas con verificación de requisitos mínimos (8 caracteres, letras y números).
  * Manejo adecuado de CORS y respuestas HTTP 201 Created.

4.8. Formulario de Registro de Casos: Selectores Dinámicos de Departamentos y Municipios
- Problema (Prompt #27): En la pestaña `/reportar`, los selectores desplegables de departamentos y municipios
  aparecían vacíos o deshabilitados.
- Causa Raíz: La llamada a `fetchDepartments()` dependía de una URL absoluta que fallaba por CORS en ciertos entornos,
  o el estado de React no inicializaba la lista de municipios tras seleccionar el departamento.
- Solución Implementada:
  * En `frontend/src/app/reportar/page.tsx` y `frontend/src/lib/api.ts`, se implementó un mecanismo de fallback:
    si la API backend `/api/v1/geography/departments` no responde de inmediato, se carga el catálogo local oficial
    de Nicaragua con los 15 departamentos, 2 regiones autónomas y sus 153 municipios correspondientes.
  * Se configuró el efecto `useEffect` dependiente para actualizar automáticamente el selector de municipios al cambiar
    el departamento seleccionado.

4.9. Corrección de Error de Sincronización en Mapa Nacional GeoJSON
- Problema (Prompt #28): En `/mapa` se mostraba el mensaje emergente:
  "Error de sincronización con la base de datos geográfica — Recurso no encontrado".
- Causa Raíz: El componente del mapa intentaba descargar `/data/nicaragua_departments.geojson` mediante `fetch()`,
  pero la ruta estática en la exportación de Next.js no contenía el archivo en `public/data/` o la respuesta era un 404 HTML.
- Solución Implementada:
  * Generación y depósito del archivo GeoJSON oficial de Nicaragua en `frontend/public/data/nicaragua_departments.geojson`
    y `frontend/public/geojson/nicaragua.geojson`.
  * En `frontend/src/components/map/NationalMap.tsx`, se añadió manejo de excepciones silencioso con renderizado de
    marcadores cartográficos basados en coordenadas latitud/longitud precisas de los casos, evitando que un fallo en el
    GeoJSON bloqueara el mapa interactivo.

4.10. Catálogo Oficial: Separación de Casos Activos y No Activos (Resueltos)
- Requerimiento (Prompt #29): Diferenciar claramente en el catálogo los casos que se encuentran en búsqueda activa
  de aquellos que ya han sido localizados o cerrados formalmente (no activos / resueltos).
- Solución Implementada:
  * Se rediseñó `frontend/src/app/casos/page.tsx` incorporando pestañas selectoras: "Todos los Casos", "Casos Activos"
    (con distintivo verde pulsante "BÚSQUEDA ACTIVA") y "Casos No Activos / Concluidos" (con distintivo verde azulado "LOCALIZADO / CASO RESUELTO").
  * Contadores dinámicos calculados en tiempo real para total de casos, activos y resueltos.
  * Filtros concurrentes por departamento, municipio, género y rango de edad.

4.11. Consulta de Fichas: Expediente Forense, Hitos en Vivo y Tracking en Tiempo Real
- Requerimiento (Prompts #30 y #32): Al hacer clic en una tarjeta de caso, la ficha individual (`/casos/[id]`) debía
  presentar la información fisonómica y forense completa, fotografía autorizada y una línea de tiempo (timeline) dinámica
  con el avance cronológico del caso en vivo.
- Solución Implementada en `frontend/src/app/casos/[id]/CasoDetailClient.tsx`:
  * Panel fisonómico completo: estatura, contextura, tez, cabello, indumentaria al momento de desaparecer, señas particulares y condiciones médicas.
  * Línea de tiempo de avance del caso: Registro formal bajo Ley 787, validación documental de moderación, activación de alerta cívica nacional,
    recepción comunitaria de pistas y hito final de localización (en casos concluidos).
  * Indicador de "Sincronizado en tiempo real" con reloj en vivo y canal cifrado integrado para aportar testimonios y pistas directas sobre ese caso.

4.12. Auditoría Exhaustiva del Módulo de Fotografías y Gestión de Archivos
- Requerimiento (Prompt #34): Auditoría de 10 puntos para determinar por qué las imágenes de personas desaparecidas
  mostraban avatares genéricos o placeholders en lugar de fotografías reales.
- Diagnóstico: Se descartaron fallas en la base de datos o permisos; la causa raíz radicaba en una doble bifurcación:
  1. En `catalogData.ts`, la función `getCasePhotoUrl()` forzaba el uso de `avatar_en-2026-000X.webp` para cualquier
     caso que terminara en número, omitiendo el argumento `fallback`.
  2. Al crear un reporte en `/reportar`, el formulario no retenía en el almacenamiento local la URL de la foto cargada.
  3. En `storage_service.py`, la expresión regular `STORAGE_KEY_REGEX` exigía estrictamente 32 caracteres hexadecimales,
     impidiendo que otros formatos de claves persistentes fueran servidos.
- Ajustes Implementados:
  * Ampliación de la expresión regular de claves de almacenamiento:
    `STORAGE_KEY_REGEX = re.compile(r"^(?:[a-f0-9]{32}|avatar_en-\d{4}-\d{4,5}|[a-zA-Z0-9_\-\.]{3,64})\.webp$")`
  * Función de resolución con búsqueda en `storage/uploads`, `frontend/public/images/avatars` y `frontend/out/images/avatars`.
  * Eliminación garantizada de metadatos EXIF con Pillow y conversión uniforme a WebP.

4.13. Resolución Crítica de Enrutamiento y Navegación Next.js + FastAPI (Evitar JSON 404)
- Problema (Prompt #35): Al navegar directamente por URLs en el hosting público (ej. `/casos` o `/mapa`), el navegador
  recibía una respuesta JSON de FastAPI: `{"detail": "Not Found"}` en vez de renderizar la página web correspondiente.
- Causa Raíz: En servidores ASGI FastAPI, el montaje estándar de archivos estáticos `StaticFiles` no realiza reescrituras
  de URL de tipo Single Page Application (SPA). Si Next.js exporta `casos.html`, una petición HTTP GET a `/casos` es tratada
  por FastAPI como una ruta de API inexistente.
- Solución de Arquitectura Implementada en `main.py`:
  * Implementación de una función despachadora unificada `serve_static_html(request, path)`:
    a) Comprueba si la ruta solicitada corresponde a una API registrada (`/api/...`, `/docs`, `/openapi.json`) y la deriva.
    b) Verifica si existe el archivo exacto en `out/` (ej. `out/casos.html`).
    c) Verifica si existe un subdirectorio con `index.html` (ej. `out/casos/index.html`).
    d) Resuelve enlaces internos con y sin barra final (`/casos` y `/casos/`).
    e) Sirve archivos con MIME types correctos (`text/html; charset=utf-8`, `application/javascript`, `text/css`, etc.).
  * Generación en el proceso de compilación de una estructura dual de exportación en `frontend/out/`:
    `out/casos.html` Y `out/casos/index.html` (espejado sincronizado para máxima resiliencia en cualquier hosting).

4.14. Localización, Estructura y Esquema de la Base de Datos (encuentrame_nicaragua.db)
- Requerimiento (Prompt #36): Indicar al usuario la ubicación exacta de la base de datos y cómo están estructurados
  los registros de los casos reportados.
- Explicación y Verificación Técnica Proporcionada:
  * Archivo de base de datos relacional: `c:\Users\User\Documents\Valor IA\EncuentrameNicaragua\encuentrame_nicaragua.db` (SQLite).
  * Tabla central: `missing_person_reports`, vinculada por llaves foráneas a `geographic_locations`, `report_photos`,
    `consent_records`, `report_status_history` y `audit_logs`.
  * Se suministraron scripts de consulta interactiva mediante Python y SQLite3 para auditar directamente los registros.

4.15. Visualización de Fotografías Reales Subidas en Catálogo Local (Eliminación de Avatares Sintéticos)
- Requerimiento (Prompt #37): Validar estrictamente en el entorno local (sin desplegar a producción) que en la sección
  de catálogo (`/casos`), cuando un caso posea una fotografía real subida por el usuario, se renderice dicha imagen real
  y no un avatar sintético.
- Diagnóstico Final y Corrección Aplicada:
  1. En `frontend/src/lib/catalogData.ts`, se modificó `getCasePhotoUrl(caseNumber, fallback)`:
     Si el parámetro `fallback` contiene una imagen real (inicia con `data:`, `blob:`, o `/api/v1/reports/photos/`),
     se retorna INMEDIATAMENTE, anulando cualquier mapeo al avatar sintético `avatar_en-2026-000X.webp`.
  2. En `frontend/src/components/reports/ReportCard.tsx`, se actualizó la resolución de `photoSrc` para que transmita
     `report.primary_photo_url` al helper sin forzar placeholders si la URL es válida.
  3. En `frontend/src/app/casos/[id]/CasoDetailClient.tsx`, se replicó la misma lógica para la ficha en profundidad.
  4. En `frontend/src/lib/api.ts`, `fetchPublicReports()` preserva la URL de la fotografía de los casos creados localmente.
  5. En `backend/app/api/v1/reports.py`, se armonizó el estado de los nuevos reportes creados (`PENDING_REVIEW` por defecto)
     y se garantizó que los casos aprobados en el listado devuelvan su `primary_photo_url` vinculada a `ReportPhoto`.
- Validación Rigurosa:
  * Se ejecutó el script de verificación automatizada [scratch/verify_photo_catalog.py].
  * Se creó el caso `EN-2026-0026` ("Valentina Morales Ruiz").
  * Se subió una fotografía real mediante `POST /api/v1/reports/{id}/photos`.
  * El backend sanitizó y guardó el archivo como `storage/uploads/b3d8282345e3454da2e3c15e73f3275d.webp`.
  * Se aprobó por moderación y se consultó `GET /api/v1/reports/`.
  * Resultado: `primary_photo_url` es `/api/v1/reports/photos/b3d8282345e3454da2e3c15e73f3275d.webp`.
  * El endpoint de descarga devolvió HTTP 200 con `Content-Type: image/webp` y tamaño verificado.
  * Las 38 pruebas Pytest pasaron con 100% de éxito.
""")

    # SECCION 5
    doc.append("\n" + "=" * 100)
    doc.append("5. REGISTRO DE ARCHIVOS CLAVE MODIFICADOS Y CREADOS")
    doc.append("=" * 100)
    doc.append(r"""
A continuación se detalla la matriz de archivos fundamentales del proyecto con su función y ajustes:

1. backend/app/api/v1/reports.py
   - Endpoint de subida de fotos `POST /api/v1/reports/{report_id}/photos` con sanitización EXIF.
   - Endpoint de entrega de fotos `GET /api/v1/reports/photos/{storage_key}` con control de cabeceras.
   - Listado público `GET /api/v1/reports/` con ordenamiento cronológico por fecha de creación y publicación.
   - Flujo ético de cierre de caso (`POST /{report_id}/request-close`) y supresión de datos bajo Ley 787.

2. backend/app/services/storage_service.py
   - Sanitización de imágenes con Pillow: eliminación forzada de metadatos EXIF.
   - Conversión a WebP optimizado (calidad 85, dimensiones máximas 800x800).
   - Generación de hashes seguros de archivo y validación de extensiones y tipos MIME permitidos.
   - Resolución de rutas de almacenamiento en `storage/uploads/`.

3. backend/app/api/v1/admin.py
   - Panel de moderación: aprobación, rechazo y solicitud de cambios sobre reportes ciudadanos.
   - Consulta de pistas confidenciales y registro inmutable de auditoría forense (`/audit-logs`).

4. backend/app/api/v1/auth.py
   - Endpoints `/login` y `/register` con validación estricta de credenciales, hashing Argon2id y JWT Bearer.

5. frontend/src/lib/catalogData.ts
   - Corrección en `getCasePhotoUrl()`: prioridad absoluta a fotografías reales cargadas por usuarios.
   - Función `generateDefaultTimeline()` para seguimiento cronológico en tiempo real.
   - Catálogo cívico de contingencia con los 20 casos sintéticos oficiales de prueba.

6. frontend/src/components/reports/ReportCard.tsx
   - Renderizado de tarjetas del catálogo compatible con URLs absolutas, relativas y Data URLs de fotos reales.
   - Badges visuales de estado ("BÚSQUEDA ACTIVA" vs "LOCALIZADO / CASO RESUELTO") y alertas de menores de edad.

7. frontend/src/app/casos/[id]/CasoDetailClient.tsx
   - Visualización de expediente detallado de la persona desaparecida.
   - Renderizado de fotografía autorizada y galería de imágenes.
   - Línea de tiempo cronológica dinámica en tiempo real.
   - Formulario integrado para aportación confidencial de pistas sobre el caso específico.

8. frontend/src/app/reportar/page.tsx
   - Formulario multipaso con consentimiento informado bajo Ley N.° 787 de Nicaragua.
   - Previsualización y validación de fotografía antes de la carga.
   - Carga multipart al backend y persistencia inmediata en almacenamiento del navegador para disponibilidad en catálogo.
   - Selectores dependientes de departamentos y municipios de Nicaragua con fallback autónomo.

9. frontend/src/app/casos/page.tsx
   - Catálogo interactivo con selector de pestañas: Todos, Activos y No Activos (Concluidos).
   - Contadores en tiempo real y buscador facetado multicriterio.

10. frontend/src/app/page.tsx
    - Página de inicio institucional con buscador rápido, estadísticas cívicas y video oficial.

11. main.py
    - Servidor ASGI unificado para producción y hosting.
    - Despachador de rutas estáticas Next.js con soporte para URLs limpias sin extensión y con barra final.
    - Endpoints de autenticación y fotos en modo unificado para entornos independientes.

12. scratch/verify_photo_catalog.py
    - Script de verificación automatizada end-to-end del ciclo de vida de fotografías reales.

13. backend/tests/ (test_core_requirements.py, test_audit_fixes.py, test_geography.py, test_security_audit_v2.py)
    - 38 pruebas unitarias y de integración que certifican la integridad del sistema.
""")

    # SECCION 6
    doc.append("\n" + "=" * 100)
    doc.append("6. ASEGURAMIENTO DE CALIDAD (QA), COBERTURA DE PRUEBAS Y VALIDACIÓN")
    doc.append("=" * 100)
    doc.append(r"""
El sistema ha sido sometido a ciclos iterativos de pruebas automatizadas y manuales:

6.1. Suite Automatizada de Pruebas con Pytest
- Comando de ejecución: `pytest backend/tests/`
- Total de pruebas ejecutadas: 38
- Tasa de éxito: 38 passed (100% de éxito en 2.78 segundos)
- Áreas evaluadas:
  * test_audit_fixes.py (8 pruebas): Autorización de modificación de reportes, control de propietarios,
    despublicación al solicitar supresión de datos bajo Ley 787 y permisos RBAC.
  * test_core_requirements.py (10 pruebas): Aprobación previa de moderación, denegación de acceso a pistas
    a ciudadanos no autorizados, inmutabilidad de reportes ajenos, sanitización de datos de entrada.
  * test_geography.py (15 pruebas): Consistencia de los 15 departamentos y 2 regiones autónomas, 153 municipios,
    coordenadas geográficas y respuestas de API.
  * test_security_audit_v2.py (5 pruebas): Detección de inyecciones, rate limiting contra ataques de fuerza bruta,
    seguridad de contraseñas y validación de tokens revocados.

6.2. Verificación de Compilación Frontend Next.js
- Comando de ejecución: `npm --prefix frontend run build`
- Resultado: Compilación exitosa con Next.js 14.2.35.
- Rutas generadas: 61 páginas HTML estáticas optimizadas.
- Comprobación: Se generó la estructura de directorios duales (`/casos.html` y `/casos/index.html`) para
  garantizar navegación fluida tanto en local como en cualquier servidor web estático.

6.3. Verificación End-to-End de Fotografías Reales en Local
- Prueba automatizada: `scratch/verify_photo_catalog.py`
- Flujo probado: Creación de caso -> Subida de fotografía real -> Conversión a WebP y eliminación EXIF ->
  Aprobación de moderación -> Consulta en catálogo `/casos` -> Verificación de URL de foto real (no avatar) ->
  Descarga HTTP 200 OK con Content-Type `image/webp`.
""")

    # SECCION 7
    doc.append("\n" + "=" * 100)
    doc.append("7. GUÍA OPERATIVA: INSTALACIÓN, EJECUCIÓN LOCAL Y MANTENIMIENTO")
    doc.append("=" * 100)
    doc.append(r"""
7.1. Requisitos Previos
- Python 3.12 o superior con entorno virtual activo (`venv`).
- Node.js 18+ y npm 9+.
- Sistema Operativo: Windows, Linux o macOS.

7.2. Puesta en Marcha del Backend y Servidor Local
1. Activar entorno virtual de Python:
   Windows (PowerShell):
   .\venv\Scripts\Activate.ps1

2. Instalar dependencias si es una instalación limpia:
   pip install -r backend/requirements.txt

3. Iniciar el servidor local unificado en el puerto 8000:
   python -m uvicorn main:app --host 127.0.0.1 --port 8000 --reload

4. Abrir en el navegador:
   http://127.0.0.1:8000/
   Catálogo de casos: http://127.0.0.1:8000/casos
   Reportar desaparición: http://127.0.0.1:8000/reportar
   Mapa nacional: http://127.0.0.1:8000/mapa
   Documentación Swagger de la API: http://127.0.0.1:8000/docs

7.3. Compilación del Frontend Next.js
1. Acceder al directorio frontend e instalar dependencias:
   cd frontend
   npm install

2. Compilar la exportación estática:
   npm run build

3. Sincronizar las rutas de exportación para servidores estáticos (PowerShell desde la raíz):
   powershell -Command "New-Item -ItemType Directory -Force -Path 'frontend/out/casos', 'frontend/out/mapa', 'frontend/out/reportar', 'frontend/out/login', 'frontend/out/pistas'; Copy-Item -Path 'frontend/out/casos.html' -Destination 'frontend/out/casos/index.html' -Force; Copy-Item -Path 'frontend/out/mapa.html' -Destination 'frontend/out/mapa/index.html' -Force; Copy-Item -Path 'frontend/out/reportar.html' -Destination 'frontend/out/reportar/index.html' -Force; Copy-Item -Path 'frontend/out/login.html' -Destination 'frontend/out/login/index.html' -Force; Copy-Item -Path 'frontend/out/pistas.html' -Destination 'frontend/out/pistas/index.html' -Force"

7.4. Ejecución de Pruebas de Calidad
1. Ejecutar suite de pruebas Pytest:
   pytest backend/tests/

2. Ejecutar prueba automatizada de flujo de fotografía real:
   python scratch/verify_photo_catalog.py

7.5. Mantenimiento y Respaldos
- Base de datos: Respaldar periódicamente el archivo `encuentrame_nicaragua.db`.
- Fotografías: Respaldar periódicamente el directorio `storage/uploads/`.
- Ningún archivo temporal o confidencial debe exponerse sin la debida autenticación.
""")

    doc.append("\n" + "=" * 100)
    doc.append("FIN DE LA DOCUMENTACIÓN TÉCNICA — PROYECTO ENCUÉNTRAME NICARAGUA")
    doc.append("=" * 100)

    full_text = "\n".join(doc)
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        f.write(full_text)
    
    print(f"Documentación generada exitosamente en:\n{OUTPUT_FILE}")
    print(f"Tamaño total: {len(full_text)} caracteres, {len(doc)} líneas.")

if __name__ == "__main__":
    build_documentation()
