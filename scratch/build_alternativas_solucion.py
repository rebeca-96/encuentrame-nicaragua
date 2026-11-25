# -*- coding: utf-8 -*-
"""
Generador de Entregables Académicos de Selección y Comparación de Alternativas:
1. MATRIZ_COMPARATIVA_ALTERNATIVAS.csv
2. MATRIZ_EVALUACION_PONDERADA.xlsx (con fórmulas verificables)
3. GRAFICO_COMPARATIVO_ALTERNATIVAS.svg
4. ANALISIS_TRES_ALTERNATIVAS.md
5. JUSTIFICACION_ALTERNATIVA_SELECCIONADA.md
6. ANALISIS_VIABILIDAD.md
"""

import os
import csv
import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter

BASE_DIR = r"c:\Users\User\Documents\Valor IA\EncuentrameNicaragua\ENTREGA_FINAL_ACADEMICA\02_Alternativas_Solucion"
os.makedirs(BASE_DIR, exist_ok=True)

# -------------------------------------------------------------------------------------------------
# 1. MATRIZ_COMPARATIVA_ALTERNATIVAS.csv
# -------------------------------------------------------------------------------------------------
def generate_matriz_comparativa_csv():
    filepath = os.path.join(BASE_DIR, "MATRIZ_COMPARATIVA_ALTERNATIVAS.csv")
    headers = [
        "Criterio / Característica",
        "Alternativa A: Redes Sociales",
        "Alternativa B: Portal Web Estático",
        "Alternativa C: Plataforma Web Full Stack (Encuéntrame Nicaragua)"
    ]
    
    rows = [
        [
            "Descripción General",
            "Publicación y difusión descentralizada en muros, páginas comunitarias y cadenas de mensajería (Facebook, WhatsApp, TikTok).",
            "Sitio web estático o CMS básico administrado manualmente para exhibir fichas informativas sin lógica de backend avanzada.",
            "Solución web integral con frontend Next.js 14, backend FastAPI, base de datos relacional SQLite/PostgreSQL, geolocalización y canal cifrado."
        ],
        [
            "Mecanismo de Publicación",
            "Cualquier usuario publica directamente sin validación ni moderación previa.",
            "El administrador edita manualmente el código HTML o sube fichas mediante interfaz básica de CMS.",
            "Formulario multipaso con consentimiento informado legal, carga con previsualización y paso obligado por moderación humana."
        ],
        [
            "Seguridad y Protección de Datos",
            "Nula. Los datos quedan alojados en servidores comerciales de terceros con fines de perfilamiento publicitario.",
            "Básica. Depende de la seguridad del servidor web básico; carece de RBAC y cifrado de datos en reposo.",
            "Avanzada (OWASP ASVS v5.0.0). Hashes Argon2id, tokens JWT, anonimización SHA-256 de identificadores e IPs, defensas contra fuerza bruta."
        ],
        [
            "Tratamiento de Metadatos EXIF",
            "Riesgoso. La mayoría de redes conservan o procesan metadatos internos, o se comparten archivos sin purga previa de coordenadas GPS.",
            "Inexistente o manual. El webmaster debe limpiar manualmente cada archivo antes de subirlo.",
            "Automatizado y forzado. El servicio backend purga 100% de metadatos EXIF (Pillow), transcodifica a WebP y renombra con hash aleatorio."
        ],
        [
            "Centralización y Búsqueda",
            "Muy baja. Información fragmentada, duplicada, desactualizada y no indexable mediante criterios estructurados.",
            "Moderada. Existe un catálogo único, pero las búsquedas son estáticas, de texto plano o rudimentarias.",
            "Óptima. Repositorio único oficial con base relacional y motor de búsqueda facetado por edad, género, departamento y municipio."
        ],
        [
            "Moderación y Verificación",
            "Inexistente. Altísima vulnerabilidad a engaños, cobro de deudas, extorsión o violencia de género vicaria.",
            "Manual diferida. Depende exclusivamente del tiempo libre del administrador; sin trazabilidad formal de decisiones.",
            "Estructurada por diseño. Roles jerárquicos (RBAC), estados formales (draft -> pending_review -> approved -> closed) y bitácora forense."
        ],
        [
            "Seguimiento y Trazabilidad",
            "Nula. Las publicaciones permanecen estáticas; personas localizadas continúan circulando como desaparecidas durante años.",
            "Pobre. Requiere reescribir manualmente la página de la ficha; difícil articular líneas de tiempo por caso.",
            "Excelente. Modelo 'Carpetas Vivas' (CICR) con Línea de Tiempo dinámica en vivo y registro inmutable de auditoría (audit_logs)."
        ],
        [
            "Geolocalización",
            "Mención textual imprecisa en la publicación; sin cartografía interactiva ni mapas territoriales.",
            "Listados estáticos por texto o mapas embebidos de Google Maps sin polígonos municipales ni privacidad diferencial.",
            "Interactiva y ética. Mapa nacional Leaflet con 15 departamentos, 2 regiones autónomas y 153 municipios con centroides aproximados."
        ],
        [
            "Recepción de Pistas",
            "Comentarios públicos abiertos o mensajes a teléfonos personales, exponiendo a familias a extorsiones de estafadores.",
            "Formulario de contacto básico por correo electrónico sin garantía de cifrado, seguimiento ni confidencialidad.",
            "Canal cívico seguro (/pistas) con opción de anonimato estricto, código de seguimiento único (tip_code) y bandeja privada de moderación."
        ],
        [
            "Cumplimiento Ley N.° 787",
            "Inviable. Imposible garantizar derechos ARCO ni derecho al olvido una vez viralizado el contenido.",
            "Parcial y precario. Requiere intervención manual del webmaster; sin registro estructurado de consentimiento.",
            "Total por diseño (Privacy by Design). Consentimiento formal, cédulas hasheadas con SHA-256, supresión y despublicación inmediata (Art. 16)."
        ],
        [
            "Costo de Desarrollo Directo",
            "Cero o despreciable (utiliza plataformas gratuitas existentes).",
            "Bajo (plantillas estáticas, CMS básico y hosting compartido económico).",
            "Moderado (requiere inversión en arquitectura de software, backend ASGI, frontend React/Next.js y base de datos relacional)."
        ],
        [
            "Costo Operativo y Mantenimiento",
            "Inmanejable si se pretende moderar millones de comentarios; desgaste humano extremo.",
            "Creciente y lineal. Cada caso suma trabajo manual al webmaster, generando cuellos de botella.",
            "Eficiente y predecible. Automatización de flujos, compilación estática de alto rendimiento y arquitectura desacoplada escalable."
        ],
        [
            "Tiempo de Puesta en Marcha",
            "Inmediato (minutos u horas).",
            "Corto (1 a 3 semanas).",
            "Medio a estructurado (requiere sprints de desarrollo, validaciones de seguridad y control de calidad QA)."
        ]
    ]

    with open(filepath, "w", encoding="utf-8-sig", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(headers)
        writer.writerows(rows)
    print("Generada MATRIZ_COMPARATIVA_ALTERNATIVAS.csv")

# -------------------------------------------------------------------------------------------------
# 2. MATRIZ_EVALUACION_PONDERADA.xlsx (con fórmulas verificables de Excel)
# -------------------------------------------------------------------------------------------------
def generate_matriz_evaluacion_excel():
    filepath = os.path.join(BASE_DIR, "MATRIZ_EVALUACION_PONDERADA.xlsx")
    wb = openpyxl.Workbook()
    
    # Hoja 1: Evaluación Ponderada
    ws1 = wb.active
    ws1.title = "Evaluación Ponderada"
    ws1.views.sheetView[0].showGridLines = True
    
    # Estilos
    font_title = Font(name="Calibri", size=15, bold=True, color="0F2A4A")
    font_subtitle = Font(name="Calibri", size=10, italic=True, color="475569")
    font_header = Font(name="Calibri", size=11, bold=True, color="FFFFFF")
    font_body = Font(name="Calibri", size=10, color="000000")
    font_bold = Font(name="Calibri", size=10, bold=True, color="000000")
    font_total = Font(name="Calibri", size=11, bold=True, color="0F2A4A")
    
    fill_header = PatternFill(start_color="0F2A4A", end_color="0F2A4A", fill_type="solid")
    fill_alt_a = PatternFill(start_color="F1F5F9", end_color="F1F5F9", fill_type="solid")
    fill_alt_b = PatternFill(start_color="E2E8F0", end_color="E2E8F0", fill_type="solid")
    fill_alt_c = PatternFill(start_color="CCFBF1", end_color="CCFBF1", fill_type="solid") # Verde azulado suave
    fill_total = PatternFill(start_color="FEF3C7", end_color="FEF3C7", fill_type="solid") # Ámbar suave
    
    thin_border = Border(
        left=Side(style='thin', color='CBD5E1'),
        right=Side(style='thin', color='CBD5E1'),
        top=Side(style='thin', color='CBD5E1'),
        bottom=Side(style='thin', color='CBD5E1')
    )
    double_bottom_border = Border(
        left=Side(style='thin', color='CBD5E1'),
        right=Side(style='thin', color='CBD5E1'),
        top=Side(style='thin', color='CBD5E1'),
        bottom=Side(style='double', color='0F2A4A')
    )
    
    align_center = Alignment(horizontal="center", vertical="center")
    align_left = Alignment(horizontal="left", vertical="center")
    align_right = Alignment(horizontal="right", vertical="center")
    align_wrap = Alignment(horizontal="left", vertical="center", wrap_text=True)
    
    # Títulos
    ws1["A1"] = "PROYECTO: ENCUÉNTRAME NICARAGUA — MATRIZ DE EVALUACIÓN PONDERADA DE ALTERNATIVAS"
    ws1["A1"].font = font_title
    ws1["A2"] = "Análisis comparativo multicriterio conforme a la metodología de evaluación de proyectos tecnológicos"
    ws1["A2"].font = font_subtitle
    
    # Encabezados de tabla
    headers = [
        "ID",
        "Criterio de Evaluación",
        "Ponderación (%)",
        "Calificación Alt A (1-5)",
        "Puntaje Ponderado Alt A",
        "Calificación Alt B (1-5)",
        "Puntaje Ponderado Alt B",
        "Calificación Alt C (1-5)",
        "Puntaje Ponderado Alt C",
        "Justificación Técnica y Fundamentación de Calificaciones"
    ]
    
    ws1.append([]) # Fila 3 vacía
    ws1.append(headers) # Fila 4
    
    for col_idx in range(1, len(headers) + 1):
        cell = ws1.cell(row=4, column=col_idx)
        cell.font = font_header
        cell.fill = fill_header
        cell.alignment = align_center
        cell.border = thin_border
    
    # Datos de los 10 criterios
    # Criterio, Ponderación, Alt A, Alt B, Alt C, Justificación
    criterios_data = [
        (
            "C1", "Seguridad y protección de datos personales", 0.20, 1, 2, 5,
            "Alt A expone números privados a extorsionistas y no purga EXIF. Alt B tiene seguridad básica sin RBAC ni cifrado. Alt C aplica OWASP ASVS v5.0.0, sanitización EXIF, Argon2id, JWT y hashes SHA-256."
        ),
        (
            "C2", "Centralización y organización de la información", 0.15, 1, 3, 5,
            "Alt A fragmenta datos en muros y chats. Alt B ofrece un portal único pero con búsquedas planas no relacionales. Alt C cuenta con base normalizada y motor de búsqueda facetado multidimensional."
        ),
        (
            "C3", "Moderación y verificación de reportes", 0.15, 1, 3, 5,
            "Alt A carece de moderación previa (vulnerable a difamación/estafas). Alt B depende de revisión manual del webmaster. Alt C implementa flujo formal de estados (draft->pending_review->approved->closed) y panel RBAC."
        ),
        (
            "C4", "Seguimiento, trazabilidad y avance de casos", 0.10, 1, 2, 5,
            "Alt A deja posts estáticos que persisten años tras la localización. Alt B requiere reescritura manual en HTML. Alt C incorpora 'Carpetas Vivas' (CICR) con timeline dinámico en vivo y audit_logs inmutable."
        ),
        (
            "C5", "Geolocalización y cobertura territorial nacional", 0.10, 1, 2, 5,
            "Alt A no ofrece soporte cartográfico estructurado. Alt B ofrece listados textuales o mapas embebidos rígidos. Alt C cuenta con mapa interactivo con 15 departamentos, 2 regiones autónomas y 153 municipios con centroides éticos."
        ),
        (
            "C6", "Accesibilidad y facilidad de uso ciudadano", 0.10, 5, 4, 4,
            "Alt A goza de familiaridad masiva inmediata en la población. Alt B ofrece lectura web sencilla. Alt C tiene interfaz responsive intuitiva en Tailwind, requiriendo navegador web moderno."
        ),
        (
            "C7", "Escalabilidad técnica e infraestructura", 0.05, 4, 4, 4,
            "Alt A aprovecha la infraestructura global de Meta. Alt B escala bien para lectura estática. Alt C implementa arquitectura híbrida desacoplada (Next.js SSG + FastAPI stateless) de alta concurrencia."
        ),
        (
            "C8", "Costo de implementación e infraestructura", 0.05, 5, 4, 3,
            "Escala favorable: menor costo = mayor puntaje. Alt A no tiene costo directo. Alt B requiere hosting económico básico. Alt C requiere inversión en desarrollo de software, base relacional y hosting ASGI."
        ),
        (
            "C9", "Facilidad y sostenibilidad del mantenimiento", 0.05, 3, 2, 4,
            "Escala favorable: mayor facilidad = mayor puntaje. Alt A no mantiene software pero moderar comentarios es caótico. Alt B genera cuellos de botella manuales. Alt C posee arquitectura modular con pruebas automatizadas (38/38 Pytest)."
        ),
        (
            "C10", "Tiempo requerido para puesta en marcha", 0.05, 5, 4, 3,
            "Escala favorable: menor tiempo = mayor puntaje. Alt A es inmediata (horas). Alt B requiere 1 a 3 semanas. Alt C requiere ciclo completo de ingeniería, seguridad, backend y frontend (semanas/meses)."
        )
    ]
    
    start_row = 5
    for idx, (cid, cname, weight, sc_a, sc_b, sc_c, just) in enumerate(criterios_data):
        r = start_row + idx
        ws1.cell(row=r, column=1, value=cid).alignment = align_center
        ws1.cell(row=r, column=2, value=cname).alignment = align_left
        
        # Ponderación
        w_cell = ws1.cell(row=r, column=3, value=weight)
        w_cell.number_format = "0.0%"
        w_cell.alignment = align_right
        
        # Alt A
        c_a = ws1.cell(row=r, column=4, value=sc_a)
        c_a.alignment = align_center
        c_a.fill = fill_alt_a
        p_a = ws1.cell(row=r, column=5, value=f"=D{r}*C{r}")
        p_a.number_format = "0.00"
        p_a.alignment = align_right
        p_a.fill = fill_alt_a
        
        # Alt B
        c_b = ws1.cell(row=r, column=6, value=sc_b)
        c_b.alignment = align_center
        c_b.fill = fill_alt_b
        p_b = ws1.cell(row=r, column=7, value=f"=F{r}*C{r}")
        p_b.number_format = "0.00"
        p_b.alignment = align_right
        p_b.fill = fill_alt_b
        
        # Alt C
        c_c = ws1.cell(row=r, column=8, value=sc_c)
        c_c.alignment = align_center
        c_c.font = font_bold
        c_c.fill = fill_alt_c
        p_c = ws1.cell(row=r, column=9, value=f"=H{r}*C{r}")
        p_c.number_format = "0.00"
        p_c.alignment = align_right
        p_c.font = font_bold
        p_c.fill = fill_alt_c
        
        # Justificación
        j_cell = ws1.cell(row=r, column=10, value=just)
        j_cell.alignment = align_wrap
        
        for col_idx in range(1, 11):
            ws1.cell(row=r, column=col_idx).border = thin_border
            if col_idx not in [4, 5, 6, 7, 8, 9]:
                ws1.cell(row=r, column=col_idx).font = font_body
    
    # Fila de Totales Ponderados (Fila 15)
    tot_row = start_row + len(criterios_data)
    ws1.cell(row=tot_row, column=1, value="TOT").alignment = align_center
    ws1.cell(row=tot_row, column=2, value="PUNTUACIÓN FINAL PONDERADA (Escala 1 a 5)").alignment = align_left
    
    w_sum = ws1.cell(row=tot_row, column=3, value=f"=SUM(C5:C14)")
    w_sum.number_format = "0.0%"
    w_sum.alignment = align_right
    
    ws1.cell(row=tot_row, column=4, value="-").alignment = align_center
    tot_a = ws1.cell(row=tot_row, column=5, value=f"=SUM(E5:E14)")
    tot_a.number_format = "0.00"
    tot_a.alignment = align_right
    
    ws1.cell(row=tot_row, column=6, value="-").alignment = align_center
    tot_b = ws1.cell(row=tot_row, column=7, value=f"=SUM(G5:G14)")
    tot_b.number_format = "0.00"
    tot_b.alignment = align_right
    
    ws1.cell(row=tot_row, column=8, value="-").alignment = align_center
    tot_c = ws1.cell(row=tot_row, column=9, value=f"=SUM(I5:I14)")
    tot_c.number_format = "0.00"
    tot_c.alignment = align_right
    
    ws1.cell(row=tot_row, column=10, value="Fórmula de suma ponderada = SUM(Puntajes Ponderados)").alignment = align_left
    
    for c_i in range(1, 11):
        cell = ws1.cell(row=tot_row, column=c_i)
        cell.font = font_total
        cell.fill = fill_total
        cell.border = thin_border
    
    # Fila de Equivalencia Porcentual (Fila 16)
    pct_row = tot_row + 1
    ws1.cell(row=pct_row, column=1, value="%").alignment = align_center
    ws1.cell(row=pct_row, column=2, value="EQUIVALENCIA PORCENTUAL RELATIVA (%)").alignment = align_left
    ws1.cell(row=pct_row, column=3, value=1.0).number_format = "0.0%"
    ws1.cell(row=pct_row, column=4, value="-").alignment = align_center
    
    pct_a = ws1.cell(row=pct_row, column=5, value=f"=E{tot_row}/5")
    pct_a.number_format = "0.0%"
    pct_a.alignment = align_right
    
    ws1.cell(row=pct_row, column=6, value="-").alignment = align_center
    pct_b = ws1.cell(row=pct_row, column=7, value=f"=G{tot_row}/5")
    pct_b.number_format = "0.0%"
    pct_b.alignment = align_right
    
    ws1.cell(row=pct_row, column=8, value="-").alignment = align_center
    pct_c = ws1.cell(row=pct_row, column=9, value=f"=I{tot_row}/5")
    pct_c.number_format = "0.0%"
    pct_c.alignment = align_right
    
    ws1.cell(row=pct_row, column=10, value="Cálculo relativo: Puntuación Final / Escala Máxima (5.0)").alignment = align_left
    
    for c_i in range(1, 11):
        cell = ws1.cell(row=pct_row, column=c_i)
        cell.font = font_total
        cell.fill = fill_total
        cell.border = double_bottom_border
    
    # Ajuste de anchos de columna
    col_widths = {
        "A": 6,
        "B": 42,
        "C": 16,
        "D": 22,
        "E": 22,
        "F": 22,
        "G": 22,
        "H": 22,
        "I": 22,
        "J": 55
    }
    for col_let, width in col_widths.items():
        ws1.column_dimensions[col_let].width = width
    
    # Hoja 2: Resumen Ejecutivo y Conclusión
    ws2 = wb.create_sheet(title="Resumen Ejecutivo")
    ws2.views.sheetView[0].showGridLines = True
    
    ws2["A1"] = "RESUMEN EJECUTIVO DE EVALUACIÓN MULTICRITERIO"
    ws2["A1"].font = font_title
    
    res_headers = ["Alternativa Evaluada", "Puntuación Final (1-5)", "Equivalencia (%)", "Posición (Ranking)", "Veredicto y Recomendación"]
    ws2.append([])
    ws2.append(res_headers)
    for ci in range(1, len(res_headers) + 1):
        c = ws2.cell(row=3, column=ci)
        c.font = font_header
        c.fill = fill_header
        c.alignment = align_center
        c.border = thin_border
        
    res_rows = [
        ("Alternativa A: Difusión mediante Redes Sociales", "='Evaluación Ponderada'!E15", "='Evaluación Ponderada'!E16", "3.° Lugar", "Descartada por graves riesgos de extorsión, violación a Ley 787 y falta de moderación."),
        ("Alternativa B: Portal Web Informativo Estático", "='Evaluación Ponderada'!G15", "='Evaluación Ponderada'!G16", "2.° Lugar", "Descartada por rigidez operativa, falta de seguimiento dinámico y cuello de botella manual."),
        ("Alternativa C: Plataforma Web Full Stack (Encuéntrame Nicaragua)", "='Evaluación Ponderada'!I15", "='Evaluación Ponderada'!I16", "1.° Lugar (Seleccionada)", "Seleccionada formalmente por máxima solidez en seguridad (ASVS), respeto a Ley 787 y 'Carpetas Vivas' (CICR).")
    ]
    
    for idx, (aname, pf, pe, rk, verd) in enumerate(res_rows, 4):
        ws2.cell(row=idx, column=1, value=aname).alignment = align_left
        c_pf = ws2.cell(row=idx, column=2, value=pf)
        c_pf.alignment = align_center
        c_pf.number_format = "0.00"
        c_pe = ws2.cell(row=idx, column=3, value=pe)
        c_pe.alignment = align_center
        c_pe.number_format = "0.0%"
        ws2.cell(row=idx, column=4, value=rk).alignment = align_center
        ws2.cell(row=idx, column=5, value=verd).alignment = align_wrap
        
        for ci in range(1, 6):
            cell = ws2.cell(row=idx, column=ci)
            cell.border = thin_border
            cell.font = font_bold if "Seleccionada" in rk else font_body
            if "Seleccionada" in rk:
                cell.fill = fill_alt_c
    
    ws2.column_dimensions["A"].width = 50
    ws2.column_dimensions["B"].width = 24
    ws2.column_dimensions["C"].width = 20
    ws2.column_dimensions["D"].width = 22
    ws2.column_dimensions["E"].width = 65
    
    wb.save(filepath)
    print("Generada MATRIZ_EVALUACION_PONDERADA.xlsx con fórmulas verificables.")

# -------------------------------------------------------------------------------------------------
# 3. GRAFICO_COMPARATIVO_ALTERNATIVAS.svg
# -------------------------------------------------------------------------------------------------
def generate_grafico_comparativo_svg():
    filepath = os.path.join(BASE_DIR, "GRAFICO_COMPARATIVO_ALTERNATIVAS.svg")
    
    # Creamos un gráfico SVG vectorial profesional de barras comparativas agrupadas
    svg_content = r'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 950 620" width="100%" height="100%" style="background:#ffffff; font-family:'Segoe UI', -apple-system, BlinkMacSystemFont, Roboto, Helvetica, Arial, sans-serif;">
  <defs>
    <style>
      .title { font-size: 20px; font-weight: 800; fill: #0f2a4a; }
      .subtitle { font-size: 13px; fill: #64748b; }
      .axis-label { font-size: 11px; fill: #475569; font-weight: 600; text-anchor: end; }
      .bar-label { font-size: 10px; font-weight: 700; fill: #ffffff; }
      .legend-text { font-size: 12px; fill: #1e293b; font-weight: 600; }
      .grid-line { stroke: #e2e8f0; stroke-dasharray: 4,4; stroke-width: 1; }
      .axis-line { stroke: #94a3b8; stroke-width: 1.5; }
      .score-box { font-size: 14px; font-weight: 800; }
    </style>
    <linearGradient id="gradAltA" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0%" stop-color="#94a3b8" />
      <stop offset="100%" stop-color="#64748b" />
    </linearGradient>
    <linearGradient id="gradAltB" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0%" stop-color="#38bdf8" />
      <stop offset="100%" stop-color="#0284c7" />
    </linearGradient>
    <linearGradient id="gradAltC" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0%" stop-color="#14b8a6" />
      <stop offset="100%" stop-color="#0f766e" />
    </linearGradient>
  </defs>

  <!-- Encabezado -->
  <text x="40" y="40" class="title">EVALUACIÓN COMPARATIVA PONDERADA DE ALTERNATIVAS DE SOLUCIÓN</text>
  <text x="40" y="62" class="subtitle">Proyecto: Encuéntrame Nicaragua — Escala de Puntuación Multicriterio (1.0 = Muy Desfavorable a 5.0 = Muy Favorable)</text>

  <!-- Leyenda Superior -->
  <g transform="translate(480, 28)">
    <!-- Alt A -->
    <rect x="0" y="0" width="16" height="16" rx="3" fill="#64748b" />
    <text x="22" y="13" class="legend-text">Alt A: Redes Sociales (2.00 / 40.0%)</text>
    
    <!-- Alt B -->
    <rect x="0" y="24" width="16" height="16" rx="3" fill="#0284c7" />
    <text x="22" y="37" class="legend-text">Alt B: Portal Estático (2.80 / 56.0%)</text>
    
    <!-- Alt C -->
    <rect x="250" y="24" width="16" height="16" rx="3" fill="#0f766e" />
    <text x="272" y="37" class="legend-text">Alt C: Full Stack (4.60 / 92.0%) [SELECCIONADA]</text>
  </g>

  <!-- Ejes y Líneas de Cuadrícula (X: 300 a 880, ancho = 580 px; Escala 0 a 5 -> 116 px por unidad) -->
  <!-- Líneas verticales de escala (1 a 5) -->
  <line x1="300" y1="95" x2="300" y2="540" class="axis-line" />
  <line x1="416" y1="95" x2="416" y2="540" class="grid-line" />
  <line x1="532" y1="95" x2="532" y2="540" class="grid-line" />
  <line x1="648" y1="95" x2="648" y2="540" class="grid-line" />
  <line x1="764" y1="95" x2="764" y2="540" class="grid-line" />
  <line x1="880" y1="95" x2="880" y2="540" class="axis-line" />

  <!-- Marcas de escala inferior -->
  <text x="300" y="560" font-size="11" fill="#64748b" text-anchor="middle">0.0</text>
  <text x="416" y="560" font-size="11" fill="#64748b" text-anchor="middle">1.0</text>
  <text x="532" y="560" font-size="11" fill="#64748b" text-anchor="middle">2.0</text>
  <text x="648" y="560" font-size="11" fill="#64748b" text-anchor="middle">3.0</text>
  <text x="764" y="560" font-size="11" fill="#64748b" text-anchor="middle">4.0</text>
  <text x="880" y="560" font-size="11" fill="#0f2a4a" font-weight="bold" text-anchor="middle">5.0 (Máx)</text>

  <!-- BARRAS AGRUPADAS POR CRITERIO -->
  
  <!-- C1: Seguridad y Datos (20%) -->
  <g transform="translate(0, 105)">
    <text x="285" y="24" class="axis-label">Seguridad y Privacidad (20%)</text>
    <!-- Alt A (1.0 = 116px) -->
    <rect x="300" y="2" width="116" height="8" rx="2" fill="url(#gradAltA)" />
    <!-- Alt B (2.0 = 232px) -->
    <rect x="300" y="13" width="232" height="8" rx="2" fill="url(#gradAltB)" />
    <!-- Alt C (5.0 = 580px) -->
    <rect x="300" y="24" width="580" height="8" rx="2" fill="url(#gradAltC)" />
  </g>

  <!-- C2: Centralización (15%) -->
  <g transform="translate(0, 145)">
    <text x="285" y="24" class="axis-label">Centralización de Información (15%)</text>
    <rect x="300" y="2" width="116" height="8" rx="2" fill="url(#gradAltA)" />
    <rect x="300" y="13" width="348" height="8" rx="2" fill="url(#gradAltB)" />
    <rect x="300" y="24" width="580" height="8" rx="2" fill="url(#gradAltC)" />
  </g>

  <!-- C3: Moderación y Verificación (15%) -->
  <g transform="translate(0, 185)">
    <text x="285" y="24" class="axis-label">Moderación y Verificación (15%)</text>
    <rect x="300" y="2" width="116" height="8" rx="2" fill="url(#gradAltA)" />
    <rect x="300" y="13" width="348" height="8" rx="2" fill="url(#gradAltB)" />
    <rect x="300" y="24" width="580" height="8" rx="2" fill="url(#gradAltC)" />
  </g>

  <!-- C4: Seguimiento y Trazabilidad (10%) -->
  <g transform="translate(0, 225)">
    <text x="285" y="24" class="axis-label">Trazabilidad 'Carpetas Vivas' (10%)</text>
    <rect x="300" y="2" width="116" height="8" rx="2" fill="url(#gradAltA)" />
    <rect x="300" y="13" width="232" height="8" rx="2" fill="url(#gradAltB)" />
    <rect x="300" y="24" width="580" height="8" rx="2" fill="url(#gradAltC)" />
  </g>

  <!-- C5: Geolocalización (10%) -->
  <g transform="translate(0, 265)">
    <text x="285" y="24" class="axis-label">Geolocalización 153 Municipios (10%)</text>
    <rect x="300" y="2" width="116" height="8" rx="2" fill="url(#gradAltA)" />
    <rect x="300" y="13" width="232" height="8" rx="2" fill="url(#gradAltB)" />
    <rect x="300" y="24" width="580" height="8" rx="2" fill="url(#gradAltC)" />
  </g>

  <!-- C6: Accesibilidad y Facilidad (10%) -->
  <g transform="translate(0, 305)">
    <text x="285" y="24" class="axis-label">Accesibilidad Ciudadana (10%)</text>
    <rect x="300" y="2" width="580" height="8" rx="2" fill="url(#gradAltA)" />
    <rect x="300" y="13" width="464" height="8" rx="2" fill="url(#gradAltB)" />
    <rect x="300" y="24" width="464" height="8" rx="2" fill="url(#gradAltC)" />
  </g>

  <!-- C7: Escalabilidad (5%) -->
  <g transform="translate(0, 345)">
    <text x="285" y="24" class="axis-label">Escalabilidad Técnica (5%)</text>
    <rect x="300" y="2" width="464" height="8" rx="2" fill="url(#gradAltA)" />
    <rect x="300" y="13" width="464" height="8" rx="2" fill="url(#gradAltB)" />
    <rect x="300" y="24" width="464" height="8" rx="2" fill="url(#gradAltC)" />
  </g>

  <!-- C8: Costo Favorable (5%) -->
  <g transform="translate(0, 385)">
    <text x="285" y="24" class="axis-label">Costo Favorable (5%)</text>
    <rect x="300" y="2" width="580" height="8" rx="2" fill="url(#gradAltA)" />
    <rect x="300" y="13" width="464" height="8" rx="2" fill="url(#gradAltB)" />
    <rect x="300" y="24" width="348" height="8" rx="2" fill="url(#gradAltC)" />
  </g>

  <!-- C9: Facilidad Mantenimiento (5%) -->
  <g transform="translate(0, 425)">
    <text x="285" y="24" class="axis-label">Facilidad de Mantenimiento (5%)</text>
    <rect x="300" y="2" width="348" height="8" rx="2" fill="url(#gradAltA)" />
    <rect x="300" y="13" width="232" height="8" rx="2" fill="url(#gradAltB)" />
    <rect x="300" y="24" width="464" height="8" rx="2" fill="url(#gradAltC)" />
  </g>

  <!-- C10: Tiempo Puesta en Marcha (5%) -->
  <g transform="translate(0, 465)">
    <text x="285" y="24" class="axis-label">Tiempo Rápido Puesta en Marcha (5%)</text>
    <rect x="300" y="2" width="580" height="8" rx="2" fill="url(#gradAltA)" />
    <rect x="300" y="13" width="464" height="8" rx="2" fill="url(#gradAltB)" />
    <rect x="300" y="24" width="348" height="8" rx="2" fill="url(#gradAltC)" />
  </g>

  <!-- RESULTADO FINAL PONDERADO -->
  <g transform="translate(0, 508)">
    <rect x="40" y="0" width="870" height="36" rx="6" fill="#f8fafc" stroke="#cbd5e1" stroke-width="1.5" />
    <text x="55" y="23" font-size="12" font-weight="bold" fill="#0f2a4a">PUNTUACIÓN GLOBAL:</text>
    <text x="220" y="23" font-size="12" font-weight="bold" fill="#64748b">Alt A: 2.00 / 5.0 (40.0%)</text>
    <text x="440" y="23" font-size="12" font-weight="bold" fill="#0284c7">Alt B: 2.80 / 5.0 (56.0%)</text>
    <text x="660" y="23" font-size="13" font-weight="bold" fill="#0f766e">★ Alt C: 4.60 / 5.0 (92.0%) [GANADORA]</text>
  </g>

  <!-- Pie de página -->
  <text x="40" y="595" font-size="10" fill="#94a3b8">Fuente: Matriz de Evaluación Ponderada Multicriterio — Proyecto Encuéntrame Nicaragua (2026). Basado en estándares Ley 787, CICR y OWASP ASVS v5.0.0.</text>
</svg>'''
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(svg_content.strip())
    print("Generado GRAFICO_COMPARATIVO_ALTERNATIVAS.svg")

if __name__ == "__main__":
    generate_matriz_comparativa_csv()
    generate_matriz_evaluacion_excel()
    generate_grafico_comparativo_svg()

# -------------------------------------------------------------------------------------------------
# 4. ANALISIS_TRES_ALTERNATIVAS.md
# -------------------------------------------------------------------------------------------------
def generate_analisis_tres_alternativas():
    filepath = os.path.join(BASE_DIR, "ANALISIS_TRES_ALTERNATIVAS.md")
    content = r"""# ANÁLISIS DETALLADO DE LAS TRES ALTERNATIVAS DE SOLUCIÓN

## PROYECTO: ENCUÉNTRAME NICARAGUA
### Plataforma Cívica de Búsqueda y Reunificación Familiar
**Rol Profesional:** Analista de Sistemas Senior, Arquitecto de Software y Evaluador de Proyectos  
**Fecha:** 24 de noviembre de 2026

---

### INTRODUCCIÓN Y CONTEXTO DE LA EVALUACIÓN

El presente documento analiza individualmente tres alternativas tecnológicas formuladas para responder a la crisis humanitaria de las personas desaparecidas y no localizadas en la República de Nicaragua. 

El análisis se efectúa bajo un enfoque metodológico riguroso, evaluando cada opción a través de 16 dimensiones estandarizadas de la ingeniería de software y la gestión de proyectos:
1. Descripción general
2. Funcionamiento operativo
3. Usuarios beneficiados
4. Requisitos técnicos e infraestructura
5. Ventajas comparativas
6. Desventajas intrínsecas
7. Costos estimados (enfoque cualitativo justificado)
8. Complejidad de implementación
9. Riesgos asociados
10. Nivel de seguridad de la información
11. Nivel de privacidad y protección de datos
12. Escalabilidad técnica
13. Mantenimiento y soporte
14. Viabilidad técnica
15. Viabilidad operativa
16. Limitaciones insalvables

---

## 1. ALTERNATIVA A: DIFUSIÓN MEDIANTE REDES SOCIALES

### 1.1. Descripción
Consiste en la utilización descentralizada de plataformas de redes sociales comerciales existentes (principalmente grupos de Facebook, estados de WhatsApp, canales de Telegram y videos cortos en TikTok) para publicar carteles, fotografías y mensajes de auxilio sobre personas desaparecidas, sin contar con una plataforma web propia ni un repositorio centralizado.

### 1.2. Funcionamiento
Un familiar o conocido elabora una imagen o texto informal con la foto del desaparecido, su nombre, el lugar del hecho y un número telefónico personal. Dicha publicación se comparte masivamente en grupos comunitarios locales, solicitando a los usuarios que "compartan para que llegue a más personas". Las interacciones ocurren en los comentarios públicos o mediante mensajes directos a las líneas personales expuestas.

### 1.3. Usuarios Beneficiados
- **Beneficiarios directos:** Familiares con acceso a telefonía móvil y cuentas activas en redes sociales.
- **Beneficiarios indirectos:** Comunidad en línea que visualiza el contenido en su muro diario.

### 1.4. Requisitos Técnicos
- Dispositivo móvil con conexión a internet básica (datos móviles o Wi-Fi).
- Cuenta de usuario registrada en las plataformas de Meta u otras redes sociales.
- Cero infraestructura de servidores o base de datos propia.

### 1.5. Ventajas
- **Adopción universal inmediata:** Prácticamente toda la población con smartphone conoce y utiliza WhatsApp y Facebook en Nicaragua.
- **Velocidad de propagación:** Un cartel puede viralizarse en cuestión de minutos dentro de una comunidad local.
- **Cero costo directo de desarrollo:** No requiere inversión inicial en programadores, diseñadores ni hosting propio.

### 1.6. Desventajas
- **Caos informativo y desorganización:** No existe indexación ni buscador semántico; la información se pierde en el feed a medida que pasan las horas.
- **Permanencia indefinida (Efecto Zombi):** Una vez que el caso se resuelve o la persona es localizada, resulta imposible retirar las miles de copias compartidas, perpetuando la condición de "desaparecido" de por vida.
- **Ausencia de moderación:** Vulnerabilidad absoluta ante publicaciones difamatorias, cobro de deudas encubierto o agresores que buscan a víctimas de violencia intrafamiliar.

### 1.7. Costos Estimados (Cualitativo)
- **Costo de desarrollo inicial:** Prácticamente nulo ($0 USD).
- **Costo operativo de moderación:** Inmanejable e infinito en términos de horas/hombre si se pretende fiscalizar manualmente millones de comentarios.
- **Costo de oportunidad y daño colateral:** Extremadamente elevado debido a estafas y extorsiones consumadas.

### 1.8. Complejidad de Implementación
- Muy baja (1/5). Puesta en marcha instantánea por cualquier ciudadano.

### 1.9. Riesgos
- **Riesgo crítico de extorsión:** Estafadores contactan a los teléfonos expuestos exigiendo rescates o transferencias falsas (CICR, 2023).
- **Riesgo de revictimización:** Comentarios revictimizantes, burlas o juicios morales públicos sobre las circunstancias de la desaparición.

### 1.10. Seguridad
- Muy deficiente (1/5). Sin defensas contra ataques dirigidos, sin control de acceso granular y dependencia de políticas opacas de moderación algorítmica de plataformas comerciales extranjeras.

### 1.11. Privacidad
- Crítica / Inadmisible (1/5). Incompatibilidad absoluta con la Ley N.° 787 de Nicaragua: no existe consentimiento documentado, no hay cómo ejercer derechos ARCO (rectificación o cancelación) ni derecho al olvido.

### 1.12. Escalabilidad
- Alta en tráfico (4/5), pero inversamente proporcional a la calidad: a mayor volumen de publicaciones, mayor confusión y menor efectividad de búsqueda.

### 1.13. Mantenimiento
- Desfavorable (2/5). No hay software que mantener, pero el mantenimiento de la veracidad de los datos es inalcanzable.

### 1.14. Viabilidad Técnica
- Favorable (4/5) por la existencia previa de la infraestructura de telecomunicaciones y aplicaciones comerciales.

### 1.15. Viabilidad Operativa
- Muy desfavorable (1/5). Fracasa como sistema ordenado de búsqueda cívica humanitaria.

### 1.16. Limitaciones
- Imposibilidad de centralizar datos, filtrar por coordenadas oficiales o proteger la integridad física y psicológica de los involucrados.

---

## 2. ALTERNATIVA B: PORTAL WEB INFORMATIVO ESTÁTICO

### 2.1. Descripción
Desarrollo de un sitio web unidireccional (basado en HTML/CSS estático o un gestor de contenidos básico tipo WordPress elemental), administrado centralmente por una organización o colectivo, cuyo objetivo exclusivo es exhibir fichas informativas de personas no localizadas, teléfonos de contacto y recomendaciones preventivas.

### 2.2. Funcionamiento
Los familiares envían los datos por correo electrónico o mensajería a un webmaster. Este revisa manualmente la información, diseña una página o entrada estática en el sitio web y publica la ficha. Si el caso se resuelve, el familiar debe contactar nuevamente al administrador para que borre o edite la página manualmente. Las pistas se reciben mediante un formulario de contacto estándar que envía correos electrónicos no cifrados.

### 2.3. Usuarios Beneficiados
- Familiares que logran establecer contacto directo con el administrador del sitio.
- Público general con acceso a navegadores web que busca información puntual.

### 2.4. Requisitos Técnicos
- Servidor web estático básico (Apache, Nginx o servicio de hosting compartido económico).
- Nombre de dominio y certificado SSL estándar (Let's Encrypt).
- Computadora para que el administrador actualice los archivos o el panel básico.

### 2.5. Ventajas
- **Punto único de referencia:** Concentra los reportes en un solo portal web formal.
- **Mayor formalidad:** Proyecta seriedad frente a las publicaciones anónimas de redes sociales.
- **Bajo costo de hosting:** Un sitio estático o CMS básico consume recursos computacionales mínimos.

### 2.6. Desventajas
- **Cuello de botella humano:** Cada reporte, corrección o retiro depende del tiempo y disponibilidad del webmaster. En crisis con decenas de reportes simultáneos, el sistema colapsa operativamente.
- **Carencia de lógica dinámica:** No permite búsquedas relacionales complejas (ej. "mujeres de 15 a 20 años en Matagalpa"), ni filtros interactivos concurrentes.
- **Sin seguimiento en tiempo real:** La ficha permanece como una foto fija; no soporta líneas de tiempo dinámicas de avance investigativo.

### 2.7. Costos Estimados (Cualitativo)
- **Costo de desarrollo inicial:** Bajo (plantillas comerciales y configuración básica de CMS).
- **Costo de hosting:** Mínimo (servidores compartidos convencionales de bajo costo mensual).
- **Costo operativo de personal:** Elevado y lineal a largo plazo: se requiere personal permanente dedicado exclusivamente a transcribir datos y subir fotos manualmente.

### 2.8. Complejidad de Implementación
- Baja a moderada (2/5). Requiere conocimientos básicos de maquetación web y administración de hosting.

### 2.9. Riesgos
- **Desactualización crítica:** Fichas obsoletas mantenidas en línea por falta de personal para editarlas.
- **Falta de confidencialidad en pistas:** Los correos electrónicos entrantes pueden ser interceptados o almacenados en servidores de correo no asegurados.

### 2.10. Seguridad
- Aceptable a baja (2/5). Vulnerable a ataques sobre el CMS, sin esquema RBAC robusto y sin políticas criptográficas avanzadas.

### 2.11. Privacidad
- Desfavorable (2/5). No automatiza la supresión de datos bajo Ley 787; el webmaster conserva fotos con metadatos EXIF sin sanitizar a menos que use herramientas externas previas.

### 2.12. Escalabilidad
- Buena en visualización (4/5), pero pésima en gestión operativa (1/5).

### 2.13. Mantenimiento
- Desfavorable (2/5). Alto desgaste manual repetitivo y riesgo constante de desincronización de contenidos.

### 2.14. Viabilidad Técnica
- Favorable (4/5). Fácilmente construible con herramientas estándar.

### 2.15. Viabilidad Operativa
- Desfavorable (2/5). Insostenible para un volumen superior a 50 casos activos concurrentes.

### 2.16. Limitaciones
- Incapacidad para procesar georreferenciación interactiva de 153 municipios, falta de anonimato para informantes y dependencia crítica de un operador manual.

---

## 3. ALTERNATIVA C: PLATAFORMA WEB FULL STACK (ENCUÉNTRAME NICARAGUA)

### 3.1. Descripción
Solución de software integral, modular y desacoplada, compuesta por un frontend moderno y reactivo (Next.js 14, TypeScript, Tailwind CSS), un backend de alto rendimiento (FastAPI, Python 3.12, Uvicorn), una base de datos relacional normalizada (SQLite/PostgreSQL con SQLAlchemy), servicios criptográficos y de seguridad (Argon2id, JWT, Pillow), cartografía interactiva local (Leaflet) y un panel administrativo de moderación con auditoría forense inmutable.

### 3.2. Funcionamiento
1. **Reporte:** El familiar ingresa a `/reportar`, completa un formulario multipaso con datos ante mortem estandarizados, adjunta fotografía y acepta los términos bajo la Ley N.° 787.
2. **Sanitización y Persistencia:** El backend purga los metadatos EXIF de la imagen, la convierte a WebP, calcula hashes irreversibles para la cédula del declarante e inserta el caso en la base de datos en estado `pending_review` (`is_public = False`).
3. **Moderación:** Un operador autorizado revisa el expediente en `/admin`. Si cumple los requisitos éticos y de verosimilitud, aprueba la publicación (`approved_published`).
4. **Difusión:** El caso se proyecta en el catálogo público (`/casos`) con distinción de activo/no activo y se georreferencia en el mapa nacional (`/mapa`) sobre centroides aproximados.
5. **Seguimiento Dinámico:** La ficha individual (`/casos/[id]`) actualiza una línea de tiempo ('Carpetas Vivas') y ofrece un canal confidencial para aportar pistas (`/pistas`) con código único.
6. **Cierre:** Al localizar a la persona, el caso se concluye o despublica inmediatamente (`is_public = False`), cumpliendo el artículo 16 de la Ley 787.

### 3.3. Usuarios Beneficiados
- **Familias de desaparecidos:** Tienen una vía segura, estructurada y respetuosa para difundir la búsqueda sin exponer su intimidad ni ser extorsionados.
- **Equipo de moderación y analistas:** Cuentan con herramientas avanzadas para clasificar, verificar y auditar indicios.
- **Ciudadanía informante:** Puede colaborar de forma anónima sin temor a represalias.
- **Sociedad nicaragüense:** Dispone de un catálogo nacional transparente, confiable y georreferenciado.

### 3.4. Requisitos Técnicos
- **Entorno Backend:** Python 3.12+, Uvicorn, SQLAlchemy, Pydantic v2, Pillow, Passlib.
- **Entorno Frontend:** Node.js 18+, Next.js 14 (App Router), TypeScript, Tailwind CSS, Leaflet 1.9.4 local.
- **Infraestructura:** Servidor ASGI local o en la nube con soporte Python, almacenamiento en disco para imágenes sanitizadas (`storage/uploads/`) y base de datos relacional.

### 3.5. Ventajas
- **Seguridad integral por diseño:** Cumplimiento verificado de OWASP ASVS v5.0.0 (Argon2id, JWT, sanitización EXIF, no-repudio).
- **Alineamiento legal estricto:** Garantía de autodeterminación informativa y derechos ARCO según Ley N.° 787.
- **Búsqueda humanitaria estructurada:** Implementación digital de la metodología de "Carpetas Vivas" recomendada por el CICR (2023).
- **Georreferenciación exhaustiva:** Cobertura de los 15 departamentos, 2 regiones autónomas y 153 municipios de Nicaragua con privacidad diferencial.
- **Autonomía operativa:** Paquetería 100% local sin dependencias críticas de CDN externas.

### 3.6. Desventajas
- **Mayor inversión inicial en ingeniería:** Exige perfiles especializados en desarrollo Full Stack, seguridad y bases de datos.
- **Mayor costo de infraestructura:** Requiere un servidor con capacidad de ejecutar procesos Python persistentes (ASGI Uvicorn) frente a un simple hosting estático.
- **Curva de aprendizaje para moderadores:** Requiere capacitar a los operadores cívicos en el uso del panel administrativo y criterios éticos de validación.

### 3.7. Costos Estimados (Cualitativo)
- **Costo de desarrollo inicial:** Moderado a elevado (compensado en este proyecto por el desarrollo previo integral documentado en `DOCUMENTACION_COMPLETA_PROYECTO.txt`).
- **Costo de infraestructura y hosting:** Moderado y altamente predecible (servidores virtuales privados o contenedores para FastAPI + almacenamiento en disco local).
- **Costo operativo de mantenimiento:** Óptimo y sostenible gracias a la automatización de flujos y suite de pruebas unitarias (38/38 Pytest).

### 3.8. Complejidad de Implementación
- Alta (4/5). Requiere integración armónica de múltiples tecnologías y protocolos de seguridad.

### 3.9. Riesgos
- **Riesgos de disponibilidad:** Caída del servidor ASGI o saturación de base de datos si no se aplican políticas de caché y rate limiting (mitigado con la exportación estática SSG de Next.js y rate limits en memoria).
- **Riesgo de brecha digital en zonas rurales:** Dificultad de acceso para familias en comunidades de la Costa Caribe sin cobertura de internet (mitigado con interfaces ultraligeras y recomendación de PWA offline).

### 3.10. Seguridad
- Muy Favorable / Excelente (5/5). Validación de entradas, control de acceso RBAC en servidor, sanitización forzada de imágenes y auditoría forense inmutable.

### 3.11. Privacidad
- Muy Favorable / Máxima (5/5). Protección rigurosa de la Ley 787: no almacenamiento de cédulas en claro, eliminación de GPS en fotos y despublicación inmediata garantizada.

### 3.12. Escalabilidad
- Favorable (4/5). La arquitectura desacoplada permite escalar la base de datos y los servidores de APIs independientemente del contenido estático frontend.

### 3.13. Mantenimiento
- Favorable (4/5). Código modular, tipado estático con TypeScript, modelos declarativos y 38 pruebas automatizadas que previenen regresiones.

### 3.14. Viabilidad Técnica
- Muy Favorable (5/5). Plenamente demostrada mediante la compilación y ejecución funcional del proyecto existente.

### 3.15. Viabilidad Operativa
- Muy Favorable (5/5). Estandariza la carga de trabajo, automatiza filtros y protege a los operadores cívicos.

### 3.16. Limitaciones
- Dependencia de conectividad a internet en el cliente y necesidad de acuerdos formales futuros para interoperabilidad con sistemas de la Policía Nacional o Ministerio Público.
"""
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(content.strip())
    print("Generado ANALISIS_TRES_ALTERNATIVAS.md")

# -------------------------------------------------------------------------------------------------
# 5. JUSTIFICACION_ALTERNATIVA_SELECCIONADA.md
# -------------------------------------------------------------------------------------------------
def generate_justificacion_seleccion():
    filepath = os.path.join(BASE_DIR, "JUSTIFICACION_ALTERNATIVA_SELECCIONADA.md")
    content = r"""# JUSTIFICACIÓN DE LA ALTERNATIVA SELECCIONADA Y ACLARACIÓN RETROSPECTIVA

## PROYECTO: ENCUÉNTRAME NICARAGUA
### Plataforma Cívica de Búsqueda y Reunificación Familiar
**Documento:** Justificación de Selección Arquitectónica  
**Fecha:** 24 de noviembre de 2026

---

### 1. ACLARACIÓN METODOLÓGICA Y ENFOQUE RETROSPECTIVO

Es imperativo establecer con rigor académico y transparencia metodológica que el presente análisis comparativo se realiza con **carácter retrospectivo**. 

La plataforma web Full Stack **Encuéntrame Nicaragua** ya ha sido diseñada, programada, testeada y auditada previamente en el entorno de desarrollo (conforme se acredita detalladamente en el archivo `DOCUMENTACION_COMPLETA_PROYECTO.txt`). 

Por consiguiente, el propósito de esta evaluación multicriterio no es simular una elección a ciegas, sino **documentar formalmente, contrastar empíricamente y validar de forma estructurada los fundamentos técnicos, jurídicos y éticos** que justifican por qué una solución Full Stack especializada es la única alternativa capaz de satisfacer los estándares humanitarios (CICR, 2021), de ciberseguridad (OWASP ASVS v5.0.0) y de privacidad legal (Ley N.° 787 de Nicaragua).

---

### 2. RESULTADOS DE LA EVALUACIÓN PONDERADA

De acuerdo con la matriz de evaluación multicriterio aplicada sobre los 10 parámetros esenciales, los resultados consolidados son los siguientes:

| Alternativa Evaluada | Puntuación Final Ponderada (Escala 1 a 5) | Equivalencia Porcentual Relativa (%) | Posición (Ranking) | Veredicto |
| :--- | :---: | :---: | :---: | :--- |
| **Alternativa A: Redes Sociales** | **2.00 / 5.00** | **40.0%** | 3.° Lugar | **Descartada** por graves vulnerabilidades a extorsión, violación de la Ley 787 e imposibilidad de moderación. |
| **Alternativa B: Portal Web Estático** | **2.80 / 5.00** | **56.0%** | 2.° Lugar | **Descartada** por rigidez operativa, cuello de botella manual, falta de seguimiento dinámico y pobre georreferenciación. |
| **Alternativa C: Plataforma Full Stack** | **4.60 / 5.00** | **92.0%** | **1.° Lugar** | **SELECCIONADA FORMALMENTE** como la solución óptima y ética para el proyecto. |

---

### 3. MOTIVOS DE LA SELECCIÓN DE LA ALTERNATIVA C

La superioridad indiscutible de la Alternativa C se fundamenta en cinco pilares interdisciplinarios:

#### 3.1. Motivos Jurídicos (Ley N.° 787 de Nicaragua)
- La difusión por redes sociales (Alt A) y los sitios web básicos (Alt B) violan sistemáticamente el derecho a la **autodeterminación informativa** (Art. 1 y 3) y el **derecho al olvido / cancelación** (Art. 16).
- La Alternativa C es la única que implementa un esquema formal de consentimiento legal informado en base de datos (`ConsentRecord`), procesa identificadores mediante hashes criptográficos irreversibles (SHA-256) cumpliendo el principio de minimización (Art. 6), y garantiza que al resolverse el caso la ficha pública sea **despublicada de manera instantánea** (`is_public = False`).

#### 3.2. Motivos de Ciberseguridad y Protección a la Integridad Física (OWASP ASVS v5.0.0)
- En redes sociales y portales estáticos, las imágenes subidas por los usuarios conservan metadatos **EXIF** que contienen las coordenadas GPS satelitales del domicilio familiar o la escuela de los hermanos del desaparecido, exponiéndolos a secuestros o represalias.
- La Alternativa C integra un pipeline forzado en el backend (`storage_service.py` con Pillow) que purga el 100% de metadatos GPS, convierte a formato WebP optimizado y genera identificadores criptográficos aleatorios, neutralizando cualquier riesgo de geolocalización involuntaria del declarante.
- Asimismo, la autenticación **Argon2id**, el control de acceso jerárquico (**RBAC**) y el rate limiting mitigan ataques de fuerza bruta y accesos no autorizados a testimonios confidenciales.

#### 3.3. Motivos Humanitarios y Metodología de "Carpetas Vivas" (CICR)
- El Comité Internacional de la Cruz Roja (CICR, 2023) exige que los expedientes de búsqueda sean dinámicos y acompañen a las familias a lo largo del tiempo.
- La Alternativa C materializa esta directriz mediante su **Línea de Tiempo Dinámica (`timeline`)**, registrando formalmente los hitos de investigación (registro formal, validación documental, activación territorial cívica, recepción de pistas y conclusión digna). Las alternativas A y B se limitan a anuncios fijos y muertos.

#### 3.4. Motivos Operativos y Prevención de Extorsiones
- En Centroamérica, la publicación de números telefónicos en redes sociales propicia que bandas delincuenciales extorsionen a las familias exigiendo dinero por supuestos datos (CICR, 2023).
- La Alternativa C suprime los teléfonos privados de las fichas públicas y canaliza los testimonios mediante un buzón institucional de pistas (`/pistas`) con opción de **anonimato estricto** y código de seguimiento único (`tip_code`), protegiendo simultáneamente a la familia y al informante.

#### 3.5. Motivos Geográficos y Cobertura Territorial Nacional (INIDE)
- Ninguna red social ni portal estático modela la realidad cartográfica de Nicaragua.
- La Alternativa C integra de forma nativa la cartografía oficial de los **15 departamentos, 2 regiones autónomas (RACCN y RACCS) y 153 municipios**, aplicando privacidad diferencial (georreferenciación aproximada a nivel municipal para evitar ubicar viviendas exactas en el mapa).

---

### 4. DESVENTAJAS, COMPLEJIDADES Y RIESGOS DE LA SOLUCIÓN FULL STACK

Una evaluación técnica rigurosa debe reconocer de forma honesta las complejidades y desventajas inherentes al desarrollo de una plataforma Full Stack:

1. **Mayor Demanda de Infraestructura y Costos Computacionales:**
   - A diferencia de un sitio estático servido en un hosting económico compartido, una plataforma Full Stack requiere un entorno de ejecución continuo para Python (servidor ASGI Uvicorn), memoria RAM suficiente para la transcodificación de imágenes con Pillow y persistencia en base de datos.
   
2. **Superficie de Ataque Ampliada:**
   - Al exponer endpoints de API REST (`/api/v1/...`), autenticación con JWT y subida de archivos multipart, el sistema está expuesto a vectores de ataque (inyección SQL, XSS, CSRF, ataques de fuerza bruta y DoS). Esto exige una disciplina estricta de parches de seguridad, auditorías continuas y mantenimiento preventivo.

3. **Curva de Aprendizaje y Necesidad de Personal Especializado:**
   - La operación de la mesa de moderación no puede delegarse a voluntarios sin entrenamiento básico. Se requiere capacitar a los operadores en la administración de roles, evaluación de verosimilitud de denuncias y cumplimiento de la Ley 787.

4. **Dependencia de Conectividad en el Cliente:**
   - La arquitectura web moderna (Next.js con hidratación de React) exige que el dispositivo cliente posea un navegador web compatible con JavaScript moderno, lo que puede representar una barrera en terminales de gama muy baja o zonas rurales sin datos móviles estables (lo que motiva la recomendación futura de un cliente PWA offline).

---

### 5. CONCLUSIÓN DEL VEREDICTO

A pesar de la mayor complejidad de ingeniería y los costos operativos asociados, **la Alternativa C (Plataforma Web Full Stack) es la única alternativa éticamente viable, jurídicamente legal y técnicamente segura**. 

Las Alternativas A y B, si bien son más económicas y rápidas de lanzar, trasladan el costo a las familias afectadas en forma de extorsión, revictimización, violación de sus datos personales y desarticulación operativa. La elección de la Alternativa C honra el principio humanitario de que las herramientas cívicas deben, ante todo, **no hacer daño** (*Do No Harm*).
"""
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(content.strip())
    print("Generado JUSTIFICACION_ALTERNATIVA_SELECCIONADA.md")

# -------------------------------------------------------------------------------------------------
# 6. ANALISIS_VIABILIDAD.md
# -------------------------------------------------------------------------------------------------
def generate_analisis_viabilidad():
    filepath = os.path.join(BASE_DIR, "ANALISIS_VIABILIDAD.md")
    content = r"""# ESTUDIO INTEGRAL DE VIABILIDAD DEL PROYECTO

## PROYECTO: ENCUÉNTRAME NICARAGUA
### Plataforma Cívica de Búsqueda y Reunificación Familiar
**Documento:** Evaluación Multidimensional de Viabilidad y Sostenibilidad  
**Fecha:** 24 de noviembre de 2026

---

### INTRODUCCIÓN

Para garantizar que la solución seleccionada (Alternativa C: Plataforma Web Full Stack) no sea únicamente un ejercicio teórico de software, sino una herramienta sostenible y de impacto tangible, se presenta la evaluación integral de viabilidad articulada en siete dimensiones:
1. Viabilidad técnica
2. Viabilidad económica
3. Viabilidad operativa
4. Viabilidad jurídica
5. Viabilidad social
6. Sostenibilidad a largo plazo
7. Riesgos residuales y matriz de mitigación

---

### 1. VIABILIDAD TÉCNICA

La viabilidad técnica evalúa la disponibilidad de herramientas, la madurez del stack tecnológico y la capacidad del sistema para cumplir los requerimientos de desempeño y confiabilidad.

#### Dictamen: **TOTALMENTE VIABLE (Plenamente Demostrada)**
- **Madurez del Stack:** Python 3.12, FastAPI, SQLAlchemy, Next.js 14, TypeScript y Leaflet representan tecnologías consolidadas a nivel global, con soporte comunitario masivo y documentación exhaustiva.
- **Evidencia Empírica de Funcionamiento:** La plataforma cuenta con una base de código funcional completa, como se documenta en `DOCUMENTACION_COMPLETA_PROYECTO.txt`. Se ha demostrado la generación de 61 rutas estáticas en Next.js (`npm run build`) y la aprobación exitosa de **38 de 38 pruebas unitarias y de integración en Pytest** (`38 passed in 2.78s`).
- **Autonomía Operativa:** El desacoplamiento de CDNs externas asegura que la plataforma no depende de proveedores foráneos para servir fuentes, estilos o scripts de mapas, funcionando en redes locales o servidores dedicados soberanos.

---

### 2. VIABILIDAD ECONÓMICA

La viabilidad económica analiza los costos de desarrollo, despliegue y mantenimiento, contrastándolos con el valor cívico generado.

#### Dictamen: **VIABLE CON ESTRUCTURA DE BAJO COSTO (Cost-Effective)**
- **Costos de Desarrollo:** La inversión en ingeniería de software ya ha sido ejecutada en su totalidad durante las fases de diseño, construcción y refinamiento del proyecto. No se requieren licencias de software privativas (100% basado en software libre y código abierto).
- **Costos de Servidores e Infraestructura (Cualitativo Justificado):**
  - La arquitectura híbrida es altamente eficiente: Next.js pre-renderiza contenido estático (SSG), reduciendo drásticamente la carga sobre el procesador.
  - La API de FastAPI es asíncrona y ligera. El sistema puede ejecutarse en un Servidor Virtual Privado (VPS) modesto (2 vCPUs, 2 a 4 GB RAM y 40 GB SSD de almacenamiento), con un coste mensual de mercado accesible para una organización no gubernamental o colectivo cívico.
  - El costo de almacenamiento para imágenes sanitizadas en formato WebP (800x800) es minúsculo: 1,000 fotografías ocupan en promedio menos de 100 MB en disco.
- **Retorno Social de Inversión (SROI):** El valor humanitario de prevenir una sola extorsión familiar o acelerar la localización de un menor supera ampliamente los costos marginales de hosting.

---

### 3. VIABILIDAD OPERATIVA

La viabilidad operativa determina si los procesos humanos, la administración de la plataforma y los flujos de moderación son sostenibles en la práctica diaria.

#### Dictamen: **ALTAMENTE VIABLE CON PROTOCOLOS DEFINIDOS**
- **Automatización de Tareas Críticas:** La transcodificación de imágenes, purga de EXIF, encriptación de identificadores de cédula, generación de códigos de pistas y asignación de números de caso ocurren de manera 100% automatizada en el backend, liberando al equipo humano de labores técnicas complejas.
- **Mesa de Moderación Ágil:** El panel `/admin` concentra las solicitudes entrantes bajo una interfaz intuitiva con acciones discretas de un solo clic: Aprobar (`approve`), Solicitar Modificaciones (`request_changes`) o Rechazar con Nota Justificada (`reject`).
- **Capacitación Requerida:** Un operador cívico promedio requiere menos de 4 horas de capacitación para dominar el flujo ético de validación documental y supervisión de pistas.

---

### 4. VIABILIDAD JURÍDICA

La viabilidad jurídica analiza la conformidad del sistema con el ordenamiento positivo vigente en la República de Nicaragua.

#### Dictamen: **VIABLE Y ALINEADO CON LA LEY N.° 787**
- **Autodeterminación y Consentimiento Informado (Arts. 1, 3 y 5):** Todo reporte formal incorpora una cláusula explícita de consentimiento legal bajo la Ley 787. No se admiten cargas sin manifestación expresa de voluntad.
- **Minimización de Datos (Art. 6):** Se prohíbe el almacenamiento en texto claro de números de cédula e IPs; se transforman irreversiblemente en hashes SHA-256 (`ConsentRecord`), protegiendo al declarante ante eventuales accesos no autorizados a la base de datos.
- **Derechos ARCO y Supresión Inmediata (Art. 16):** La plataforma implementa el endpoint formal `request-deletion` y el mecanismo de despublicación instantánea de casos resueltos (`request-close`), eliminando la información del dominio público para salvaguardar la intimidad cívica.
- **Protección a Menores (Ley N.° 287):** Se priorizan alertas de menores bajo el principio del interés superior del niño, supervisadas obligatoriamente por moderación humana.

---

### 5. VIABILIDAD SOCIAL

La viabilidad social examina la aceptación de la plataforma por parte de las familias, la comunidad y las organizaciones defensoras de derechos humanos.

#### Dictamen: **AMPLIAMENTE FAVORABLE Y DE ALTO IMPACTO**
- **Respaldo a Familias Desamparadas:** La plataforma llena un vacío crítico al ofrecer un espacio digno, ordenado y libre de estigmatizaciones frente al caos de las redes sociales.
- **Fomento de la Solidaridad Segura:** El canal confidencial de pistas (`/pistas`) empodera a los ciudadanos para colaborar con testimonios relevantes sin temor a ser expuestos públicamente ni involucrarse en procesos judiciales engorrosos.
- **Confianza Comunitaria:** La ausencia de anuncios comerciales y el rigor visual transmiten seriedad y neutralidad ética.

---

### 6. SOSTENIBILIDAD A LARGO PLAZO

La sostenibilidad asegura que el proyecto pueda perdurar en el tiempo sin degradar su servicio:
1. **Sostenibilidad Tecnológica:** Al utilizar código abierto estándar sin dependencias propietarias ni contratos de permanencia en la nube, el sistema puede migrarse libremente entre diferentes proveedores de infraestructura o alojarse en servidores locales.
2. **Sostenibilidad de Mantenimiento:** La presencia de 38 pruebas automatizadas de regresión en Pytest y tipado estricto con TypeScript permite que nuevos desarrolladores asuman el mantenimiento del código sin riesgo de corromper la lógica de negocio.
3. **Sostenibilidad Comunitaria:** La plataforma puede ser custodiada de forma colaborativa por consorcios de derechos humanos, universidades o redes de familiares de personas no localizadas.

---

### 7. RIESGOS RESIDUALES Y PLAN DE MITIGACIÓN

Todo sistema que procese datos sensibles conserva riesgos residuales que deben ser gestionados proactivamente:

| Riesgo Residual Identificado | Nivel de Impacto | Probabilidad | Medidas de Mitigación Implementadas en la Arquitectura |
| :--- | :---: | :---: | :--- |
| **1. Intentos de denegación de servicio (DoS) o ataques de fuerza bruta contra login y APIs** | Alto | Media | Rate limiting en memoria por IP (`rate_limit.py`), hashing Argon2id con alto costo computacional y servido estático SSG en frontend para desacoplar el tráfico de lectura. |
| **2. Carga malintencionada de imágenes corruptas o ejecutables encubiertos** | Alto | Baja | Validación estricta de firma binaria MIME, reconstrucción completa de imagen con Pillow (destrucción de payloads ocultos) y extensión forzada a `.webp`. |
| **3. Filtración de datos de declarantes ante intrusiones físicas a la base de datos** | Crítico | Muy Baja | Las cédulas y las direcciones IP no existen en texto claro; solo residen hashes criptográficos unidireccionales SHA-256 no reversibles. |
| **4. Brecha de conectividad en zonas rurales remotas (Costa Caribe)** | Medio | Alta | Optimización extrema del First Load JS (<120 KB), diseño mobile-first y recomendación formal de arquitectura para cliente offline PWA en fase 2. |
| **5. Cierre intempestivo de hosting o contingencia de infraestructura** | Medio | Baja | Base de datos relacional estándar SQLite/PostgreSQL fácilmente respaldable en archivos planos y portabilidad completa en contenedores Docker (`backend/Dockerfile`). |

---

### CONCLUSIÓN GENERAL DE VIABILIDAD

El proyecto **Encuéntrame Nicaragua** es **técnica, económica, operativa, jurídica y socialmente viable**. Resuelve una necesidad humanitaria indiscutible mediante una arquitectura moderna, segura, ética y legalmente irreprochable, consolidándose como una referencia de ingeniería de software al servicio de los derechos humanos.
"""
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(content.strip())
    print("Generado ANALISIS_VIABILIDAD.md")

if __name__ == "__main__":
    generate_analisis_tres_alternativas()
    generate_justificacion_seleccion()
    generate_analisis_viabilidad()
    print("\nTodos los documentos de la Entrega 02 generados exitosamente.")
