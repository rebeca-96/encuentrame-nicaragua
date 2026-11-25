# EVIDENCIAS DE CONSULTA Y VERIFICACIÓN DE FUENTES

## PROYECTO: ENCUÉNTRAME NICARAGUA
**Fecha de Verificación:** 24 de noviembre de 2026  
**Auditor:** Especialista de Investigación y QA Documental

---

### 1. OBJETIVO DEL REGISTRO DE EVIDENCIAS

Este documento certifica la trazabilidad, disponibilidad técnica, vigencia normativa y límites metodológicos de las fuentes documentales primarias y secundarias consultadas durante la fundamentación de la plataforma cívica **Encuéntrame Nicaragua**.

Se da estricto cumplimiento a la instrucción de **no inventar** enlaces, estadísticas ni atribuciones institucionales que no estén expresamente acreditadas en la evidencia empírica o documental.

---

### 2. MATRIZ DE VERIFICACIÓN DE FUENTES Y ACCESO TÉCNICO

| ID | Fuente / Institución | Documento / Recurso | URL Verificada | Estado HTTP | Fecha Consulta | Verificación de Vigencia y Estado |
| :--- | :--- | :--- | :--- | :---: | :---: | :--- |
| **F-JUR-01** | Asamblea Nacional de Nicaragua | Ley N.° 787 de Protección de Datos Personales | https://sajurin.enriquebolanos.org/docs/G-2012-03-29.pdf | 200 OK | 2026-11-24 | **Vigente**. Publicada en La Gaceta N.° 61 del 29/03/2012. Sin reformas derogatorias sustanciales registradas en los repertorios legislativos oficiales. |
| **F-JUR-02** | Poder Ejecutivo de Nicaragua | Decreto N.° 36-2012 (Reglamento Ley 787) | https://sajurin.enriquebolanos.org/docs/G-2012-10-19.pdf | 200 OK | 2026-11-24 | **Vigente**. Publicado en La Gaceta N.° 200 del 19/10/2012. Regula plazos administrativos de 10 días para derechos ARCO y medidas de seguridad. |
| **F-SOC-01** | Comité Internacional de la Cruz Roja (CICR) | Proceso de búsqueda de personas desaparecidas | https://missingpersons.icrc.org/es/search-process | 200 OK | 2026-11-24 | **Activo y oficial**. Portal especializado *Missing Persons Global Response*. Establece los estándares internacionales para búsqueda humanitaria. |
| **F-SOC-02** | Comité Internacional de la Cruz Roja (CICR) | México y América Central: personas desaparecidas | https://www.icrc.org/es/document/mexico-y-america-central-personas-desaparecidas-y-sus-familiares | 200 OK | 2026-11-24 | **Activo y oficial**. Publicación de la Delegación Regional para México y América Central. Aborda la multicausalidad y la metodología de 'Carpetas Vivas'. |
| **F-TEC-01** | OWASP Foundation | Application Security Verification Standard (ASVS) v5.0.0 | https://asvs.owasp.org/ | 200 OK | 2026-11-24 | **Estándar Oficial Vigente**. Versión 5.0.0 liberada en mayo de 2025. Restructuración a 17 capítulos de control en aplicaciones modernas y APIs REST. |
| **F-EST-01** | INIDE / INETER | División Político-Administrativa de Nicaragua | https://www.inide.gob.ni/ | 200 OK | 2026-11-24 | **Oficial**. Compendio territorial: 15 departamentos, 2 regiones autónomas (RACCN y RACCS) y 153 municipios. |
| **F-INV-01** | IPANDETEC | Informe de Protección de Datos Personales | https://ipandetec.org/ | 200 OK | 2026-11-24 | **Activo**. Documento de análisis regional sobre la aplicación de marcos de protección de datos en Centroamérica. |

---

### 3. HALLAZGOS ESPECÍFICOS SOBRE VIGENCIA Y REALIDAD INSTITUCIONAL EN NICARAGUA

#### A. Vigencia Formal vs. Operatividad Práctica de la Ley N.° 787
- **Evidencia jurídica:** La Ley N.° 787 se encuentra formalmente promulgada y forma parte del ordenamiento jurídico positivo de la República de Nicaragua.
- **Evidencia institucional:** El artículo 29 de la Ley 787 creó la **Dirección de Protección de Datos Personales (DIPRODAP)** como entidad descentralizada encargada de llevar el Registro Nacional de Ficheros de Datos, fiscalizar a responsables públicos y privados y emitir sanciones administrativas.
- **Límite evidenciado:** Las investigaciones independientes y monitoreos de sociedad civil (IPANDETEC, 2021) constatan que la DIPRODAP no cuenta actualmente con un portal web activo, ventanilla pública digitalizada de registro ni memorias públicas de resoluciones o sanciones.
- **Decisión de diseño en el proyecto:** Ante la falta de fiscalización estatal externa activa, la aplicación **Encuéntrame Nicaragua** no puede alegar "homologación oficial estatal", pero asume los principios de la Ley 787 de manera autoimpuesta y verificable mediante arquitectura (*Privacy by Design*).

#### B. Ausencia de un Registro Público Unificado de Personas Desaparecidas en Nicaragua
- **Evidencia documental y oficial:** A la fecha de esta investigación, el Estado de Nicaragua no dispone de un portal web público, unificado y de acceso libre con series estadísticas abiertas y georreferenciadas sobre personas desaparecidas o extraviadas.
- **Evidencia operativa:** Las denuncias de desaparición son procesadas de manera dispersa a través de las delegaciones de la Policía Nacional y el Ministerio Público, sin un buscador centralizado orientado a la colaboración cívica ni mecanismos de interoperabilidad pública en línea.
- **Decisión de diseño en el proyecto:** **Encuéntrame Nicaragua** se posiciona técnicamente como una **plataforma cívica independiente y complementaria**, diseñada para mitigar este vacío de centralización, articulando información estructurada con consentimiento expreso de los familiares y estricta moderación.

---

### 4. DIFERENCIACIÓN OBLIGATORIA ENTRE FUENTES, INTERPRETACIONES Y BENEFICIOS

Para garantizar la honestidad intelectual y la precisión metodológica:

1. **Datos de Fuentes Primarias:**
   - Textos de leyes y reglamentos oficiales (La Gaceta N.° 61 y N.° 200).
   - Directrices humanitarias del CICR (enfoque centrado en familiares, recopilación ante mortem, desvinculación de la investigación penal).
   - Requisitos de seguridad ASVS 5.0.0 de OWASP (Argon2id, JWT, sanitización de imágenes WebP, RBAC, rate limiting).

2. **Interpretaciones del Equipo de Ingeniería:**
   - La deducción de que el almacenamiento de números de cédula debe realizarse exclusivamente como hash SHA-256 unidireccional para satisfacer el principio de minimización del artículo 5 de la Ley 787.
   - La determinación de que el proceso de "Carpetas Vivas" del CICR se materializa digitalmente en una línea de tiempo dinámica (`timeline`) en Next.js con estados `draft`, `pending_review`, `approved_published` y `closed_resolved`.

3. **Beneficios Estimados (No atribuidos a estadísticas oficiales inexistentes):**
   - Reducción del tiempo de difusión de alertas comunitarias ante extravíos de menores o ancianos con desorientación.
   - Mitigación del riesgo de revictimización y extorsiones mediante moderación previa del 100% de los reportes.
   - Protección de la intimidad y seguridad física mediante la eliminación absoluta de metadatos GPS (EXIF) en fotografías públicas.