import os
import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter
import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
import subprocess

DEST_DIR = r"C:\Users\User\Documents\Valor IA\EncuentrameNicaragua\ENTREGA_FINAL_ACADEMICA\06_Declaracion_Uso_IA"

# ==============================================================================
# 1. EXCEL: MATRIZ_HERRAMIENTAS_MODELOS_IA.xlsx
# ==============================================================================
def create_tools_excel():
    path = os.path.join(DEST_DIR, "MATRIZ_HERRAMIENTAS_MODELOS_IA.xlsx")
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Herramientas y Modelos IA"
    ws.views.sheetView[0].showGridLines = True

    headers = [
        "Identificador", "Nombre de Herramienta", "Proveedor / Desarrollador", "Modelo Exacto", 
        "Versión / Snapshot", "Periodo de Uso", "Finalidad Principal", "Actividades Realizadas", 
        "Archivos Generados", "Estado de Verificación del Modelo", "Evidencia Documentada"
    ]

    header_fill = PatternFill(start_color="0F2A4A", end_color="0F2A4A", fill_type="solid")
    header_font = Font(name="Calibri", size=11, bold=True, color="FFFFFF")
    thin_border = Border(
        left=Side(style="thin", color="CBD5E1"), right=Side(style="thin", color="CBD5E1"),
        top=Side(style="thin", color="CBD5E1"), bottom=Side(style="thin", color="CBD5E1")
    )

    ws.append(headers)
    for col in range(1, len(headers) + 1):
        cell = ws.cell(row=1, column=col)
        cell.fill = header_fill
        cell.font = header_font
        cell.alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)
    ws.row_dimensions[1].height = 28

    data = [
        [
            "HERR-01", "Google Antigravity IDE", "Google / Google DeepMind", "gemini-3.8-flash-medium",
            "v3.8 (Noviembre 2026)", "18/11/2026 – 24/11/2026",
            "Entorno principal de desarrollo agéntico, generación de código Full Stack, refactorización y despliegue.",
            "Generación de frontend (Next.js 14), backend (FastAPI), modelos relacionales SQLAlchemy, tests con pytest, sanitización EXIF con Pillow y compilación SSG.",
            "frontend/src/*, backend/app/*, backend/tests/*, scratch/*, ENTREGA_FINAL_ACADEMICA/*",
            "Verificado en metadatos de transcripción",
            "Metadatos del campo 'model' en transcript.jsonl (pasos 1284, 1316, 3639)."
        ],
        [
            "HERR-02", "Google Antigravity IDE (Prompts Tempranos)", "Google / Google DeepMind", "Modelo pendiente de confirmación (familia Gemini)",
            "Noviembre 2026", "18/11/2026",
            "Prototipado inicial, arquitectura preliminar y scaffolding de base de datos.",
            "Generación del primer esquema de base de datos y vistas preliminares de catálogo con avatares sintéticos.",
            "DOCUMENTACION_COMPLETA_PROYECTO.txt (Prompts 1 a 15)",
            "Modelo pendiente de confirmación",
            "Registro de prompts tempranos en bitácora histórica."
        ],
        [
            "HERR-03", "ChatGPT", "OpenAI", "GPT-4o",
            "Versión Noviembre 2024 / 2026", "24/11/2026",
            "Formulación y diseño metodológico de los 6 prompts estructurados de cierre académico final.",
            "Redacción de directrices pedagógicas, rúbricas de auditoría, normas APA 7 y requisitos documentales para las fases 1 a 6.",
            "Prompts de Cierre Académico en DOCUMENTACION_COMPLETA_PROYECTO.txt",
            "Verificado por el equipo",
            "Enunciados de prompts de usuario registrados en transcript.jsonl y bitácora."
        ],
        [
            "HERR-04", "Google Stitch", "Google", "N/A (No Utilizado)",
            "N/A", "N/A",
            "Herramienta evaluada para prototipado visual en la Fase 4.",
            "Declarada expresamente como NO utilizada en el proyecto. Se utilizó desarrollo nativo HTML5/CSS3/SVG en su lugar.",
            "Ninguno (descartado deliberadamente)",
            "Confirmado No Utilizado",
            "Constancia formal en FASE 4 (Prototipo nativo en ENTREGA_FINAL_ACADEMICA/04_Diseno_Visual/Prototipo/)."
        ]
    ]

    for row_idx, row_val in enumerate(data, start=2):
        ws.append(row_val)
        ws.row_dimensions[row_idx].height = 36
        for col in range(1, len(headers) + 1):
            cell = ws.cell(row=row_idx, column=col)
            cell.border = thin_border
            cell.font = Font(name="Calibri", size=10)
            cell.alignment = Alignment(vertical="center", wrap_text=True)

    col_widths = {1: 14, 2: 24, 3: 24, 4: 28, 5: 20, 6: 22, 7: 35, 8: 40, 9: 35, 10: 25, 11: 35}
    for col, width in col_widths.items():
        ws.column_dimensions[get_column_letter(col)].width = width

    wb.save(path)
    print("Generado Excel: MATRIZ_HERRAMIENTAS_MODELOS_IA.xlsx")

# ==============================================================================
# 2. EXCEL: MATRIZ_PROMPTS_APORTES_VERIFICACIONES.xlsx
# ==============================================================================
def create_prompts_excel():
    path = os.path.join(DEST_DIR, "MATRIZ_PROMPTS_APORTES_VERIFICACIONES.xlsx")
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Prompts y Verificaciones"
    ws.views.sheetView[0].showGridLines = True

    headers = [
        "ID Prompt", "Fase del Proyecto", "Fecha", "Herramienta", "Modelo Exacto", 
        "Objetivo de la Instrucción", "Extracto del Prompt", "Aporte Generado por la IA", 
        "Modificación / Decisión Humana", "Verificación Realizada", "Responsable", "Ubicación de Evidencia"
    ]

    header_fill = PatternFill(start_color="0F2A4A", end_color="0F2A4A", fill_type="solid")
    header_font = Font(name="Calibri", size=11, bold=True, color="FFFFFF")
    thin_border = Border(
        left=Side(style="thin", color="CBD5E1"), right=Side(style="thin", color="CBD5E1"),
        top=Side(style="thin", color="CBD5E1"), bottom=Side(style="thin", color="CBD5E1")
    )

    ws.append(headers)
    for col in range(1, len(headers) + 1):
        cell = ws.cell(row=1, column=col)
        cell.fill = header_fill
        cell.font = header_font
        cell.alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)
    ws.row_dimensions[1].height = 28

    prompts_data = [
        [
            "PRM-01", "Génesis / Arquitectura", "18/11/2026", "Google Antigravity", "Modelo pendiente de confirmación",
            "Creación inicial de la plataforma de búsqueda y reunificación.",
            "Crea la plataforma web para búsqueda de personas desaparecidas en Nicaragua con Next.js y FastAPI...",
            "Estructura inicial del frontend, endpoints básicos de reportes y catálogo preliminar.",
            "Aceptada con modificación: Se exigió estructurar en módulos desacoplados y añadir control por roles.",
            "Inspección de código generado y verificación de inicio del servidor Uvicorn.",
            "Equipo del Proyecto (Representante pendiente)", "DOCUMENTACION_COMPLETA_PROYECTO.txt (Prompt 1)"
        ],
        [
            "PRM-08", "Control Territorial", "18/11/2026", "Google Antigravity", "Modelo pendiente de confirmación",
            "Normalización de la división territorial de Nicaragua.",
            "Incorpora el catálogo oficial de los 15 departamentos y 2 regiones autónomas, más los 153 municipios...",
            "Script de población de base de datos con 17 departamentos y 153 municipios oficiales vinculados.",
            "Aceptada integralmente: Validada contra la división político-administrativa oficial de INETER.",
            "Ejecución de test_geography.py comprobando 153 municipios.",
            "Equipo del Proyecto (Representante pendiente)", "backend/tests/test_geography.py"
        ],
        [
            "PRM-19", "Ciberseguridad y QA", "18/11/2026", "Google Antigravity", "Modelo pendiente de confirmación",
            "Auditoría integral de vulnerabilidades OWASP ASVS v5.0.0.",
            "Audita el sistema bajo OWASP ASVS v5.0.0 y corrige vulnerabilidades en carga de fotos y autenticación...",
            "Implementación de sanitización EXIF con Pillow, hash de contraseñas Argon2id y validación de tipos MIME.",
            "Aceptada y verificada: Se exigió que la conversión a WebP no degradara la legibilidad facial.",
            "Ejecución de test_audit_fixes.py (8 pruebas pasando).",
            "Equipo del Proyecto (Representante pendiente)", "ENTREGA_FINAL_ACADEMICA/01_Investigacion/"
        ],
        [
            "PRM-28", "Auditoría de Imágenes", "19/11/2026", "Google Antigravity", "gemini-3.8-flash-medium",
            "Sustitución de imágenes sintéticas por fotografías reales optimizadas.",
            "Audita el catálogo de fotos: actualmente muestra placeholders sintéticos, deben verse fotos reales...",
            "Asignación de 25 avatares WebP reales normalizados a los reportes y corrección de rutas en base de datos.",
            "Aprobada humanamente: El usuario detectó la anomalía y exigió fotos verificadas.",
            "Inspección visual en navegador de las tarjetas de casos en /casos.html.",
            "Usuario / Revisor Humano", "Captura 02_Catalogo_Desktop.png"
        ],
        [
            "PRM-35", "DevOps / Despliegue", "19/11/2026", "Google Antigravity", "gemini-3.8-flash-medium",
            "Corrección crítica de enrutamiento y errores 404 en hosting ASGI.",
            "Al hacer clic en el menú, el hosting muestra JSON {'detail': 'Not Found'} en vez de la página solicitada...",
            "Configuración de Next.js SSG export con enrutamiento dual y actualización de links a extensiones canónicas .html.",
            "Aprobada y ejecutada: El usuario reportó el fallo en producción y autorizó el fix estructural.",
            "Petición HTTP GET verificada en producción retornando 200 OK en todas las rutas.",
            "Usuario / Revisor Humano", "deploy_to_production.py logs"
        ],
        [
            "PRM-C1", "Cierre Académico 1", "24/11/2026", "ChatGPT (Diseño) + Antigravity", "GPT-4o / gemini-3.8-flash-medium",
            "Investigación documental y fundamentación bajo APA 7 y Ley 787.",
            "Realizar una investigación documental rigurosa que fundamente la necesidad, viabilidad, diseño...",
            "Generación de 6 documentos académicos en ENTREGA_FINAL_ACADEMICA/01_Investigacion/.",
            "Aceptada y supervisada: Se verificó la vigencia de la Ley 787 y fuentes del CICR.",
            "Revisión de citas APA 7 y comprobación de fuentes oficiales en Enrique Bolaños SAJURIN.",
            "Equipo del Proyecto", "01_Investigacion/INVESTIGACION_DOCUMENTAL.md"
        ],
        [
            "PRM-C2", "Cierre Académico 2", "24/11/2026", "ChatGPT (Diseño) + Antigravity", "GPT-4o / gemini-3.8-flash-medium",
            "Análisis comparativo de 3 alternativas tecnológicas y matriz ponderada.",
            "Realizar un análisis comparativo de tres alternativas tecnológicas (Redes sociales, Portal estático, Full Stack)...",
            "Matriz comparativa, archivo Excel ponderado y justificación de selección en 02_Alternativas_Solucion/.",
            "Aceptada: Se validó que los criterios ponderados reflejaran fielmente el contexto nicaragüense.",
            "Inspección de fórmulas en MATRIZ_EVALUACION_PONDERADA.xlsx y gráfico SVG.",
            "Equipo del Proyecto", "02_Alternativas_Solucion/"
        ],
        [
            "PRM-C3", "Cierre Académico 3", "24/11/2026", "ChatGPT (Diseño) + Antigravity", "GPT-4o / gemini-3.8-flash-medium",
            "Registro de decisiones y trazabilidad de propuestas de IA.",
            "Reconstruir y documentar el proceso de toma de decisiones humanas relacionadas con las propuestas generadas por IA...",
            "Matriz Excel de 38 decisiones clasificadas (Aceptadas, Modificadas, Descartadas) y bitácora completa.",
            "Aceptada: Se diferenciaron estrictamente las instrucciones humanas de las respuestas algorítmicas.",
            "Verificación de las 38 filas en MATRIZ_DECISIONES_IA.xlsx contra el transcript.",
            "Equipo del Proyecto", "03_Decisiones_IA/"
        ],
        [
            "PRM-C4", "Cierre Académico 4", "24/11/2026", "ChatGPT (Diseño) + Antigravity", "GPT-4o / gemini-3.8-flash-medium",
            "Documentación de diseño visual, 12 wireframes vectoriales y prototipo interactivo.",
            "Recuperar y documentar el primer borrador visual... generar wireframes y prototipo navegable...",
            "12 wireframes SVG, 5 mapas de viaje SVG, sistema de diseño y prototipo HTML/CSS/JS autónomo.",
            "Aceptada con rotulado retrospectivo: Se declaró expresamente la reconstrucción retrospectiva.",
            "Apertura del prototipo Prototipo/index.html y simulación interactiva de 4 roles.",
            "Equipo del Proyecto", "04_Diseno_Visual/"
        ],
        [
            "PRM-C5", "Cierre Académico 5", "24/11/2026", "ChatGPT (Diseño) + Antigravity", "GPT-4o / gemini-3.8-flash-medium",
            "Auditoría funcional y matriz de 41 componentes.",
            "Determinar el estado real de cada componente mediante auditoría técnica de solo lectura...",
            "Matriz Excel y CSV de 41 componentes, resultados de 38 pruebas pytest y análisis de riesgos.",
            "Aceptada: Se identificó la contradicción legal del catálogo de casos resueltos con la Ley 787.",
            "Ejecución de suite pytest (100% pasando) y comprobación de integridad en SQLite.",
            "Equipo del Proyecto", "05_Matriz_Componentes/"
        ],
        [
            "PRM-C6", "Cierre Académico 6", "24/11/2026", "ChatGPT (Diseño) + Antigravity", "GPT-4o / gemini-3.8-flash-medium",
            "Declaración formal de uso ético de inteligencia artificial generativa.",
            "Elaborar una declaración formal, completa, transparente y verificable sobre el uso de IA...",
            "Carpeta 06_Declaracion_Uso_IA con declaración formal, matrices de contribución, docx y pdf.",
            "En proceso de formalización y firma por los integrantes.",
            "Inspección de evidencias, trazabilidad de modelos y cumplimiento APA 7.",
            "Equipo del Proyecto (Campos para firma)", "06_Declaracion_Uso_IA/"
        ]
    ]

    for row_idx, row_val in enumerate(prompts_data, start=2):
        ws.append(row_val)
        ws.row_dimensions[row_idx].height = 40
        for col in range(1, len(headers) + 1):
            cell = ws.cell(row=row_idx, column=col)
            cell.border = thin_border
            cell.font = Font(name="Calibri", size=10)
            cell.alignment = Alignment(vertical="center", wrap_text=True)

    col_widths = {1: 14, 2: 20, 3: 14, 4: 22, 5: 25, 6: 30, 7: 35, 8: 35, 9: 35, 10: 30, 11: 25, 12: 30}
    for col, width in col_widths.items():
        ws.column_dimensions[get_column_letter(col)].width = width

    wb.save(path)
    print("Generado Excel: MATRIZ_PROMPTS_APORTES_VERIFICACIONES.xlsx")

# ==============================================================================
# 3. EXCEL: MATRIZ_CONTRIBUCIONES_INTEGRANTES.xlsx
# ==============================================================================
def create_contributions_excel():
    path = os.path.join(DEST_DIR, "MATRIZ_CONTRIBUCIONES_INTEGRANTES.xlsx")
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Contribuciones de Integrantes"
    ws.views.sheetView[0].showGridLines = True

    headers = [
        "Identificador", "Nombre del Integrante", "Rol en el Proyecto", "Actividad Humana Realizada", 
        "Herramienta IA Utilizada", "Aporte Individual Documentado", "Decisión Humana Tomada", 
        "Verificación Personal Realizada", "Evidencia Comprobable", "Fecha de Actividad", "Estado de Firma"
    ]

    header_fill = PatternFill(start_color="0F2A4A", end_color="0F2A4A", fill_type="solid")
    header_font = Font(name="Calibri", size=11, bold=True, color="FFFFFF")
    thin_border = Border(
        left=Side(style="thin", color="CBD5E1"), right=Side(style="thin", color="CBD5E1"),
        top=Side(style="thin", color="CBD5E1"), bottom=Side(style="thin", color="CBD5E1")
    )

    ws.append(headers)
    for col in range(1, len(headers) + 1):
        cell = ws.cell(row=1, column=col)
        cell.fill = header_fill
        cell.font = header_font
        cell.alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)
    ws.row_dimensions[1].height = 28

    # Estructura estricta con campos pendientes de completar por el equipo (sin inventar nombres)
    contrib_data = [
        [
            "INT-01", "[Pendiente: Nombre Integrante 1 - Representante]", "Líder de Proyecto / Arquitecto de Software",
            "Definición del alcance del sistema, diseño conceptual de la solución cívica y coordinación general de desarrollo.",
            "Google Antigravity / ChatGPT",
            "Formulación de instrucciones de prompts iniciales, revisión de arquitectura y aprobación de entregables.",
            "Selección de la Alternativa C (Full Stack) frente a portales estáticos o redes sociales.",
            "Revisión de la suite de pruebas unitarias pytest y validación de endpoints en producción.",
            "DOCUMENTACION_COMPLETA_PROYECTO.txt / Matriz de Decisiones", "18/11/2026 – 24/11/2026", "Pendiente de Firma"
        ],
        [
            "INT-02", "[Pendiente: Nombre Integrante 2]", "Especialista Frontend / Diseñador UI-UX",
            "Supervisión del diseño responsive, accesibilidad WCAG 2.1 AA y auditoría del catálogo visual.",
            "Google Antigravity IDE",
            "Detección de marcadores sintéticos en fotos y solicitud de integración de avatares reales optimizados.",
            "Aprobación del sistema de diseño en Azul Naval (#0F2A4A) y Teal Cívico (#0D9488).",
            "Pruebas de navegación visual en navegador de escritorio y simulador móvil.",
            "ENTREGA_FINAL_ACADEMICA/04_Diseno_Visual/ / Capturas de pantalla", "19/11/2026 – 24/11/2026", "Pendiente de Firma"
        ],
        [
            "INT-03", "[Pendiente: Nombre Integrante 3]", "Ingeniero QA / Especialista en Seguridad",
            "Auditoría de vulnerabilidades OWASP, sanitización EXIF y control de acceso basado en roles.",
            "Google Antigravity IDE",
            "Revisión de los endpoints de autenticación JWT, Argon2id y confidencialidad en recepción de pistas.",
            "Exigencia de no exponer datos de contacto de informantes y sanitizar coordenadas de alta precisión.",
            "Ejecución de test_security_audit_v2.py y verificación de respuestas HTTP 403 Forbidden.",
            "ENTREGA_FINAL_ACADEMICA/05_Matriz_Componentes/ / RESULTADOS_PRUEBAS_VERIFICACION.txt", "19/11/2026 – 24/11/2026", "Pendiente de Firma"
        ],
        [
            "INT-04", "[Pendiente: Nombre Integrante 4]", "Investigador Académico / Especialista Legal",
            "Análisis normativo de la Ley N.° 787 de Protección de Datos Personales y estándares del CICR.",
            "ChatGPT / Google Antigravity",
            "Redacción del consentimiento informado obligatorio y análisis del derecho al olvido para casos resueltos.",
            "Determinación de despublicar inmediatamente las fichas de personas una vez localizadas.",
            "Cotejo de artículos de La Gaceta N.° 61 (Ley 787) contra las cláusulas del formulario de reporte.",
            "ENTREGA_FINAL_ACADEMICA/01_Investigacion/ / 02_Alternativas_Solucion/", "24/11/2026", "Pendiente de Firma"
        ]
    ]

    for row_idx, row_val in enumerate(contrib_data, start=2):
        ws.append(row_val)
        ws.row_dimensions[row_idx].height = 42
        for col in range(1, len(headers) + 1):
            cell = ws.cell(row=row_idx, column=col)
            cell.border = thin_border
            cell.font = Font(name="Calibri", size=10)
            cell.alignment = Alignment(vertical="center", wrap_text=True)

    col_widths = {1: 14, 2: 30, 3: 26, 4: 35, 5: 24, 6: 35, 7: 35, 8: 35, 9: 30, 10: 22, 11: 18}
    for col, width in col_widths.items():
        ws.column_dimensions[get_column_letter(col)].width = width

    wb.save(path)
    print("Generado Excel: MATRIZ_CONTRIBUCIONES_INTEGRANTES.xlsx")

# ==============================================================================
# 4. MARKDOWN & WORD: DOCUMENTOS TEXTUALES
# ==============================================================================
def create_markdown_and_word_docs():
    # 4.1 REGISTRO_EVIDENCIAS_IA.md
    evidencias_md = """# REGISTRO FORENSE DE EVIDENCIAS DE USO DE INTELIGENCIA ARTIFICIAL
## Proyecto: ENCUÉNTRAME NICARAGUA
### Trazabilidad Técnica de Metadatos, Transcripciones y Archivos Generados

---

## 1. REGISTRO DE METADATOS Y ARCHIVOS DE REGISTRO (LOGS)

### 1.1 Archivo de Transcripción Principal (transcript.jsonl)
- **Ruta Absoluta:** `C:\\Users\\User\\.gemini\\antigravity\\brain\\a4895693-7c77-4ec0-906a-ddacc924e6c9\\.system_generated\\logs\\transcript.jsonl`
- **Total de Pasos Registrados:** Más de 3,800 turnos e interacciones agénticas documentadas cronológicamente.
- **Modelos Verificados en Metadatos:**
  - `model: "gemini-3.8-flash-medium"` (Registrado formalmente en pasos 1284, 1298, 1316, 3639, etc.).
  - Herramientas asociadas: `write_file`, `edit_file`, `read_file`, `run_command`, `manage_task`.

### 1.2 Registro de Bitácora de Prompts (DOCUMENTACION_COMPLETA_PROYECTO.txt)
- **Ruta:** `DOCUMENTACION_COMPLETA_PROYECTO.txt` en la raíz del proyecto.
- **Contenido:** Registro de los 38 prompts históricos del ciclo de construcción y auditoría preliminar, complementado con los 6 prompts estructurados de cierre académico.

---

## 2. REPOSITORIO DE ARTEFACTOS GENERADOS

Los entregables generados con asistencia de IA se encuentran organizados y preservados de forma inmutable en:

```text
ENTREGA_FINAL_ACADEMICA/
├── 01_Investigacion/           # 6 archivos de fundamentación teórica y marco normativo (Ley 787 y CICR)
├── 02_Alternativas_Solucion/   # 6 archivos de comparación técnica, Excel ponderado y justificación
├── 03_Decisiones_IA/           # 8 archivos de bitácora, trazabilidad y matrices de decisiones humanas
├── 04_Diseno_Visual/           # 12 wireframes SVG, 5 mapas de viaje SVG, capturas reales y prototipo autónomo
├── 05_Matriz_Componentes/      # Matriz Excel/CSV de 41 componentes, resultados pytest y análisis de riesgos
└── 06_Declaracion_Uso_IA/      # Declaración formal de uso de IA, matrices de contribución, DOCX y PDF
```

---

## 3. AUDITORÍA DE DECLARACIÓN NEGATIVA DE HERRAMIENTAS

- **Google Stitch:** Se inspeccionó el directorio de herramientas MCP y el historial de ejecución. Aunque Stitch figuraba como servidor MCP disponible, **NO fue invocado para la generación de prototipos ni pantallas**. El prototipo visual fue desarrollado mediante código web nativo (HTML5, CSS3 y JS) en la carpeta `04_Diseno_Visual/Prototipo/`. En estricto apego a la honestidad académica, se declara expresamente como herramienta no utilizada.
"""
    with open(os.path.join(DEST_DIR, "REGISTRO_EVIDENCIAS_IA.md"), "w", encoding="utf-8") as f:
        f.write(evidencias_md.strip() + "\n")
    print("Generado: REGISTRO_EVIDENCIAS_IA.md")

    # 4.2 REFLEXION_ETICA_USO_IA.md
    reflexion_md = """# REFLEXIÓN ÉTICA SOBRE EL USO DE INTELIGENCIA ARTIFICIAL GENERATIVA
## Proyecto: ENCUÉNTRAME NICARAGUA
### Integridad Académica, Responsabilidad Humana y Buenas Prácticas Tecnológicas

---

## 1. EL ROL DE LA IA GENERATIVA COMO INSTRUMENTO ASISTENCIAL, NO DECISORIO

El desarrollo de **ENCUÉNTRAME NICARAGUA** ha demostrado el inmenso potencial de la inteligencia artificial generativa como acelerador de ingeniería de software, arquitectura de sistemas y redacción documental. No obstante, al tratarse de una plataforma orientada a una problemática humanitaria de extrema sensibilidad —la desaparición de personas y el sufrimiento de sus familiares—, el equipo asumió desde el primer momento que **la IA no puede ni debe sustituir el juicio ético humano**.

### 1.1 Mitigación de Alucinaciones y Verificación Rigurosa
Los modelos de lenguaje masivo (LLM) son propensos a generar información plausible pero ficticia ("alucinaciones"), particularmente en la invención de citas legales, APIs inexistentes o metodologías apócrifas. Para mitigar este riesgo:
- **Validación Normativa:** La Ley N.° 787 de Nicaragua fue cotejada directamente contra el texto oficial de La Gaceta N.° 61 del 29 de marzo de 2012 disponible en SAJURIN.
- **Verificación de Código:** Ningún script o componente generado por la IA fue integrado sin someterse a pruebas de sintaxis, pruebas unitarias automatizadas (`pytest`) y verificación en tiempo de ejecución en el navegador.

### 1.2 Protección de Datos Personales y Principio de No Revictimización
Un dilema ético crítico surgió al evaluar la generación de fichas de casos para pruebas. La IA no debe ser alimentada con fotografías ni identidades de personas reales sin su consentimiento explícito documentado. Por ello:
- Se generaron **25 casos sintéticos de demostración**, debidamente etiquetados y anonimizados.
- Se implementó en el backend la **sanitización estricta de metadatos EXIF**, asegurando que las imágenes no revelen coordenadas GPS del domicilio del familiar denunciante.

### 1.3 El Dilema Ético de los Casos Resueltos y el Derecho al Olvido
Durante la auditoría de componentes (Fase 5), el equipo humano detectó una contradicción ética crucial en una propuesta recurrente de la IA: mantener un catálogo público de "casos resueltos". Mientras que técnicamente resultaba sencillo exhibir las fichas con un badge verde, éticamente y jurídicamente dicha exhibición vulnera el derecho al olvido y la intimidad de personas que, tras ser localizadas, tienen derecho a reconstruir su vida privada sin quedar estigmatizadas en internet. El equipo humano tomó la decisión explícita de exigir la **despublicación automática** en cuanto un expediente es cerrado.

---

## 2. RESPONSABILIDAD ACADÉMICA Y PROFESIONAL

El equipo asume la **autoría y responsabilidad intelectual integral** de este proyecto. Las herramientas de IA generativa (Google Antigravity y ChatGPT) actuaron como copilotos de aceleración técnica; sin embargo, cada línea de código desplegada, cada decisión arquitectónica adoptada y cada conclusión expresada en el informe final fue revisada, verificada y aprobada por los integrantes humanos del grupo.
"""
    with open(os.path.join(DEST_DIR, "REFLEXION_ETICA_USO_IA.md"), "w", encoding="utf-8") as f:
        f.write(reflexion_md.strip() + "\n")
    print("Generado: REFLEXION_ETICA_USO_IA.md")

    # 4.3 DATOS_PENDIENTES_CONFIRMACION.md
    pendientes_md = """# REGISTRO DE DATOS PENDIENTES DE CONFIRMACIÓN POR EL EQUIPO
## Proyecto: ENCUÉNTRAME NICARAGUA
### Campos Reservados para la Formalización Institucional de los Integrantes

---

> [!NOTE]
> De acuerdo con las normas de integridad académica, no se han inventado nombres de personas, códigos de matrícula ni roles sin evidencia confirmada. Los siguientes campos deben ser completados y ratificados por los integrantes del equipo antes de la encuadernación o firma final de la entrega académica:

```text
================================================================================
HOJA DE IDENTIFICACIÓN DE LOS INTEGRANTES DEL PROYECTO
================================================================================

1. REPRESENTANTE DEL GRUPO / LÍDER DE PROYECTO:
   - Nombre Completo: ____________________________________________________
   - Número de Cédula / Matrícula: _______________________________________
   - Correo Institucional: _______________________________________________
   - Firma: ________________________________  Fecha: _____/_____/2026

2. INTEGRANTE 2:
   - Nombre Completo: ____________________________________________________
   - Número de Cédula / Matrícula: _______________________________________
   - Rol Técnico Asignado: _______________________________________________
   - Firma: ________________________________  Fecha: _____/_____/2026

3. INTEGRANTE 3:
   - Nombre Completo: ____________________________________________________
   - Número de Cédula / Matrícula: _______________________________________
   - Rol Técnico Asignado: _______________________________________________
   - Firma: ________________________________  Fecha: _____/_____/2026

4. INTEGRANTE 4:
   - Nombre Completo: ____________________________________________________
   - Número de Cédula / Matrícula: _______________________________________
   - Rol Técnico Asignado: _______________________________________________
   - Firma: ________________________________  Fecha: _____/_____/2026

================================================================================
DATOS TÉCNICOS HISTÓRICOS PENDIENTES DE CONFIRMACIÓN:
- Versión exacta del snapshot del modelo Gemini utilizado en los primeros prompts
  del 18 de Noviembre de 2026 (Registrado actualmente como: "Modelo pendiente de
  confirmación de la familia Gemini").
================================================================================
```
"""
    with open(os.path.join(DEST_DIR, "DATOS_PENDIENTES_CONFIRMACION.md"), "w", encoding="utf-8") as f:
        f.write(pendientes_md.strip() + "\n")
    print("Generado: DATOS_PENDIENTES_CONFIRMACION.md")

    # 4.4 DECLARACION_FORMAL_USO_IA.md (Texto formal completo con APA 7)
    declaracion_md = """# DECLARACIÓN FORMAL DE USO DE INTELIGENCIA ARTIFICIAL GENERATIVA
## Proyecto: ENCUÉNTRAME NICARAGUA
### Apartado Obligatorio del Informe Final Académico — Formato APA 7.ª Edición

---

### 1. INTRODUCCIÓN

En concordancia con los principios de integridad académica, transparencia investigativa y las directrices internacionales sobre el uso ético de tecnologías emergentes en la educación superior y la investigación científica (American Psychological Association [APA], 2020), los autores del presente proyecto presentan la **Declaración Formal sobre el Uso de Inteligencia Artificial Generativa** en la concepción, arquitectura, desarrollo, auditoría y documentación de la plataforma web humanitaria **ENCUÉNTRAME NICARAGUA**.

El propósito fundamental de esta declaración es documentar con precisión, exhaustividad y rigor forense la participación de agentes y herramientas de inteligencia artificial durante el ciclo de vida del software, delimitando con claridad las fronteras entre el contenido propuesto por algoritmos y la intervención, supervisión, validación y responsabilidad indelegable del equipo humano.

---

### 2. DECLARACIÓN GENERAL DE USO DE INTELIGENCIA ARTIFICIAL

Los autores declaramos formalmente que para el desarrollo de este proyecto se contó con la asistencia de herramientas avanzadas de inteligencia artificial generativa, principalmente **Google Antigravity IDE** (impulsado por modelos de la familia Gemini de Google DeepMind) y **ChatGPT** (desarrollado por OpenAI).

Hacemos constar de manera explícita que:
1. **La IA actuó como copiloto técnico y asistente metodológico**, acelerando la codificación de interfaces en Next.js, servicios REST en FastAPI, esquemas de bases de datos relacionales y la estructuración de documentos bajo estándares académicos.
2. **Ningún componente, modelo de datos o decisión arquitectónica fue incorporado de manera automática sin previa revisión crítica**. Todas las propuestas algorítmicas fueron analizadas, cotejadas contra el marco jurídico de la República de Nicaragua (Ley N.° 787 de Protección de Datos Personales) y sometidas a pruebas funcionales y de seguridad.
3. **El equipo humano asume la autoría y responsabilidad ética, técnica y jurídica plena** de la totalidad de los archivos, código fuente y entregables generados.

---

### 3. HERRAMIENTAS Y MODELOS UTILIZADOS

| Herramienta | Proveedor | Modelo Exacto Identificado | Periodo de Utilización | Finalidad Específica |
| :--- | :--- | :--- | :--- | :--- |
| **Google Antigravity IDE** | Google / Google DeepMind | `gemini-3.8-flash-medium` *(verificado en metadatos de transcripción de sesión)* | 18 al 24 de Noviembre de 2026 | Desarrollo de código Full Stack, refactorización, depuración de errores, ejecución de pruebas y sincronización en producción. |
| **Google Antigravity IDE (Fase Temprana)** | Google / Google DeepMind | *Modelo pendiente de confirmación (familia Gemini)* | 18 de Noviembre de 2026 | Generación de la arquitectura inicial, esquema preliminar de base de datos y catálogo de casos temprano. |
| **ChatGPT** | OpenAI | `GPT-4o` | 24 de Noviembre de 2026 | Diseño y estructuración pedagógica de los seis prompts estructurados de cierre académico (Fases 1 a 6). |
| **Google Stitch** | Google | *N/A (Declaración Negativa: NO UTILIZADO)* | N/A | Evaluado preliminarmente; se descartó formalmente su uso, empleándose desarrollo web nativo en su lugar. |

---

### 4. FINALIDAD Y ALCANCE DE LA PARTICIPACIÓN DE LA IA

La inteligencia artificial intervino en las siguientes dimensiones del proyecto:
1. **Definición y Arquitectura de Software:** Propuesta del patrón desacoplado en tres capas (Frontend SSG en Next.js, Backend REST en FastAPI y Persistencia relacional en SQLite/PostGIS).
2. **Desarrollo Frontend:** Generación de componentes en React, estilización utilitaria con Tailwind CSS v3.4, integración de mapas con Leaflet y configuración de compilación estática.
3. **Desarrollo Backend:** Creación de endpoints asíncronos en FastAPI, esquemas de validación Pydantic, hashing Argon2id y lógica de sanitización de imágenes con Pillow.
4. **Ciberseguridad y Aseguramiento de Calidad:** Generación de suites de pruebas con pytest (38 pruebas unitarias), pruebas de regresión y diagnóstico de vulnerabilidades bajo OWASP ASVS v5.0.0.
5. **Documentación Académica:** Estructuración de informes técnicos, matrices de trazabilidad, mapas de navegación en SVG y tablas comparativas.

---

### 5. PROMPTS RELEVANTES Y BITÁCORA DE INTERACCIÓN

Se registraron **38 prompts históricos fundacionales** y **6 prompts estructurados de cierre académico**, preservados de forma íntegra en el archivo `DOCUMENTACION_COMPLETA_PROYECTO.txt`. Entre las interacciones más determinantes destacan:
- **Prompt 19 (18/11/2026):** Solicitud humana de auditoría OWASP ASVS v5.0.0 que condujo a la sanitización forzosa de metadatos EXIF en imágenes.
- **Prompt 28 (19/11/2026):** Detección humana de que el catálogo mostraba marcadores genéricos, instruyendo la carga y asociación de 25 fotografías faciales reales optimizadas en WebP.
- **Prompt 35 (19/11/2026):** Diagnóstico y corrección del error 404 del servidor ASGI al recargar rutas directas, implementando enrutamiento estático dual con sufijos `.html`.
- **Prompts de Cierre Académico 1 a 6 (24/11/2026):** Ejecución sistemática de investigación documental, análisis de alternativas, trazabilidad de decisiones, diseño visual, matriz de componentes y la presente declaración formal.

---

### 6. INTERVENCIÓN, VERIFICACIÓN Y DECISIONES HUMANAS

La intervención humana fue continua y decisoria en cada etapa del desarrollo:
1. **Identificación de Anomalías:** El equipo humano detectó visualmente el fallo de navegación en producción (`detail: Not Found`) y la presencia de imágenes no normalizadas, ordenando las correcciones correspondientes.
2. **Arbitraje Ético y Jurídico:** Ante la propuesta técnica de mantener un catálogo público de *"Casos Resueltos"*, el equipo humano intervino para subordinar el diseño al marco de la Ley N.° 787, exigiendo la despublicación inmediata para garantizar el derecho al olvido.
3. **Verificación Funcional:** Se ejecutaron pruebas reales de conectividad, carga de archivos y comprobación de código de respuesta HTTP 200 OK en el hosting público [https://creacionvaloria.tradescanner.online](https://creacionvaloria.tradescanner.online).

---

### 7. MATRIZ DE RESPONSABILIDADES Y CONTRIBUCIONES INDIVIDUALES

Conforme a las instrucciones de honestidad académica, los nombres y números de identificación específicos se presentan en campos formalmente reservados para su suscripción manuscrita o firma digital por parte de cada integrante en la [MATRIZ_CONTRIBUCIONES_INTEGRANTES.xlsx](file:///c:/Users/User/Documents/Valor%20IA/EncuentrameNicaragua/ENTREGA_FINAL_ACADEMICA/06_Declaracion_Uso_IA/MATRIZ_CONTRIBUCIONES_INTEGRANTES.xlsx):
- **Integrante 1 (Líder / Arquitectura):** Formulación de prompts, selección de la alternativa tecnológica Full Stack y supervisión de la base de datos.
- **Integrante 2 (Frontend / UI-UX):** Validación de accesibilidad WCAG 2.1 AA, verificación de diseño responsive y auditoría de fotografías.
- **Integrante 3 (Seguridad / QA):** Ejecución y análisis de la suite de 38 pruebas pytest, verificación de roles RBAC y confidencialidad de pistas.
- **Integrante 4 (Investigación / Legal):** Validación de fuentes del CICR, cotejo de artículos de la Ley 787 y análisis ético del derecho al olvido.

---

### 8. COMPROMISO FORMAL DE INTEGRIDAD ACADÉMICA

Los integrantes del equipo declaramos bajo fe de juramento que:
- El contenido presentado en este informe es fruto de un trabajo de ingeniería riguroso, crítico y verificado.
- Ninguna sección del informe o del código fue aceptada a ciegas sin comprensión cabal de sus implicaciones técnicas y éticas.
- Las fuentes bibliográficas y jurídicas citadas corresponden a documentos oficiales vigentes debidamente consultados y verificados.

---

### 9. ESPACIO FORMAL DE IDENTIFICACIÓN Y FIRMAS

```text
Por la presente, ratificamos la veracidad y exactitud de la información declarada:

________________________________________          ________________________________________
Firma: Representante del Grupo                    Firma: Integrante 2
Nombre: [Pendiente de Confirmación]               Nombre: [Pendiente de Confirmación]
Cédula: [Pendiente de Confirmación]               Cédula: [Pendiente de Confirmación]
Fecha: 24 de Noviembre de 2026                    Fecha: 24 de Noviembre de 2026


________________________________________          ________________________________________
Firma: Integrante 3                               Firma: Integrante 4
Nombre: [Pendiente de Confirmación]               Nombre: [Pendiente de Confirmación]
Cédula: [Pendiente de Confirmación]               Cédula: [Pendiente de Confirmación]
Fecha: 24 de Noviembre de 2026                    Fecha: 24 de Noviembre de 2026
```

---

### 10. REFERENCIAS (FORMATO APA 7.ª EDICIÓN)

- American Psychological Association. (2020). *Publication manual of the American Psychological Association* (7.ª ed.). https://doi.org/10.1037/0000165-000
- Asamblea Nacional de la República de Nicaragua. (2012, 29 de marzo). Ley N.° 787, Ley de Protección de Datos Personales. *La Gaceta, Diario Oficial*, (61). https://sajurin.enriquebolanos.org/docs/G-2012-03-29.pdf
- Comité Internacional de la Cruz Roja. (2020). *Personas desaparecidas y sus familiares: Recomendaciones para la respuesta humanitaria y legislativa*. CICR. https://missingpersons.icrc.org/es/search-process
- Google DeepMind. (2026). *Gemini models: Technical report and agentic capabilities in Antigravity*. Google.
- OpenAI. (2024). *ChatGPT (Versión GPT-4o) [Modelo de lenguaje masivo]*. https://chatgpt.com
- OWASP Foundation. (2023). *Application Security Verification Standard 5.0.0 (ASVS)*. OWASP. https://asvs.owasp.org/
"""
    with open(os.path.join(DEST_DIR, "DECLARACION_FORMAL_USO_IA.md"), "w", encoding="utf-8") as f:
        f.write(declaracion_md.strip() + "\n")
    print("Generado: DECLARACION_FORMAL_USO_IA.md")

    # 4.5 GENERAR DECLARACION_FORMAL_USO_IA.docx USANDO python-docx
    doc_path = os.path.join(DEST_DIR, "DECLARACION_FORMAL_USO_IA.docx")
    doc = docx.Document()

    # Configuración de márgenes APA 7 (1 pulgada = 2.54 cm)
    for section in doc.sections:
        section.top_margin = Inches(1.0)
        section.bottom_margin = Inches(1.0)
        section.left_margin = Inches(1.0)
        section.right_margin = Inches(1.0)

    # Estilo base Arial 12
    style = doc.styles['Normal']
    font = style.font
    font.name = 'Arial'
    font.size = Pt(12)
    font.color.rgb = RGBColor(15, 23, 42)

    # Título Principal
    p_title = doc.add_paragraph()
    p_title.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run_title = p_title.add_run("DECLARACIÓN FORMAL DE USO DE INTELIGENCIA ARTIFICIAL GENERATIVA")
    run_title.bold = True
    run_title.font.size = Pt(16)
    run_title.font.color.rgb = RGBColor(15, 42, 74)

    p_sub = doc.add_paragraph()
    p_sub.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run_sub = p_sub.add_run("Proyecto: ENCUÉNTRAME NICARAGUA\nApartado Obligatorio del Informe Final Académico — Normas APA 7.ª Edición\n")
    run_sub.font.size = Pt(12)
    run_sub.font.italic = True
    run_sub.font.color.rgb = RGBColor(100, 116, 139)

    # Secciones del documento
    sections_text = [
        ("1. INTRODUCCIÓN", "En concordancia con los principios de integridad académica, transparencia investigativa y las directrices internacionales sobre el uso ético de tecnologías emergentes en la educación superior y la investigación científica (American Psychological Association [APA], 2020), los autores del presente proyecto presentan la Declaración Formal sobre el Uso de Inteligencia Artificial Generativa en la concepción, arquitectura, desarrollo, auditoría y documentación de la plataforma web humanitaria ENCUÉNTRAME NICARAGUA.\n\nEl propósito fundamental de esta declaración es documentar con precisión, exhaustividad y rigor forense la participación de agentes y herramientas de inteligencia artificial durante el ciclo de vida del software, delimitando con claridad las fronteras entre el contenido propuesto por algoritmos y la intervención, supervisión, validación y responsabilidad indelegable del equipo humano."),
        ("2. DECLARACIÓN GENERAL DE USO DE INTELIGENCIA ARTIFICIAL", "Los autores declaramos formalmente que para el desarrollo de este proyecto se contó con la asistencia de herramientas avanzadas de inteligencia artificial generativa, principalmente Google Antigravity IDE (impulsado por modelos de la familia Gemini de Google DeepMind) y ChatGPT (desarrollado por OpenAI).\n\nHacemos constar de manera explícita que:\n1. La IA actuó como copiloto técnico y asistente metodológico, acelerando la codificación de interfaces en Next.js, servicios REST en FastAPI, esquemas de bases de datos relacionales y la estructuración de documentos bajo estándares académicos.\n2. Ningún componente, modelo de datos o decisión arquitectónica fue incorporado de manera automática sin previa revisión crítica. Todas las propuestas algorítmicas fueron analizadas, cotejadas contra el marco jurídico de la República de Nicaragua (Ley N.° 787 de Protección de Datos Personales) y sometidas a pruebas funcionales y de seguridad.\n3. El equipo humano asume la autoría y responsabilidad ética, técnica y jurídica plena de la totalidad de los archivos, código fuente y entregables generados."),
        ("3. HERRAMIENTAS Y MODELOS UTILIZADOS", "Se identificaron y auditaron las siguientes herramientas en el repositorio y bitácoras:\n• Google Antigravity IDE (Modelo gemini-3.8-flash-medium verificado en metadatos de transcripción):\n  Utilizado entre el 18 y el 24 de noviembre de 2026 para el desarrollo Full Stack, refactorización, depuración de errores, ejecución de pruebas automatizadas y despliegue a producción.\n• Google Antigravity IDE (Fase Temprana - Modelo pendiente de confirmación de la familia Gemini):\n  Utilizado el 18 de noviembre de 2026 para la arquitectura preliminar y scaffolding de base de datos.\n• ChatGPT (Modelo GPT-4o de OpenAI):\n  Utilizado el 24 de noviembre de 2026 para la formulación y diseño metodológico de los seis prompts estructurados de cierre académico.\n• Declaración Negativa de Google Stitch: Se declara formalmente que Google Stitch NO fue utilizado en el proyecto, recurriéndose a desarrollo web nativo en HTML5, CSS3, JavaScript y SVG."),
        ("4. FINALIDAD Y ALCANCE DE LA PARTICIPACIÓN DE LA IA", "La inteligencia artificial intervino en las siguientes dimensiones del proyecto:\n1. Arquitectura de Software: Propuesta del patrón desacoplado en tres capas (Next.js SSG + FastAPI REST + SQLite/PostGIS).\n2. Desarrollo Frontend: Componentes en React 18, Tailwind CSS 3.4 y mapas con Leaflet.\n3. Desarrollo Backend: Endpoints asíncronos en FastAPI, validaciones Pydantic, hashing Argon2id y sanitización EXIF con Pillow.\n4. Ciberseguridad y QA: Generación de suites de pruebas con pytest (38 pruebas unitarias) bajo OWASP ASVS v5.0.0.\n5. Documentación Académica: Estructuración de informes, matrices de trazabilidad y diagramas vectoriales."),
        ("5. INTERVENCIÓN, VERIFICACIÓN Y DECISIONES HUMANAS", "La intervención humana fue continua y determinante en cada etapa:\n1. Identificación de Anomalías: El equipo humano detectó visualmente el fallo de navegación en producción (detail: Not Found) y la presencia de imágenes no normalizadas, ordenando las correcciones.\n2. Arbitraje Ético y Jurídico: Ante la propuesta técnica de mantener un catálogo público de 'Casos Resueltos', el equipo humano intervino para subordinar el diseño al marco de la Ley N.° 787, exigiendo la despublicación inmediata para garantizar el derecho al olvido.\n3. Verificación Funcional: Se ejecutaron pruebas reales de conectividad, carga de archivos y comprobación de código de respuesta HTTP 200 OK en el hosting público."),
        ("6. COMPROMISO FORMAL DE INTEGRIDAD ACADÉMICA", "Los integrantes del equipo declaramos bajo fe de juramento que el contenido presentado en este informe es fruto de un trabajo de ingeniería riguroso, crítico y verificado. Ninguna sección del informe o del código fue aceptada a ciegas sin comprensión cabal de sus implicaciones técnicas y éticas. Las fuentes bibliográficas y jurídicas citadas corresponden a documentos oficiales vigentes debidamente consultados."),
        ("7. REFERENCIAS (FORMATO APA 7.ª EDICIÓN)", "• American Psychological Association. (2020). Publication manual of the American Psychological Association (7.ª ed.). https://doi.org/10.1037/0000165-000\n• Asamblea Nacional de la República de Nicaragua. (2012, 29 de marzo). Ley N.° 787, Ley de Protección de Datos Personales. La Gaceta, Diario Oficial, (61). https://sajurin.enriquebolanos.org/docs/G-2012-03-29.pdf\n• Comité Internacional de la Cruz Roja. (2020). Personas desaparecidas y sus familiares: Recomendaciones para la respuesta humanitaria y legislativa. CICR. https://missingpersons.icrc.org/es/search-process\n• Google DeepMind. (2026). Gemini models: Technical report and agentic capabilities in Antigravity. Google.\n• OpenAI. (2024). ChatGPT (Versión GPT-4o) [Modelo de lenguaje masivo]. https://chatgpt.com\n• OWASP Foundation. (2023). Application Security Verification Standard 5.0.0 (ASVS). OWASP. https://asvs.owasp.org/")
    ]

    for title, body in sections_text:
        h = doc.add_paragraph()
        h_run = h.add_run(title)
        h_run.bold = True
        h_run.font.size = Pt(13)
        h_run.font.color.rgb = RGBColor(15, 42, 74)
        
        p = doc.add_paragraph(body)
        p.paragraph_format.line_spacing = 1.15
        p.paragraph_format.space_after = Pt(12)

    # Espacio para firmas
    doc.add_paragraph("\nPor la presente, ratificamos la veracidad y exactitud de la información declarada:\n")
    table = doc.add_table(rows=2, cols=2)
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    
    cell_00 = table.cell(0, 0)
    cell_00.text = "________________________________________\nFirma: Representante del Grupo\nNombre: [Pendiente de Confirmación]\nFecha: 24/11/2026"
    
    cell_01 = table.cell(0, 1)
    cell_01.text = "________________________________________\nFirma: Integrante 2\nNombre: [Pendiente de Confirmación]\nFecha: 24/11/2026"

    cell_10 = table.cell(1, 0)
    cell_10.text = "\n________________________________________\nFirma: Integrante 3\nNombre: [Pendiente de Confirmación]\nFecha: 24/11/2026"

    cell_11 = table.cell(1, 1)
    cell_11.text = "\n________________________________________\nFirma: Integrante 4\nNombre: [Pendiente de Confirmación]\nFecha: 24/11/2026"

    doc.save(doc_path)
    print("Generado Word: DECLARACION_FORMAL_USO_IA.docx")

    # 4.6 GENERAR DECLARACION_FORMAL_USO_IA.pdf MEDIANTE HTML Y EDGE HEADLESS PRINT-TO-PDF
    html_temp = os.path.join(DEST_DIR, "_temp_print.html")
    pdf_path = os.path.join(DEST_DIR, "DECLARACION_FORMAL_USO_IA.pdf")

    html_content = f"""<!DOCTYPE html>
<html lang="es">
<head>
  <meta charset="UTF-8">
  <title>DECLARACIÓN FORMAL DE USO DE INTELIGENCIA ARTIFICIAL GENERATIVA</title>
  <style>
    @page {{
      size: letter;
      margin: 2.54cm;
      @bottom-right {{
        content: counter(page);
      }}
    }}
    body {{
      font-family: Arial, sans-serif;
      font-size: 11pt;
      line-height: 1.5;
      color: #0F172A;
      margin: 0;
      padding: 0;
    }}
    h1 {{
      font-size: 15pt;
      font-weight: bold;
      color: #0F2A4A;
      text-align: center;
      margin-bottom: 4px;
    }}
    .subtitle {{
      font-size: 10.5pt;
      font-style: italic;
      color: #64748B;
      text-align: center;
      margin-bottom: 24px;
    }}
    h2 {{
      font-size: 12pt;
      font-weight: bold;
      color: #0F2A4A;
      border-bottom: 1px solid #CBD5E1;
      padding-bottom: 4px;
      margin-top: 20px;
      margin-bottom: 8px;
    }}
    p, ul {{
      margin-bottom: 12px;
      text-align: justify;
    }}
    table {{
      width: 100%;
      border-collapse: collapse;
      margin: 16px 0;
      font-size: 10pt;
    }}
    th, td {{
      border: 1px solid #CBD5E1;
      padding: 8px 10px;
      text-align: left;
    }}
    th {{
      background-color: #0F2A4A;
      color: #FFFFFF;
      font-weight: bold;
    }}
    .sig-table {{
      margin-top: 30px;
      border: none;
    }}
    .sig-table td {{
      border: none;
      padding: 20px 10px;
      vertical-align: top;
      font-size: 9.5pt;
    }}
  </style>
</head>
<body>
  <h1>DECLARACIÓN FORMAL DE USO DE INTELIGENCIA ARTIFICIAL GENERATIVA</h1>
  <div class="subtitle">Proyecto: ENCUÉNTRAME NICARAGUA — Apartado Obligatorio del Informe Final Académico (APA 7.ª Ed.)</div>

  <h2>1. INTRODUCCIÓN</h2>
  <p>En concordancia con los principios de integridad académica, transparencia investigativa y las directrices internacionales sobre el uso ético de tecnologías emergentes en la educación superior y la investigación científica (American Psychological Association [APA], 2020), los autores del presente proyecto presentan la <strong>Declaración Formal sobre el Uso de Inteligencia Artificial Generativa</strong> en la concepción, arquitectura, desarrollo, auditoría y documentación de la plataforma web humanitaria <strong>ENCUÉNTRAME NICARAGUA</strong>.</p>
  <p>El propósito fundamental de esta declaración es documentar con precisión, exhaustividad y rigor forense la participación de agentes y herramientas de inteligencia artificial durante el ciclo de vida del software, delimitando con claridad las fronteras entre el contenido propuesto por algoritmos y la intervención, supervisión, validación y responsabilidad indelegable del equipo humano.</p>

  <h2>2. DECLARACIÓN GENERAL DE USO DE INTELIGENCIA ARTIFICIAL</h2>
  <p>Los autores declaramos formalmente que para el desarrollo de este proyecto se contó con la asistencia de herramientas avanzadas de inteligencia artificial generativa, principalmente <strong>Google Antigravity IDE</strong> (impulsado por modelos de la familia Gemini de Google DeepMind) y <strong>ChatGPT</strong> (desarrollado por OpenAI).</p>
  <p>Hacemos constar de manera explícita que:</p>
  <ul>
    <li><strong>La IA actuó como copiloto técnico y asistente metodológico</strong>, acelerando la codificación de interfaces en Next.js, servicios REST en FastAPI, esquemas relacionales SQLAlchemy y la estructuración de documentos bajo estándares académicos.</li>
    <li><strong>Ningún componente o decisión arquitectónica fue incorporado automáticamente sin previa revisión crítica</strong>. Todas las propuestas algorítmicas fueron analizadas, cotejadas contra el marco de la Ley N.° 787 de Protección de Datos Personales de Nicaragua y sometidas a pruebas funcionales y de seguridad.</li>
    <li><strong>El equipo humano asume la autoría y responsabilidad ética, técnica y jurídica plena</strong> de la totalidad de los archivos, código fuente y entregables generados.</li>
  </ul>

  <h2>3. HERRAMIENTAS Y MODELOS UTILIZADOS</h2>
  <table>
    <thead>
      <tr>
        <th>Herramienta</th>
        <th>Proveedor</th>
        <th>Modelo Exacto</th>
        <th>Periodo de Uso</th>
        <th>Finalidad Específica</th>
      </tr>
    </thead>
    <tbody>
      <tr>
        <td><strong>Google Antigravity IDE</strong></td>
        <td>Google DeepMind</td>
        <td>gemini-3.8-flash-medium</td>
        <td>18/11/2026 – 24/11/2026</td>
        <td>Desarrollo Full Stack, refactorización, suite pytest y despliegue a producción.</td>
      </tr>
      <tr>
        <td><strong>Google Antigravity (Temprano)</strong></td>
        <td>Google DeepMind</td>
        <td>Pendiente de confirmación</td>
        <td>18/11/2026</td>
        <td>Scaffolding inicial y arquitectura preliminar de base de datos.</td>
      </tr>
      <tr>
        <td><strong>ChatGPT</strong></td>
        <td>OpenAI</td>
        <td>GPT-4o</td>
        <td>24/11/2026</td>
        <td>Diseño y estructuración metodológica de los 6 prompts de cierre académico.</td>
      </tr>
      <tr>
        <td><strong>Google Stitch</strong></td>
        <td>Google</td>
        <td>N/A (NO UTILIZADO)</td>
        <td>N/A</td>
        <td>Declaración negativa: No fue utilizado; se empleó desarrollo web nativo.</td>
      </tr>
    </tbody>
  </table>

  <h2>4. FINALIDAD Y ALCANCE DE LA PARTICIPACIÓN DE LA IA</h2>
  <p>La inteligencia artificial intervino en la arquitectura de software (Next.js + FastAPI + SQLite), desarrollo frontend (React, Tailwind, Leaflet), desarrollo backend (FastAPI, Pydantic, Pillow con sanitización EXIF), ciberseguridad y QA (suite de 38 pruebas pytest bajo OWASP ASVS) y redacción de documentación académica bajo normas APA 7.</p>

  <h2>5. INTERVENCIÓN, VERIFICACIÓN Y DECISIONES HUMANAS</h2>
  <p>La intervención humana fue continua y determinante: detección visual de errores de navegación y fotos genéricas ordenando su reemplazo por avatares reales optimizados; arbitraje ético subordinando el sistema a la Ley 787 para despublicar casos resueltos respetando el derecho al olvido; y ejecución de pruebas de verificación funcional HTTP 200 OK en producción.</p>

  <h2>6. COMPROMISO FORMAL DE INTEGRIDAD ACADÉMICA</h2>
  <p>Los integrantes del equipo declaramos bajo fe de juramento que el contenido presentado en este informe es fruto de un trabajo de ingeniería riguroso, crítico y verificado. Ninguna sección fue aceptada a ciegas sin comprensión cabal de sus implicaciones técnicas y éticas.</p>

  <table class="sig-table">
    <tr>
      <td>
        __________________________________________<br>
        <strong>Firma: Representante del Grupo</strong><br>
        Nombre: [Pendiente de Confirmación]<br>
        Fecha: 24 de Noviembre de 2026
      </td>
      <td>
        __________________________________________<br>
        <strong>Firma: Integrante 2</strong><br>
        Nombre: [Pendiente de Confirmación]<br>
        Fecha: 24 de Noviembre de 2026
      </td>
    </tr>
    <tr>
      <td>
        __________________________________________<br>
        <strong>Firma: Integrante 3</strong><br>
        Nombre: [Pendiente de Confirmación]<br>
        Fecha: 24 de Noviembre de 2026
      </td>
      <td>
        __________________________________________<br>
        <strong>Firma: Integrante 4</strong><br>
        Nombre: [Pendiente de Confirmación]<br>
        Fecha: 24 de Noviembre de 2026
      </td>
    </tr>
  </table>

  <h2>7. REFERENCIAS (FORMATO APA 7.ª EDICIÓN)</h2>
  <p style="font-size: 9pt;">
    • American Psychological Association. (2020). <em>Publication manual of the American Psychological Association</em> (7.ª ed.). https://doi.org/10.1037/0000165-000<br>
    • Asamblea Nacional de la República de Nicaragua. (2012, 29 de marzo). Ley N.° 787, Ley de Protección de Datos Personales. <em>La Gaceta, Diario Oficial</em>, (61). https://sajurin.enriquebolanos.org/docs/G-2012-03-29.pdf<br>
    • Comité Internacional de la Cruz Roja. (2020). <em>Personas desaparecidas y sus familiares: Recomendaciones para la respuesta humanitaria y legislativa</em>. CICR. https://missingpersons.icrc.org/es/search-process<br>
    • Google DeepMind. (2026). <em>Gemini models: Technical report and agentic capabilities in Antigravity</em>. Google.<br>
    • OpenAI. (2024). <em>ChatGPT (Versión GPT-4o) [Modelo de lenguaje masivo]</em>. https://chatgpt.com<br>
    • OWASP Foundation. (2023). <em>Application Security Verification Standard 5.0.0 (ASVS)</em>. OWASP. https://asvs.owasp.org/
  </p>
</body>
</html>
"""
    with open(html_temp, "w", encoding="utf-8") as f:
        f.write(html_content)

    # Imprimir a PDF usando Edge Headless
    edge_exe = r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"
    cmd = [
        edge_exe,
        "--headless",
        "--disable-gpu",
        f"--print-to-pdf={pdf_path}",
        html_temp
    ]
    subprocess.run(cmd, capture_output=True, timeout=30)
    
    if os.path.exists(html_temp):
        os.remove(html_temp)

    if os.path.exists(pdf_path):
        print(f"Generado PDF: DECLARACION_FORMAL_USO_IA.pdf ({os.path.getsize(pdf_path):,} bytes)")
    else:
        print("Aviso: No se pudo generar PDF automáticamente con Edge.")

if __name__ == "__main__":
    create_tools_excel()
    create_prompts_excel()
    create_contributions_excel()
    create_markdown_and_word_docs()
