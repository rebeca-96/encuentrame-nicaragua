# -*- coding: utf-8 -*-
"""
Generador de Entregables Académicos:
1. MATRIZ_FUENTES_CONSULTADAS.csv
2. REFERENCIAS_APA7.md
3. EVIDENCIAS_CONSULTA_FUENTES.md
4. HALLAZGOS_INVESTIGACION.md
5. REQUISITOS_DERIVADOS_INVESTIGACION.md
6. INVESTIGACION_DOCUMENTAL.md
"""

import os
import csv

BASE_DIR = r"c:\Users\User\Documents\Valor IA\EncuentrameNicaragua\ENTREGA_FINAL_ACADEMICA\01_Investigacion"
os.makedirs(BASE_DIR, exist_ok=True)

# -------------------------------------------------------------------------------------------------
# 1. MATRIZ_FUENTES_CONSULTADAS.csv
# -------------------------------------------------------------------------------------------------
def generate_matriz_csv():
    filepath = os.path.join(BASE_DIR, "MATRIZ_FUENTES_CONSULTADAS.csv")
    headers = [
        "Identificador",
        "Autor o institución",
        "Título del documento",
        "Año de publicación",
        "Tipo de fuente",
        "URL",
        "Fecha real de consulta",
        "Hallazgos relevantes",
        "Requisitos derivados",
        "Aplicación dentro del proyecto",
        "Evidencia disponible",
        "Limitaciones de la fuente"
    ]

    rows = [
        [
            "F-JUR-01",
            "Asamblea Nacional de la República de Nicaragua",
            "Ley N.° 787, Ley de Protección de Datos Personales (La Gaceta, Diario Oficial N.° 61 del 29 de marzo de 2012)",
            "2012",
            "Jurídica / Legal Oficial",
            "https://sajurin.enriquebolanos.org/docs/G-2012-03-29.pdf",
            "2026-11-24",
            "Regula el tratamiento de datos personales en ficheros públicos y privados; consagra el principio de autodeterminación informativa (Art. 1 y 3); exige consentimiento previo e informado del titular (Art. 5); establece derechos ARCO (Art. 13-17); regula ficheros sensibles y de seguridad (Art. 24); crea la DIPRODAP como ente regulador (Art. 29).",
            "Consentimiento informado obligatorio; trazabilidad de declarante; no almacenamiento de documentos en texto plano (hash SHA-256); despublicación y supresión inmediata ante petición formal (Art. 16).",
            "Módulo de Reportar (/reportar), ConsentRecord en backend, función request_deletion_case y despublicación en base de datos.",
            "Texto oficial publicado en La Gaceta N.° 61 disponible en el repositorio SAJURIN y portal parlamentario.",
            "La autoridad de aplicación (DIPRODAP) carece de operatividad pública y precedentes jurisprudenciales accesibles en línea; no contempla específicamente plataformas cívicas de búsqueda humanitaria."
        ],
        [
            "F-JUR-02",
            "Poder Ejecutivo de la República de Nicaragua",
            "Decreto N.° 36-2012, Reglamento de la Ley N.° 787 (La Gaceta, Diario Oficial N.° 200 del 19 de octubre de 2012)",
            "2012",
            "Normativa Reglamentaria Oficial",
            "https://sajurin.enriquebolanos.org/docs/G-2012-10-19.pdf",
            "2026-11-24",
            "Detalla medidas de seguridad técnicas, físicas y organizativas para ficheros automatizados; define procedimientos para ejercicio de derechos ARCO y plazos de respuesta administrativa (10 días).",
            "Control de accesos por roles (RBAC); registro inmutable de auditoría (logs de acceso y modificación); bloqueo preventivo de datos.",
            "Módulos de autenticación JWT (deps.py), RBAC (UserRole), tabla audit_logs y almacenamiento seguro de imágenes.",
            "Texto oficial de La Gaceta N.° 200 debidamente promulgado y compilado en el sistema legislativo.",
            "Enfocado primordialmente en relaciones comerciales y laborales; no detalla estándares forenses para imágenes de personas desaparecidas."
        ],
        [
            "F-SOC-01",
            "Comité Internacional de la Cruz Roja (CICR)",
            "Proceso de búsqueda de personas desaparecidas (Missing Persons Global Response)",
            "2021",
            "Guía Humanitaria / Internacional",
            "https://missingpersons.icrc.org/es/search-process",
            "2026-11-24",
            "Define la búsqueda como un proceso integral, multidisciplinario y continuo para determinar la suerte y el paradero; establece que los familiares deben estar en el centro del proceso; distingue la búsqueda humanitaria de la persecución penal; destaca la recopilación estandarizada de datos ante mortem y la centralidad de hipótesis dinámicas.",
            "Recopilación estructurada de datos ante mortem (ropa, señas particulares, condiciones médicas); línea de tiempo de avance del caso; canal confidencial y seguro de pistas; preservación de dignidad y no revictimización.",
            "Formulario de registro multipaso, ficha detallada del caso (/casos/[id]) con línea de tiempo cronológica, módulo de recepción de testimonios confidenciales (/pistas).",
            "Plataforma global pública y directrices metodológicas operativas validadas por el CICR a nivel mundial.",
            "Plantea directrices generales aplicables a Estados y Cruz Roja; su implementación en plataformas de software libre requiere adaptaciones específicas al entorno digital."
        ],
        [
            "F-SOC-02",
            "Comité Internacional de la Cruz Roja (CICR)",
            "México y América Central: personas desaparecidas y sus familiares",
            "2023",
            "Informe Humanitario Regional",
            "https://www.icrc.org/es/document/mexico-y-america-central-personas-desaparecidas-y-sus-familiares",
            "2026-11-24",
            "Analiza las causas multicausales de desaparición en la región (violencia armada, delincuencia común, rutas migratorias, desastres); denuncia el limbo humanitario que sufren las familias; impulsa la metodología de 'Carpetas Vivas' como expedientes dinámicos y coordinados; enfatiza el deber estatal de dar respuestas oportunas.",
            "Gestión dinámica de casos (expedientes vivos en constante actualización); mecanismos de aportación de datos de la comunidad; atención prioritaria a personas en rutas migratorias y personas vulnerables.",
            "Fichas de caso con actualización continua de hitos (/casos/[id]), tracking en vivo de estado y módulo de reportes sin caducidad burocrática.",
            "Publicación institucional del CICR para la delegación regional de México y América Central.",
            "Proporciona datos cualitativos e institucionales agregados; no ofrece series estadísticas desagregadas por municipio para Nicaragua debido a falta de datos abiertos oficiales."
        ],
        [
            "F-TEC-01",
            "OWASP Foundation",
            "OWASP Application Security Verification Standard (ASVS), Versión 5.0.0",
            "2025",
            "Estándar Técnico de Ciberseguridad",
            "https://asvs.owasp.org/",
            "2026-11-24",
            "Proporciona un marco moderno de verificación de seguridad con ~350 requisitos en 17 capítulos; moderniza el manejo de tokens JWT, control de acceso por atributos, sanitización de archivos multimedia, defensas contra ataques de fuerza bruta y rate limiting, y seguridad de APIs REST.",
            "Almacenamiento seguro de credenciales con Argon2id; invalidación y revocación de tokens JWT; sanitización estricta de imágenes (eliminación de cabeceras EXIF/GPS, conversión WebP, nombres no predecibles); rate limiting en endpoints de login y reportes; principios de menor privilegio.",
            "Implementación en FastAPI: security.py, rate_limit.py, storage_service.py (sanitización Pillow), deps.py (RBAC estricto), y endpoints /photos.",
            "Repositorio oficial de OWASP y estándar técnico versión 5.0.0 liberado en mayo de 2025.",
            "Es un estándar de verificación técnica, no un framework de código; requiere pruebas unitarias y de integración para comprobar la adherencia efectiva."
        ],
        [
            "F-EST-01",
            "Instituto Nicaragüense de Información de Desarrollo (INIDE)",
            "División Político-Administrativa de la República de Nicaragua",
            "2021",
            "Oficial / Cartográfica y Estadística",
            "https://www.inide.gob.ni/",
            "2026-11-24",
            "Define la estructura territorial oficial de Nicaragua conformada por 15 departamentos y 2 regiones autónomas (Costa Caribe Norte - RACCN y Costa Caribe Sur - RACCS), desagregadas en 153 municipios con sus respectivas cabeceras y coordenadas.",
            "Estructuración de base de datos relacional para departamentos y municipios; selectores geográficos jerárquicos y dependientes; coordenadas aproximadas para georreferenciación sin vulnerar el domicilio exacto.",
            "Tablas geographic_locations, departments, municipalities en backend; selector dinámico en /reportar y mapa nacional interactivo en /mapa.",
            "Datos cartográficos y de división administrativa publicados por INIDE e Instituto Nicaragüense de Estudios Territoriales (INETER).",
            "Carencia de capas GeoJSON vectoriales actualizadas en tiempo real en formatos abiertos directos; requirió consolidación de geometrías locales."
        ],
        [
            "F-INV-01",
            "IPANDETEC Centroamérica",
            "Estado de la Protección de Datos Personales en Nicaragua y Centroamérica",
            "2021",
            "Investigación Jurídica / Sociedad Civil",
            "https://ipandetec.org/",
            "2026-11-24",
            "Evidencia la brecha de implementación de la Ley 787 en Nicaragua; señala la inoperancia práctica de la DIPRODAP y la escasa fiscalización estatal a bases de datos; enfatiza la necesidad de autorregulación ética y cumplimiento por diseño en plataformas digitales.",
            "Diseño ético 'Privacy by Design'; minimización proactiva de datos; auditoría forense inmutable propia; mecanismos de autodeterminación del usuario independientemente de la supervisión estatal.",
            "Arquitectura de auditoría en audit_service.py, encriptación unidireccional de cédulas, sanitización de metadatos EXIF sin requerimiento punitivo externo.",
            "Informe de investigación regional publicado y citado en foros de gobernanza de internet.",
            "Estudio cualitativo descriptivo basado en monitoreo de fuentes públicas y entrevistas a expertos legales."
        ]
    ]

    with open(filepath, "w", encoding="utf-8-sig", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(headers)
        writer.writerows(rows)
    print("Generada MATRIZ_FUENTES_CONSULTADAS.csv")

if __name__ == "__main__":
    generate_matriz_csv()
