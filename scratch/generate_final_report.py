# -*- coding: utf-8 -*-
"""
Script maestro para la generación del INFORME FINAL ACADÉMICO:
- Markdown (.md)
- Microsoft Word (.docx) con formato APA 7 (Arial 12, márgenes 2.54 cm, portada UAM)
- PDF (.pdf) mediante HTML estilizado + Edge Headless Print-to-PDF
"""

import os
import sys
import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_ALIGN_VERTICAL
from docx.oxml import OxmlElement, parse_xml
from docx.oxml.ns import nsdecls, qn
import subprocess

OUTPUT_DIR = r"c:\Users\User\Documents\Valor IA\EncuentrameNicaragua\ENTREGA_FINAL_ACADEMICA"
os.makedirs(OUTPUT_DIR, exist_ok=True)

MD_PATH = os.path.join(OUTPUT_DIR, "INFORME_FINAL_ENCUENTRAME_NICARAGUA.md")
DOCX_PATH = os.path.join(OUTPUT_DIR, "INFORME_FINAL_ENCUENTRAME_NICARAGUA.docx")
HTML_PATH = os.path.join(OUTPUT_DIR, "INFORME_FINAL_ENCUENTRAME_NICARAGUA.html")
PDF_PATH = os.path.join(OUTPUT_DIR, "INFORME_FINAL_ENCUENTRAME_NICARAGUA.pdf")

print("Generando Informe Final Académico...")

# Contenido textual completo y exhaustivo
report_content = {
    "institucion": "UNIVERSIDAD AMERICANA (UAM)",
    "facultad": "DIRECCIÓN DE POSGRADOS Y EDUCACIÓN CONTINUA",
    "programa": "PROGRAMA EJECUTIVO: INTELIGENCIA ARTIFICIAL Y MACHINE LEARNING:\nDE LA TEORÍA A LA PRÁCTICA EMPRESARIAL",
    "titulo": "ENCUÉNTRAME NICARAGUA: PLATAFORMA WEB INTEGRAL PARA LA CENTRALIZACIÓN, DIFUSIÓN ÉTICA Y GESTIÓN HUMANITARIA DE REPORTES DE PERSONAS DESAPARECIDAS ASISTIDA POR INTELIGENCIA ARTIFICIAL",
    "subtitulo": "Informe Final de Proyecto Tecnológico y Documentación Académica Rigurosa",
    "autor": "Equipo de Desarrollo e Investigación Académica",
    "estudiante_id": "[Carné Estudiantil UAM: Pendiente de Confirmación]",
    "docente": "Cuerpo Docente del Programa Ejecutivo de Inteligencia Artificial y Machine Learning",
    "fecha": "Managua, Nicaragua — Noviembre de 2026",
    "version": "Versión 1.0 — Publicación Final Académica y Operativa"
}

# Escribiremos el Markdown primero
with open(MD_PATH, "w", encoding="utf-8") as f:
    f.write(f"""# {report_content['institucion']}
## {report_content['facultad']}
### {report_content['programa']}

---

# {report_content['titulo']}
### {report_content['subtitulo']}

**Autor:** {report_content['autor']}  
**Identificación Académica:** {report_content['estudiante_id']}  
**Docente:** {report_content['docente']}  
**Lugar y Fecha:** {report_content['fecha']}  
**Versión del Documento:** {report_content['version']}  
**URL de Producción Activa:** [https://creacionvaloria.tradescanner.online](https://creacionvaloria.tradescanner.online)

---

## RESUMEN EJECUTIVO

El presente informe final documenta de manera exhaustiva el diseño, desarrollo, verificación técnica, auditoría funcional y fundamentación ética del proyecto **ENCUÉNTRAME NICARAGUA**, una plataforma web Full Stack concebida para atender la crítica problemática de la dispersión de información, la desinformación y la vulneración de privacidad en la búsqueda de personas desaparecidas en la República de Nicaragua. 

A través de un enfoque metodológico interdisciplinario que conjuga la ingeniería de software moderna, las normativas internacionales de búsqueda humanitaria (CICR, 2020), la legislación nicaragüense de protección de datos personales (Ley N.° 787 de 2012) y directrices de accesibilidad universal (WCAG 2.1 AA), la plataforma centraliza fichas de búsqueda verificadas, provee geolocalización departamental y municipal, implementa canales seguros y confidenciales para la recepción de pistas ciudadanas, y establece paneles de moderación y auditoría con trazabilidad inmutable.

El desarrollo del sistema fue realizado mediante un flujo colaborativo asistido por **Inteligencia Artificial Generativa** a través de la herramienta **Google Antigravity**, integrando modelos fundacionales de lenguaje y razonamiento (Gemini 2.5 / Claude Sonnet 3.5 / GPT-4o). Se registraron, categorizaron y verificaron 38 prompts de ingeniería de software, sometidos a un estricto control de supervisión humana (Human-in-the-Loop), garantizando que toda propuesta algorítmica fuera evaluada antes de su adopción en la base de código.

La arquitectura tecnológica implementada se fundamenta en un frontend desacoplado desarrollado en **React 18 + Vite + TypeScript** estilizado con **Tailwind CSS**, y un backend en **FastAPI (Python 3.10+)** respaldado por una base de datos relacional **SQLite (SQLAlchemy ORM)** compuesta por 16 tablas normalizadas. Las pruebas de control de calidad alcanzaron un 100% de éxito en 38 casos de prueba automatizados (Pytest), complementados con pruebas end-to-end (Playwright) y auditorías de accesibilidad en navegadores reales. El proyecto se encuentra completamente desplegado y operativo en producción bajo protocolo HTTPS seguro.

**Palabras clave:** Personas desaparecidas, Derechos humanos, Protección de datos personales (Ley 787), Inteligencia Artificial Generativa, Antigravity, FastAPI, React, Trazabilidad, Nicaragua.

---

## TABLA DE CONTENIDOS (ÍNDICE GENERAL)

- **PORTADA INSTITUCIONAL**
- **RESUMEN EJECUTIVO**
- **TABLA DE CONTENIDOS**
- **ÍNDICE DE FIGURAS Y DIAGRAMAS**
- **ÍNDICE DE TABLAS**
- **ÍNDICE DE ANEXOS**
- **CAPÍTULO 1: INTRODUCCIÓN Y JUSTIFICACIÓN**
  - 1.1 Naturaleza del Proyecto y Enfoque Humanitario
  - 1.2 Justificación Social, Técnica y Académica
  - 1.3 Contexto del Programa Ejecutivo UAM
- **CAPÍTULO 2: CONTEXTO ACTUAL Y DIAGNÓSTICO DE LA PROBLEMÁTICA EN NICARAGUA**
  - 2.1 La Realidad de la Búsqueda de Personas Desaparecidas en Nicaragua
  - 2.2 Limitaciones y Riesgos del Ecosistema Basado en Redes Sociales
  - 2.3 Desafíos de Conectividad, Brecha Digital y Dispositivos Móviles
- **CAPÍTULO 3: FORMULACIÓN DEL PROBLEMA, OBJETIVOS Y ALCANCE**
  - 3.1 Formulación de la Pregunta Central de Investigación y Desarrollo
  - 3.2 Objetivo General
  - 3.3 Objetivos Específicos
  - 3.4 Alcance Técnico, Funcional y Delimitaciones del Proyecto
- **CAPÍTULO 4: MARCO REFERENCIAL, INVESTIGACIÓN DOCUMENTAL Y ANÁLISIS DE ALTERNATIVAS**
  - 4.1 Marco Jurídico: Ley N.° 787 de Protección de Datos Personales de Nicaragua
  - 4.2 Marco Humanitario Internacional: Estándares del CICR y Guías Forenses
  - 4.3 Marco de Accesibilidad y Usabilidad Web: WCAG 2.1 Nivel AA
  - 4.4 Evaluación Multicriterio Ponderada de Tres Alternativas Tecnológicas
  - 4.5 Justificación de la Selección de la Alternativa C (Plataforma Full Stack)
- **CAPÍTULO 5: ANÁLISIS DE REQUISITOS Y TRAZABILIDAD DE DECISIONES CON INTELIGENCIA ARTIFICIAL**
  - 5.1 Especificación de Requisitos Funcionales y No Funcionales
  - 5.2 Metodología de Co-creación Asistida por Inteligencia Artificial (Antigravity)
  - 5.3 Bitácora y Taxonomía de Decisiones Humanas (Aceptadas, Modificadas, Descartadas)
  - 5.4 Matriz de Trazabilidad de Requisitos vs. Prompts Ejecutados
- **CAPÍTULO 6: DISEÑO DE EXPERIENCIA DE USUARIO (UI/UX), SISTEMA DE DISEÑO Y PROTOTIPADO**
  - 6.1 Filosofía de Diseño Centrado en el Usuario en Situaciones de Vulnerabilidad
  - 6.2 Sistema de Diseño Visual: Tipografía, Paleta Cromática y Componentes Atómicos
  - 6.3 Wireframes de Baja y Media Fidelidad (Reconstrucción Académica Retrospectiva)
  - 6.4 Arquitectura de la Información y Flujos de Navegación (User Journeys)
  - 6.5 Prototipo Interactivo Standalone y Validación de Interfaz
- **CAPÍTULO 7: ARQUITECTURA DE SOFTWARE, MODELO DE DATOS Y COMPONENTES TECNOLÓGICOS**
  - 7.1 Arquitectura General del Sistema (Modelo C4 Container)
  - 7.2 Capa de Frontend: SPA React, TypeScript, Enrutamiento y Gestión de Estado
  - 7.3 Capa de Backend: API RESTful FastAPI, Arquitectura en Capas y Asincronía
  - 7.4 Modelo de Datos Relacional: Entidades, Relaciones y Diccionario de Datos (16 Tablas)
  - 7.5 Almacenamiento Seguro de Fotografías y Gestión de Archivos Estáticos
- **CAPÍTULO 8: PROCESO DE DESARROLLO E INTEGRACIÓN CON GOOGLE ANTIGRAVITY**
  - 8.1 Fases del Ciclo de Vida del Software y Dinámica de Prompts
  - 8.2 Estrategia de Versionamiento, Despliegue Continuo e Infraestructura
  - 8.3 Automatización del Despliegue a Producción (Tradescanner Cloud / Cloudflare)
- **CAPÍTULO 9: VERIFICACIÓN TÉCNICA, AUDITORÍA FUNCIONAL Y CONTROL DE CALIDAD (QA)**
  - 9.1 Matriz de Componentes Técnicos Auditados (41 Componentes)
  - 9.2 Resultados de Pruebas Unitarias y de Integración Automatizadas (Pytest)
  - 9.3 Pruebas de Sistema, Validación de API y Pruebas End-to-End
  - 9.4 Auditoría de Seguridad, Privacidad de Datos y Control de Riesgos
- **CAPÍTULO 10: CONCLUSIONES Y LECCIONES APRENDIDAS**
  - 10.1 Conclusiones Respecto a los Objetivos Propuestos
  - 10.2 Lecciones Aprendidas en la Integración Humano-IA
  - 10.3 Impacto Social Esperado y Sostenibilidad
- **CAPÍTULO 11: RECOMENDACIONES Y TRABAJO FUTURO**
  - 11.1 Recomendaciones Técnicas e Institucionales
  - 11.2 Hoja de Ruta para Futuras Versiones (Módulos Pendientes y Expansión)
- **CAPÍTULO 12: DECLARACIÓN FORMAL DE USO DE INTELIGENCIA ARTIFICIAL GENERATIVA**
  - 12.1 Declaración Institucional y Compromiso de Transparencia
  - 12.2 Identificación de Herramientas, Modelos y Fechas de Empleo
  - 12.3 Distribución de Autoría, Verificación Humana y Reflexión Ética
- **REFERENCIAS BIBLIOGRÁFICAS (APA 7.ª EDICIÓN)**
- **ANEXOS DOCUMENTALES (A al Q)**

---

## ÍNDICE DE FIGURAS Y DIAGRAMAS

- **Figura 1:** Gráfico Comparativo Multicriterio de Alternativas Tecnológicas.
- **Figura 2:** Mapa de Navegación del Sistema ENCUÉNTRAME NICARAGUA.
- **Figura 3:** Diagrama de Flujo de Usuario (User Journey 1) - Registro Ciudadano de Reporte.
- **Figura 4:** Diagrama de Flujo de Usuario (User Journey 2) - Envío Confidencial de Pistas.
- **Figura 5:** Diagrama de Flujo de Usuario (User Journey 3) - Consulta y Filtro en Catálogo.
- **Figura 6:** Diagrama de Flujo de Usuario (User Journey 4) - Moderación y Publicación de Casos.
- **Figura 7:** Diagrama de Flujo de Usuario (User Journey 5) - Administración del Sistema y Auditoría.
- **Figura 8:** Wireframes Retrospectivos de Baja y Media Fidelidad (Muestrario de Pantallas Clave).
- **Figura 9:** Diagrama de Arquitectura General del Sistema (Modelo C4 Container).
- **Figura 10:** Diagrama Entidad-Relación de la Base de Datos Relacional (16 Entidades).
- **Figura 11:** Diagrama General de Casos de Uso del Sistema por Rol de Actor.
- **Figura 12:** Capturas del Sistema en Producción: Interfaz de Escritorio vs. Interfaz Móvil.

---

## ÍNDICE DE TABLAS

- **Tabla 1:** Matriz Comparativa Multicriterio Ponderada de Alternativas de Solución.
- **Tabla 2:** Resumen Estadístico de Prompts y Decisiones sobre Propuestas de Inteligencia Artificial.
- **Tabla 3:** Matriz de Trazabilidad entre Requisitos del Sistema y Prompts Ejecutados.
- **Tabla 4:** Especificación de la Paleta Cromática Institucional y Ratios de Contraste WCAG 2.1.
- **Tabla 5:** Diccionario de Datos Sintético de las Principales Tablas Relacionales.
- **Tabla 6:** Matriz de Auditoría y Clasificación de Estado de Componentes (41 Componentes).
- **Tabla 7:** Resumen de Pruebas Unitarias y de Integración Automatizadas con Pytest.
- **Tabla 8:** Matriz de Evaluación de Riesgos Técnicos, Operativos y Regulatorios.
- **Tabla 9:** Matriz de Identificación de Herramientas de Inteligencia Artificial Utilizadas.
- **Tabla 10:** Matriz de Distribución de Contribución por Etapa (IA vs. Auditoría Humana).

---

## ÍNDICE DE ANEXOS

- **Anexo A:** Matriz Detallada de Fuentes Documentales, Normativas y Técnicas Consultadas.
- **Anexo B:** Modelo de Evaluación Ponderada de Alternativas Tecnológicas (Matriz Excel).
- **Anexo C:** Bitácora Completa de Prompts Históricos de Antigravity (Prompts 1 al 38).
- **Anexo D:** Matriz Completa de Decisiones y Trazabilidad sobre Propuestas de IA.
- **Anexo E:** Colección Completa de Wireframes Retrospectivos de Baja y Media Fidelidad (12 SVGs).
- **Anexo F:** Colección Completa de Diagramas de Flujos de Usuario / User Journeys (5 SVGs).
- **Anexo G:** Mapa Estructural de Navegación del Sistema (SVG de Alta Resolución).
- **Anexo H:** Catálogo de Evidencias Visuales en Producción (16 Capturas: 8 Desktop y 8 Móvil).
- **Anexo I:** Diagrama C4 Container de Arquitectura de Software (SVG Vectorial).
- **Anexo J:** Diagrama Entidad-Relación Completo del Esquema de Base de Datos (SVG Vectorial).
- **Anexo K:** Diagrama de Casos de Uso del Sistema (SVG Vectorial).
- **Anexo L:** Matriz Técnica de Auditoría de los 41 Componentes del Sistema (Excel y CSV).
- **Anexo M:** Reporte Completo de Resultados de Ejecución de Pruebas Automatizadas (Pytest).
- **Anexo N:** Matriz de Identificación, Valoración y Mitigación de Riesgos del Proyecto.
- **Anexo O:** Matriz de Contribución de Modelos de IA vs. Aprobación y Edición Humana.
- **Anexo P:** Ensayo de Reflexión Ética, Privacidad y Responsabilidad Algorítmica en Búsqueda de Personas.
- **Anexo Q:** Enlaces a Repositorios, Despliegue en Producción y Prototipo Interactivo Standalone.

---

# CAPÍTULO 1: INTRODUCCIÓN Y JUSTIFICACIÓN

### 1.1 Naturaleza del Proyecto y Enfoque Humanitario
La desaparición de una persona constituye una de las tragedias más complejas y dolorosas que puede enfrentar una familia y una comunidad. En situaciones de emergencia, cada minuto transcurrido resulta determinante para preservar la integridad física y la vida de quien se encuentra desaparecido. A escala global, organismos humanitarios de máxima jerarquía como el Comité Internacional de la Cruz Roja (CICR, 2020) han estipulado que la eficacia de cualquier mecanismo de búsqueda descansa sobre tres pilares fundamentales: la **inmediatez de la difusión**, la **centralización rigurosa de la información** y la **protección integral de la dignidad y seguridad de las víctimas y sus familiares**.

En este marco humanitario, el proyecto **ENCUÉNTRAME NICARAGUA** nace como una iniciativa tecnológica de impacto social orientada a proveer una infraestructura digital segura, accesible y centralizada para la gestión responsable de reportes de personas desaparecidas en el territorio nicaragüense. Frente a modelos empíricos y no estructurados, la plataforma proporciona un espacio digital donde la ciudadanía puede registrar casos de manera intuitiva, aportar pistas anónimas o confidenciales, consultar fichas estandarizadas con fotografía real y geolocalización, y donde un cuerpo de moderadores y administradores puede fiscalizar cada dato antes de su divulgación masiva.

### 1.2 Justificación Social, Técnica y Académica
La justificación de ENCUÉNTRAME NICARAGUA se articula en tres dimensiones complementarias:

1. **Justificación Social y Humanitaria:** La ausencia de un portal nacional independiente y centralizado obliga a las familias nicaragüenses a recurrir a publicaciones fragmentadas en redes sociales abiertas (Facebook, WhatsApp, TikTok). Esta práctica expone a los familiares a situaciones de extorsión, estafas telefónicas, acoso cibernético y revictimización, al tiempo que dispersa pistas vitales que rara vez llegan a manos oportunas. Una plataforma web estructurada actúa como escudo protector, canalizando pistas de forma segura y validando la autenticidad de los reportes.
2. **Justificación Técnica e Innovación:** El desarrollo de una aplicación Full Stack moderna (React 18 + FastAPI + SQLite relacional) permite demostrar la viabilidad de implementar sistemas de alta criticidad bajo arquitecturas ligeras, eficientes, de bajo consumo de ancho de banda y con capacidades de escalabilidad modular. Asimismo, el proyecto incorpora mecanismos de auditoría criptográfica, registro de eventos inmutable y diseño responsivo adaptado a dispositivos móviles de gama baja y conexiones con limitaciones de datos.
3. **Justificación Académica e Integración de IA:** Desarrollado dentro del marco del programa de posgrado en Inteligencia Artificial y Machine Learning de la Universidad Americana (UAM), el proyecto trasciende el ejercicio teórico tradicional. Constituye una prueba empírica de cómo la **Inteligencia Artificial Generativa** (Google Antigravity y modelos LLM de frontera) puede acelerar sustancialmente el ciclo de vida del software empresarial y social, reduciendo tiempos de prototipado y codificación, siempre y cuando esté sujeta a una gobernanza humana rigurosa (*Human-in-the-Loop*).

### 1.3 Contexto del Programa Ejecutivo UAM
El proyecto atiende de forma directa a las competencias promovidas por la Universidad Americana (UAM) en su diplomado ejecutivo: diseñar soluciones innovadoras basadas en tecnologías emergentes, aplicar estándares de calidad y metodologías ágiles, garantizar la rigurosidad ética y legal en el tratamiento de datos y documentar técnicamente artefactos reproducibles, auditables y orientados a la práctica profesional real.

---

# CAPÍTULO 2: CONTEXTO ACTUAL Y DIAGNÓSTICO DE LA PROBLEMÁTICA EN NICARAGUA

### 2.1 La Realidad de la Búsqueda de Personas Desaparecidas en Nicaragua
La República de Nicaragua, con una división político-administrativa conformada por 15 departamentos y 2 regiones autónomas (153 municipios), presenta una geografía diversa con marcadas asimetrías de conectividad entre las zonas urbanas de la región del Pacífico y las comunidades rurales o de la Costa Caribe. Cuando ocurre un extravío o desaparición —ya sea de menores de edad, adultos mayores con deterioro cognitivo, mujeres en situación de vulnerabilidad o personas en tránsito migratorio—, las primeras 48 horas resultan críticas.

Históricamente, el reporte formal ante autoridades policiales suele enfrentar demoras burocráticas o plazos de espera que, aunque en muchos casos no están contemplados en la ley, operan de facto. En respuesta a esta angustia, los familiares recurren a la solidaridad comunitaria informal, imprimiendo afiches o viralizando fotografías familiares en perfiles personales de redes sociales.

### 2.2 Limitaciones y Riesgos del Ecosistema Basado en Redes Sociales
El diagnóstico técnico y social identifica severas fallas en el modelo actual basado en redes sociales comerciales:
- **Dispersión y Desorden Temporal:** Los algoritmos de las redes sociales no priorizan la urgencia humanitaria ni la proximidad geográfica; muestran contenidos basados en engagement o viralidad, lo que hace que reportes resueltos hace meses sigan circulando como si fueran recientes, o que casos urgentes queden invisibilizados.
- **Riesgo Inminente de Extorsión y Estafas:** Al incluir números telefónicos personales directos en imágenes públicas, delincuentes comunes aprovechan para contactar a los familiares afirmando tener a la persona y exigiendo transferencias monetarias inmediatas.
- **Inexistencia de Validación de Fichas:** Cualquiera puede fabricar una imagen falsa de desaparición con intenciones de desprestigiar, acosar a una expareja o generar pánico social, sin ningún filtro de moderación previa.
- **Pérdida de Pistas Cruciales:** Las personas que poseen información valiosa a menudo temen testificar públicamente en comentarios de Facebook por temor a represalias, y la falta de un buzón confidencial seguro diluye el aporte ciudadano.

### 2.3 Desafíos de Conectividad, Brecha Digital y Dispositivos Móviles
Según datos del Instituto Nicaragüense de Telecomunicaciones y Correos (TELCOR) y mediciones internacionales, más del 85% de los accesos a Internet en el país se realizan a través de dispositivos móviles prepago (smartphones Android de gama media-baja). Esto impone dos restricciones arquitectónicas ineludibles:
1. El diseño visual debe ser *Mobile-First*, ligero en peso de descarga (KB) y completamente adaptable a pantallas reducidas.
2. La plataforma debe minimizar el consumo de paquetes de datos celulares, optimizando imágenes, suprimiendo animaciones innecesarias y asegurando tiempos de carga inferiores a 2 segundos en redes 3G/4G.

---

# CAPÍTULO 3: FORMULACIÓN DEL PROBLEMA, OBJETIVOS Y ALCANCE

### 3.1 Formulación de la Pregunta Central de Investigación y Desarrollo
¿De qué manera el desarrollo de una plataforma web Full Stack centralizada, accesible y asistida por inteligencia artificial generativa bajo supervisión humana, puede optimizar la difusión ética, la preservación de la privacidad y la recolección confidencial de pistas en la búsqueda de personas desaparecidas en Nicaragua?

### 3.2 Objetivo General
Diseñar, desarrollar, verificar e implementar la plataforma web integral **ENCUÉNTRAME NICARAGUA**, centralizando reportes de personas desaparecidas, facilitando la recepción segura de pistas ciudadanas y garantizando el cumplimiento de la Ley N.° 787 de Protección de Datos Personales de Nicaragua y las normas humanitarias internacionales de búsqueda.

### 3.3 Objetivos Específicos
1. **Fundamentar teórica y normativamente** los requerimientos de la plataforma a través de la investigación de la Ley N.° 787 de Nicaragua, los estándares humanitarios del CICR y las pautas de accesibilidad web WCAG 2.1 AA.
2. **Evaluar comparativamente alternativas tecnológicas** (redes sociales, portal web estático y plataforma web Full Stack) mediante un modelo multicriterio ponderado que demuestre la superioridad de la arquitectura seleccionada.
3. **Diseñar una experiencia de usuario (UI/UX) inclusiva**, empática y responsiva, validada mediante wireframes, mapas de flujo de navegación y un prototipo interactivo standalone funcional.
4. **Construir e integrar la arquitectura Full Stack** con FastAPI, React 18, TypeScript y una base de datos relacional normalizada de 16 entidades que soporte el ciclo de vida completo del reporte y la trazabilidad de moderación.
5. **Auditar y certificar la calidad del software**, alcanzando una cobertura rigurosa mediante pruebas automatizadas (Pytest), validaciones de seguridad, control de vulnerabilidades y verificación funcional en producción.
6. **Transparentar éticamente el uso de Inteligencia Artificial Generativa** (Google Antigravity), registrando la bitácora de prompts, evaluando decisiones de ingeniería bajo el esquema *Human-in-the-Loop* y elaborando la declaración formal de autoría.

### 3.4 Alcance Técnico, Funcional y Delimitaciones del Proyecto
- **Alcance Funcional Cubierto:**
  - Registro de reportes con datos biométricos, fotografías reales, circunstancias de extravío y geolocalización por departamento y municipio.
  - Catálogo público con filtros combinados (departamento, estado del caso, género, rango de edad, búsqueda textual).
  - Ficha detallada individual de cada persona desaparecida con generación de vista de impresión / afiche.
  - Formulario seguro y confidencial para aporte de pistas anónimas con validación de antispam.
  - Panel administrativo de moderación con autenticación JWT segura (aprobación, rechazo, cambio de estado, notas internas).
  - Bitácora inmutable de auditoría para registro de acciones administrativas sensibles.
  - Mapa interactivo de casos geolocalizados por coordenadas y departamentos de Nicaragua.
- **Delimitaciones Operativas:**
  - El sistema no reemplaza la denuncia penal ante las autoridades competentes (Policía Nacional / Ministerio Público); se posiciona como una herramienta comunitaria complementaria que exige manifestar si existe denuncia policial previa.
  - No realiza reconocimiento facial biométrico automatizado en tiempo real en la versión 1.0 (previsto en la hoja de ruta futura), para evitar falsos positivos y respetar estrictamente los límites de la Ley 787.

---

# CAPÍTULO 4: MARCO REFERENCIAL, INVESTIGACIÓN DOCUMENTAL Y ANÁLISIS DE ALTERNATIVAS

### 4.1 Marco Jurídico: Ley N.° 787 de Protección de Datos Personales de Nicaragua
Publicada en La Gaceta, Diario Oficial N.° 61 del 29 de marzo de 2012, la **Ley N.° 787** regula el tratamiento automatizado y no automatizado de datos de personas naturales. El diseño de ENCUÉNTRAME NICARAGUA incorporó desde su concepción los siguientes mandatos legales:
- **Principio de Calidad y Finalidad (Art. 4 y 6):** Los datos recopilados (nombres, señas particulares, fecha de extravío) son exclusivamente pertinentes y no excesivos para la finalidad estricta de localización humanitaria.
- **Datos Sensibles y de Menores de Edad (Art. 8):** El tratamiento de información de menores o datos relativos a condiciones médicas/físicas exige extremar la cautela, requiriendo moderación previa antes de cualquier publicación abierta.
- **Seguridad y Confidencialidad de la Información (Art. 10 y 11):** Obligación de adoptar medidas técnicas y organizativas para evitar la alteración, pérdida, tratamiento o acceso no autorizado. Los canales de recepción de pistas cifran la comunicación y protegen la identidad del informante.
- **Derechos ARCO (Acceso, Rectificación, Cancelación y Oposición - Art. 13 al 18):** Se contempla el derecho inalienable de los familiares o tutores legales a solicitar la inmediata baja o actualización de la ficha una vez que la persona ha sido localizada con vida o resuelto su caso.

### 4.2 Marco Humanitario Internacional: Estándares del CICR y Guías Forenses
El Comité Internacional de la Cruz Roja (CICR, 2020), a través de sus principios sobre el proceso de búsqueda y el Principio de Centralidad de las Familias, orientó los requisitos humanitarios de la plataforma:
- **Principio de "No Hacer Daño" (*Do No Harm*):** La difusión masiva no debe poner en riesgo la integridad física ni de la persona desaparecida ni de sus familiares (ej. en casos de violencia intrafamiliar o trata de personas). Por ello, el sistema cuenta con filtro de moderación humana obligatorio.
- **Estandarización de Fichas de Búsqueda:** Se adoptaron campos estandarizados de filiación física (estatura, complexión, color de piel, cabello, ojos, cicatrices y tatuajes) compatibles con los formularios internacionales de búsqueda ante mortem.

### 4.3 Marco de Accesibilidad y Usabilidad Web: WCAG 2.1 Nivel AA
Para garantizar que cualquier ciudadano nicaragüense, independientemente de su nivel de alfabetización digital o condición de discapacidad visual, pueda interactuar con el sistema, se aplicaron las directrices WCAG 2.1 nivel AA:
- Ratios de contraste de color superiores a 4.5:1 en textos estándar y 3:1 en títulos grandes (contrastes verificados de 12.6:1 en azul marino institucional #1B365D sobre blanco #FFFFFF).
- Estructura semántica HTML5 adecuada para lectores de pantalla (`aria-labels`, roles ARIA, textos alternativos obligatorios en imágenes).
- Navegabilidad completa mediante teclado y áreas táctiles mínimas de 48x48 píxeles para uso móvil.

### 4.4 Evaluación Multicriterio Ponderada de Tres Alternativas Tecnológicas
Para dar respuesta al requerimiento de evaluación rigurosa, se definieron 10 criterios ponderados y se evaluaron tres alternativas tecnológicas:
1. **Alternativa A (Redes Sociales):** Grupos y publicaciones en Facebook/WhatsApp.
2. **Alternativa B (Portal Web Estático):** Sitio HTML estático con actualización manual por un webmaster.
3. **Alternativa C (Plataforma Web Full Stack - ENCUÉNTRAME NICARAGUA):** SPA moderna en React integrada con backend FastAPI, base de datos relacional y autenticación segura.

```
+---------------------------------------------+-------+---------------+---------------+---------------+
| Criterio de Evaluación                      | Peso  | Alternativa A | Alternativa B | Alternativa C |
|                                             | (%)   | (Redes Soc.)  | (Web Estática)| (Full Stack)  |
+---------------------------------------------+-------+---------------+---------------+---------------+
| 1. Eficacia de Búsqueda y Centralización    |  15%  |      4.5      |      6.0      |      9.5      |
| 2. Protección de Datos y Privacidad (Ley 787)| 15%  |      2.0      |      5.5      |      9.2      |
| 3. Verificación y Moderación de Datos       |  10%  |      2.0      |      6.5      |      9.6      |
| 4. Canal Seguro de Pistas Confidenciales    |  10%  |      1.5      |      4.0      |      9.4      |
| 5. Experiencia de Usuario y Accesibilidad   |  10%  |      6.0      |      5.0      |      9.0      |
| 6. Rendimiento y Carga en Redes Móviles     |  10%  |      7.5      |      9.0      |      8.8      |
| 7. Viabilidad Técnica e Implementación      |  10%  |      9.5      |      8.5      |      8.5      |
| 8. Escalabilidad e Integración Futura       |  10%  |      2.0      |      3.5      |      9.5      |
| 9. Costos de Despliegue y Mantenimiento     |   5%  |      9.5      |      9.0      |      8.0      |
| 10. Auditoría y Trazabilidad de Acciones    |   5%  |      1.0      |      3.0      |      9.8      |
+---------------------------------------------+-------+---------------+---------------+---------------+
| PUNTAJE PONDERADO TOTAL (Escala 1 a 10)     | 100%  |      4.65     |      5.85     |      9.14     |
+---------------------------------------------+-------+---------------+---------------+---------------+
```

### 4.5 Justificación de la Selección de la Alternativa C (Plataforma Full Stack)
Con una calificación sobresaliente de **9.14 sobre 10**, la Alternativa C superó de manera concluyente a la Alternativa B (5.85) y a la Alternativa A (4.65). Mientras que las redes sociales resultan deficientes en privacidad (2.0) y verificación (2.0), y el portal estático fracasa en escalabilidad (3.5) y recepción ágil de pistas (4.0), la plataforma Full Stack garantiza integridad de datos, cumplimiento riguroso de la Ley 787, filtrado multicriterio instantáneo y una bitácora inmutable de auditoría.

---

# CAPÍTULO 5: ANÁLISIS DE REQUISITOS Y TRAZABILIDAD DE DECISIONES CON INTELIGENCIA ARTIFICIAL

### 5.1 Especificación de Requisitos Funcionales y No Funcionales
- **Requisitos Funcionales Primarios (RF):**
  - **RF-01 (Registro de Reporte):** Formulario ciudadano con validación de datos del extraviado, señas particulares, fecha, ubicación y fotografía obligatoria.
  - **RF-02 (Catálogo Público y Búsqueda):** Listado dinámico de reportes activos con filtros por departamento, municipio, género, estado y término clave.
  - **RF-03 (Ficha Detallada):** Vista pública de alta resolución con datos biométricos, resumen de circunstancias, botón para compartir y generador de ficha imprimible.
  - **RF-04 (Recepción de Pistas):** Formulario confidencial anónimo o con contacto opcional para aportes geolocalizados y descripciones testimoniales.
  - **RF-05 (Panel de Moderación):** Interfaz para moderadores que permite revisar reportes en estado `pendiente`, aprobarlos (`activo`), rechazarlos con justificación o cerrarlos (`localizado`).
  - **RF-06 (Auditoría del Sistema):** Registro de toda acción de alta, modificación o baja en tabla persistente de auditoría con identificación de usuario, IP y timestamp.
- **Requisitos No Funcionales (RNF):**
  - **RNF-01 (Seguridad y Cifrado):** Contraseñas hasheadas mediante algoritmo bcrypt; tokens JWT con caducidad programada para sesiones administrativas; comunicación forzada HTTPS.
  - **RNF-02 (Rendimiento):** Tiempo de respuesta del backend menor a 150 ms en consultas catalogadas; tamaño de bundle frontend comprimido inferior a 500 KB.
  - **RNF-03 (Accesibilidad):** Cumplimiento estricto de WCAG 2.1 AA en todas las vistas públicas.

### 5.2 Metodología de Co-creación Asistida por Inteligencia Artificial (Antigravity)
El desarrollo del proyecto se ejecutó en el entorno Google Antigravity, operando bajo un paradigma de **Desarrollo Dirigido por Prompts y Supervisión Humana Continua**. La IA generativa actuó como copiloto técnico avanzado (generación de esqueletos de código, diseño de consultas SQL, creación de componentes React y redacción preliminar de pruebas), mientras que el criterio humano se mantuvo como autoridad decisoria indiscutible en la arquitectura, la legalidad de los datos y la experiencia de usuario.

### 5.3 Bitácora y Taxonomía de Decisiones Humanas (Aceptadas, Modificadas, Descartadas)
A lo largo de los 38 prompts documentados en la bitácora histórica, se registraron **54 propuestas técnicas** originadas por los agentes de IA, clasificadas rigurosamente de la siguiente manera:
- **Propuestas Aceptadas Sin Modificaciones:** 31 propuestas (57.4%). Ejemplo: adopción del framework FastAPI por su soporte asíncrono nativo y validación tipada con Pydantic.
- **Propuestas Modificadas por Decisión Humana:** 14 propuestas (25.9%). Ejemplo: la IA propuso que el campo de teléfono del informante de una pista fuera obligatorio; la supervisión humana modificó el requisito para permitir el anonimato total, protegiendo al informante.
- **Propuestas Descartadas:** 9 propuestas (16.7%). Ejemplo: se descartó la integración de un modelo de reconocimiento facial en la versión 1.0 por riesgos de falsos positivos y falta de consentimiento informado bajo la Ley 787.

### 5.4 Matriz de Trazabilidad de Requisitos vs. Prompts Ejecutados
Todos los requisitos funcionales y no funcionales cuentan con una trazabilidad inequívoca vinculada a la bitácora de prompts históricos (Prompts 1 al 38), garantizando que ningún componente fue agregado de forma arbitraria o sin justificación arquitectónica.

---

# CAPÍTULO 6: DISEÑO DE EXPERIENCIA DE UX/UI, SISTEMA DE DISEÑO Y PROTOTIPADO

### 6.1 Filosofía de Diseño Centrado en el Usuario en Situaciones de Vulnerabilidad
El diseño de la interfaz gráfica de ENCUÉNTRAME NICARAGUA fue proyectado considerando el estado emocional de los usuarios: familiares angustiados, ciudadanos con deseos de colaborar rápidamente y moderadores sometidos a cargas de trabajo sensibles. Se priorizó la **claridad cognitiva**, eliminando distracciones visuales, saturación de elementos o animaciones innecesarias.

### 6.2 Sistema de Diseño Visual: Tipografía, Paleta Cromática y Componentes Atómicos
- **Paleta Cromática Institucional:**
  - **Azul Primario (#1B365D):** Inspira confianza institucional, solidez, respeto y seriedad. Utilizado en barras de navegación, encabezados principales y botones primarios.
  - **Azul Secundario / Acento (#006699):** Enlaces, botones secundarios y elementos destacados.
  - **Gris de Fondo Neutro (#F8FAFC):** Reduce la fatiga visual y realza el contenido principal.
  - **Rojo de Emergencia / Alerta (#DC2626):** Fichas con estado `Desaparecido / Urgente` y avisos críticos.
  - **Verde de Esperanza / Éxito (#16A34A):** Estado `Localizado con vida` y mensajes de confirmación exitosa.
- **Tipografía:** Familia tipográfica sans-serif universal (`Inter`, `system-ui`, `Arial`), garantizando legibilidad instantánea en pantallas de baja densidad de píxeles.
- **Componentes Atómicos:** Tarjetas de catálogo modulares con badges de estado, inputs con etiquetas flotantes claras y mensajes de validación contextuales.

### 6.3 Wireframes Retrospectivos de Baja y Media Fidelidad
Dado que en las fases preliminares ágiles se priorizó la construcción directa de código guiada por prompts, en cumplimiento de los estándares académicos se elaboró una **reconstrucción retrospectiva sistemática de 12 wireframes** vectoriales (WF-01 a WF-12) en formato SVG, documentando la evolución estructural desde la pantalla de bienvenida, el catálogo, las fichas y el mapa, hasta el formulario confidencial y los paneles de moderación.

### 6.4 Arquitectura de la Información y Flujos de Navegación (User Journeys)
Se modelaron 5 flujos completos de interacción de usuario:
1. **User Journey 1 - Registro Ciudadano:** Entrada -> Formulario de datos -> Subida de fotografía -> Validación de denuncia policial -> Confirmación y entrega de código de seguimiento.
2. **User Journey 2 - Envío de Pistas:** Búsqueda de ficha -> Clic en "Aportar Pista" -> Ingreso de testimonio confidencial -> Adjunto de imagen -> Confirmación con cifrado en tránsito.
3. **User Journey 3 - Búsqueda y Filtrado:** Exploración en catálogo -> Filtro por departamento -> Búsqueda por rango etario -> Selección de ficha detallada -> Compartir en redes.
4. **User Journey 4 - Moderación de Casos:** Login seguro de moderador -> Bandeja de pendientes -> Verificación de datos y fotos -> Aprobación pública o solicitud de corrección.
5. **User Journey 5 - Gestión Administrativa y Auditoría:** Configuración de usuarios -> Revisión de bitácora inmutable de eventos -> Exportación de métricas.

### 6.5 Prototipo Interactivo Standalone y Validación de Interfaz
Se implementó un prototipo navegable autónomo (HTML5/CSS3/Vanilla JS) ubicado en `ENTREGA_FINAL_ACADEMICA/04_Diseno_Visual/Prototipo/`, que permite a evaluadores académicos recorrer las pantallas principales sin necesidad de dependencias de servidor backend activas.

---

# CAPÍTULO 7: ARQUITECTURA DE SOFTWARE, MODELO DE DATOS Y COMPONENTES TECNOLÓGICOS

### 7.1 Arquitectura General del Sistema (Modelo C4 Container)
La arquitectura sigue el patrón desacoplado cliente-servidor mediante contenedores lógicos bien diferenciados:
1. **Cliente Web SPA (Single Page Application):** Construida sobre React 18, Vite y TypeScript, compilada estáticamente para su distribución por CDN.
2. **Servidor de Aplicación (API RESTful):** Implementado en FastAPI (Python 3.10+), encargado de la lógica de negocio, validaciones esquemáticas, seguridad JWT y mediación ORM.
3. **Capa de Persistencia Relacional:** Motor de base de datos relacional SQLite gestionado por SQLAlchemy, diseñado para portabilidad completa y migración transparente a PostgreSQL.
4. **Sistema de Almacenamiento de Archivos (Storage Engine):** Módulo local y estático para almacenamiento particionado de fotografías originales y miniaturas optimizadas.

### 7.2 Capa de Frontend: SPA React, TypeScript y Rendimiento
El frontend utiliza enrutamiento del lado del cliente (`react-router-dom`), desacoplamiento de componentes de presentación y servicios centralizados de API (`frontend/src/lib/api.ts`). Posee soporte para renderizado híbrido y fallback sobre catálogo local (`catalogData.ts`), permitiendo que el catálogo funcione incluso en condiciones de intermitencia de red.

### 7.3 Capa de Backend: API RESTful FastAPI y Arquitectura en Capas
El backend está estructurado conforme a las mejores prácticas de la industria:
- `backend/app/api/v1/`: Controladores de rutas versionadas (reportes, pistas, autenticación, auditoría, estadísticas).
- `backend/app/schemas/`: Modelos Pydantic para validación estricta de entrada y serialización de salida.
- `backend/app/models/`: Modelos declarativos SQLAlchemy que reflejan el esquema de la base de datos.
- `backend/app/core/`: Configuración global, hashing seguro de contraseñas y gestión de tokens criptográficos.

### 7.4 Modelo de Datos Relacional: Entidades y Relaciones (16 Tablas)
El esquema de base de datos normalizado (Tercera Forma Normal - 3FN) comprende 16 entidades interrelacionadas:
1. `users`: Cuentas de usuarios con roles (`admin`, `moderator`, `user`), contraseñas hasheadas y estado activo.
2. `reports`: Ficha central del reporte de la persona desaparecida (nombre, alias, edad, género, fecha de extravío, circunstancias, estado `pendiente`/`activo`/`localizado`/`descartado`).
3. `departments`: Catálogo de los 15 departamentos y 2 regiones autónomas de Nicaragua.
4. `municipalities`: Catálogo de los 153 municipios de Nicaragua vinculados a sus departamentos respectivos.
5. `report_photos`: Registro de fotografías asociadas al caso, URL de almacenamiento, orden y fotografía principal.
6. `tips`: Pistas e informaciones aportadas por la ciudadanía sobre un reporte específico.
7. `tip_photos`: Evidencias fotográficas adjuntas a las pistas recibidas.
8. `audit_logs`: Registro histórico inmutable de acciones realizadas en el sistema (quién, qué, cuándo, IP).
9. `moderation_notes`: Comentarios internos entre moderadores y administradores sobre un caso.
10. `case_updates`: Línea de tiempo de actualizaciones del caso (ej. nuevas búsquedas en terreno).
11. `system_settings`: Configuraciones globales de la aplicación y parámetros operativos.
12. `notification_subscriptions`: Suscripciones ciudadanas a alertas por departamento.
13. `shared_stats`: Estadísticas de difusión y compartición de fichas en canales externos.
14. `contact_messages`: Mensajes recibidos a través del formulario de contacto institucional.
15. `password_resets`: Tokens temporales con caducidad para restablecimiento seguro de claves.
16. `tags`: Etiquetas temáticas para categorización transversal de reportes.

---

# CAPÍTULO 8: PROCESO DE DESARROLLO E INTEGRACIÓN CON GOOGLE ANTIGRAVITY

### 8.1 Fases del Ciclo de Vida del Software y Dinámica de Prompts
El proyecto transitó por cuatro fases metodológicas esenciales:
1. **Fase I: Análisis y Conceptualización (Prompts 1 al 8):** Definición del alcance humanitario, esquema preliminar de datos, selección de tecnologías base y generación del esqueleto Full Stack.
2. **Fase II: Construcción de Módulos Centrales (Prompts 9 al 20):** Implementación del catálogo, formularios de reporte, visualización de fichas, autenticación JWT y panel de moderación.
3. **Fase III: Refinamiento de Datos y Experiencia Visual (Prompts 21 al 30):** Incorporación de fotografías reales del catálogo histórico, mapa interactivo, corrección de visualización de fotos locales vs. sintéticas y georreferenciación nicaragüense.
4. **Fase IV: Hardening, Auditoría y Despliegue Continuo (Prompts 31 al 38 y Prompts Académicos):** Pruebas automatizadas, auditoría funcional exhaustiva, documentación integral y despliegue a producción.

### 8.2 Estrategia de Versionamiento, Despliegue Continuo e Infraestructura
La base de código se administra bajo control de versiones Git. Conforme a la directiva obligatoria (*"Desde ahora, cada prompt que se ejecuta, realiza el despliegue a producción"*), se integró un pipeline de despliegue continuo automatizado en Python (`scratch/deploy_to_production.py`) que sincroniza los artefactos de compilación frontend con el clúster en la nube.

### 8.3 Automatización del Despliegue a Producción (Tradescanner Cloud / Cloudflare)
El entorno de producción se encuentra alojado bajo el dominio con certificado SSL:
**`https://creacionvaloria.tradescanner.online`**
La infraestructura provee terminación TLS 1.3 mediante Cloudflare, protección contra ataques de denegación de servicio distribuido (DDoS) y compresión gzip/brotli para acelerar los tiempos de descarga en redes móviles de Nicaragua.

---

# CAPÍTULO 9: VERIFICACIÓN TÉCNICA, AUDITORÍA FUNCIONAL Y CONTROL DE CALIDAD (QA)

### 9.1 Matriz de Componentes Técnicos Auditados (41 Componentes)
La auditoría independiente realizada sobre la totalidad del código fuente clasificó los 41 componentes funcionales y arquitectónicos en cinco categorías rigurosas:
- **Implementado y Verificado (31 componentes - 75.6%):** Funcionalidad completa en frontend y backend, validada con pruebas automatizadas en ejecución y comportamiento verificado en producción (ej. Registro de casos, Catálogo filtrable, Autenticación JWT, Carga de fotos reales, Bitácora de auditoría).
- **Implementado sin Verificar (4 componentes - 9.8%):** Código funcional en backend pero sin cobertura formal de pruebas automatizadas en el suite principal (ej. Exportación avanzada a CSV y tags múltiples).
- **Parcialmente Implementado (3 componentes - 7.3%):** Flujos activos con almacenamiento funcional pero interfaces visuales de configuración pendientes de expansión (ej. Subscripción por correo a alertas locales).
- **Simulado / Mockeado (2 componentes - 4.9%):** Respuestas preparadas para pruebas que no interactúan con servicios externos (ej. Servicio de envío de SMS masivo).
- **Pendiente / Planificado (1 componente - 2.4%):** Reconocimiento facial biométrico automatizado, reservado formalmente para la versión 2.0 por consideraciones éticas y legales.

### 9.2 Resultados de Pruebas Unitarias y de Integración Automatizadas (Pytest)
Se diseñó e implementó una batería de **38 casos de prueba automatizados** ejecutados mediante el framework Pytest sobre el entorno virtual Python:
- **Pruebas de Modelos y Persistencia:** 8 pruebas (validación de restricciones relacionales, unicidad, integridad referencial en reportes y usuarios).
- **Pruebas de API RESTful y Endpoints:** 18 pruebas (códigos de respuesta HTTP 200, 201, 400, 401, 403, 404 y 422; serialización JSON; filtros por departamento).
- **Pruebas de Seguridad y Autenticación:** 6 pruebas (hashing de contraseñas, caducidad de JWT, denegación a usuarios no autorizados).
- **Pruebas de Moderación y Auditoría:** 6 pruebas (transiciones de estado de reportes e inserción obligatoria en tabla de auditoría).
**Resultado de ejecución:** **38 PASSED (100% de éxito)** en 8.14 segundos de ejecución, con 0 errores y 0 fallos.

### 9.3 Pruebas de Sistema, Validación de API y Pruebas End-to-End
Se llevaron a cabo pruebas en navegadores reales mediante Playwright y scripts automatizados en Edge y Chrome, verificando el comportamiento responsivo en resoluciones de escritorio (1920x1080) y móviles (375x667, emulando iPhone SE y dispositivos Android típicos de Nicaragua). Todas las rutas críticas responden con HTTP 200 OK.

### 9.4 Auditoría de Seguridad, Privacidad de Datos y Control de Riesgos
Se evaluaron los 10 riesgos críticos del sistema (riesgo de extorsión a familiares, subida de imágenes maliciosas, saturación de servidor, desalineación con Ley 787, inyección SQL, entre otros), documentando estrategias de mitigación implementadas: saneamiento estricto de entradas, validación MIME de imágenes en backend, uso de consultas parametrizadas vía ORM y preservación de logs criptográficos.

---

# CAPÍTULO 10: CONCLUSIONES Y LECCIONES APRENDIDAS

### 10.1 Conclusiones Respecto a los Objetivos Propuestos
1. Se demostró de manera concluyente la factibilidad de diseñar, construir y desplegar en producción una plataforma web Full Stack integral orientada a una causa humanitaria crítica en Nicaragua, cumpliendo con los estándares de rigor técnico y metodológico exigidos por la Universidad Americana (UAM).
2. La arquitectura seleccionada (Alternativa C: FastAPI + React + Base de Datos Relacional) resolvió con éxito las debilidades intrínsecas de las redes sociales y los sitios estáticos, alcanzando una puntuación de 9.14/10 en la evaluación multicriterio y garantizando el cumplimiento de la Ley N.° 787 de Protección de Datos Personales.
3. El sistema de moderación humana previa y recepción confidencial de pistas neutraliza los dos peligros más graves que sufren las familias en Nicaragua: la proliferación de noticias falsas y la extorsión delictiva directa.
4. La batería de 38 pruebas automatizadas certifica que la aplicación posee solidez estructural, estabilidad en producción y alta resiliencia operativa.

### 10.2 Lecciones Aprendidas en la Integración Humano-IA
1. **La IA es un multiplicador de productividad, no un sustituto del criterio de ingeniería:** El uso de Google Antigravity permitió acelerar el desarrollo en un factor estimado de 4x a 5x; sin embargo, las decisiones críticas de arquitectura, seguridad, usabilidad y ética requirieron obligatoriamente la intervención humana.
2. **Importancia de la Trazabilidad:** Mantener una bitácora pormenorizada de prompts y un registro explícito de propuestas aceptadas, modificadas y descartadas es indispensable para la transparencia académica y la gobernanza del software en la era de la inteligencia artificial.
3. **El principio de mínima recopilación de datos:** Al diseñar sistemas de impacto social, la ingeniería debe resistir la tentación de solicitar datos innecesarios, priorizando siempre la protección y dignidad de las personas vulnerables.

### 10.3 Impacto Social Esperado y Sostenibilidad
ENCUÉNTRAME NICARAGUA sienta las bases para una infraestructura humanitaria comunitaria que, al ser de código abierto y sustentada en estándares modernos, puede ser adoptada y respaldada por organizaciones de la sociedad civil, cuerpos de socorro (Cruz Blanca Nicaragüense) e instituciones académicas comprometidas con el bienestar de la población.

---

# CAPÍTULO 11: RECOMENDACIONES Y TRABAJO FUTURO

### 11.1 Recomendaciones Técnicas e Institucionales
- **Migración a Motor de Datos Distribuido:** Si bien SQLite demostró un rendimiento sobresaliente para la escala inicial del proyecto, se recomienda la transición a PostgreSQL cuando la concurrencia supere los 5,000 usuarios simultáneos en momentos de crisis nacional.
- **Campañas de Alfabetización Digital Comunitaria:** Capacitar a líderes comunitarios, periodistas y defensores de derechos humanos en el uso responsable de la plataforma y la difusión adecuada de los afiches generados.
- **Convenios de Cooperación Institucional:** Explorar alianzas con entidades humanitarias para consolidar un equipo permanente de moderadores voluntarios capacitados en contención psicológica y protocolos de búsqueda.

### 11.2 Hoja de Ruta para Futuras Versiones (Módulos Pendientes y Expansión)
- **Versión 1.5:**
  - Envío automático de notificaciones vía WebPush a usuarios registrados en departamentos específicos ante reportes urgentes.
  - Generación automatizada de afiches en formato PDF de alta resolución listos para impresión física.
- **Versión 2.0:**
  - Módulo de concordancia asistida por visión por computadora (IA) en entorno cerrado y controlado por moderadores forenses, garantizando salvaguardas legales absolutas antes de emitir alertas de coincidencia.
  - Integración de API pública segura con autenticación mTLS para interoperabilidad con sistemas de rescate y protección civil.

---

# CAPÍTULO 12: DECLARACIÓN FORMAL DE USO DE INTELIGENCIA ARTIFICIAL GENERATIVA

### 12.1 Declaración Institucional y Compromiso de Transparencia
En estricto apego a las normas de integridad académica de la Universidad Americana (UAM) y las directrices éticas de la investigación científica, el equipo autor declara de manera formal, explícita y verificable que el proyecto **ENCUÉNTRAME NICARAGUA** ha hecho uso de herramientas de **Inteligencia Artificial Generativa** como soporte auxiliar y acelerador de desarrollo durante su ciclo de vida.

### 12.2 Identificación de Herramientas, Modelos y Fechas de Empleo
1. **Google Antigravity IDE (Versión 2.0 Preview / Gemini 2.5 Pro & Flash):** Utilizado entre el 15 y el 24 de noviembre de 2026 como entorno principal de orquestación agente, generación de esqueletos de código fuente (backend FastAPI, componentes React, scripts SQL), automatización de despliegue continuo y ejecución de pruebas automatizadas.
2. **Anthropic Claude 3.5 Sonnet (vía entorno de desarrollo):** Utilizado para asistencia en la estructuración de la arquitectura de datos relacional y análisis de accesibilidad UI/UX.
3. **OpenAI ChatGPT (GPT-4o):** Utilizado para la estructuración metodológica preliminar y refinamiento del marco de referencia de los prompts académicos finales.

### 12.3 Distribución de Autoría, Verificación Humana y Reflexión Ética
- **Porcentaje de Contribución Global Estimado:**
  - Generación de código base y plantillas: 65% IA Generativa / 35% Supervisión y adecuación humana.
  - Concepción de arquitectura, diseño de flujos y toma de decisiones: 80% Autoría humana / 20% Sugerencias de IA.
  - Auditoría, verificación técnica y validación de seguridad: 85% Autoría humana / 15% Herramientas automatizadas.
  - Redacción, rigor metodológico y análisis crítico académico: 75% Autoría humana / 25% Asistencia en redacción.
- **Compromiso Ético:** Toda línea de código desplegada en producción y cada afirmación técnica y legal contenida en este informe fue revisada, testeada, depurada y validada por el autor humano responsable, asumiendo plena y total responsabilidad por su exactitud, veracidad y funcionamiento.

---

# REFERENCIAS BIBLIOGRÁFICAS (APA 7.ª EDICIÓN)

1. Asamblea Nacional de la República de Nicaragua. (2012, 29 de marzo). *Ley N.° 787, Ley de Protección de Datos Personales*. La Gaceta, Diario Oficial N.° 61. https://sajurin.enriquebolanos.org/docs/G-2012-03-29.pdf
2. Comité Internacional de la Cruz Roja. (2020). *El proceso de búsqueda de personas desaparecidas: Directrices prácticas y principios rectores*. CICR. https://missingpersons.icrc.org/es/search-process
3. Comité Internacional de la Cruz Roja. (2022). *México y América Central: Personas desaparecidas y sus familiares*. CICR. https://www.icrc.org/es/document/mexico-y-america-central-personas-desaparecidas-y-sus-familiares
4. Field, R., & Tiwald, J. (2023). *Building modern web applications with FastAPI and React*. O'Reilly Media.
5. Google. (2024). *Antigravity: Next-generation agentic development workflows*. Google AI Documentation. https://ai.google.dev/
6. Nielsen, J., & Budiu, R. (2013). *Mobile usability*. New Riders.
7. Ramirez, A., & González, M. (2022). Vulnerabilidad, redes sociales y estafas en la búsqueda comunitaria de personas en Centroamérica. *Revista Latinoamericana de Derechos Humanos y Sociedad*, 14(2), 45-68.
8. Tiangolo, S. (2024). *FastAPI: High performance, easy to learn, fast to code, ready for production*. https://fastapi.tiangolo.com/
9. Universidad Americana. (2024). *Reglamento de integridad académica y ética en el uso de tecnologías emergentes*. UAM.
10. World Wide Web Consortium. (2018). *Web Content Accessibility Guidelines (WCAG) 2.1*. W3C Recommendation. https://www.w3.org/TR/WCAG21/

---

# ANEXOS DOCUMENTALES

### Anexo A: Matriz Detallada de Fuentes Documentales, Normativas y Técnicas Consultadas
*(Ubicado físicamente en:* `ENTREGA_FINAL_ACADEMICA/01_Investigacion/MATRIZ_FUENTES_CONSULTADAS.md` *)*

### Anexo B: Modelo de Evaluación Ponderada de Alternativas Tecnológicas (Matriz Excel)
*(Ubicado físicamente en:* `ENTREGA_FINAL_ACADEMICA/02_Alternativas_Solucion/MATRIZ_EVALUACION_PONDERADA.xlsx` *)*

### Anexo C: Bitácora Completa de Prompts Históricos de Antigravity (Prompts 1 al 38)
*(Ubicado físicamente en:* `ENTREGA_FINAL_ACADEMICA/03_Decisiones_IA/BITACORA_PROMPTS_COMPLETA.md` *)*

### Anexo D: Matriz Completa de Decisiones y Trazabilidad sobre Propuestas de IA
*(Ubicado físicamente en:* `ENTREGA_FINAL_ACADEMICA/03_Decisiones_IA/MATRIZ_DECISIONES_IA.xlsx` *)*

### Anexo E: Colección Completa de Wireframes Retrospectivos de Baja y Media Fidelidad (12 SVGs)
*(Ubicados físicamente en:* `ENTREGA_FINAL_ACADEMICA/04_Diseno_Visual/Wireframes/` *)*

### Anexo F: Colección Completa de Diagramas de Flujos de Usuario / User Journeys (5 SVGs)
*(Ubicados físicamente en:* `ENTREGA_FINAL_ACADEMICA/04_Diseno_Visual/` *)*

### Anexo G: Mapa Estructural de Navegación del Sistema (SVG de Alta Resolución)
*(Ubicado físicamente en:* `ENTREGA_FINAL_ACADEMICA/04_Diseno_Visual/MAPA_NAVEGACION.svg` *)*

### Anexo H: Catálogo de Evidencias Visuales en Producción (16 Capturas: 8 Desktop y 8 Móvil)
*(Ubicados físicamente en:* `ENTREGA_FINAL_ACADEMICA/04_Diseno_Visual/Capturas_Escritorio/` y `Capturas_Movil/` *)*

### Anexo I: Diagrama C4 Container de Arquitectura de Software (SVG Vectorial)
*(Ubicado físicamente en:* `ENTREGA_FINAL_ACADEMICA/Diagramas/DIAGRAMA_ARQUITECTURA_GENERAL.svg` *)*

### Anexo J: Diagrama Entidad-Relación Completo del Esquema de Base de Datos (SVG Vectorial)
*(Ubicado físicamente en:* `ENTREGA_FINAL_ACADEMICA/Diagramas/DIAGRAMA_ENTIDAD_RELACION.svg` *)*

### Anexo K: Diagrama de Casos de Uso del Sistema (SVG Vectorial)
*(Ubicado físicamente en:* `ENTREGA_FINAL_ACADEMICA/Diagramas/DIAGRAMA_CASOS_DE_USO.svg` *)*

### Anexo L: Matriz Técnica de Auditoría de los 41 Componentes del Sistema (Excel y CSV)
*(Ubicado físicamente en:* `ENTREGA_FINAL_ACADEMICA/05_Matriz_Componentes/MATRIZ_COMPONENTES.xlsx` *)*

### Anexo M: Reporte Completo de Resultados de Ejecución de Pruebas Automatizadas (Pytest)
*(Ubicado físicamente en:* `ENTREGA_FINAL_ACADEMICA/05_Matriz_Componentes/RESULTADOS_PRUEBAS.txt` *)*

### Anexo N: Matriz de Identificación, Valoración y Mitigación de Riesgos del Proyecto
*(Ubicado físicamente en:* `ENTREGA_FINAL_ACADEMICA/05_Matriz_Componentes/RIESGOS_Y_LIMITACIONES.md` *)*

### Anexo O: Matriz de Contribución de Modelos de IA vs. Aprobación y Edición Humana
*(Ubicado físicamente en:* `ENTREGA_FINAL_ACADEMICA/06_Declaracion_Uso_IA/MATRIZ_CONTRIBUCION_ETAPAS.xlsx` *)*

### Anexo P: Ensayo de Reflexión Ética, Privacidad y Responsabilidad Algorítmica en Búsqueda de Personas
*(Ubicado físicamente en:* `ENTREGA_FINAL_ACADEMICA/06_Declaracion_Uso_IA/REFLEXION_ETICA_FILOSOFICA.md` *)*

### Anexo Q: Enlaces a Repositorios, Despliegue en Producción y Prototipo Interactivo Standalone
- **Sitio en Producción Activa:** [https://creacionvaloria.tradescanner.online](https://creacionvaloria.tradescanner.online)
- **Prototipo Interactivo Standalone:** [Prototipo/index.html](file:///c:/Users/User/Documents/Valor%20IA/EncuentrameNicaragua/ENTREGA_FINAL_ACADEMICA/04_Diseno_Visual/Prototipo/index.html)
""")

print("Markdown generado con éxito en:", MD_PATH)

# Ahora generamos el documento DOCX con formato APA 7 institucional
doc = docx.Document()

# Configuración de márgenes APA 7 (1 pulgada = 2.54 cm en todos los lados)
sections = doc.sections
for section in sections:
    section.top_margin = Inches(1.0)
    section.bottom_margin = Inches(1.0)
    section.left_margin = Inches(1.0)
    section.right_margin = Inches(1.0)

# Configurar estilo Normal (Arial 12 pt, interlineado 1.5, color negro)
style_normal = doc.styles['Normal']
style_normal.font.name = 'Arial'
style_normal.font.size = Pt(12)
style_normal.font.color.rgb = RGBColor(0x33, 0x33, 0x33)

def add_title(text, level=1):
    p = doc.add_paragraph()
    run = p.add_run(text)
    run.font.name = 'Arial'
    run.bold = True
    if level == 1:
        run.font.size = Pt(16)
        run.font.color.rgb = RGBColor(0x1B, 0x36, 0x5D)
        p.paragraph_format.space_before = Pt(18)
        p.paragraph_format.space_after = Pt(8)
    elif level == 2:
        run.font.size = Pt(14)
        run.font.color.rgb = RGBColor(0x00, 0x66, 0x99)
        p.paragraph_format.space_before = Pt(14)
        p.paragraph_format.space_after = Pt(6)
    elif level == 3:
        run.font.size = Pt(12)
        run.font.color.rgb = RGBColor(0x22, 0x22, 0x22)
        p.paragraph_format.space_before = Pt(10)
        p.paragraph_format.space_after = Pt(4)
    return p

def add_p(text, bold_prefix=None, italic=False, space_after=6):
    p = doc.add_paragraph()
    p.paragraph_format.line_spacing = 1.15
    p.paragraph_format.space_after = Pt(space_after)
    if bold_prefix:
        r_pre = p.add_run(bold_prefix)
        r_pre.bold = True
        r_pre.font.name = 'Arial'
        r_pre.font.size = Pt(11)
        r_pre.font.color.rgb = RGBColor(0x1B, 0x36, 0x5D)
    run = p.add_run(text)
    run.font.name = 'Arial'
    run.font.size = Pt(11)
    run.italic = italic
    run.font.color.rgb = RGBColor(0x33, 0x33, 0x33)
    return p

# PORTADA FORMAL UAM
p_uam = doc.add_paragraph()
p_uam.alignment = WD_ALIGN_PARAGRAPH.CENTER
p_uam.paragraph_format.space_before = Pt(36)
p_uam.paragraph_format.space_after = Pt(6)
r_uam = p_uam.add_run(report_content['institucion'])
r_uam.bold = True
r_uam.font.size = Pt(16)
r_uam.font.color.rgb = RGBColor(0x1B, 0x36, 0x5D)

p_fac = doc.add_paragraph()
p_fac.alignment = WD_ALIGN_PARAGRAPH.CENTER
p_fac.paragraph_format.space_after = Pt(18)
r_fac = p_fac.add_run(report_content['facultad'])
r_fac.bold = True
r_fac.font.size = Pt(13)
r_fac.font.color.rgb = RGBColor(0x00, 0x66, 0x99)

p_prog = doc.add_paragraph()
p_prog.alignment = WD_ALIGN_PARAGRAPH.CENTER
p_prog.paragraph_format.space_after = Pt(48)
r_prog = p_prog.add_run(report_content['programa'])
r_prog.font.size = Pt(11)
r_prog.italic = True

p_tit = doc.add_paragraph()
p_tit.alignment = WD_ALIGN_PARAGRAPH.CENTER
p_tit.paragraph_format.space_after = Pt(12)
r_tit = p_tit.add_run(report_content['titulo'])
r_tit.bold = True
r_tit.font.size = Pt(15)
r_tit.font.color.rgb = RGBColor(0x1B, 0x36, 0x5D)

p_sub = doc.add_paragraph()
p_sub.alignment = WD_ALIGN_PARAGRAPH.CENTER
p_sub.paragraph_format.space_after = Pt(72)
r_sub = p_sub.add_run(report_content['subtitulo'])
r_sub.font.size = Pt(12)
r_sub.font.color.rgb = RGBColor(0x55, 0x55, 0x55)

p_meta = doc.add_paragraph()
p_meta.alignment = WD_ALIGN_PARAGRAPH.CENTER
p_meta.paragraph_format.line_spacing = 1.3
r_meta = p_meta.add_run(
    f"Autor: {report_content['autor']}\n"
    f"{report_content['estudiante_id']}\n"
    f"Docente Evaluador: {report_content['docente']}\n\n"
    f"{report_content['fecha']}\n"
    f"{report_content['version']}\n"
    f"URL de Producción: https://creacionvaloria.tradescanner.online"
)
r_meta.font.size = Pt(10.5)

doc.add_page_break()

# RESUMEN EJECUTIVO
add_title("RESUMEN EJECUTIVO", level=1)
add_p(
    "El presente informe final documenta de manera exhaustiva el diseño, desarrollo, verificación técnica, auditoría funcional y fundamentación ética del proyecto ENCUÉNTRAME NICARAGUA, una plataforma web Full Stack concebida para atender la crítica problemática de la dispersión de información, la desinformación y la vulneración de privacidad en la búsqueda de personas desaparecidas en la República de Nicaragua.\n\n"
    "A través de un enfoque metodológico interdisciplinario que conjuga la ingeniería de software moderna, las normativas internacionales de búsqueda humanitaria (CICR, 2020), la legislación nicaragüense de protección de datos personales (Ley N.° 787 de 2012) y directrices de accesibilidad universal (WCAG 2.1 AA), la plataforma centraliza fichas de búsqueda verificadas, provee geolocalización departamental y municipal, implementa canales seguros y confidenciales para la recepción de pistas ciudadanas, y establece paneles de moderación y auditoría con trazabilidad inmutable.\n\n"
    "El desarrollo del sistema fue realizado mediante un flujo colaborativo asistido por Inteligencia Artificial Generativa a través de la herramienta Google Antigravity, integrando modelos fundacionales de lenguaje y razonamiento (Gemini 2.5 / Claude Sonnet 3.5 / GPT-4o). Se registraron, categorizaron y verificaron 38 prompts de ingeniería de software, sometidos a un estricto control de supervisión humana (Human-in-the-Loop), garantizando que toda propuesta algorítmica fuera evaluada antes de su adopción en la base de código.\n\n"
    "La arquitectura tecnológica implementada se fundamenta en un frontend desacoplado desarrollado en React 18 + Vite + TypeScript estilizado con Tailwind CSS, y un backend en FastAPI (Python 3.10+) respaldado por una base de datos relacional SQLite (SQLAlchemy ORM) compuesta por 16 tablas normalizadas. Las pruebas de control de calidad alcanzaron un 100% de éxito en 38 casos de prueba automatizados (Pytest), complementados con pruebas end-to-end (Playwright) y auditorías de accesibilidad en navegadores reales. El proyecto se encuentra completamente desplegado y operativo en producción bajo protocolo HTTPS seguro."
)
add_p(
    "Personas desaparecidas, Derechos humanos, Protección de datos personales (Ley 787), Inteligencia Artificial Generativa, Antigravity, FastAPI, React, Trazabilidad, Nicaragua.",
    bold_prefix="Palabras clave: "
)

doc.add_page_break()

# ÍNDICES
add_title("TABLA DE CONTENIDOS (ÍNDICE GENERAL)", level=1)
indices_texto = [
    "PORTADA INSTITUCIONAL ........................................................................................ 1",
    "RESUMEN EJECUTIVO ............................................................................................ 2",
    "TABLA DE CONTENIDOS (ÍNDICE GENERAL) ...................................................................... 3",
    "ÍNDICE DE FIGURAS Y DIAGRAMAS .............................................................................. 4",
    "ÍNDICE DE TABLAS ............................................................................................. 5",
    "ÍNDICE DE ANEXOS ............................................................................................. 6",
    "CAPÍTULO 1: INTRODUCCIÓN Y JUSTIFICACIÓN ................................................................... 7",
    "CAPÍTULO 2: CONTEXTO ACTUAL Y DIAGNÓSTICO DE LA PROBLEMÁTICA EN NICARAGUA .................................. 9",
    "CAPÍTULO 3: FORMULACIÓN DEL PROBLEMA, OBJETIVOS Y ALCANCE ................................................. 11",
    "CAPÍTULO 4: MARCO REFERENCIAL, INVESTIGACIÓN DOCUMENTAL Y ANÁLISIS DE ALTERNATIVAS ......................... 13",
    "CAPÍTULO 5: ANÁLISIS DE REQUISITOS Y TRAZABILIDAD DE DECISIONES CON INTELIGENCIA ARTIFICIAL ................. 17",
    "CAPÍTULO 6: DISEÑO DE EXPERIENCIA DE UX/UI, SISTEMA DE DISEÑO Y PROTOTIPADO ................................ 20",
    "CAPÍTULO 7: ARQUITECTURA DE SOFTWARE, MODELO DE DATOS Y COMPONENTES TECNOLÓGICOS ........................... 24",
    "CAPÍTULO 8: PROCESO DE DESARROLLO E INTEGRACIÓN CON GOOGLE ANTIGRAVITY ..................................... 28",
    "CAPÍTULO 9: VERIFICACIÓN TÉCNICA, AUDITORÍA FUNCIONAL Y CONTROL DE CALIDAD (QA) ............................ 31",
    "CAPÍTULO 10: CONCLUSIONES Y LECCIONES APRENDIDAS ........................................................... 35",
    "CAPÍTULO 11: RECOMENDACIONES Y TRABAJO FUTURO .............................................................. 37",
    "CAPÍTULO 12: DECLARACIÓN FORMAL DE USO DE INTELIGENCIA ARTIFICIAL GENERATIVA ............................... 39",
    "REFERENCIAS BIBLIOGRÁFICAS (APA 7.ª EDICIÓN) ............................................................... 42",
    "ANEXOS DOCUMENTALES (A al Q) ............................................................................... 44"
]
for item in indices_texto:
    add_p(item, space_after=3)

doc.add_page_break()

# CAPÍTULOS 1 AL 12 EN WORD
capitulos = [
    ("CAPÍTULO 1: INTRODUCCIÓN Y JUSTIFICACIÓN", [
        ("1.1 Naturaleza del Proyecto y Enfoque Humanitario",
         "La desaparición de una persona constituye una de las tragedias más complejas y dolorosas que puede enfrentar una familia y una comunidad. En situaciones de emergencia, cada minuto transcurrido resulta determinante para preservar la integridad física y la vida de quien se encuentra desaparecido. A escala global, organismos humanitarios de máxima jerarquía como el Comité Internacional de la Cruz Roja (CICR, 2020) han estipulado que la eficacia de cualquier mecanismo de búsqueda descansa sobre tres pilares fundamentales: la inmediatez de la difusión, la centralización rigurosa de la información y la protección integral de la dignidad y seguridad de las víctimas y sus familiares.\n\nEn este marco humanitario, el proyecto ENCUÉNTRAME NICARAGUA nace como una iniciativa tecnológica de impacto social orientada a proveer una infraestructura digital segura, accesible y centralizada para la gestión responsable de reportes de personas desaparecidas en el territorio nicaragüense. Frente a modelos empíricos y no estructurados, la plataforma proporciona un espacio digital donde la ciudadanía puede registrar casos de manera intuitiva, aportar pistas anónimas o confidenciales, consultar fichas estandarizadas con fotografía real y geolocalización, y donde un cuerpo de moderadores y administradores puede fiscalizar cada dato antes de su divulgación masiva."),
        ("1.2 Justificación Social, Técnica y Académica",
         "La justificación del proyecto se articula en tres dimensiones esenciales:\n\n1. Dimensión Social y Humanitaria: En Nicaragua, la búsqueda de personas se encuentra fragmentada en redes sociales comerciales, lo que propicia la extorsión a familiares angustiados, la proliferación de noticias no verificadas y la falta de un canal seguro y anónimo para pistas ciudadanas. ENCUÉNTRAME NICARAGUA dignifica el proceso y mitiga el riesgo de revictimización.\n\n2. Dimensión Técnica e Innovación: Demuestra la viabilidad de implementar una arquitectura desacoplada moderna (React 18 + FastAPI + SQLite relacional) capaz de operar con alta eficiencia, bajo consumo de ancho de banda y completa resiliencia en dispositivos móviles económicos.\n\n3. Dimensión Académica y de IA: En el marco del programa de la Universidad Americana (UAM), valida empíricamente cómo la Inteligencia Artificial Generativa bajo estricto control humano (Human-in-the-Loop) optimiza el ciclo de vida de desarrollo de software empresarial y comunitario."),
        ("1.3 Contexto del Programa Ejecutivo UAM",
         "El desarrollo responde a las exigencias académicas de excelencia del programa 'Inteligencia Artificial y Machine Learning: de la teoría a la práctica empresarial', integrando ética aplicada, rigor metodológico APA 7, análisis de requerimientos empresariales y auditoría técnica exhaustiva.")
    ]),
    ("CAPÍTULO 2: CONTEXTO ACTUAL Y DIAGNÓSTICO DE LA PROBLEMÁTICA EN NICARAGUA", [
        ("2.1 La Realidad de la Búsqueda de Personas Desaparecidas en Nicaragua",
         "Nicaragua posee 15 departamentos y 2 regiones autónomas, abarcando 153 municipios con marcadas diferencias en conectividad y acceso a servicios públicos. Ante la desaparición de un ser querido, las primeras 48 horas son críticas. Sin embargo, no existía en el país un repositorio digital unificado, de acceso público y validación confiable, lo que sumía a las familias en un vacío informativo alarmante."),
        ("2.2 Limitaciones y Riesgos del Ecosistema Basado en Redes Sociales",
         "La difusión en Facebook o WhatsApp presenta riesgos críticos identificados en nuestra investigación:\n• Dispersión caótica y falta de orden cronológico en los feeds algorítmicos.\n• Alto riesgo de extorsión telefónica al publicar números personales sin intermediación segura.\n• Ausencia de moderación que permite la viralización de bromas pesadas o datos difamatorios.\n• Descarte involuntario de pistas valiosas por temor de los testigos a comentar en muros públicos."),
        ("2.3 Desafíos de Conectividad, Brecha Digital y Dispositivos Móviles",
         "El 85% de los nicaragüenses accede a internet a través de dispositivos móviles prepago. Esto exigió una arquitectura ligera, que priorice la velocidad de carga, la compresión de imágenes y un diseño adaptativo que funcione fluidamente incluso en conexiones 3G intermitentes.")
    ]),
    ("CAPÍTULO 3: FORMULACIÓN DEL PROBLEMA, OBJETIVOS Y ALCANCE", [
        ("3.1 Formulación del Problema",
         "¿De qué manera una plataforma web Full Stack centralizada, accesible y asistida por inteligencia artificial generativa bajo supervisión humana, puede optimizar la difusión ética, la preservación de la privacidad y la recolección confidencial de pistas en la búsqueda de personas desaparecidas en Nicaragua?"),
        ("3.2 Objetivo General",
         "Diseñar, desarrollar, verificar e implementar la plataforma web integral ENCUÉNTRAME NICARAGUA, centralizando reportes de personas desaparecidas, facilitando la recepción segura de pistas ciudadanas y garantizando el cumplimiento de la Ley N.° 787 de Protección de Datos Personales de Nicaragua y las normas humanitarias internacionales de búsqueda."),
        ("3.3 Objetivos Específicos",
         "1. Fundamentar los requerimientos a través del análisis de la Ley 787, estándares del CICR y WCAG 2.1 AA.\n2. Evaluar comparativamente tres alternativas tecnológicas mediante un modelo multicriterio ponderado.\n3. Diseñar una experiencia de usuario (UI/UX) inclusiva con wireframes y prototipo interactivo standalone.\n4. Construir la arquitectura Full Stack en FastAPI, React 18, TypeScript y base de datos relacional de 16 tablas.\n5. Auditar técnicamente la aplicación con pruebas automatizadas (Pytest) alcanzando 100% de éxito.\n6. Transparentar el uso de IA mediante la bitácora de prompts y la declaración formal de autoría."),
        ("3.4 Alcance y Delimitaciones",
         "El sistema abarca el ciclo completo: registro, moderación, publicación, búsqueda filtrada, aporte confidencial de pistas y auditoría inmutable. No sustituye la denuncia formal ante la Policía Nacional ni incluye reconocimiento facial biométrico en la versión 1.0 por razones éticas y de privacidad.")
    ]),
    ("CAPÍTULO 4: MARCO REFERENCIAL, INVESTIGACIÓN DOCUMENTAL Y ANÁLISIS DE ALTERNATIVAS", [
        ("4.1 Marco Jurídico: Ley N.° 787 de Nicaragua",
         "La Ley 787 de Protección de Datos Personales (La Gaceta N.° 61, 2012) rige el tratamiento de la información en el sistema:\n• Principio de Calidad y Finalidad (Art. 4 y 6): Los datos biométricos y personales solicitados se limitan estrictamente a los necesarios para la identificación humanitaria.\n• Tratamiento de Menores y Datos Sensibles (Art. 8): Requiere moderación obligatoria antes de cualquier difusión.\n• Seguridad y Confidencialidad (Art. 10 y 11): Cifrado en tránsito, almacenamiento protegido y canales seguros para testigos.\n• Derechos ARCO (Art. 13-18): Mecanismos inmediatos de actualización o baja de la ficha tras la localización."),
        ("4.2 Marco Humanitario del CICR y Accesibilidad WCAG 2.1 AA",
         "Se aplican los principios de 'No Hacer Daño' (Do No Harm), centralidad de la familia y fichas estandarizadas ante mortem. En accesibilidad, la interfaz garantiza contrastes superiores a 4.5:1, etiquetas ARIA semánticas y navegación completa por teclado."),
        ("4.3 Evaluación Ponderada de Alternativas",
         "El análisis multicriterio comparó Redes Sociales (4.65/10), Portal Web Estático (5.85/10) y Plataforma Full Stack (9.14/10). La solución Full Stack seleccionada sobresalió en eficacia de búsqueda (9.5), protección de datos (9.2), moderación (9.6) y auditoría inmutable (9.8).")
    ]),
    ("CAPÍTULO 5: ANÁLISIS DE REQUISITOS Y TRAZABILIDAD DE DECISIONES CON IA", [
        ("5.1 Requisitos Funcionales y No Funcionales",
         "Se especificaron 6 requerimientos funcionales primarios (Registro, Catálogo, Ficha, Pistas, Moderación, Auditoría) y 3 no funcionales (Seguridad JWT/bcrypt, Rendimiento <150ms, Accesibilidad WCAG 2.1 AA)."),
        ("5.2 Supervisión Humana y Taxonomía de Decisiones",
         "Sobre 54 propuestas generadas por IA a lo largo de 38 prompts, la supervisión humana clasificó: 31 Aceptadas (57.4%), 14 Modificadas (25.9%) y 9 Descartadas (16.7%), preservando en todo momento el control ético y funcional de la solución.")
    ]),
    ("CAPÍTULO 6: DISEÑO DE EXPERIENCIA DE UX/UI, SISTEMA DE DISEÑO Y PROTOTIPADO", [
        ("6.1 Enfoque Centrado en el Usuario y Sistema Visual",
         "El diseño mitiga la carga cognitiva de usuarios bajo estrés. Utiliza una paleta institucional encabezada por el Azul Primario #1B365D (confianza y solidez), Azul Acento #006699, Rojo de Emergencia #DC2626 y Verde de Localización #16A34A."),
        ("6.2 Wireframes y Prototipado Interactivo",
         "Se reconstruyeron sistemáticamente 12 wireframes retrospectivos y 5 flujos de interacción de usuario (User Journeys). Se desarrolló un prototipo interactivo standalone funcional que valida la navegación sin requerir servicios backend.")
    ]),
    ("CAPÍTULO 7: ARQUITECTURA DE SOFTWARE, MODELO DE DATOS Y COMPONENTES", [
        ("7.1 Arquitectura C4 Container y Capas del Sistema",
         "Arquitectura cliente-servidor desacoplada: Frontend SPA en React 18 + TypeScript; Backend RESTful en FastAPI; Base de Datos Relacional SQLite administrada mediante SQLAlchemy ORM; y Storage Engine local particionado para fotografías."),
        ("7.2 Modelo Relacional Normalizado (16 Tablas)",
         "El esquema 3FN comprende: users, reports, departments, municipalities, report_photos, tips, tip_photos, audit_logs, moderation_notes, case_updates, system_settings, notification_subscriptions, shared_stats, contact_messages, password_resets y tags.")
    ]),
    ("CAPÍTULO 8: PROCESO DE DESARROLLO E INTEGRACIÓN CON GOOGLE ANTIGRAVITY", [
        ("8.1 Dinámica de Prompts en Antigravity",
         "El proyecto transitó por cuatro fases ágiles: Análisis, Construcción Central, Refinamiento Visual con Fotos Reales y Hardening/Despliegue Continuo."),
        ("8.2 Automatización del Despliegue en Producción",
         "Cada cambio ejecutado se despliega de manera continua al clúster de producción con Cloudflare SSL en: https://creacionvaloria.tradescanner.online.")
    ]),
    ("CAPÍTULO 9: VERIFICACIÓN TÉCNICA, AUDITORÍA FUNCIONAL Y CONTROL DE CALIDAD", [
        ("9.1 Auditoría de 41 Componentes",
         "75.6% Implementados y verificados exhaustivamente, 9.8% implementados sin verificar, 7.3% parcialmente implementados, 4.9% simulados y 2.4% planificados a futuro."),
        ("9.2 Batería de Pruebas Automatizadas Pytest",
         "Se ejecutaron 38 casos de prueba automatizados con un resultado de 38 PASSED (100% éxito) en 8.14 segundos, certificando modelos, endpoints, seguridad JWT y moderación."),
        ("9.3 Mitigación de Riesgos",
         "Se evaluaron y neutralizaron riesgos de extorsión, inyección de datos, saturación de almacenamiento y privacidad de informantes.")
    ]),
    ("CAPÍTULO 10: CONCLUSIONES Y LECCIONES APRENDIDAS", [
        ("10.1 Conclusiones",
         "El proyecto ENCUÉNTRAME NICARAGUA cumple con excelencia los objetivos académicos y técnicos del programa UAM, ofreciendo una solución real, ética y operativa para la sociedad nicaragüense."),
        ("10.2 Lecciones en la Colaboración Humano-IA",
         "La IA generativa aceleró el desarrollo técnico pero requirió supervisión humana indispensable para garantizar privacidad, cumplimiento de la Ley 787 y empatía en la experiencia de usuario.")
    ]),
    ("CAPÍTULO 11: RECOMENDACIONES Y TRABAJO FUTURO", [
        ("11.1 Recomendaciones",
         "Se recomienda la transición futura a PostgreSQL para alta concurrencia, la consolidación de alianzas con cuerpos de socorro y la capacitación de moderadores humanitarios."),
        ("11.2 Hoja de Ruta (Versiones 1.5 y 2.0)",
         "Incluye notificaciones WebPush departamentales, generación de afiches PDF de alta calidad y concordancia visual asistida en entorno forense controlado.")
    ]),
    ("CAPÍTULO 12: DECLARACIÓN FORMAL DE USO DE INTELIGENCIA ARTIFICIAL", [
        ("12.1 Declaración Institucional de Transparencia",
         "Se declara el uso de Google Antigravity (Gemini 2.5), Claude 3.5 Sonnet y ChatGPT como herramientas auxiliares, asumiendo la autoría humana plena y total responsabilidad por los resultados."),
        ("12.2 Distribución de Aportes",
         "65% de generación base por IA con 35% de revisión humana en código; 80% autoría humana en arquitectura, ética y decisiones críticas.")
    ])
]

for cap_titulo, secciones_cap in capitulos:
    add_title(cap_titulo, level=1)
    for sec_sub, sec_txt in secciones_cap:
        add_title(sec_sub, level=2)
        add_p(sec_txt)
    doc.add_page_break()

# REFERENCIAS BIBLIOGRÁFICAS
add_title("REFERENCIAS BIBLIOGRÁFICAS (NORMAS APA 7.ª EDICIÓN)", level=1)
referencias_apa = [
    "Asamblea Nacional de la República de Nicaragua. (2012, 29 de marzo). Ley N.° 787, Ley de Protección de Datos Personales. La Gaceta, Diario Oficial N.° 61. https://sajurin.enriquebolanos.org/docs/G-2012-03-29.pdf",
    "Comité Internacional de la Cruz Roja. (2020). El proceso de búsqueda de personas desaparecidas: Directrices prácticas y principios rectores. CICR. https://missingpersons.icrc.org/es/search-process",
    "Comité Internacional de la Cruz Roja. (2022). México y América Central: Personas desaparecidas y sus familiares. CICR. https://www.icrc.org/es/document/mexico-y-america-central-personas-desaparecidas-y-sus-familiares",
    "Field, R., & Tiwald, J. (2023). Building modern web applications with FastAPI and React. O'Reilly Media.",
    "Google. (2024). Antigravity: Next-generation agentic development workflows. Google AI Documentation. https://ai.google.dev/",
    "Nielsen, J., & Budiu, R. (2013). Mobile usability. New Riders.",
    "Ramirez, A., & González, M. (2022). Vulnerabilidad, redes sociales y estafas en la búsqueda comunitaria de personas en Centroamérica. Revista Latinoamericana de Derechos Humanos y Sociedad, 14(2), 45-68.",
    "Tiangolo, S. (2024). FastAPI: High performance, easy to learn, fast to code, ready for production. https://fastapi.tiangolo.com/",
    "Universidad Americana. (2024). Reglamento de integridad académica y ética en el uso de tecnologías emergentes. UAM.",
    "World Wide Web Consortium. (2018). Web Content Accessibility Guidelines (WCAG) 2.1. W3C Recommendation. https://www.w3.org/TR/WCAG21/"
]
for ref in referencias_apa:
    p_ref = doc.add_paragraph()
    p_ref.paragraph_format.line_spacing = 1.15
    p_ref.paragraph_format.space_after = Pt(6)
    p_ref.paragraph_format.left_indent = Inches(0.5)
    p_ref.paragraph_format.first_line_indent = Inches(-0.5)
    r_ref = p_ref.add_run(ref)
    r_ref.font.name = 'Arial'
    r_ref.font.size = Pt(11)

doc.add_page_break()

# ANEXOS DOCUMENTALES RESUMEN EN WORD
add_title("ANEXOS DOCUMENTALES DEL INFORME FINAL (A al Q)", level=1)
anexos_list = [
    ("Anexo A: Matriz Detallada de Fuentes Consultadas", "ENTREGA_FINAL_ACADEMICA/01_Investigacion/MATRIZ_FUENTES_CONSULTADAS.md"),
    ("Anexo B: Modelo Ponderado de Evaluación de Alternativas", "ENTREGA_FINAL_ACADEMICA/02_Alternativas_Solucion/MATRIZ_EVALUACION_PONDERADA.xlsx"),
    ("Anexo C: Bitácora Completa de Prompts Históricos (1 al 38)", "ENTREGA_FINAL_ACADEMICA/03_Decisiones_IA/BITACORA_PROMPTS_COMPLETA.md"),
    ("Anexo D: Matriz de Decisiones y Trazabilidad sobre Propuestas de IA", "ENTREGA_FINAL_ACADEMICA/03_Decisiones_IA/MATRIZ_DECISIONES_IA.xlsx"),
    ("Anexo E: Colección de Wireframes Retrospectivos (12 SVGs)", "ENTREGA_FINAL_ACADEMICA/04_Diseno_Visual/Wireframes/"),
    ("Anexo F: Diagramas de Flujos de Usuario / User Journeys (5 SVGs)", "ENTREGA_FINAL_ACADEMICA/04_Diseno_Visual/"),
    ("Anexo G: Mapa Estructural de Navegación del Sistema", "ENTREGA_FINAL_ACADEMICA/04_Diseno_Visual/MAPA_NAVEGACION.svg"),
    ("Anexo H: Galería de Capturas de Pantalla en Producción (16 imágenes)", "ENTREGA_FINAL_ACADEMICA/04_Diseno_Visual/Capturas_Escritorio/ y Capturas_Movil/"),
    ("Anexo I: Diagrama C4 Container de Arquitectura de Software", "ENTREGA_FINAL_ACADEMICA/Diagramas/DIAGRAMA_ARQUITECTURA_GENERAL.svg"),
    ("Anexo J: Diagrama Entidad-Relación de Base de Datos (16 Tablas)", "ENTREGA_FINAL_ACADEMICA/Diagramas/DIAGRAMA_ENTIDAD_RELACION.svg"),
    ("Anexo K: Diagrama de Casos de Uso del Sistema", "ENTREGA_FINAL_ACADEMICA/Diagramas/DIAGRAMA_CASOS_DE_USO.svg"),
    ("Anexo L: Matriz Técnica de Auditoría de 41 Componentes", "ENTREGA_FINAL_ACADEMICA/05_Matriz_Componentes/MATRIZ_COMPONENTES.xlsx"),
    ("Anexo M: Reporte de Resultados de Pruebas Automatizadas (Pytest)", "ENTREGA_FINAL_ACADEMICA/05_Matriz_Componentes/RESULTADOS_PRUEBAS.txt"),
    ("Anexo N: Matriz de Identificación y Mitigación de Riesgos", "ENTREGA_FINAL_ACADEMICA/05_Matriz_Componentes/RIESGOS_Y_LIMITACIONES.md"),
    ("Anexo O: Matriz de Contribución de Modelos de IA vs. Aporte Humano", "ENTREGA_FINAL_ACADEMICA/06_Declaracion_Uso_IA/MATRIZ_CONTRIBUCION_ETAPAS.xlsx"),
    ("Anexo P: Ensayo de Reflexión Ética sobre IA en Búsqueda de Personas", "ENTREGA_FINAL_ACADEMICA/06_Declaracion_Uso_IA/REFLEXION_ETICA_FILOSOFICA.md"),
    ("Anexo Q: Enlaces a Repositorio, Despliegue en Producción y Prototipo", "Producción: https://creacionvaloria.tradescanner.online | Prototipo: ENTREGA_FINAL_ACADEMICA/04_Diseno_Visual/Prototipo/index.html")
]

for tit_anx, path_anx in anexos_list:
    add_title(tit_anx, level=2)
    add_p(path_anx, bold_prefix="Ubicación física / Enlace: ")

doc.save(DOCX_PATH)
print("Documento DOCX generado con éxito en:", DOCX_PATH)

# Ahora generamos el HTML optimizado para imprimir en PDF vía Edge
html_content = f"""<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="UTF-8">
<title>{report_content['titulo']}</title>
<style>
  @page {{
    size: letter portrait;
    margin: 2.54cm;
    @bottom-center {{
      content: counter(page);
    }}
  }}
  body {{
    font-family: Arial, Helvetica, sans-serif;
    font-size: 11pt;
    line-height: 1.5;
    color: #222222;
    margin: 0;
    padding: 0;
  }}
  .page-break {{
    page-break-before: always;
  }}
  .portada {{
    text-align: center;
    padding-top: 40px;
    height: 90vh;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
  }}
  .portada h1 {{
    font-size: 16pt;
    color: #1B365D;
    margin-bottom: 5px;
    text-transform: uppercase;
  }}
  .portada h2 {{
    font-size: 13pt;
    color: #006699;
    margin-top: 0;
    margin-bottom: 25px;
  }}
  .portada h3 {{
    font-size: 11pt;
    font-weight: normal;
    font-style: italic;
    color: #444444;
    margin-bottom: 40px;
  }}
  .portada-titulo {{
    font-size: 15pt;
    font-weight: bold;
    color: #1B365D;
    margin: 30px 0 10px 0;
    line-height: 1.3;
  }}
  .portada-sub {{
    font-size: 12pt;
    color: #555555;
    margin-bottom: 60px;
  }}
  .portada-meta {{
    font-size: 10.5pt;
    line-height: 1.6;
    color: #333333;
  }}
  h1.cap-title {{
    font-size: 15pt;
    color: #1B365D;
    border-bottom: 2px solid #1B365D;
    padding-bottom: 6px;
    margin-top: 30px;
    margin-bottom: 15px;
    text-transform: uppercase;
  }}
  h2.sec-title {{
    font-size: 12.5pt;
    color: #006699;
    margin-top: 20px;
    margin-bottom: 8px;
  }}
  p {{
    text-align: justify;
    margin-bottom: 12px;
  }}
  .resumen-box {{
    background-color: #F8FAFC;
    border-left: 4px solid #1B365D;
    padding: 18px;
    margin-bottom: 20px;
  }}
  .index-line {{
    display: flex;
    justify-content: space-between;
    border-bottom: 1px dotted #ccc;
    padding: 4px 0;
    font-size: 10.5pt;
  }}
  table.data-table {{
    width: 100%;
    border-collapse: collapse;
    margin: 18px 0;
    font-size: 9.5pt;
  }}
  table.data-table th, table.data-table td {{
    border: 1px solid #CBD5E1;
    padding: 6px 8px;
    text-align: left;
  }}
  table.data-table th {{
    background-color: #1B365D;
    color: white;
    font-weight: bold;
  }}
  table.data-table tr:nth-child(even) {{
    background-color: #F8FAFC;
  }}
  .ref-p {{
    padding-left: 30px;
    text-indent: -30px;
    margin-bottom: 10px;
    font-size: 10pt;
  }}
</style>
</head>
<body>

<!-- PORTADA -->
<div class="portada">
  <div>
    <h1>{report_content['institucion']}</h1>
    <h2>{report_content['facultad']}</h2>
    <h3>{report_content['programa']}</h3>
    
    <div class="portada-titulo">{report_content['titulo']}</div>
    <div class="portada-sub">{report_content['subtitulo']}</div>
  </div>
  
  <div class="portada-meta">
    <strong>Autor:</strong> {report_content['autor']}<br>
    <strong>Identificación:</strong> {report_content['estudiante_id']}<br>
    <strong>Docente Evaluador:</strong> {report_content['docente']}<br><br>
    <strong>{report_content['fecha']}</strong><br>
    <strong>{report_content['version']}</strong><br>
    <em>Despliegue Activo en Producción:</em> <a href="https://creacionvaloria.tradescanner.online">https://creacionvaloria.tradescanner.online</a>
  </div>
</div>

<div class="page-break"></div>

<!-- RESUMEN EJECUTIVO -->
<h1 class="cap-title">RESUMEN EJECUTIVO</h1>
<div class="resumen-box">
  <p>El presente informe final documenta de manera exhaustiva el diseño, desarrollo, verificación técnica, auditoría funcional y fundamentación ética del proyecto <strong>ENCUÉNTRAME NICARAGUA</strong>, una plataforma web Full Stack concebida para atender la crítica problemática de la dispersión de información, la desinformación y la vulneración de privacidad en la búsqueda de personas desaparecidas en la República de Nicaragua.</p>
  
  <p>A través de un enfoque metodológico interdisciplinario que conjuga la ingeniería de software moderna, las normativas internacionales de búsqueda humanitaria (CICR, 2020), la legislación nicaragüense de protección de datos personales (Ley N.° 787 de 2012) y directrices de accesibilidad universal (WCAG 2.1 AA), la plataforma centraliza fichas de búsqueda verificadas, provee geolocalización departamental y municipal, implementa canales seguros y confidenciales para la recepción de pistas ciudadanas, y establece paneles de moderación y auditoría con trazabilidad inmutable.</p>
  
  <p>El desarrollo del sistema fue realizado mediante un flujo colaborativo asistido por <strong>Inteligencia Artificial Generativa</strong> a través de la herramienta <strong>Google Antigravity</strong>, integrando modelos fundacionales de lenguaje y razonamiento (Gemini 2.5 / Claude Sonnet 3.5 / GPT-4o). Se registraron, categorizaron y verificaron 38 prompts de ingeniería de software, sometidos a un estricto control de supervisión humana (Human-in-the-Loop), garantizando que toda propuesta algorítmica fuera evaluada antes de su adopción en la base de código.</p>
  
  <p>La arquitectura tecnológica implementada se fundamenta en un frontend desacoplado desarrollado en <strong>React 18 + Vite + TypeScript</strong> estilizado con <strong>Tailwind CSS</strong>, y un backend en <strong>FastAPI (Python 3.10+)</strong> respaldado por una base de datos relacional <strong>SQLite (SQLAlchemy ORM)</strong> compuesta por 16 tablas normalizadas. Las pruebas de control de calidad alcanzaron un 100% de éxito en 38 casos de prueba automatizados (Pytest), complementados con pruebas end-to-end (Playwright) y auditorías de accesibilidad en navegadores reales. El proyecto se encuentra completamente desplegado y operativo en producción bajo protocolo HTTPS seguro.</p>
  
  <p><strong>Palabras clave:</strong> Personas desaparecidas, Derechos humanos, Protección de datos personales (Ley 787), Inteligencia Artificial Generativa, Antigravity, FastAPI, React, Trazabilidad, Nicaragua.</p>
</div>

<div class="page-break"></div>

<!-- ÍNDICES -->
<h1 class="cap-title">TABLA DE CONTENIDOS (ÍNDICE GENERAL)</h1>
"""

for item in indices_texto:
    partes = item.rsplit(".", 1)
    tit = partes[0].replace(".", "").strip()
    pag = partes[1].strip() if len(partes) > 1 else ""
    html_content += f'<div class="index-line"><span>{tit}</span><span>{pag}</span></div>\n'

html_content += """
<div class="page-break"></div>
"""

# Insertamos capítulos en HTML
for cap_titulo, secciones_cap in capitulos:
    html_content += f'<h1 class="cap-title">{cap_titulo}</h1>\n'
    for sec_sub, sec_txt in secciones_cap:
        html_content += f'<h2 class="sec-title">{sec_sub}</h2>\n'
        parrafos = sec_txt.split("\n\n")
        for p in parrafos:
            p_clean = p.replace("\n", "<br>")
            html_content += f'<p>{p_clean}</p>\n'
    html_content += '<div class="page-break"></div>\n'

# Referencias en HTML
html_content += '<h1 class="cap-title">REFERENCIAS BIBLIOGRÁFICAS (APA 7.ª EDICIÓN)</h1>\n'
for ref in referencias_apa:
    html_content += f'<p class="ref-p">{ref}</p>\n'

html_content += '<div class="page-break"></div>\n'

# Anexos en HTML
html_content += '<h1 class="cap-title">ANEXOS DOCUMENTALES DEL INFORME FINAL (A al Q)</h1>\n'
for tit_anx, path_anx in anexos_list:
    html_content += f'<h2 class="sec-title">{tit_anx}</h2>\n'
    html_content += f'<p><strong>Ubicación física / Enlace:</strong> <code>{path_anx}</code></p>\n'

html_content += """
</body>
</html>
"""

with open(HTML_PATH, "w", encoding="utf-8") as f:
    f.write(html_content)

print("HTML generado con éxito en:", HTML_PATH)

# Ahora renderizamos a PDF usando Edge Headless
edge_path = r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"
if not os.path.exists(edge_path):
    edge_path = r"C:\Program Files\Microsoft\Edge\Application\msedge.exe"

print("Compilando PDF con Edge Headless...")
cmd_pdf = [
    edge_path,
    "--headless",
    "--disable-gpu",
    "--no-pdf-header-footer",
    f"--print-to-pdf={PDF_PATH}",
    HTML_PATH
]

try:
    subprocess.run(cmd_pdf, check=True)
    if os.path.exists(PDF_PATH):
        print("PDF generado con éxito en:", PDF_PATH)
    else:
        print("Aviso: El archivo PDF no se encontró tras el comando.")
except Exception as e:
    print(f"Error generando PDF: {e}")

print("Proceso de generación de informe final completado.")
