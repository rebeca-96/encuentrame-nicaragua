import os

DIAG_DIR = r"C:\Users\User\Documents\Valor IA\EncuentrameNicaragua\ENTREGA_FINAL_ACADEMICA\Diagramas"

def create_diagrams():
    # 1. DIAGRAMA_ARQUITECTURA_GENERAL.svg
    arch_svg = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1200 800" width="100%" height="100%">
  <defs>
    <style>
      .bg { fill: #0B192C; }
      .title { font-family: 'Segoe UI', Inter, sans-serif; font-size: 22px; font-weight: bold; fill: #FFFFFF; }
      .subtitle { font-family: 'Segoe UI', Inter, sans-serif; font-size: 13px; fill: #94A3B8; }
      .layer-title { font-family: 'Segoe UI', Inter, sans-serif; font-size: 12px; font-weight: bold; fill: #38BDF8; letter-spacing: 1px; }
      .box-user { fill: #1E293B; stroke: #38BDF8; stroke-width: 1.5; rx: 8; }
      .box-edge { fill: #1E293B; stroke: #F59E0B; stroke-width: 1.5; rx: 8; }
      .box-fe { fill: #1E293B; stroke: #0D9488; stroke-width: 1.5; rx: 8; }
      .box-be { fill: #1E293B; stroke: #10B981; stroke-width: 1.5; rx: 8; }
      .box-db { fill: #1E293B; stroke: #EC4899; stroke-width: 1.5; rx: 8; }
      .node-text-title { font-family: 'Segoe UI', Inter, sans-serif; font-size: 13px; font-weight: bold; fill: #FFFFFF; text-anchor: middle; }
      .node-text-sub { font-family: 'Segoe UI', Inter, sans-serif; font-size: 10.5px; fill: #CBD5E1; text-anchor: middle; }
      .node-text-code { font-family: monospace; font-size: 9.5px; fill: #94A3B8; text-anchor: middle; }
      .line { stroke: #475569; stroke-width: 1.5; stroke-dasharray: 4,4; }
      .line-solid { stroke: #0D9488; stroke-width: 2; }
    </style>
    <marker id="arrow" viewBox="0 0 10 10" refX="6" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
      <path d="M 0 1 L 10 5 L 0 9 z" fill="#0D9488" />
    </marker>
  </defs>

  <!-- Background -->
  <rect width="1200" height="800" class="bg" />

  <!-- Header -->
  <text x="50" y="50" class="title">DIAGRAMA DE ARQUITECTURA GENERAL DEL SISTEMA (C4 CONTAINERS)</text>
  <text x="50" y="75" class="subtitle">ENCUÉNTRAME NICARAGUA — Arquitectura Desacoplada en Tres Capas con Mecanismo de Resiliencia Estática</text>

  <!-- CAPA 1: ACTORES Y CLIENTES (Y: 110) -->
  <text x="50" y="115" class="layer-title">CAPA DE CLIENTES Y USUARIOS (DISPOSITIVOS MULTIPLATAFORMA)</text>
  <g transform="translate(50, 130)">
    <rect x="0" y="0" width="240" height="70" class="box-user" />
    <text x="120" y="30" class="node-text-title">Ciudadano / Testigo</text>
    <text x="120" y="50" class="node-text-sub">Buscador, Mapa, Pistas Confidenciales</text>
  </g>
  <g transform="translate(340, 130)">
    <rect x="0" y="0" width="240" height="70" class="box-user" />
    <text x="120" y="30" class="node-text-title">Familiar / Reportante</text>
    <text x="120" y="50" class="node-text-sub">Wizard 4 Pasos, Consentimiento Ley 787</text>
  </g>
  <g transform="translate(630, 130)">
    <rect x="0" y="0" width="240" height="70" class="box-user" />
    <text x="120" y="30" class="node-text-title">Moderador Cívico</text>
    <text x="120" y="50" class="node-text-sub">Control de Calidad, Triage de Pistas</text>
  </g>
  <g transform="translate(910, 130)">
    <rect x="0" y="0" width="240" height="70" class="box-user" />
    <text x="120" y="30" class="node-text-title">Administrador General</text>
    <text x="120" y="50" class="node-text-sub">RBAC, Métricas, Logs Forenses</text>
  </g>

  <!-- LÍNEAS HACIA EDGE/CDN -->
  <line x1="600" y1="200" x2="600" y2="250" class="line-solid" marker-end="url(#arrow)" />

  <!-- CAPA 2: EDGE / CDN / SEGURIDAD (Y: 250) -->
  <text x="50" y="245" class="layer-title">CAPA PERIMETRAL: CDN, SSL Y PROXY REVERSO</text>
  <g transform="translate(50, 260)">
    <rect x="0" y="0" width="1100" height="60" class="box-edge" />
    <text x="550" y="28" class="node-text-title">Cloudflare Edge &amp; SSL/TLS Termination</text>
    <text x="550" y="46" class="node-text-sub">HTTPS (TLS 1.3), Protección DDoS, Caché HTTP de Activos Estáticos y Compresión Gzip/Brotli</text>
  </g>

  <!-- LÍNEA HACIA FRONTEND -->
  <line x1="600" y1="320" x2="600" y2="370" class="line-solid" marker-end="url(#arrow)" />

  <!-- CAPA 3: FRONTEND NEXT.JS (Y: 370) -->
  <text x="50" y="365" class="layer-title">CAPA FRONTEND: PRESENTACIÓN Y ENRUTAMIENTO ESTÁTICO (NEXT.JS 14 / REACT 18)</text>
  <g transform="translate(50, 380)">
    <rect x="0" y="0" width="340" height="120" class="box-fe" />
    <text x="170" y="30" class="node-text-title">Vistas Públicas (SSG Export)</text>
    <text x="170" y="52" class="node-text-sub">Inicio, Catálogo, Fichas de Casos</text>
    <text x="170" y="70" class="node-text-sub">Rutas Canónicas Duales (*.html)</text>
    <text x="170" y="95" class="node-text-code">Tailwind CSS 3.4 / Lucide React</text>
  </g>
  <g transform="translate(430, 380)">
    <rect x="0" y="0" width="340" height="120" class="box-fe" />
    <text x="170" y="30" class="node-text-title">Módulos Dinámicos y Mapas</text>
    <text x="170" y="52" class="node-text-sub">Leaflet 1.9.4 / OpenStreetMap Tiles</text>
    <text x="170" y="70" class="node-text-sub">Wizard de Reporte y Subida de Fotos</text>
    <text x="170" y="95" class="node-text-code">HTML5 Geolocation / Canvas Preview</text>
  </g>
  <g transform="translate(810, 380)">
    <rect x="0" y="0" width="340" height="120" class="box-fe" />
    <text x="170" y="30" class="node-text-title">Cliente API Resiliente (api.ts)</text>
    <text x="170" y="52" class="node-text-sub">Mecanismo Fallback Local Integrado</text>
    <text x="170" y="70" class="node-text-sub">Gestión de Sesión JWT en localStorage</text>
    <text x="170" y="95" class="node-text-code">Fetch API / Deduplicación de Requests</text>
  </g>

  <!-- LÍNEA HACIA BACKEND -->
  <line x1="600" y1="500" x2="600" y2="550" class="line-solid" marker-end="url(#arrow)" />

  <!-- CAPA 4: BACKEND FASTAPI (Y: 550) -->
  <text x="50" y="545" class="layer-title">CAPA BACKEND: SERVICIOS REST Y PROCESAMIENTO MULTIMEDIA (FASTAPI / PYTHON 3.12)</text>
  <g transform="translate(50, 560)">
    <rect x="0" y="0" width="260" height="110" class="box-be" />
    <text x="130" y="25" class="node-text-title">Servicios de Dominio</text>
    <text x="130" y="45" class="node-text-sub">/reports, /tips, /locations</text>
    <text x="130" y="65" class="node-text-sub">Validación Pydantic v2</text>
    <text x="130" y="88" class="node-text-code">Cálculo de Estadísticas y Filtros</text>
  </g>
  <g transform="translate(330, 560)">
    <rect x="0" y="0" width="260" height="110" class="box-be" />
    <text x="130" y="25" class="node-text-title">Seguridad y Criptografía</text>
    <text x="130" y="45" class="node-text-sub">Argon2id (argon2-cffi)</text>
    <text x="130" y="65" class="node-text-sub">JWT HS256 Token Handling</text>
    <text x="130" y="88" class="node-text-code">Control RBAC en Dependencies</text>
  </g>
  <g transform="translate(610, 560)">
    <rect x="0" y="0" width="260" height="110" class="box-be" />
    <text x="130" y="25" class="node-text-title">Pipeline Multimedia</text>
    <text x="130" y="45" class="node-text-sub">Pillow (PIL) Image Processing</text>
    <text x="130" y="65" class="node-text-sub">Sanitización Forzosa de EXIF</text>
    <text x="130" y="88" class="node-text-code">Compresión WebP / Hash SHA-256</text>
  </g>
  <g transform="translate(890, 560)">
    <rect x="0" y="0" width="260" height="110" class="box-be" />
    <text x="130" y="25" class="node-text-title">Asistencia Supervisada</text>
    <text x="130" y="45" class="node-text-sub">Heurística de Similitud (Jaccard)</text>
    <text x="130" y="65" class="node-text-sub">Detección de Duplicados</text>
    <text x="130" y="88" class="node-text-code">ai_service.py (Sin llamadas a LLMs)</text>
  </g>

  <!-- LÍNEA HACIA PERSISTENCIA -->
  <line x1="600" y1="670" x2="600" y2="710" class="line-solid" marker-end="url(#arrow)" />

  <!-- CAPA 5: PERSISTENCIA (Y: 710) -->
  <text x="50" y="705" class="layer-title">CAPA DE PERSISTENCIA Y ALMACENAMIENTO DE ARCHIVOS</text>
  <g transform="translate(50, 720)">
    <rect x="0" y="0" width="530" height="60" class="box-db" />
    <text x="265" y="25" class="node-text-title">Motor Relacional SQLite (SQLAlchemy 2.0 ORM)</text>
    <text x="265" y="45" class="node-text-sub">16 Tablas: users, reports, photos, tips, consent_records, audit_logs, locations, etc.</text>
  </g>
  <g transform="translate(620, 720)">
    <rect x="0" y="0" width="530" height="60" class="box-db" />
    <text x="265" y="25" class="node-text-title">Almacenamiento Local de Archivos / Assets WebP</text>
    <text x="265" y="45" class="node-text-sub">storage/uploads/ (25 avatares WebP sanitizados + Personas_Desaparecidas_Nicaragua.mp4)</text>
  </g>
</svg>"""
    with open(os.path.join(DIAG_DIR, "DIAGRAMA_ARQUITECTURA_GENERAL.svg"), "w", encoding="utf-8") as f:
        f.write(arch_svg.strip())
    print("Generado: DIAGRAMA_ARQUITECTURA_GENERAL.svg")

    # 2. DIAGRAMA_ENTIDAD_RELACION.svg
    der_svg = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1200 850" width="100%" height="100%">
  <defs>
    <style>
      .bg { fill: #0B192C; }
      .title { font-family: 'Segoe UI', Inter, sans-serif; font-size: 22px; font-weight: bold; fill: #FFFFFF; }
      .subtitle { font-family: 'Segoe UI', Inter, sans-serif; font-size: 13px; fill: #94A3B8; }
      .entity-box { fill: #1E293B; stroke: #334155; stroke-width: 1.5; rx: 6; }
      .entity-header { fill: #0F2A4A; rx: 4; }
      .entity-name { font-family: 'Segoe UI', Inter, sans-serif; font-size: 13px; font-weight: bold; fill: #14B8A6; }
      .attr-pk { font-family: monospace; font-size: 10px; font-weight: bold; fill: #F59E0B; }
      .attr-fk { font-family: monospace; font-size: 10px; font-weight: bold; fill: #38BDF8; }
      .attr-reg { font-family: monospace; font-size: 10px; fill: #CBD5E1; }
      .rel-line { stroke: #14B8A6; stroke-width: 1.5; stroke-dasharray: 3,3; }
    </style>
  </defs>

  <rect width="1200" height="850" class="bg" />
  <text x="50" y="45" class="title">DIAGRAMA ENTIDAD - RELACIÓN (MODELO FÍSICO DE BASE DE DATOS)</text>
  <text x="50" y="70" class="subtitle">ENCUÉNTRAME NICARAGUA — 16 Tablas Relacionales, Integridad Referencial y Trazabilidad Forense</text>

  <!-- TABLA 1: users -->
  <g transform="translate(50, 100)">
    <rect width="250" height="190" class="entity-box" />
    <rect width="250" height="28" class="entity-header" />
    <text x="15" y="19" class="entity-name">users (17 registros)</text>
    <text x="15" y="48" class="attr-pk">PK id : VARCHAR(36)</text>
    <text x="15" y="68" class="attr-reg">email : VARCHAR(255) [UQ]</text>
    <text x="15" y="88" class="attr-reg">password_hash : VARCHAR(255)</text>
    <text x="15" y="108" class="attr-reg">full_name : VARCHAR(255)</text>
    <text x="15" y="128" class="attr-reg">role : ENUM(admin, mod, rep, cit)</text>
    <text x="15" y="148" class="attr-reg">is_active : BOOLEAN</text>
    <text x="15" y="168" class="attr-reg">created_at : DATETIME</text>
  </g>

  <!-- TABLA 2: missing_person_reports (CENTRAL) -->
  <g transform="translate(360, 100)">
    <rect width="320" height="360" class="entity-box" />
    <rect width="320" height="28" class="entity-header" />
    <text x="15" y="19" class="entity-name">missing_person_reports (26 registros)</text>
    <text x="15" y="48" class="attr-pk">PK id : VARCHAR(36)</text>
    <text x="15" y="68" class="attr-reg">case_number : VARCHAR(32) [UQ]</text>
    <text x="15" y="88" class="attr-fk">FK reporter_id : VARCHAR(36) -> users</text>
    <text x="15" y="108" class="attr-fk">FK location_id : VARCHAR(36) -> geoloc</text>
    <text x="15" y="128" class="attr-reg">status : ENUM(draft, pending, approved...)</text>
    <text x="15" y="148" class="attr-reg">first_name : VARCHAR(100)</text>
    <text x="15" y="168" class="attr-reg">last_name : VARCHAR(100)</text>
    <text x="15" y="188" class="attr-reg">age_at_disappearance : INT</text>
    <text x="15" y="208" class="attr-reg">gender : ENUM(male, female, other)</text>
    <text x="15" y="228" class="attr-reg">disappearance_date : DATETIME</text>
    <text x="15" y="248" class="attr-reg">physical_description : TEXT</text>
    <text x="15" y="268" class="attr-reg">clothing_description : TEXT</text>
    <text x="15" y="288" class="attr-reg">is_minor : BOOLEAN</text>
    <text x="15" y="308" class="attr-reg">vulnerability_flag : BOOLEAN</text>
    <text x="15" y="328" class="attr-reg">is_public : BOOLEAN</text>
    <text x="15" y="348" class="attr-reg">created_at, updated_at : DATETIME</text>
  </g>

  <!-- TABLA 3: geographic_locations -->
  <g transform="translate(740, 100)">
    <rect width="240" height="150" class="entity-box" />
    <rect width="240" height="28" class="entity-header" />
    <text x="15" y="19" class="entity-name">geographic_locations (29)</text>
    <text x="15" y="48" class="attr-pk">PK id : VARCHAR(36)</text>
    <text x="15" y="68" class="attr-reg">department : VARCHAR(100)</text>
    <text x="15" y="88" class="attr-reg">municipality : VARCHAR(100)</text>
    <text x="15" y="108" class="attr-reg">approximate_lat : FLOAT</text>
    <text x="15" y="128" class="attr-reg">approximate_lng : FLOAT</text>
  </g>

  <!-- TABLA 4: report_photos -->
  <g transform="translate(740, 290)">
    <rect width="240" height="170" class="entity-box" />
    <rect width="240" height="28" class="entity-header" />
    <text x="15" y="19" class="entity-name">report_photos (25)</text>
    <text x="15" y="48" class="attr-pk">PK id : VARCHAR(36)</text>
    <text x="15" y="68" class="attr-fk">FK report_id : VARCHAR(36) -> reports</text>
    <text x="15" y="88" class="attr-reg">storage_key : VARCHAR(255)</text>
    <text x="15" y="108" class="attr-reg">is_primary : BOOLEAN</text>
    <text x="15" y="128" class="attr-reg">is_approved : BOOLEAN</text>
    <text x="15" y="148" class="attr-reg">file_hash_sha256 : VARCHAR(64)</text>
  </g>

  <!-- TABLA 5: confidential_tips -->
  <g transform="translate(50, 330)">
    <rect width="250" height="180" class="entity-box" />
    <rect width="250" height="28" class="entity-header" />
    <text x="15" y="19" class="entity-name">confidential_tips (5)</text>
    <text x="15" y="48" class="attr-pk">PK id : VARCHAR(36)</text>
    <text x="15" y="68" class="attr-fk">FK report_id : VARCHAR(36) -> reports</text>
    <text x="15" y="88" class="attr-reg">tip_code : VARCHAR(32)</text>
    <text x="15" y="108" class="attr-reg">description : TEXT</text>
    <text x="15" y="128" class="attr-reg">sighting_date : DATETIME</text>
    <text x="15" y="148" class="attr-reg">is_anonymous : BOOLEAN</text>
    <text x="15" y="168" class="attr-reg">status : VARCHAR(32)</text>
  </g>

  <!-- TABLA 6: consent_records (LEY 787) -->
  <g transform="translate(50, 550)">
    <rect width="250" height="130" class="entity-box" />
    <rect width="250" height="28" class="entity-header" />
    <text x="15" y="19" class="entity-name">consent_records (26)</text>
    <text x="15" y="48" class="attr-pk">PK id : VARCHAR(36)</text>
    <text x="15" y="68" class="attr-fk">FK report_id : VARCHAR(36) -> reports</text>
    <text x="15" y="88" class="attr-reg">declared_relationship : VARCHAR(100)</text>
    <text x="15" y="108" class="attr-reg">signed_at : DATETIME</text>
  </g>

  <!-- TABLA 7: report_status_history -->
  <g transform="translate(360, 500)">
    <rect width="320" height="140" class="entity-box" />
    <rect width="320" height="28" class="entity-header" />
    <text x="15" y="19" class="entity-name">report_status_history (27)</text>
    <text x="15" y="48" class="attr-pk">PK id : VARCHAR(36)</text>
    <text x="15" y="68" class="attr-fk">FK report_id : VARCHAR(36) -> reports</text>
    <text x="15" y="88" class="attr-reg">previous_status : VARCHAR(50)</text>
    <text x="15" y="108" class="attr-reg">new_status : VARCHAR(50)</text>
    <text x="15" y="128" class="attr-reg">created_at : DATETIME</text>
  </g>

  <!-- TABLA 8: moderation_reviews -->
  <g transform="translate(740, 500)">
    <rect width="240" height="130" class="entity-box" />
    <rect width="240" height="28" class="entity-header" />
    <text x="15" y="19" class="entity-name">moderation_reviews (18)</text>
    <text x="15" y="48" class="attr-pk">PK id : VARCHAR(36)</text>
    <text x="15" y="68" class="attr-fk">FK report_id : VARCHAR(36) -> reports</text>
    <text x="15" y="88" class="attr-reg">decision : VARCHAR(50)</text>
    <text x="15" y="108" class="attr-reg">reviewed_at : DATETIME</text>
  </g>

  <!-- TABLA 9: audit_logs -->
  <g transform="translate(360, 680)">
    <rect width="320" height="130" class="entity-box" />
    <rect width="320" height="28" class="entity-header" />
    <text x="15" y="19" class="entity-name">audit_logs (46 registros)</text>
    <text x="15" y="48" class="attr-pk">PK id : VARCHAR(36)</text>
    <text x="15" y="68" class="attr-reg">action : VARCHAR(100)</text>
    <text x="15" y="88" class="attr-reg">entity_name : VARCHAR(100)</text>
    <text x="15" y="108" class="attr-reg">ip_address : VARCHAR(45) | created_at</text>
  </g>

  <!-- TABLAS GEOGRAFICAS -->
  <g transform="translate(740, 660)">
    <rect width="240" height="70" class="entity-box" />
    <rect width="240" height="24" class="entity-header" />
    <text x="15" y="16" class="entity-name">departments (17)</text>
    <text x="15" y="42" class="attr-pk">PK id | name | code</text>
  </g>
  <g transform="translate(740, 750)">
    <rect width="240" height="70" class="entity-box" />
    <rect width="240" height="24" class="entity-header" />
    <text x="15" y="16" class="entity-name">municipalities (153)</text>
    <text x="15" y="42" class="attr-pk">PK id | FK dept_id | name</text>
  </g>

  <!-- LÍNEAS DE RELACIÓN -->
  <line x1="300" y1="150" x2="360" y2="150" class="rel-line" />
  <line x1="680" y1="150" x2="740" y2="150" class="rel-line" />
  <line x1="680" y1="350" x2="740" y2="350" class="rel-line" />
  <line x1="300" y1="400" x2="360" y2="400" class="rel-line" />
  <line x1="300" y1="580" x2="360" y2="440" class="rel-line" />
  <line x1="520" y1="460" x2="520" y2="500" class="rel-line" />
  <line x1="680" y1="420" x2="740" y2="520" class="rel-line" />
</svg>"""
    with open(os.path.join(DIAG_DIR, "DIAGRAMA_ENTIDAD_RELACION.svg"), "w", encoding="utf-8") as f:
        f.write(der_svg.strip())
    print("Generado: DIAGRAMA_ENTIDAD_RELACION.svg")

    # 3. DIAGRAMA_CASOS_DE_USO.svg
    uc_svg = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1100 700" width="100%" height="100%">
  <defs>
    <style>
      .bg { fill: #0B192C; }
      .title { font-family: 'Segoe UI', Inter, sans-serif; font-size: 22px; font-weight: bold; fill: #FFFFFF; }
      .subtitle { font-family: 'Segoe UI', Inter, sans-serif; font-size: 13px; fill: #94A3B8; }
      .boundary { fill: #1E293B; stroke: #334155; stroke-width: 2; rx: 12; }
      .boundary-title { font-family: 'Segoe UI', Inter, sans-serif; font-size: 14px; font-weight: bold; fill: #14B8A6; }
      .uc-oval { fill: #0F2A4A; stroke: #38BDF8; stroke-width: 1.5; rx: 30; ry: 18; }
      .uc-text { font-family: 'Segoe UI', Inter, sans-serif; font-size: 11px; font-weight: 600; fill: #FFFFFF; text-anchor: middle; }
      .actor-box { fill: #0F172A; stroke: #F59E0B; stroke-width: 1.5; rx: 8; }
      .actor-text { font-family: 'Segoe UI', Inter, sans-serif; font-size: 12px; font-weight: bold; fill: #F59E0B; text-anchor: middle; }
      .conn-line { stroke: #64748B; stroke-width: 1.5; }
    </style>
  </defs>

  <rect width="1100" height="700" class="bg" />
  <text x="50" y="45" class="title">DIAGRAMA DE CASOS DE USO GENERAL DEL SISTEMA</text>
  <text x="50" y="70" class="subtitle">ENCUÉNTRAME NICARAGUA — Actores del Sistema y Casos de Uso Fundamentales</text>

  <!-- Límite del Sistema -->
  <rect x="260" y="100" width="580" height="560" class="boundary" />
  <text x="290" y="130" class="boundary-title">PLATAFORMA ENCUÉNTRAME NICARAGUA</text>

  <!-- ACTORES A LA IZQUIERDA -->
  <!-- Actor 1: Ciudadano -->
  <g transform="translate(50, 160)">
    <rect width="160" height="60" class="actor-box" />
    <circle cx="80" cy="20" r="10" fill="#F59E0B" />
    <text x="80" y="48" class="actor-text">CIUDADANO</text>
  </g>

  <!-- Actor 2: Reportante -->
  <g transform="translate(50, 360)">
    <rect width="160" height="60" class="actor-box" />
    <circle cx="80" cy="20" r="10" fill="#F59E0B" />
    <text x="80" y="48" class="actor-text">REPORTANTE</text>
  </g>

  <!-- ACTORES A LA DERECHA -->
  <!-- Actor 3: Moderador -->
  <g transform="translate(890, 200)">
    <rect width="160" height="60" class="actor-box" stroke="#10B981" />
    <circle cx="80" cy="20" r="10" fill="#10B981" />
    <text x="80" y="48" class="actor-text" fill="#10B981">MODERADOR</text>
  </g>

  <!-- Actor 4: Administrador -->
  <g transform="translate(890, 440)">
    <rect width="160" height="60" class="actor-box" stroke="#EC4899" />
    <circle cx="80" cy="20" r="10" fill="#EC4899" />
    <text x="80" y="48" class="actor-text" fill="#EC4899">ADMINISTRADOR</text>
  </g>

  <!-- CASOS DE USO (ÓVALOS) -->
  <!-- UC 1: Consultar Catálogo y Fichas -->
  <g transform="translate(420, 150)">
    <rect x="-120" y="-18" width="240" height="36" rx="18" class="uc-oval" />
    <text x="0" y="5" class="uc-text">Consultar Catálogo y Fichas</text>
  </g>
  <!-- UC 2: Explorar Mapa Geoespacial -->
  <g transform="translate(420, 210)">
    <rect x="-120" y="-18" width="240" height="36" rx="18" class="uc-oval" />
    <text x="0" y="5" class="uc-text">Explorar Mapa Geoespacial</text>
  </g>
  <!-- UC 3: Aportar Pista Confidencial -->
  <g transform="translate(420, 270)">
    <rect x="-120" y="-18" width="240" height="36" rx="18" class="uc-oval" />
    <text x="0" y="5" class="uc-text">Aportar Pista Confidencial</text>
  </g>
  <!-- UC 4: Registrar Persona Desaparecida -->
  <g transform="translate(420, 340)">
    <rect x="-120" y="-18" width="240" height="36" rx="18" class="uc-oval" />
    <text x="0" y="5" class="uc-text">Registrar Persona Desaparecida</text>
  </g>
  <!-- UC 5: Declarar Consentimiento Ley 787 -->
  <g transform="translate(420, 400)">
    <rect x="-120" y="-18" width="240" height="36" rx="18" class="uc-oval" />
    <text x="0" y="5" class="uc-text">Declarar Consentimiento Ley 787</text>
  </g>
  <!-- UC 6: Cargar y Sanitizar Foto -->
  <g transform="translate(420, 460)">
    <rect x="-120" y="-18" width="240" height="36" rx="18" class="uc-oval" />
    <text x="0" y="5" class="uc-text">Cargar y Previsualizar Fotografía</text>
  </g>
  <!-- UC 7: Auditar y Aprobar Reporte -->
  <g transform="translate(680, 230)">
    <rect x="-120" y="-18" width="240" height="36" rx="18" class="uc-oval" stroke="#10B981" />
    <text x="0" y="5" class="uc-text">Auditar y Aprobar Reporte</text>
  </g>
  <!-- UC 8: Triage de Pistas Ciudadanas -->
  <g transform="translate(680, 300)">
    <rect x="-120" y="-18" width="240" height="36" rx="18" class="uc-oval" stroke="#10B981" />
    <text x="0" y="5" class="uc-text">Triage de Pistas Ciudadanas</text>
  </g>
  <!-- UC 9: Gestión de Roles y Usuarios -->
  <g transform="translate(680, 450)">
    <rect x="-120" y="-18" width="240" height="36" rx="18" class="uc-oval" stroke="#EC4899" />
    <text x="0" y="5" class="uc-text">Gestión de Roles y Usuarios</text>
  </g>
  <!-- UC 10: Auditoría Forense de Logs -->
  <g transform="translate(680, 520)">
    <rect x="-120" y="-18" width="240" height="36" rx="18" class="uc-oval" stroke="#EC4899" />
    <text x="0" y="5" class="uc-text">Auditoría Forense de Logs</text>
  </g>
  <!-- UC 11: Despublicar / Cerrar Caso -->
  <g transform="translate(680, 590)">
    <rect x="-120" y="-18" width="240" height="36" rx="18" class="uc-oval" stroke="#EC4899" />
    <text x="0" y="5" class="uc-text">Despublicar / Cerrar Caso</text>
  </g>

  <!-- CONEXIONES -->
  <!-- Ciudadano -->
  <line x1="210" y1="180" x2="300" y2="150" class="conn-line" />
  <line x1="210" y1="190" x2="300" y2="210" class="conn-line" />
  <line x1="210" y1="200" x2="300" y2="270" class="conn-line" />

  <!-- Reportante -->
  <line x1="210" y1="380" x2="300" y2="340" class="conn-line" />
  <line x1="210" y1="390" x2="300" y2="400" class="conn-line" />
  <line x1="210" y1="400" x2="300" y2="460" class="conn-line" />

  <!-- Moderador -->
  <line x1="890" y1="230" x2="800" y2="230" class="conn-line" />
  <line x1="890" y1="240" x2="800" y2="300" class="conn-line" />

  <!-- Administrador -->
  <line x1="890" y1="460" x2="800" y2="450" class="conn-line" />
  <line x1="890" y1="470" x2="800" y2="520" class="conn-line" />
  <line x1="890" y1="480" x2="800" y2="590" class="conn-line" />
</svg>"""
    with open(os.path.join(DIAG_DIR, "DIAGRAMA_CASOS_DE_USO.svg"), "w", encoding="utf-8") as f:
        f.write(uc_svg.strip())
    print("Generado: DIAGRAMA_CASOS_DE_USO.svg")

if __name__ == "__main__":
    create_diagrams()
