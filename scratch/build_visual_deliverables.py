import os
import json

BASE_DIR = r"C:\Users\User\Documents\Valor IA\EncuentrameNicaragua\ENTREGA_FINAL_ACADEMICA\04_Diseno_Visual"
WF_DIR = os.path.join(BASE_DIR, "Wireframes")

def create_svg(path, content):
    with open(path, "w", encoding="utf-8") as f:
        f.write(content.strip())
    print(f"Generado SVG: {os.path.basename(path)}")

# -------------------------------------------------------------
# 1. MAPA DE NAVEGACIÓN SVG
# -------------------------------------------------------------
def generate_navigation_map():
    svg = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1200 900" width="100%" height="100%">
  <defs>
    <style>
      .bg { fill: #0B192C; }
      .title { font-family: 'Segoe UI', Inter, sans-serif; font-size: 24px; font-weight: bold; fill: #FFFFFF; }
      .subtitle { font-family: 'Segoe UI', Inter, sans-serif; font-size: 14px; fill: #94A3B8; }
      .node-core { fill: #0F2A4A; stroke: #14B8A6; stroke-width: 2.5; rx: 10; }
      .node-pub { fill: #1E293B; stroke: #38BDF8; stroke-width: 2; rx: 8; }
      .node-rep { fill: #1E293B; stroke: #F59E0B; stroke-width: 2; rx: 8; }
      .node-mod { fill: #1E293B; stroke: #10B981; stroke-width: 2; rx: 8; }
      .node-adm { fill: #1E293B; stroke: #EC4899; stroke-width: 2; rx: 8; }
      .text-title { font-family: 'Segoe UI', Inter, sans-serif; font-size: 14px; font-weight: bold; fill: #FFFFFF; text-anchor: middle; }
      .text-route { font-family: monospace; font-size: 11px; fill: #94A3B8; text-anchor: middle; }
      .text-desc { font-family: 'Segoe UI', Inter, sans-serif; font-size: 10px; fill: #CBD5E1; text-anchor: middle; }
      .line { stroke: #475569; stroke-width: 1.5; stroke-dasharray: 4,4; }
      .line-solid { stroke: #14B8A6; stroke-width: 2; }
      .legend-box { fill: #1E293B; stroke: #334155; stroke-width: 1; rx: 6; }
      .legend-text { font-family: 'Segoe UI', Inter, sans-serif; font-size: 11px; fill: #E2E8F0; }
    </style>
    <marker id="arrow" viewBox="0 0 10 10" refX="6" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
      <path d="M 0 1 L 10 5 L 0 9 z" fill="#14B8A6" />
    </marker>
  </defs>

  <!-- Background -->
  <rect width="1200" height="900" class="bg" />

  <!-- Header -->
  <text x="50" y="55" class="title">MAPA DE NAVEGACIÓN Y ARQUITECTURA DE INFORMACIÓN</text>
  <text x="50" y="80" class="subtitle">ENCUÉNTRAME NICARAGUA — Estructura Jerárquica de Rutas, Componentes y Accesos por Rol</text>

  <!-- Leyenda -->
  <g transform="translate(850, 30)">
    <rect width="300" height="85" class="legend-box" />
    <circle cx="20" cy="20" r="6" fill="#38BDF8" />
    <text x="35" y="24" class="legend-text">Acceso Público / Ciudadano</text>
    <circle cx="20" cy="40" r="6" fill="#F59E0B" />
    <text x="35" y="44" class="legend-text">Portal Reportante (Requiere Verificación)</text>
    <circle cx="20" cy="60" r="6" fill="#10B981" />
    <text x="35" y="64" class="legend-text">Moderación y Gestión de Casos</text>
    <circle cx="170" cy="60" r="6" fill="#EC4899" />
    <text x="185" y="64" class="legend-text">Administración Total</text>
  </g>

  <!-- NODO CENTRAL: HOME -->
  <g transform="translate(475, 140)">
    <rect width="250" height="75" class="node-core" />
    <text x="125" y="30" class="text-title">Página de Inicio</text>
    <text x="125" y="48" class="text-route">/ o /index.html</text>
    <text x="125" y="64" class="text-desc">Buscador, Estadísticas, Casos Recientes</text>
  </g>

  <!-- CONEXIONES DESDE HOME -->
  <line x1="600" y1="215" x2="600" y2="280" class="line-solid" />
  <line x1="150" y1="280" x2="1050" y2="280" class="line-solid" />

  <!-- RAMA 1: CATÁLOGO Y FICHAS -->
  <line x1="150" y1="280" x2="150" y2="330" class="line-solid" marker-end="url(#arrow)" />
  <g transform="translate(50, 330)">
    <rect width="200" height="70" class="node-pub" />
    <text x="100" y="25" class="text-title">Catálogo de Casos</text>
    <text x="100" y="43" class="text-route">/casos.html</text>
    <text x="100" y="58" class="text-desc">Filtros, Búsqueda, Paginación</text>
  </g>

  <!-- Sub-nodo: Ficha Detalle -->
  <line x1="150" y1="400" x2="150" y2="470" class="line-solid" marker-end="url(#arrow)" />
  <g transform="translate(50, 470)">
    <rect width="200" height="85" class="node-pub" />
    <text x="100" y="25" class="text-title">Ficha Individual de Caso</text>
    <text x="100" y="43" class="text-route">/casos/EN-2026-XXXX.html</text>
    <text x="100" y="58" class="text-desc">Fotografía, Biometría, Mapa</text>
    <text x="100" y="73" class="text-desc">Compartir en Redes / Descargar PDF</text>
  </g>

  <!-- RAMA 2: MAPA NACIONAL -->
  <line x1="380" y1="280" x2="380" y2="330" class="line-solid" marker-end="url(#arrow)" />
  <g transform="translate(280, 330)">
    <rect width="200" height="70" class="node-pub" />
    <text x="100" y="25" class="text-title">Mapa Geoespacial</text>
    <text x="100" y="43" class="text-route">/mapa.html</text>
    <text x="100" y="58" class="text-desc">Clusters por Departamento, Leaflet</text>
  </g>

  <!-- RAMA 3: APORTAR PISTA -->
  <line x1="600" y1="280" x2="600" y2="330" class="line-solid" marker-end="url(#arrow)" />
  <g transform="translate(500, 330)">
    <rect width="200" height="70" class="node-pub" />
    <text x="100" y="25" class="text-title">Aportar Pista Anónima</text>
    <text x="100" y="43" class="text-route">/pistas.html</text>
    <text x="100" y="58" class="text-desc">Canal Seguro, Cifrado, Confidencial</text>
  </g>

  <!-- Conexión Ficha Detalle -> Pistas -->
  <path d="M 250 512 Q 375 512 500 370" fill="none" stroke="#14B8A6" stroke-width="1.5" stroke-dasharray="4,4" marker-end="url(#arrow)" />

  <!-- RAMA 4: REPORTAR CASO -->
  <line x1="820" y1="280" x2="820" y2="330" class="line-solid" marker-end="url(#arrow)" />
  <g transform="translate(720, 330)">
    <rect width="200" height="70" class="node-rep" />
    <text x="100" y="25" class="text-title">Reportar Caso (Wizard)</text>
    <text x="100" y="43" class="text-route">/reportar.html</text>
    <text x="100" y="58" class="text-desc">Datos, Ubicación, Foto, Ley 787</text>
  </g>

  <!-- Sub-nodo: Subida de Foto y Consentimiento -->
  <line x1="820" y1="400" x2="820" y2="470" class="line-solid" marker-end="url(#arrow)" />
  <g transform="translate(720, 470)">
    <rect width="200" height="75" class="node-rep" />
    <text x="100" y="25" class="text-title">Gestión de Foto & Consent.</text>
    <text x="100" y="43" class="text-route">Modal/Step 3 & 4</text>
    <text x="100" y="58" class="text-desc">Validación WebP/JPEG & Declaración</text>
  </g>

  <!-- RAMA 5: AUTENTICACIÓN Y ROLES -->
  <line x1="1050" y1="280" x2="1050" y2="330" class="line-solid" marker-end="url(#arrow)" />
  <g transform="translate(950, 330)">
    <rect width="200" height="70" class="node-core" />
    <text x="100" y="25" class="text-title">Autenticación (Login)</text>
    <text x="100" y="43" class="text-route">/login.html</text>
    <text x="100" y="58" class="text-desc">JWT, Control de Sesión, Roles</text>
  </g>

  <!-- Sub-nodos de Autenticación -->
  <line x1="1050" y1="400" x2="1050" y2="470" class="line-solid" marker-end="url(#arrow)" />

  <!-- NODO MODERADOR / ADMIN -->
  <g transform="translate(950, 470)">
    <rect width="200" height="85" class="node-mod" />
    <text x="100" y="25" class="text-title">Bandeja de Moderación</text>
    <text x="100" y="43" class="text-route">/admin.html#moderation</text>
    <text x="100" y="58" class="text-desc">Aprobación de Casos</text>
    <text x="100" y="73" class="text-desc">Revisión de Pistas Confidenciales</text>
  </g>

  <line x1="1050" y1="555" x2="1050" y2="620" class="line-solid" marker-end="url(#arrow)" />

  <!-- NODO ADMINISTRADOR TOTAL -->
  <g transform="translate(950, 620)">
    <rect width="200" height="85" class="node-adm" />
    <text x="100" y="25" class="text-title">Panel de Administración</text>
    <text x="100" y="43" class="text-route">/admin.html#system</text>
    <text x="100" y="58" class="text-desc">Gestión de Usuarios y Roles</text>
    <text x="100" y="73" class="text-desc">Métricas y Auditoría</text>
  </g>

  <!-- Footer descriptivo -->
  <rect x="50" y="820" width="1100" height="50" rx="6" fill="#1E293B" stroke="#334155" />
  <text x="600" y="850" class="subtitle" text-anchor="middle">Desarrollado bajo principios de Accesibilidad WCAG 2.1 AA, Enrutamiento Estático Resiliente y Seguridad OWASP ASVS v5.0.0</text>
</svg>"""
    create_svg(os.path.join(BASE_DIR, "MAPA_NAVEGACION.svg"), svg)

# -------------------------------------------------------------
# 2. USER JOURNEYS SVG
# -------------------------------------------------------------
def generate_user_journeys():
    journeys = [
        ("USER_JOURNEY_CIUDADANO.svg", "CIUDADANO", "#38BDF8", [
            ("1. Descubrimiento", "Llegada al portal", "Accede a la página de inicio desde redes o búsqueda pública.", "Visualiza estadísticas y casos urgentes con avatares reales.", "Interés cívico / Solidaridad"),
            ("2. Búsqueda y Filtros", "Exploración del catálogo", "Utiliza el buscador por nombre o filtra por departamento y rango de edad.", "Resultados inmediatos con tarjetas detalladas y badges.", "Claridad y Facilidad"),
            ("3. Consulta de Ficha", "Reconocimiento visual", "Abre la ficha del caso EN-2026-XXXX para ver señas particulares y mapa.", "Revisa ropa, última ubicación conocida y datos de contacto.", "Empatía / Verificación"),
            ("4. Aporte de Pista", "Colaboración confidencial", "Hace clic en 'Aportar Pista' tras recordar un avistamiento relevante.", "Llena el formulario sin necesidad de registrarse si elige anonimato.", "Seguridad y Confianza"),
            ("5. Cierre y Difusión", "Multiplicación comunitaria", "Comparte la ficha en redes sociales o WhatsApp para alertar a vecinos.", "Generación de enlaces canónicos y visualización rápida.", "Sentido de Contribución")
        ]),
        ("USER_JOURNEY_REPORTANTE.svg", "REPORTANTE (FAMILIAR)", "#F59E0B", [
            ("1. Urgencia Inicial", "Situación de emergencia", "Familiar o tutor legal busca un canal ordenado para difundir la desaparición.", "Accede directamente al botón destacado 'Reportar Caso'.", "Angustia / Esperanza"),
            ("2. Identificación y Rol", "Inicio / Validación", "Inicia sesión o registra datos de contacto de emergencia para seguimiento.", "Comprueba que la plataforma respeta su privacidad.", "Alivio por seriedad"),
            ("3. Formulario Guiado", "Captura de datos clave", "Ingresa nombres, señas, condiciones médicas y fecha/hora del suceso.", "Asistente paso a paso con validación de campos obligatorios.", "Concentración"),
            ("4. Foto y Consentimiento", "Carga segura y legal", "Carga fotografía reciente de calidad y firma el consentimiento Ley 787.", "Vista previa inmediata y checklist de verificación ética.", "Seguridad jurídica"),
            ("5. Espera y Seguimiento", "Notificación de moderación", "El reporte pasa a estado 'Pendiente de Revisión' con código de radicado.", "Recibe retroalimentación cuando el equipo valida y publica.", "Paz mental")
        ]),
        ("USER_JOURNEY_MODERADOR.svg", "MODERADOR CÍVICO", "#10B981", [
            ("1. Acceso a Consola", "Ingreso autenticado", "Accede al módulo /admin.html con credenciales y rol autorizado.", "Bandeja de reportes entrantes organizada cronológicamente.", "Responsabilidad"),
            ("2. Auditoría del Caso", "Inspección detallada", "Abre caso pendiente: revisa coherencia de datos, parentesco y contacto.", "Contrasta con criterios de no revictimización y filtros de género.", "Rigurosidad analítica"),
            ("3. Validación de Foto", "Control de calidad gráfica", "Verifica que la imagen corresponda a la persona y no vulnere la dignidad.", "Herramienta de inspección de avatar y saneamiento de metadatos.", "Atención al detalle"),
            ("4. Aprobación / Rechazo", "Toma de decisión", "Aprueba con un clic (pasa a 'approved_published') o solicita ajustes.", "En caso de rechazo, emite motivo formal documentado.", "Justicia y Eficacia"),
            ("5. Gestión de Pistas", "Recepción y canalización", "Revisa testimonios ciudadanos confidenciales recibidos y filtra spam.", "Deriva pistas de alta credibilidad a los canales pertinentes.", "Impacto humanitario")
        ]),
        ("USER_JOURNEY_ADMINISTRADOR.svg", "ADMINISTRADOR DEL SISTEMA", "#EC4899", [
            ("1. Supervisión Global", "Monitoreo operativo", "Ingresa al panel integral para revisar métricas de actividad y uptime.", "Métricas de casos activos, pistas recibidas y tiempo medio de revisión.", "Control gerencial"),
            ("2. Gestión de Usuarios", "Gobernanza de identidades", "Gestiona roles de personal (moderadores, administradores, ciudadanos).", "Habilita, suspende o reasigna permisos según convenios.", "Seguridad operativa"),
            ("3. Auditoría de Casos", "Trazabilidad de acciones", "Inspecciona bitácoras históricas de modificaciones y decisiones tomadas.", "Registros inmutables de aprobación, cierre de casos y accesos.", "Transparencia legal"),
            ("4. Mantenimiento y Backups", "Continuidad de servicio", "Verifica estado del almacenamiento multimedia, backups y despliegues.", "Sincronización de exportaciones estáticas y salud del API.", "Confianza técnica"),
            ("5. Cierre y Reunificación", "Balance de casos resueltos", "Formaliza el cierre de expedientes resueltos y despublicación protegida.", "Garantiza el derecho al olvido y resguardo histórico seguro.", "Satisfacción de misión")
        ])
    ]

    for fname, role_title, color, steps in journeys:
        svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1150 560" width="100%" height="100%">
  <defs>
    <style>
      .bg {{ fill: #0F172A; }}
      .title {{ font-family: 'Segoe UI', Inter, sans-serif; font-size: 22px; font-weight: bold; fill: #FFFFFF; }}
      .subtitle {{ font-family: 'Segoe UI', Inter, sans-serif; font-size: 13px; fill: #94A3B8; }}
      .card {{ fill: #1E293B; stroke: #334155; stroke-width: 1.5; rx: 8; }}
      .card-header {{ fill: {color}; rx: 6; }}
      .step-num {{ font-family: 'Segoe UI', Inter, sans-serif; font-size: 12px; font-weight: bold; fill: #0F172A; }}
      .step-title {{ font-family: 'Segoe UI', Inter, sans-serif; font-size: 13px; font-weight: bold; fill: #FFFFFF; }}
      .phase-text {{ font-family: 'Segoe UI', Inter, sans-serif; font-size: 11px; font-weight: 600; fill: {color}; }}
      .body-text {{ font-family: 'Segoe UI', Inter, sans-serif; font-size: 11px; fill: #CBD5E1; }}
      .label-text {{ font-family: 'Segoe UI', Inter, sans-serif; font-size: 10px; font-weight: bold; fill: #94A3B8; }}
      .emo-text {{ font-family: 'Segoe UI', Inter, sans-serif; font-size: 11px; font-style: italic; fill: #FDE047; }}
      .line-conn {{ stroke: {color}; stroke-width: 2; stroke-dasharray: 4,4; }}
    </style>
  </defs>

  <!-- Background -->
  <rect width="1150" height="560" class="bg" />

  <!-- Header -->
  <text x="40" y="45" class="title">MAPA DE VIAJE DEL USUARIO (USER JOURNEY MAP) — ROL: {role_title}</text>
  <text x="40" y="70" class="subtitle">Plataforma Encuéntrame Nicaragua — Fases, Acciones, Puntos de Contacto y Estado Emocional</text>

  <!-- Linea conectora central -->
  <line x1="130" y1="120" x2="1010" y2="120" class="line-conn" />
"""
        x_start = 40
        card_w = 200
        gap = 25

        for i, (fase, accion, desc, touch, emo) in enumerate(steps):
            cx = x_start + i * (card_w + gap)
            svg += f"""
  <!-- Paso {i+1} -->
  <g transform="translate({cx}, 100)">
    <!-- Header Circulo -->
    <circle cx="100" cy="20" r="16" fill="{color}" />
    <text x="100" y="25" class="step-num" text-anchor="middle">{i+1}</text>

    <!-- Tarjeta de Contenido -->
    <rect x="0" y="50" width="{card_w}" height="350" class="card" />

    <!-- Fase -->
    <text x="15" y="80" class="phase-text">{fase.upper()}</text>
    <text x="15" y="102" class="step-title">{accion}</text>
    <line x1="15" y1="115" x2="185" y2="115" stroke="#334155" stroke-width="1" />

    <!-- Objetivo / Acción -->
    <text x="15" y="135" class="label-text">ACCIÓN DEL USUARIO:</text>
    <foreignObject x="15" y="145" width="170" height="70">
      <p xmlns="http://www.w3.org/1999/xhtml" style="color: #CBD5E1; font-family: sans-serif; font-size: 11px; margin: 0; line-height: 1.35;">
        {desc}
      </p>
    </foreignObject>

    <!-- Punto de contacto -->
    <text x="15" y="235" class="label-text">PUNTO DE CONTACTO:</text>
    <foreignObject x="15" y="245" width="170" height="70">
      <p xmlns="http://www.w3.org/1999/xhtml" style="color: #94A3B8; font-family: sans-serif; font-size: 10.5px; margin: 0; line-height: 1.35;">
        {touch}
      </p>
    </foreignObject>

    <!-- Estado Emocional -->
    <line x1="15" y1="330" x2="185" y2="330" stroke="#334155" stroke-width="1" />
    <text x="15" y="350" class="label-text">ESTADO / SENTIMIENTO:</text>
    <text x="15" y="375" class="emo-text">“{emo}”</text>
  </g>
"""
        svg += f"""
  <!-- Footer de la lámina -->
  <rect x="40" y="500" width="1070" height="35" rx="4" fill="#1E293B" stroke="#334155" />
  <text x="575" y="522" class="subtitle" text-anchor="middle">Metodología Human-Centered Design (HCD) adaptada al contexto de búsqueda y reunificación familiar cívica</text>
</svg>"""
        create_svg(os.path.join(BASE_DIR, fname), svg)

# -------------------------------------------------------------
# 3. GENERADOR DE WIREFRAMES (12 Pantallas)
# -------------------------------------------------------------
def generate_wireframes():
    wireframes = [
        ("WF_01_Inicio.svg", "01. PÁGINA DE INICIO (HOME)", "Ciudadano / Público General", """
  <!-- Header Wireframe -->
  <rect x="50" y="80" width="900" height="50" fill="#E2E8F0" stroke="#94A3B8" />
  <rect x="65" y="90" width="30" height="30" fill="#0D9488" rx="4" />
  <text x="110" y="110" font-family="sans-serif" font-weight="bold" font-size="14" fill="#0F172A">ENCUÉNTRAME NICARAGUA</text>
  <rect x="450" y="95" width="60" height="20" fill="#CBD5E1" rx="3" />
  <rect x="525" y="95" width="70" height="20" fill="#CBD5E1" rx="3" />
  <rect x="610" y="95" width="60" height="20" fill="#CBD5E1" rx="3" />
  <rect x="685" y="95" width="65" height="20" fill="#CBD5E1" rx="3" />
  <rect x="800" y="90" width="130" height="30" fill="#0D9488" rx="4" />
  <text x="865" y="110" font-family="sans-serif" font-weight="bold" font-size="11" fill="#FFFFFF" text-anchor="middle">+ Reportar Caso</text>

  <!-- Hero Wireframe -->
  <rect x="50" y="145" width="900" height="180" fill="#F1F5F9" stroke="#CBD5E1" />
  <text x="500" y="195" font-family="sans-serif" font-weight="bold" font-size="20" fill="#1E293B" text-anchor="middle">[ Título Principal: Cada Persona Importa ]</text>
  <text x="500" y="225" font-family="sans-serif" font-size="12" fill="#64748B" text-anchor="middle">[ Buscador rápido de personas reportadas por nombre o código ]</text>
  <rect x="250" y="245" width="400" height="40" fill="#FFFFFF" stroke="#94A3B8" rx="6" />
  <rect x="660" y="245" width="90" height="40" fill="#0F2A4A" rx="6" />
  <text x="705" y="270" font-family="sans-serif" font-size="12" fill="#FFFFFF" text-anchor="middle">Buscar</text>

  <!-- Contadores / Estadísticas -->
  <rect x="150" y="340" width="180" height="70" fill="#FFFFFF" stroke="#CBD5E1" rx="6" />
  <text x="240" y="370" font-family="sans-serif" font-weight="bold" font-size="18" fill="#0F2A4A" text-anchor="middle">25</text>
  <text x="240" y="390" font-family="sans-serif" font-size="11" fill="#64748B" text-anchor="middle">Casos Registrados</text>

  <rect x="410" y="340" width="180" height="70" fill="#FFFFFF" stroke="#CBD5E1" rx="6" />
  <text x="500" y="370" font-family="sans-serif" font-weight="bold" font-size="18" fill="#0D9488" text-anchor="middle">100%</text>
  <text x="500" y="390" font-family="sans-serif" font-size="11" fill="#64748B" text-anchor="middle">Verificación Humana</text>

  <rect x="670" y="340" width="180" height="70" fill="#FFFFFF" stroke="#CBD5E1" rx="6" />
  <text x="760" y="370" font-family="sans-serif" font-weight="bold" font-size="18" fill="#E11D48" text-anchor="middle">03</text>
  <text x="760" y="390" font-family="sans-serif" font-size="11" fill="#64748B" text-anchor="middle">Casos de Urgencia</text>

  <!-- Tarjetas de Casos Recientes -->
  <text x="50" y="445" font-family="sans-serif" font-weight="bold" font-size="14" fill="#0F172A">CASOS RECIENTES REPORTADOS</text>
  <g transform="translate(50, 460)">
    <rect x="0" y="0" width="280" height="180" fill="#FFFFFF" stroke="#CBD5E1" rx="6" />
    <rect x="15" y="15" width="70" height="85" fill="#E2E8F0" stroke="#94A3B8" />
    <text x="50" y="60" font-family="sans-serif" font-size="9" fill="#64748B" text-anchor="middle">[ Foto ]</text>
    <rect x="100" y="20" width="160" height="14" fill="#94A3B8" />
    <rect x="100" y="42" width="110" height="10" fill="#CBD5E1" />
    <rect x="100" y="58" width="130" height="10" fill="#CBD5E1" />
    <rect x="15" y="120" width="250" height="35" fill="#0D9488" rx="4" />
    <text x="140" y="142" font-family="sans-serif" font-weight="bold" font-size="11" fill="#FFFFFF" text-anchor="middle">Ver Ficha Completa</text>
  </g>

  <g transform="translate(360, 460)">
    <rect x="0" y="0" width="280" height="180" fill="#FFFFFF" stroke="#CBD5E1" rx="6" />
    <rect x="15" y="15" width="70" height="85" fill="#E2E8F0" stroke="#94A3B8" />
    <text x="50" y="60" font-family="sans-serif" font-size="9" fill="#64748B" text-anchor="middle">[ Foto ]</text>
    <rect x="100" y="20" width="160" height="14" fill="#94A3B8" />
    <rect x="100" y="42" width="110" height="10" fill="#CBD5E1" />
    <rect x="100" y="58" width="130" height="10" fill="#CBD5E1" />
    <rect x="15" y="120" width="250" height="35" fill="#0D9488" rx="4" />
    <text x="140" y="142" font-family="sans-serif" font-weight="bold" font-size="11" fill="#FFFFFF" text-anchor="middle">Ver Ficha Completa</text>
  </g>

  <g transform="translate(670, 460)">
    <rect x="0" y="0" width="280" height="180" fill="#FFFFFF" stroke="#CBD5E1" rx="6" />
    <rect x="15" y="15" width="70" height="85" fill="#E2E8F0" stroke="#94A3B8" />
    <text x="50" y="60" font-family="sans-serif" font-size="9" fill="#64748B" text-anchor="middle">[ Foto ]</text>
    <rect x="100" y="20" width="160" height="14" fill="#94A3B8" />
    <rect x="100" y="42" width="110" height="10" fill="#CBD5E1" />
    <rect x="100" y="58" width="130" height="10" fill="#CBD5E1" />
    <rect x="15" y="120" width="250" height="35" fill="#0D9488" rx="4" />
    <text x="140" y="142" font-family="sans-serif" font-weight="bold" font-size="11" fill="#FFFFFF" text-anchor="middle">Ver Ficha Completa</text>
  </g>
"""),
        ("WF_02_Catalogo.svg", "02. CATÁLOGO DE CASOS", "Ciudadano / Investigador / Familiares", """
  <!-- Barra de Filtros -->
  <rect x="50" y="80" width="900" height="80" fill="#F8FAFC" stroke="#CBD5E1" rx="6" />
  <rect x="70" y="100" width="220" height="35" fill="#FFFFFF" stroke="#94A3B8" rx="4" />
  <text x="80" y="122" font-family="sans-serif" font-size="11" fill="#64748B">Buscar por nombre o código...</text>
  <rect x="310" y="100" width="160" height="35" fill="#FFFFFF" stroke="#94A3B8" rx="4" />
  <text x="320" y="122" font-family="sans-serif" font-size="11" fill="#64748B">Departamento: Todos ▾</text>
  <rect x="490" y="100" width="130" height="35" fill="#FFFFFF" stroke="#94A3B8" rx="4" />
  <text x="500" y="122" font-family="sans-serif" font-size="11" fill="#64748B">Género: Todos ▾</text>
  <rect x="640" y="100" width="130" height="35" fill="#FFFFFF" stroke="#94A3B8" rx="4" />
  <text x="650" y="122" font-family="sans-serif" font-size="11" fill="#64748B">Estado: Todos ▾</text>
  <rect x="790" y="100" width="140" height="35" fill="#0F2A4A" rx="4" />
  <text x="860" y="122" font-family="sans-serif" font-size="11" fill="#FFFFFF" text-anchor="middle">Aplicar Filtros</text>

  <!-- Grilla 3x2 de Casos -->
  <g transform="translate(50, 180)">
    <!-- Fila 1 -->
    <rect x="0" y="0" width="280" height="200" fill="#FFFFFF" stroke="#CBD5E1" rx="6" />
    <rect x="15" y="15" width="80" height="100" fill="#E2E8F0" stroke="#94A3B8" />
    <rect x="110" y="20" width="150" height="14" fill="#94A3B8" />
    <rect x="110" y="42" width="120" height="10" fill="#CBD5E1" />
    <rect x="110" y="58" width="80" height="18" fill="#FEF3C7" stroke="#F59E0B" rx="3" />
    <text x="150" y="71" font-family="sans-serif" font-size="9" fill="#B45309" text-anchor="middle">EN BÚSQUEDA</text>
    <rect x="15" y="140" width="250" height="35" fill="#0D9488" rx="4" />
    <text x="140" y="162" font-family="sans-serif" font-weight="bold" font-size="11" fill="#FFFFFF" text-anchor="middle">Ver Ficha</text>

    <rect x="310" y="0" width="280" height="200" fill="#FFFFFF" stroke="#CBD5E1" rx="6" />
    <rect x="325" y="15" width="80" height="100" fill="#E2E8F0" stroke="#94A3B8" />
    <rect x="420" y="20" width="150" height="14" fill="#94A3B8" />
    <rect x="420" y="42" width="120" height="10" fill="#CBD5E1" />
    <rect x="420" y="58" width="80" height="18" fill="#FEE2E2" stroke="#EF4444" rx="3" />
    <text x="460" y="71" font-family="sans-serif" font-size="9" fill="#B91C1C" text-anchor="middle">URGENTE</text>
    <rect x="325" y="140" width="250" height="35" fill="#0D9488" rx="4" />
    <text x="450" y="162" font-family="sans-serif" font-weight="bold" font-size="11" fill="#FFFFFF" text-anchor="middle">Ver Ficha</text>

    <rect x="620" y="0" width="280" height="200" fill="#FFFFFF" stroke="#CBD5E1" rx="6" />
    <rect x="635" y="15" width="80" height="100" fill="#E2E8F0" stroke="#94A3B8" />
    <rect x="730" y="20" width="150" height="14" fill="#94A3B8" />
    <rect x="730" y="42" width="120" height="10" fill="#CBD5E1" />
    <rect x="730" y="58" width="80" height="18" fill="#FEF3C7" stroke="#F59E0B" rx="3" />
    <text x="770" y="71" font-family="sans-serif" font-size="9" fill="#B45309" text-anchor="middle">EN BÚSQUEDA</text>
    <rect x="635" y="140" width="250" height="35" fill="#0D9488" rx="4" />
    <text x="760" y="162" font-family="sans-serif" font-weight="bold" font-size="11" fill="#FFFFFF" text-anchor="middle">Ver Ficha</text>
  </g>

  <!-- Paginación -->
  <rect x="400" y="420" width="200" height="35" fill="#FFFFFF" stroke="#CBD5E1" rx="4" />
  <text x="500" y="442" font-family="sans-serif" font-size="11" fill="#0F172A" text-anchor="middle">«  Página 1 de 3  »</text>
"""),
        ("WF_03_Ficha_Detalle.svg", "03. FICHA INDIVIDUAL DE CASO", "Público General / Ciudadano / Autoridades", """
  <!-- Breadcrumb -->
  <rect x="50" y="80" width="250" height="20" fill="#E2E8F0" rx="3" />
  <text x="60" y="94" font-family="sans-serif" font-size="10" fill="#475569">Inicio / Catálogo / EN-2026-0001</text>

  <!-- Contenedor Principal: 2 Columnas -->
  <g transform="translate(50, 115)">
    <!-- Columna Izquierda: Fotografía y Acciones -->
    <rect x="0" y="0" width="320" height="480" fill="#FFFFFF" stroke="#CBD5E1" rx="8" />
    <rect x="25" y="25" width="270" height="270" fill="#F1F5F9" stroke="#94A3B8" rx="6" />
    <text x="160" y="160" font-family="sans-serif" font-size="13" fill="#64748B" text-anchor="middle">[ Fotografía Oficial Verificada ]</text>
    <rect x="25" y="315" width="270" height="40" fill="#0D9488" rx="6" />
    <text x="160" y="340" font-family="sans-serif" font-weight="bold" font-size="12" fill="#FFFFFF" text-anchor="middle">Aportar Pista Confidencial</text>
    <rect x="25" y="365" width="270" height="35" fill="#F8FAFC" stroke="#94A3B8" rx="6" />
    <text x="160" y="388" font-family="sans-serif" font-size="11" fill="#1E293B" text-anchor="middle">Compartir en Redes Sociales</text>
    <rect x="25" y="410" width="270" height="35" fill="#F8FAFC" stroke="#94A3B8" rx="6" />
    <text x="160" y="433" font-family="sans-serif" font-size="11" fill="#1E293B" text-anchor="middle">Descargar Ficha para Imprimir</text>

    <!-- Columna Derecha: Expediente y Detalles Biométricos -->
    <rect x="350" y="0" width="550" height="480" fill="#FFFFFF" stroke="#CBD5E1" rx="8" />
    <!-- Cabecera del expediente -->
    <rect x="375" y="25" width="120" height="24" fill="#FEF3C7" stroke="#F59E0B" rx="4" />
    <text x="435" y="41" font-family="sans-serif" font-size="10" font-weight="bold" fill="#B45309" text-anchor="middle">EN BÚSQUEDA</text>
    <text x="375" y="80" font-family="sans-serif" font-size="18" font-weight="bold" fill="#0F172A">Sofía Alejandra Morales Rivas</text>
    <text x="375" y="100" font-family="sans-serif" font-size="11" fill="#64748B">Expediente Oficial: EN-2026-0001 | Publicado: 18/11/2026</text>

    <!-- Bloque Datos Biométricos -->
    <rect x="375" y="120" width="500" height="90" fill="#F8FAFC" stroke="#E2E8F0" rx="6" />
    <text x="390" y="145" font-family="sans-serif" font-size="11" fill="#334155"><tspan font-weight="bold">Edad:</tspan> 24 años   |   <tspan font-weight="bold">Género:</tspan> Femenino   |   <tspan font-weight="bold">Estatura:</tspan> 1.62 m</text>
    <text x="390" y="170" font-family="sans-serif" font-size="11" fill="#334155"><tspan font-weight="bold">Tez:</tspan> Trigueña clara   |   <tspan font-weight="bold">Ojos:</tspan> Café oscuro   |   <tspan font-weight="bold">Cabello:</tspan> Castaño largo</text>
    <text x="390" y="195" font-family="sans-serif" font-size="11" fill="#334155"><tspan font-weight="bold">Señas particulares:</tspan> Cicatriz pequeña en ceja izquierda, lunar en mejilla.</text>

    <!-- Bloque Circunstancias -->
    <text x="375" y="235" font-family="sans-serif" font-size="12" font-weight="bold" fill="#0F172A">Circunstancias de la desaparición:</text>
    <rect x="375" y="245" width="500" height="55" fill="#F8FAFC" stroke="#E2E8F0" rx="4" />
    <text x="390" y="265" font-family="sans-serif" font-size="10.5" fill="#475569">Vista por última vez en sector Metrocentro, Managua, vistiendo blusa blanca y jeans.</text>

    <!-- Mini Mapa de Ubicación -->
    <text x="375" y="325" font-family="sans-serif" font-size="12" font-weight="bold" fill="#0F172A">Última ubicación geográfica referencial:</text>
    <rect x="375" y="335" width="500" height="120" fill="#E2E8F0" stroke="#94A3B8" rx="6" />
    <circle cx="625" cy="395" r="10" fill="#EF4444" />
    <text x="625" y="420" font-family="sans-serif" font-size="9" fill="#1E293B" text-anchor="middle">Managua, Metrocentro (Punto Aproximado)</text>
  </g>
"""),
        ("WF_04_Mapa_Nacional.svg", "04. MAPA GEOESPACIAL NACIONAL", "Ciudadano / Brigadas de Búsqueda", """
  <!-- Contenedor del Mapa -->
  <rect x="50" y="80" width="600" height="520" fill="#E2E8F0" stroke="#94A3B8" rx="8" />
  <text x="350" y="200" font-family="sans-serif" font-size="18" fill="#64748B" text-anchor="middle">[ Vista Satelital / Vectorial Nicaragua (Leaflet) ]</text>
  <!-- Marcadores / Clusters -->
  <circle cx="280" cy="330" r="22" fill="#0D9488" opacity="0.9" />
  <text x="280" y="335" font-family="sans-serif" font-weight="bold" font-size="12" fill="#FFFFFF" text-anchor="middle">12</text>
  <text x="280" y="365" font-family="sans-serif" font-size="10" fill="#0F172A" text-anchor="middle">Managua</text>

  <circle cx="340" cy="240" r="18" fill="#0D9488" opacity="0.9" />
  <text x="340" y="245" font-family="sans-serif" font-weight="bold" font-size="11" fill="#FFFFFF" text-anchor="middle">5</text>
  <text x="340" y="270" font-family="sans-serif" font-size="10" fill="#0F172A" text-anchor="middle">Matagalpa</text>

  <circle cx="220" cy="270" r="16" fill="#0D9488" opacity="0.9" />
  <text x="220" y="275" font-family="sans-serif" font-weight="bold" font-size="10" fill="#FFFFFF" text-anchor="middle">3</text>
  <text x="220" y="300" font-family="sans-serif" font-size="10" fill="#0F172A" text-anchor="middle">León</text>

  <!-- Panel Lateral de Filtros y Detalle Rápido -->
  <g transform="translate(670, 80)">
    <rect x="0" y="0" width="280" height="520" fill="#FFFFFF" stroke="#CBD5E1" rx="8" />
    <text x="20" y="30" font-family="sans-serif" font-weight="bold" font-size="14" fill="#0F172A">FILTROS DEL MAPA</text>
    <rect x="20" y="45" width="240" height="35" fill="#F8FAFC" stroke="#94A3B8" rx="4" />
    <text x="30" y="67" font-family="sans-serif" font-size="11" fill="#64748B">Filtrar por Departamento ▾</text>

    <!-- Lista de Casos en la Zona -->
    <text x="20" y="115" font-family="sans-serif" font-weight="bold" font-size="12" fill="#0F172A">Casos en la Zona Seleccionada (12):</text>
    <rect x="20" y="130" width="240" height="70" fill="#F8FAFC" stroke="#E2E8F0" rx="6" />
    <rect x="30" y="140" width="40" height="50" fill="#E2E8F0" />
    <text x="80" y="155" font-family="sans-serif" font-weight="bold" font-size="10" fill="#0F172A">Sofía Morales (24 a)</text>
    <text x="80" y="170" font-family="sans-serif" font-size="9" fill="#64748B">Managua, Metrocentro</text>

    <rect x="20" y="210" width="240" height="70" fill="#F8FAFC" stroke="#E2E8F0" rx="6" />
    <rect x="30" y="220" width="40" height="50" fill="#E2E8F0" />
    <text x="80" y="235" font-family="sans-serif" font-weight="bold" font-size="10" fill="#0F172A">Carlos Mendoza (17 a)</text>
    <text x="80" y="250" font-family="sans-serif" font-size="9" fill="#64748B">Managua, Tipitapa</text>

    <rect x="20" y="290" width="240" height="70" fill="#F8FAFC" stroke="#E2E8F0" rx="6" />
    <rect x="30" y="300" width="40" height="50" fill="#E2E8F0" />
    <text x="80" y="315" font-family="sans-serif" font-weight="bold" font-size="10" fill="#0F172A">Elena Ruiz (31 a)</text>
    <text x="80" y="330" font-family="sans-serif" font-size="9" fill="#64748B">Managua, Ciudad Sandino</text>
  </g>
"""),
        ("WF_05_Registro_Reporte.svg", "05. FORMULARIO DE REPORTE (WIZARD)", "Familiar / Reportante Acreditado", """
  <!-- Stepper de Progreso -->
  <g transform="translate(100, 80)">
    <circle cx="50" cy="20" r="16" fill="#0D9488" />
    <text x="50" y="25" font-family="sans-serif" font-weight="bold" font-size="11" fill="#FFFFFF" text-anchor="middle">1</text>
    <text x="50" y="50" font-family="sans-serif" font-size="10" fill="#0F172A" text-anchor="middle">Datos Personales</text>

    <line x1="80" y1="20" x2="220" y2="20" stroke="#0D9488" stroke-width="2" />

    <circle cx="250" cy="20" r="16" fill="#0D9488" />
    <text x="250" y="25" font-family="sans-serif" font-weight="bold" font-size="11" fill="#FFFFFF" text-anchor="middle">2</text>
    <text x="250" y="50" font-family="sans-serif" font-size="10" fill="#0F172A" text-anchor="middle">Circunstancias</text>

    <line x1="280" y1="20" x2="420" y2="20" stroke="#0D9488" stroke-width="2" />

    <circle cx="450" cy="20" r="16" fill="#0F2A4A" />
    <text x="450" y="25" font-family="sans-serif" font-weight="bold" font-size="11" fill="#FFFFFF" text-anchor="middle">3</text>
    <text x="450" y="50" font-family="sans-serif" font-weight="bold" font-size="10" fill="#0F2A4A" text-anchor="middle">Fotografía</text>

    <line x1="480" y1="20" x2="620" y2="20" stroke="#CBD5E1" stroke-width="2" />

    <circle cx="650" cy="20" r="16" fill="#CBD5E1" />
    <text x="650" y="25" font-family="sans-serif" font-weight="bold" font-size="11" fill="#475569" text-anchor="middle">4</text>
    <text x="650" y="50" font-family="sans-serif" font-size="10" fill="#64748B" text-anchor="middle">Consentimiento</text>
  </g>

  <!-- Formulario Paso Actual -->
  <g transform="translate(150, 160)">
    <rect x="0" y="0" width="700" height="420" fill="#FFFFFF" stroke="#CBD5E1" rx="8" />
    <text x="40" y="40" font-family="sans-serif" font-weight="bold" font-size="15" fill="#0F172A">PASO 1: DATOS DE LA PERSONA REPORTADA</text>

    <text x="40" y="80" font-family="sans-serif" font-size="11" fill="#334155">Nombre Completo *</text>
    <rect x="40" y="90" width="300" height="35" fill="#F8FAFC" stroke="#94A3B8" rx="4" />

    <text x="360" y="80" font-family="sans-serif" font-size="11" fill="#334155">Edad al desaparecer *</text>
    <rect x="360" y="90" width="140" height="35" fill="#F8FAFC" stroke="#94A3B8" rx="4" />

    <text x="520" y="80" font-family="sans-serif" font-size="11" fill="#334155">Género *</text>
    <rect x="520" y="90" width="140" height="35" fill="#F8FAFC" stroke="#94A3B8" rx="4" />

    <text x="40" y="150" font-family="sans-serif" font-size="11" fill="#334155">Departamento de última ubicación *</text>
    <rect x="40" y="160" width="300" height="35" fill="#F8FAFC" stroke="#94A3B8" rx="4" />

    <text x="360" y="150" font-family="sans-serif" font-size="11" fill="#334155">Fecha y hora aproximada *</text>
    <rect x="360" y="160" width="300" height="35" fill="#F8FAFC" stroke="#94A3B8" rx="4" />

    <text x="40" y="220" font-family="sans-serif" font-size="11" fill="#334155">Descripción física detallada (estatura, cabello, ojos, señas) *</text>
    <rect x="40" y="230" width="620" height="60" fill="#F8FAFC" stroke="#94A3B8" rx="4" />

    <text x="40" y="315" font-family="sans-serif" font-size="11" fill="#334155">Vestimenta que portaba al momento de ser vista/o</text>
    <rect x="40" y="325" width="620" height="40" fill="#F8FAFC" stroke="#94A3B8" rx="4" />

    <!-- Botonera -->
    <rect x="40" y="380" width="120" height="35" fill="#F1F5F9" stroke="#CBD5E1" rx="4" />
    <text x="100" y="402" font-family="sans-serif" font-size="11" fill="#475569" text-anchor="middle">Cancelar</text>

    <rect x="520" y="380" width="140" height="35" fill="#0D9488" rx="4" />
    <text x="590" y="402" font-family="sans-serif" font-weight="bold" font-size="11" fill="#FFFFFF" text-anchor="middle">Siguiente Paso »</text>
  </g>
"""),
        ("WF_06_Aporte_Pistas.svg", "06. APORTE DE PISTAS CONFIDENCIALES", "Ciudadano Testigo / Informante", """
  <g transform="translate(150, 80)">
    <rect x="0" y="0" width="700" height="520" fill="#FFFFFF" stroke="#CBD5E1" rx="8" />
    <text x="40" y="35" font-family="sans-serif" font-weight="bold" font-size="16" fill="#0F172A">CANAL SEGURO DE APORTACIÓN DE PISTAS</text>

    <!-- Banner de confidencialidad -->
    <rect x="40" y="55" width="620" height="45" fill="#FEF3C7" stroke="#F59E0B" rx="4" />
    <text x="55" y="80" font-family="sans-serif" font-size="10.5" fill="#92400E">🛡 Toda información es recibida bajo estricta confidencialidad por el equipo de moderación.</text>

    <text x="40" y="125" font-family="sans-serif" font-size="11" fill="#334155">Caso al que se refiere la información *</text>
    <rect x="40" y="135" width="620" height="35" fill="#F8FAFC" stroke="#94A3B8" rx="4" />
    <text x="55" y="157" font-family="sans-serif" font-size="11" fill="#0F172A">EN-2026-0001 — Sofía Alejandra Morales Rivas</text>

    <text x="40" y="195" font-family="sans-serif" font-size="11" fill="#334155">Fecha y hora en que fue vista la persona *</text>
    <rect x="40" y="205" width="300" height="35" fill="#F8FAFC" stroke="#94A3B8" rx="4" />

    <text x="360" y="195" font-family="sans-serif" font-size="11" fill="#334155">Lugar o punto de referencia del avistamiento *</text>
    <rect x="360" y="205" width="300" height="35" fill="#F8FAFC" stroke="#94A3B8" rx="4" />

    <text x="40" y="265" font-family="sans-serif" font-size="11" fill="#334155">Descripción de lo observado (compañía, dirección, estado) *</text>
    <rect x="40" y="275" width="620" height="75" fill="#F8FAFC" stroke="#94A3B8" rx="4" />

    <text x="40" y="375" font-family="sans-serif" font-size="11" fill="#334155">Teléfono o correo de contacto (Opcional si prefiere seguimiento directo):</text>
    <rect x="40" y="385" width="300" height="35" fill="#F8FAFC" stroke="#94A3B8" rx="4" />

    <!-- Checkbox Anónimo -->
    <rect x="40" y="440" width="18" height="18" fill="#0D9488" rx="3" />
    <text x="70" y="454" font-family="sans-serif" font-size="11" fill="#334155">Deseo que mi testimonio sea tratado con carácter 100% anónimo.</text>

    <!-- Botón Enviar -->
    <rect x="40" y="475" width="220" height="35" fill="#0D9488" rx="4" />
    <text x="150" y="497" font-family="sans-serif" font-weight="bold" font-size="11" fill="#FFFFFF" text-anchor="middle">Enviar Pista con Seguridad</text>
  </g>
"""),
        ("WF_07_Login.svg", "07. INICIO DE SESIÓN (LOGIN)", "Reportante / Moderador / Administrador", """
  <g transform="translate(280, 100)">
    <rect x="0" y="0" width="440" height="420" fill="#FFFFFF" stroke="#CBD5E1" rx="8" />
    <rect x="195" y="30" width="50" height="50" fill="#0D9488" rx="8" />
    <text x="220" y="62" font-family="sans-serif" font-weight="bold" font-size="22" fill="#FFFFFF" text-anchor="middle">EN</text>

    <text x="220" y="110" font-family="sans-serif" font-weight="bold" font-size="16" fill="#0F172A" text-anchor="middle">Acceso al Sistema</text>
    <text x="220" y="130" font-family="sans-serif" font-size="11" fill="#64748B" text-anchor="middle">Ingresa con tus credenciales asignadas</text>

    <text x="40" y="165" font-family="sans-serif" font-size="11" fill="#334155">Correo Electrónico</text>
    <rect x="40" y="175" width="360" height="40" fill="#F8FAFC" stroke="#94A3B8" rx="4" />

    <text x="40" y="235" font-family="sans-serif" font-size="11" fill="#334155">Contraseña</text>
    <rect x="40" y="245" width="360" height="40" fill="#F8FAFC" stroke="#94A3B8" rx="4" />

    <!-- Botón Ingresar -->
    <rect x="40" y="310" width="360" height="45" fill="#0F2A4A" rx="6" />
    <text x="220" y="337" font-family="sans-serif" font-weight="bold" font-size="12" fill="#FFFFFF" text-anchor="middle">Iniciar Sesión</text>

    <text x="220" y="380" font-family="sans-serif" font-size="10.5" fill="#64748B" text-anchor="middle">🔒 Conexión segura bajo protocolo HTTPS y Argon2id</text>
  </g>
"""),
        ("WF_08_Registro_Usuario.svg", "08. REGISTRO DE USUARIOS (BACKEND / PREVISTO)", "Ciudadano / Reportante (Estado: Previsto en API)", """
  <!-- Nota de Estado Real -->
  <rect x="100" y="70" width="800" height="45" fill="#FEF3C7" stroke="#F59E0B" rx="6" />
  <text x="500" y="97" font-family="sans-serif" font-size="11" font-weight="bold" fill="#92400E" text-anchor="middle">ESTADO TÉCNICO: Modelo de base de datos y endpoint backend implementados (POST /auth/register);</text>
  <text x="500" y="110" font-family="sans-serif" font-size="10" fill="#92400E" text-anchor="middle">en el MVP actual el reporte permite flujo directo y se documenta aquí como reconstrucción retrospectiva.</text>

  <g transform="translate(250, 135)">
    <rect x="0" y="0" width="500" height="420" fill="#FFFFFF" stroke="#CBD5E1" rx="8" />
    <text x="250" y="40" font-family="sans-serif" font-weight="bold" font-size="16" fill="#0F172A" text-anchor="middle">Registro de Cuenta Ciudadana</text>

    <text x="50" y="80" font-family="sans-serif" font-size="11" fill="#334155">Nombre Completo</text>
    <rect x="50" y="90" width="400" height="35" fill="#F8FAFC" stroke="#94A3B8" rx="4" />

    <text x="50" y="145" font-family="sans-serif" font-size="11" fill="#334155">Correo Electrónico Institucional o Personal</text>
    <rect x="50" y="155" width="400" height="35" fill="#F8FAFC" stroke="#94A3B8" rx="4" />

    <text x="50" y="210" font-family="sans-serif" font-size="11" fill="#334155">Teléfono Celular de Verificación (SMS / WhatsApp)</text>
    <rect x="50" y="220" width="400" height="35" fill="#F8FAFC" stroke="#94A3B8" rx="4" />

    <text x="50" y="275" font-family="sans-serif" font-size="11" fill="#334155">Contraseña (Mínimo 8 caracteres, números y símbolos)</text>
    <rect x="50" y="285" width="400" height="35" fill="#F8FAFC" stroke="#94A3B8" rx="4" />

    <rect x="50" y="345" width="400" height="40" fill="#0D9488" rx="4" />
    <text x="250" y="370" font-family="sans-serif" font-weight="bold" font-size="12" fill="#FFFFFF" text-anchor="middle">Crear Cuenta Segura</text>
  </g>
"""),
        ("WF_09_Panel_Administracion.svg", "09. PANEL DE ADMINISTRACIÓN TOTAL", "Administrador del Sistema", """
  <!-- Layout 2 Columnas: Sidebar + Contenido -->
  <g transform="translate(50, 80)">
    <!-- Sidebar -->
    <rect x="0" y="0" width="200" height="520" fill="#0F2A4A" rx="8" />
    <text x="20" y="35" font-family="sans-serif" font-weight="bold" font-size="13" fill="#FFFFFF">ADMIN CONSOLE</text>
    <rect x="15" y="60" width="170" height="35" fill="#1E3A8A" rx="4" />
    <text x="30" y="82" font-family="sans-serif" font-size="11" fill="#FFFFFF">📊 Métricas y Salud</text>
    <rect x="15" y="105" width="170" height="35" fill="none" rx="4" />
    <text x="30" y="127" font-family="sans-serif" font-size="11" fill="#94A3B8">👥 Gestión Usuarios</text>
    <rect x="15" y="150" width="170" height="35" fill="none" rx="4" />
    <text x="30" y="172" font-family="sans-serif" font-size="11" fill="#94A3B8">🛡 Roles y Permisos</text>
    <rect x="15" y="195" width="170" height="35" fill="none" rx="4" />
    <text x="30" y="217" font-family="sans-serif" font-size="11" fill="#94A3B8">📜 Logs de Auditoría</text>

    <!-- Contenido Principal -->
    <rect x="220" y="0" width="680" height="520" fill="#FFFFFF" stroke="#CBD5E1" rx="8" />
    <text x="245" y="35" font-family="sans-serif" font-weight="bold" font-size="15" fill="#0F172A">PANEL DE CONTROL GENERAL</text>

    <!-- Tarjetas KPI -->
    <rect x="245" y="60" width="190" height="70" fill="#F8FAFC" stroke="#E2E8F0" rx="6" />
    <text x="260" y="85" font-family="sans-serif" font-size="11" fill="#64748B">Total Casos</text>
    <text x="260" y="112" font-family="sans-serif" font-weight="bold" font-size="20" fill="#0F2A4A">25</text>

    <rect x="455" y="60" width="190" height="70" fill="#F8FAFC" stroke="#E2E8F0" rx="6" />
    <text x="470" y="85" font-family="sans-serif" font-size="11" fill="#64748B">Pistas Pendientes</text>
    <text x="470" y="112" font-family="sans-serif" font-weight="bold" font-size="20" fill="#D97706">04</text>

    <rect x="665" y="60" width="190" height="70" fill="#F8FAFC" stroke="#E2E8F0" rx="6" />
    <text x="680" y="85" font-family="sans-serif" font-size="11" fill="#64748B">Usuarios Activos</text>
    <text x="680" y="112" font-family="sans-serif" font-weight="bold" font-size="20" fill="#059669">18</text>

    <!-- Tabla de Usuarios -->
    <text x="245" y="165" font-family="sans-serif" font-weight="bold" font-size="12" fill="#0F172A">Usuarios del Sistema y Permisos:</text>
    <rect x="245" y="180" width="630" height="300" fill="#F8FAFC" stroke="#CBD5E1" rx="4" />
    <!-- Cabecera Tabla -->
    <rect x="245" y="180" width="630" height="30" fill="#E2E8F0" />
    <text x="260" y="200" font-family="sans-serif" font-weight="bold" font-size="10" fill="#334155">NOMBRE</text>
    <text x="420" y="200" font-family="sans-serif" font-weight="bold" font-size="10" fill="#334155">EMAIL</text>
    <text x="580" y="200" font-family="sans-serif" font-weight="bold" font-size="10" fill="#334155">ROL</text>
    <text x="720" y="200" font-family="sans-serif" font-weight="bold" font-size="10" fill="#334155">ACCIONES</text>

    <!-- Fila 1 -->
    <text x="260" y="235" font-family="sans-serif" font-size="10" fill="#0F172A">Admin General</text>
    <text x="420" y="235" font-family="sans-serif" font-size="10" fill="#64748B">admin@encuentrame.ni</text>
    <text x="580" y="235" font-family="sans-serif" font-size="10" font-weight="bold" fill="#EC4899">ADMIN</text>
    <text x="720" y="235" font-family="sans-serif" font-size="10" fill="#0D9488">[Editar]</text>

    <!-- Fila 2 -->
    <text x="260" y="270" font-family="sans-serif" font-size="10" fill="#0F172A">Lic. María Gómez</text>
    <text x="420" y="270" font-family="sans-serif" font-size="10" fill="#64748B">moderador1@encuentrame.ni</text>
    <text x="580" y="270" font-family="sans-serif" font-size="10" font-weight="bold" fill="#10B981">MODERADOR</text>
    <text x="720" y="270" font-family="sans-serif" font-size="10" fill="#0D9488">[Editar]</text>
  </g>
"""),
        ("WF_10_Panel_Moderacion.svg", "10. PANEL DE MODERACIÓN DE REPORTES Y PISTAS", "Equipo de Moderadores Humanos", """
  <g transform="translate(50, 80)">
    <rect x="0" y="0" width="900" height="520" fill="#FFFFFF" stroke="#CBD5E1" rx="8" />
    <text x="30" y="35" font-family="sans-serif" font-weight="bold" font-size="15" fill="#0F172A">BANDEJA DE MODERACIÓN Y CONTROL DE CALIDAD</text>

    <!-- Tabs -->
    <rect x="30" y="55" width="160" height="30" fill="#0D9488" rx="4" />
    <text x="110" y="74" font-family="sans-serif" font-weight="bold" font-size="11" fill="#FFFFFF" text-anchor="middle">Reportes Pendientes (3)</text>
    <rect x="200" y="55" width="160" height="30" fill="#F1F5F9" stroke="#CBD5E1" rx="4" />
    <text x="280" y="74" font-family="sans-serif" font-size="11" fill="#475569" text-anchor="middle">Pistas por Validar (4)</text>

    <!-- Caso en revisión activa -->
    <g transform="translate(30, 100)">
      <rect x="0" y="0" width="840" height="200" fill="#F8FAFC" stroke="#CBD5E1" rx="6" />
      <rect x="20" y="20" width="100" height="120" fill="#E2E8F0" stroke="#94A3B8" />
      <text x="70" y="80" font-family="sans-serif" font-size="10" fill="#64748B" text-anchor="middle">[ Foto Adjunta ]</text>

      <text x="140" y="40" font-family="sans-serif" font-weight="bold" font-size="14" fill="#0F172A">Expediente: EN-2026-0026 — Roberto Antonio López</text>
      <text x="140" y="65" font-family="sans-serif" font-size="11" fill="#334155">Reportante: Martha López (Madre) | Teléfono: +505 8888-0000</text>
      <text x="140" y="90" font-family="sans-serif" font-size="11" fill="#334155">Documento de Consentimiento Ley 787: [ Firmado y Adjunto ]</text>
      <text x="140" y="115" font-family="sans-serif" font-size="10.5" fill="#475569">Circunstancias: Visto por última vez en parada de buses Matagalpa hace 24 horas.</text>

      <!-- Botonera de Aprobación -->
      <rect x="520" y="145" width="140" height="35" fill="#DC2626" rx="4" />
      <text x="590" y="167" font-family="sans-serif" font-weight="bold" font-size="11" fill="#FFFFFF" text-anchor="middle">Rechazar con Motivo</text>

      <rect x="680" y="145" width="140" height="35" fill="#16A34A" rx="4" />
      <text x="750" y="167" font-family="sans-serif" font-weight="bold" font-size="11" fill="#FFFFFF" text-anchor="middle">Aprobar y Publicar</text>
    </g>

    <!-- Lista de Pistas Recibidas -->
    <text x="30" y="335" font-family="sans-serif" font-weight="bold" font-size="13" fill="#0F172A">Últimas Pistas Ciudadanas Recibidas:</text>
    <rect x="30" y="350" width="840" height="140" fill="#F8FAFC" stroke="#CBD5E1" rx="4" />
    <rect x="30" y="350" width="840" height="25" fill="#E2E8F0" />
    <text x="50" y="367" font-family="sans-serif" font-weight="bold" font-size="10" fill="#334155">FECHA</text>
    <text x="160" y="367" font-family="sans-serif" font-weight="bold" font-size="10" fill="#334155">CASO ASOCIADO</text>
    <text x="360" y="367" font-family="sans-serif" font-weight="bold" font-size="10" fill="#334155">DESCRIPCIÓN DE LA PISTA</text>
    <text x="750" y="367" font-family="sans-serif" font-weight="bold" font-size="10" fill="#334155">ESTADO</text>

    <text x="50" y="400" font-family="sans-serif" font-size="10" fill="#0F172A">19/11 14:20</text>
    <text x="160" y="400" font-family="sans-serif" font-size="10" fill="#0F172A">EN-2026-0001 (Sofía)</text>
    <text x="360" y="400" font-family="sans-serif" font-size="10" fill="#475569">Se observó persona de similares características en Mercado Huembes...</text>
    <text x="750" y="400" font-family="sans-serif" font-size="10" font-weight="bold" fill="#D97706">POR REVISAR</text>
  </g>
"""),
        ("WF_11_Seguimiento_Casos.svg", "11. SEGUIMIENTO DE CASOS REPORTADOS", "Familiar / Reportante (Estado: Integrado en Detalle/Panel)", """
  <!-- Nota de Estado Real -->
  <rect x="100" y="70" width="800" height="40" fill="#F1F5F9" stroke="#CBD5E1" rx="6" />
  <text x="500" y="95" font-family="sans-serif" font-size="11" fill="#475569" text-anchor="middle">ESTADO TÉCNICO: Integrado dentro del módulo de fichas individuales y panel de control con código EN-2026-XXXX.</text>

  <g transform="translate(150, 130)">
    <rect x="0" y="0" width="700" height="420" fill="#FFFFFF" stroke="#CBD5E1" rx="8" />
    <text x="40" y="40" font-family="sans-serif" font-weight="bold" font-size="15" fill="#0F172A">ESTADO DE TU REPORTE: EN-2026-0001</text>

    <!-- Línea de Tiempo del Expediente -->
    <g transform="translate(40, 70)">
      <circle cx="30" cy="30" r="12" fill="#16A34A" />
      <text x="30" y="34" font-family="sans-serif" font-size="10" font-weight="bold" fill="#FFFFFF" text-anchor="middle">✓</text>
      <text x="60" y="34" font-family="sans-serif" font-weight="bold" font-size="12" fill="#0F172A">1. Reporte Creado con Éxito (18/11/2026 10:00)</text>

      <line x1="30" y1="45" x2="30" y2="75" stroke="#16A34A" stroke-width="2" />

      <circle cx="30" cy="90" r="12" fill="#16A34A" />
      <text x="30" y="94" font-family="sans-serif" font-size="10" font-weight="bold" fill="#FFFFFF" text-anchor="middle">✓</text>
      <text x="60" y="94" font-family="sans-serif" font-weight="bold" font-size="12" fill="#0F172A">2. Verificado y Aprobado por Moderación (18/11/2026 12:30)</text>

      <line x1="30" y1="105" x2="30" y2="135" stroke="#0D9488" stroke-width="2" />

      <circle cx="30" cy="150" r="12" fill="#0D9488" />
      <text x="30" y="154" font-family="sans-serif" font-size="10" font-weight="bold" fill="#FFFFFF" text-anchor="middle">●</text>
      <text x="60" y="154" font-family="sans-serif" font-weight="bold" font-size="12" fill="#0D9488">3. Difusión Activa en Catálogo y Redes (En curso)</text>

      <line x1="30" y1="165" x2="30" y2="195" stroke="#CBD5E1" stroke-width="2" />

      <circle cx="30" cy="210" r="12" fill="#CBD5E1" />
      <text x="30" y="214" font-family="sans-serif" font-size="10" font-weight="bold" fill="#475569" text-anchor="middle">○</text>
      <text x="60" y="214" font-family="sans-serif" font-size="12" fill="#64748B">4. Cierre y Reunificación Familiar</text>
    </g>

    <!-- Pistas Recibidas Relacionadas -->
    <rect x="40" y="310" width="620" height="80" fill="#F8FAFC" stroke="#E2E8F0" rx="6" />
    <text x="60" y="335" font-family="sans-serif" font-weight="bold" font-size="11" fill="#0F172A">Pistas recibidas sobre este caso:</text>
    <text x="60" y="360" font-family="sans-serif" font-size="11" fill="#475569">El equipo de moderación ha canalizado 2 pistas preliminares a las instancias de apoyo.</text>
  </g>
"""),
        ("WF_12_Gestion_Fotografias.svg", "12. GESTIÓN Y SANITIZACIÓN DE FOTOGRAFÍAS", "Reportante / Moderador (Componente Especializado)", """
  <g transform="translate(150, 80)">
    <rect x="0" y="0" width="700" height="520" fill="#FFFFFF" stroke="#CBD5E1" rx="8" />
    <text x="40" y="35" font-family="sans-serif" font-weight="bold" font-size="15" fill="#0F172A">MÓDULO DE CARGA Y GESTIÓN SEGURA DE FOTOGRAFÍAS</text>

    <!-- Zona Drag & Drop -->
    <rect x="40" y="60" width="620" height="150" fill="#F8FAFC" stroke="#94A3B8" stroke-dasharray="6,6" rx="8" />
    <circle cx="350" cy="115" r="22" fill="#E2E8F0" />
    <text x="350" y="122" font-family="sans-serif" font-size="20" fill="#0D9488" text-anchor="middle">📷</text>
    <text x="350" y="160" font-family="sans-serif" font-size="12" font-weight="bold" fill="#1E293B" text-anchor="middle">Arrastra la fotografía aquí o haz clic para seleccionar</text>
    <text x="350" y="180" font-family="sans-serif" font-size="10" fill="#64748B" text-anchor="middle">Formatos admitidos: JPEG, PNG, WebP (Máx: 5MB)</text>

    <!-- Vista Previa y Controles -->
    <text x="40" y="240" font-family="sans-serif" font-weight="bold" font-size="12" fill="#0F172A">Vista Previa y Recorte Centrado:</text>
    <rect x="40" y="255" width="160" height="190" fill="#E2E8F0" stroke="#94A3B8" rx="6" />
    <text x="120" y="350" font-family="sans-serif" font-size="10" fill="#475569" text-anchor="middle">[ Vista Previa WebP ]</text>

    <!-- Checklist de Seguridad Técnica -->
    <g transform="translate(225, 255)">
      <rect x="0" y="0" width="435" height="190" fill="#F8FAFC" stroke="#E2E8F0" rx="6" />
      <text x="20" y="30" font-family="sans-serif" font-weight="bold" font-size="11" fill="#0F172A">Validaciones Automáticas OWASP / Backend:</text>
      <text x="20" y="60" font-family="sans-serif" font-size="10.5" fill="#16A34A">✔ Conversión y compresión a WebP (resolución optimizada)</text>
      <text x="20" y="85" font-family="sans-serif" font-size="10.5" fill="#16A34A">✔ Sanitización de metadatos EXIF (eliminación de GPS/cámara)</text>
      <text x="20" y="110" font-family="sans-serif" font-size="10.5" fill="#16A34A">✔ Verificación de tipo MIME contra inyección de ejecutables</text>
      <text x="20" y="135" font-family="sans-serif" font-size="10.5" fill="#16A34A">✔ Nombre de archivo generado mediante hash UUIDv4</text>
      <text x="20" y="165" font-family="sans-serif" font-size="10.5" fill="#0F2A4A">✔ Servido mediante endpoint estático con caché HTTP</text>
    </g>

    <!-- Botón Confirmar Carga -->
    <rect x="40" y="465" width="220" height="35" fill="#0D9488" rx="4" />
    <text x="150" y="487" font-family="sans-serif" font-weight="bold" font-size="11" fill="#FFFFFF" text-anchor="middle">Confirmar y Guardar Imagen</text>
  </g>
""")
    ]

    for fname, title, user_target, inner in wireframes:
        svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1000 680" width="100%" height="100%">
  <defs>
    <style>
      .bg {{ fill: #F1F5F9; }}
      .header-title {{ font-family: 'Segoe UI', Inter, sans-serif; font-size: 16px; font-weight: bold; fill: #0F2A4A; }}
      .header-sub {{ font-family: 'Segoe UI', Inter, sans-serif; font-size: 11px; fill: #64748B; }}
      .badge-ret {{ fill: #FEF3C7; stroke: #F59E0B; rx: 4; }}
    </style>
  </defs>

  <!-- Canvas Background -->
  <rect width="1000" height="680" class="bg" />

  <!-- Wireframe Frame Header -->
  <rect x="50" y="20" width="900" height="45" fill="#FFFFFF" stroke="#CBD5E1" rx="6" />
  <text x="70" y="47" class="header-title">WIREFRAME: {title}</text>
  <text x="600" y="47" class="header-sub">Usuario Objetivo: {user_target}</text>

  <!-- Contenido Específico del Wireframe -->
  {inner}

  <!-- Footer Wireframe -->
  <text x="500" y="660" font-family="sans-serif" font-size="10" fill="#94A3B8" text-anchor="middle">Encuéntrame Nicaragua — Documentación Visual Académica — Reconstrucción Retrospectiva y Modelo de Interfaz</text>
</svg>"""
        create_svg(os.path.join(WF_DIR, fname), svg)

if __name__ == "__main__":
    generate_navigation_map()
    generate_user_journeys()
    generate_wireframes()
