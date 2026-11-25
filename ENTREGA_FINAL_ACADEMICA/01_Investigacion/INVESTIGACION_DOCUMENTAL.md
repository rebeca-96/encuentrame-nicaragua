# INVESTIGACIÓN ACADÉMICA Y FUNDAMENTACIÓN DOCUMENTAL
## Plataforma Cívica de Búsqueda y Reunificación Familiar: ENCUÉNTRAME NICARAGUA

**Investigador Principal:** Equipo de Investigación Académica Senior, Arquitectura de Software y Derechos Humanos  
**Fecha de Edición:** 24 de noviembre de 2026  
**Estándar de Documentación:** Normas APA 7.ª edición  
**Área de Conocimiento:** Ingeniería de Software, Derechos Humanos, Protección de Datos y Ciberseguridad

---

## ÍNDICE DE CONTENIDOS

1. Introducción de la investigación
2. Metodología de investigación documental
3. Contexto de las personas desaparecidas en Nicaragua
4. Necesidades de las familias afectadas
5. Dificultades para centralizar reportes
6. Importancia de la recopilación y verificación de información
7. Protección de datos personales (Ley N.° 787 de Nicaragua)
8. Consentimiento informado
9. Protección de menores y personas vulnerables
10. Importancia de la moderación humana
11. Seguridad de aplicaciones web (OWASP ASVS v5.0.0)
12. Participación ciudadana responsable
13. Utilidad de los sistemas de información geográfica (SIG)
14. Justificación de una plataforma tecnológica centralizada
15. Limitaciones de la investigación
16. Conclusiones

---

### 1. INTRODUCCIÓN DE LA INVESTIGACIÓN

La desaparición de un ser querido constituye una de las crisis humanas y psicosociales más devastadoras que puede experimentar una familia y una comunidad (Comité Internacional de la Cruz Roja [CICR], 2021). A nivel global y regional, la ausencia involuntaria o el extravío de personas —derivado de dinámicas migratorias irregulares, accidentes en zonas remotas, delincuencia común, violencia intrafamiliar o desorientación de personas vulnerables— sumerge a sus familiares en lo que el derecho humanitario internacional define como un estado de incertidumbre prolongada o "limbo humanitario" (CICR, 2023).

En la República de Nicaragua, las familias que enfrentan la no localización de un pariente recurren habitualmente a esfuerzos dispersos: carteles impresos en postes de alumbrado público, cadenas informales en redes sociales y solicitudes de apoyo en medios locales. Aunque estas iniciativas reflejan la desesperada resiliencia familiar, adolecen de graves vulnerabilidades: falta de verificación de datos, exposición masiva de números telefónicos privados susceptibles a extorsiones, revictimización de menores y permanencia indefinida de fotografías en la web una vez que la persona ha sido localizada (IPANDETEC, 2021).

Frente a esta problemática, la ingeniería de software moderna ofrece herramientas determinantes para articular esfuerzos cívicos seguros y colaborativos. No obstante, una solución tecnológica destinada a la búsqueda de personas no puede concebirse como un simple tablón digital de anuncios; demanda una fundamentación rigurosa en tres pilares inseparables:
1. **El marco jurídico nacional**, centrado en la *Ley N.° 787 de Protección de Datos Personales* de Nicaragua (Asamblea Nacional de Nicaragua, 2012) y su Reglamento (Poder Ejecutivo de Nicaragua, 2012).
2. **Los principios ético-humanitarios internacionales**, consagrados en las directrices del CICR (2021, 2023), que priorizan la centralidad de las familias y la desvinculación de la búsqueda humanitaria de fines punitivos.
3. **Los estándares técnicos de ciberseguridad**, fundamentados en el *Application Security Verification Standard* (ASVS) versión 5.0.0 de la OWASP Foundation (2025).

El propósito de la presente investigación documental es fundamentar rigurosamente la necesidad, viabilidad social, diseño funcional y arquitectura de software de la plataforma cívica **Encuéntrame Nicaragua**, asegurando que cada componente técnico responda a imperativos éticos, legales y humanitarios verificables.

---

### 2. METODOLOGÍA DE INVESTIGACIÓN DOCUMENTAL

La investigación se desarrolló bajo un enfoque metodológico cualitativo, de diseño documental, descriptivo y aplicado, orientado a la derivación de requisitos para sistemas de información críticos. 

El procedimiento se articuló en cuatro fases secuenciales:

1. **Fase Heurística (Búsqueda y Compilación):**
   Se recopilaron y verificaron fuentes documentales primarias y secundarias a través de repositorios normativos oficiales del Estado nicaragüense (Sistema de Información Jurídica SAJURIN de la Biblioteca Enrique Bolaños y Diario Oficial La Gaceta), bases de datos especializadas del CICR (*Missing Persons Global Response*) y especificaciones técnicas de la OWASP Foundation.

2. **Fase Hermenéutica (Crítica y Análisis Documental):**
   Se realizó un análisis de contenido y exégesis normativa de la Ley N.° 787 y su Reglamento (Decreto N.° 36-2012), correlacionando los mandatos legales sobre consentimiento, derechos ARCO y calidad de datos con los estándares técnicos de seguridad de ASVS v5.0.0. Asimismo, se contrastaron las directrices operativas del CICR para el restablecimiento del contacto familiar con la realidad socioterritorial de Nicaragua (INIDE, 2021).

3. **Fase de Derivación Arquitectónica (Trazabilidad hacia el Software):**
   Cada hallazgo documental fue traducido en requisitos funcionales (RF) y no funcionales (RNF) aplicables a la arquitectura web existente desarrollada en Next.js 14 y FastAPI, evaluando su correspondencia en los módulos de registro, catálogo, geolocalización, gestión de fotografías, moderación y auditoría.

4. **Fase de Validación y Control de Integridad:**
   Se aplicó un principio estricto de honestidad académica: no inventar datos estadísticos inexistentes en fuentes oficiales nicaragüenses, transparentar la falta de operatividad de entes de control como la DIPRODAP, y diferenciar taxativamente los hechos demostrados en la literatura de las interpretaciones y beneficios proyectados por el equipo de diseño.

---

### 3. CONTEXTO DE LAS PERSONAS DESAPARECIDAS EN NICARAGUA

El análisis de la desaparición y extravío de personas en Nicaragua presenta características socioterritoriales particulares que condicionan cualquier respuesta tecnológica:

#### 3.1. Multicausalidad del Fenómeno
A partir de los informes regionales del CICR (2023) y diagnósticos sociodemográficos de Centroamérica, se identifican las principales causas de pérdida de contacto familiar en el país:
a) **Flujos Migratorios:** Personas que inician trayectos migratorios hacia el norte (México y Estados Unidos) o hacia el sur (Costa Rica y Panamá), perdiendo comunicación en zonas de frontera, selvas o desiertos.
b) **Extravíos por Vulnerabilidad Física o Cognitiva:** Niñas, niños y adolescentes que abandonan temporalmente sus hogares por conflictos familiares o violencia, así como personas adultas mayores con demencia senil, Alzheimer o condiciones médicas que provocan desorientación en entornos urbanos o rurales.
c) **Eventos Naturales y Emergencias Climáticas:** Nicaragua es altamente propensa a inundaciones, huracanes y deslizamientos que aíslan comunidades completas en la cuenca del Caribe y zonas montañosas del norte.
d) **Violencia Común y Delincuencia:** Casos de personas que son víctimas de delitos en zonas urbanas o rurales sin que sus familias reciban aviso oportuno.

#### 3.2. Vacío de Información Oficial Centralizada y Accesible
Un hallazgo crítico de esta investigación es la **ausencia de un Registro Nacional Público y Unificado de Personas Desaparecidas** con portal digital abierto mantenido por el Estado de Nicaragua. Si bien la Policía Nacional y el Ministerio Público procesan denuncias penales individuales, la ciudadanía no cuenta con un motor de búsqueda oficial, centralizado, georreferenciado y accesible en línea donde consultar alertas activas o cotejar indicios. Esta fragmentación institucional obliga a la sociedad civil a buscar alternativas cívicas independientes para articular la solidaridad comunitaria.

---

### 4. NECESIDADES DE LAS FAMILIAS AFECTADAS

El CICR (2021, 2023) documenta de forma exhaustiva las necesidades prioritarias que enfrentan los familiares:
1. **El Derecho a Saber:** Conocer la suerte y el paradero del ser querido es la necesidad primordial e innegociable. El limbo de no saber si la persona está viva, herida o en resguardo paraliza el duelo y desestructura a la familia.
2. **Centralización y Difusión Inmediata:** La eficacia de la búsqueda disminuye exponencialmente a medida que transcurren las primeras 24 a 72 horas. Las familias requieren canales ágiles que difundan la alerta en el territorio relevante sin retrasos burocráticos.
3. **Protección Contra la Extorsión y el Fraude:** En Centroamérica, cuando las familias publican desesperadamente sus números personales en redes sociales, con frecuencia reciben llamadas de estafadores que exigen recargas telefónicas o transferencias bancarias a cambio de información falsa (CICR, 2023).
4. **Respeto a la Dignidad y Preservación de la Privacidad:** La familia exige que los datos íntimos de la persona (condiciones de salud, ropa íntima o historial familiar) sean tratados con respeto y retirados cuando el caso concluya.

---

### 5. DIFICULTADES PARA CENTRALIZAR REPORTES

La dispersión de los esfuerzos comunitarios genera severos cuellos de botella:
- **Sobrecarga y Duplicidad en Redes Sociales:** Las publicaciones en Facebook, TikTok o WhatsApp carecen de estructura semántica; una misma persona es reportada múltiples veces con nombres alterados o fotografías obsoletas, dificultando el filtrado por departamento o fecha.
- **Persistencia Indeseada de Fichas:** En redes sociales, una alerta compartida cientos de veces permanece en línea durante años tras la localización de la persona, provocando que personas ya reintegradas a su vida social continúen siendo señaladas como "desaparecidas".
- **Brecha Digital Rural:** Zonas del interior del país y de las regiones autónomas de la Costa Caribe poseen baja penetración de banda ancha, lo que requiere plataformas ligeras, con bajo consumo de datos y compatibilidad móvil extrema.

---

### 6. IMPORTANCIA DE LA RECOPILACIÓN Y VERIFICACIÓN DE INFORMACIÓN

El CICR (2021) subraya que un proceso de búsqueda eficaz depende de la **calidad técnica de los datos ante mortem**. No basta un nombre y una fotografía; se requieren:
- Rasgos fisonómicos inmutables (lunares visibles, cicatrices, tatuajes, prótesis).
- Indumentaria exacta y pertenencias portadas en el momento del último contacto.
- Padecimientos médicos críticos que demanden medicación urgente (asma, diabetes, hipertensión).
- Circunstancias temporales y espaciales del hecho (fecha, hora, contexto del trayecto).

En **Encuéntrame Nicaragua**, esta recopilación se implementa a través de un esquema relacional normalizado (`missing_person_reports`), asegurando que la información sea estructurada y comparable, facilitando búsquedas facetadas por edad, género, departamento y municipio.

---

### 7. PROTECCIÓN DE DATOS PERSONALES (LEY N.° 787 DE NICARAGUA)

#### 7.1. Marco Legal Aplicable
La *Ley N.° 787, Ley de Protección de Datos Personales* (Asamblea Nacional de Nicaragua, 2012), regula el tratamiento de información en ficheros automatizados públicos y privados. El artículo 1 consagra como bien jurídico protegido la privacidad personal y familiar, y el derecho fundamental a la **autodeterminación informativa** (artículo 3).

#### 7.2. Principio de Minimización y Proporcionalidad (Artículo 6)
El artículo 6 estipula que los datos personales recabados deben ser adecuados, pertinentes y no excesivos en relación con el ámbito y las finalidades determinadas. En el diseño de la plataforma:
- Se recopilan únicamente los datos estrictamente necesarios para la identificación visual y biográfica de la persona buscada.
- No se almacenan datos sensibles innecesarios (orientación política, creencias religiosas o datos patrimoniales).

#### 7.3. Ejercicio de Derechos ARCO y Supresión (Artículos 13 al 17)
La ley reconoce a los titulares los derechos de Acceso, Rectificación, Cancelación y Oposición. El artículo 16 exige la supresión de datos cuando hayan dejado de ser pertinentes.
- **Implementación:** Se diseñó el endpoint `POST /api/v1/reports/{id}/request-deletion` que permite al declarante o titular solicitar formalmente el borrado de sus registros, despublicando inmediatamente la información durante la tramitación administrativa.

#### 7.4. Estado de la Autoridad de Aplicación (DIPRODAP)
El artículo 29 de la Ley 787 previó la creación de la Dirección de Protección de Datos Personales (DIPRODAP). Como se documentó en las evidencias (IPANDETEC, 2021), dicho órgano no tiene una presencia digital activa ni un esquema de supervisión operativa verificable. Ante esta realidad, la plataforma asume los postulados de la ley bajo un modelo de **cumplimiento autoimpuesto y verificable por diseño (*Privacy by Design*)**.

---

### 8. CONSENTIMIENTO INFORMADO

El artículo 5 de la Ley N.° 787 establece que el tratamiento de datos personales exige el consentimiento libre, previo, expreso e informado del titular. En casos de personas desaparecidas donde el titular se encuentra ausente, el consentimiento debe ser otorgado legítimamente por el familiar más cercano o representante legal (CICR, 2018).

En **Encuéntrame Nicaragua**:
- Todo reporte exige marcar una casilla de verificación obligatoria de consentimiento legal que invoca la Ley 787.
- Se registra la relación de parentesco declarada (Madre, Padre, Cónyuge, Hermano/a, Tutor Legal).
- **Protección Criptográfica:** El número de documento de identidad del declarante se procesa mediante una función hash criptográfica SHA-256 (`doc_hash`), y la dirección IP se anonimiza mediante hash unidireccional. Esto permite demostrar la trazabilidad legal ante una auditoría sin almacenar datos de identidad en texto claro en la base de datos (`ConsentRecord`).

---

### 9. PROTECCIÓN DE MENORES Y PERSONAS VULNERABLES

#### 9.1. Marco del Código de la Niñez y la Adolescencia (Ley N.° 287)
El *Código de la Niñez y la Adolescencia* (Asamblea Nacional de Nicaragua, 1998) establece el principio universal del **Interés Superior del Niño**. La difusión pública de la imagen de un menor de 18 años debe ser extremadamente prudente para evitar estigmatización o vulneración de su integridad física o psíquica.

#### 9.2. Banderas de Vulnerabilidad en el Sistema
La plataforma incorpora una bandera booleana (`vulnerability_flag`) que se activa de forma automática cuando:
- La persona es menor de 18 años (`is_minor = true`).
- La persona tiene 65 años o más (adulto mayor).
- El reporte declara condiciones médicas críticas (ej. autismo, discapacidad cognitiva, asma severa).

Estas fichas reciben un distintivo visual prioritario en color rojo de alerta temprana (`MENOR DE EDAD`), atrayendo la atención inmediata de la comunidad y priorizando su revisión en la mesa de moderación humana.

---

### 10. IMPORTANCIA DE LA MODERACIÓN HUMANA

Un principio técnico y ético innegociable derivado de la investigación es la **imposibilidad de publicación automática directa**. Permitir que un formulario web publique fichas sin revisión previa habilitaría:
1. Denuncias falsas dirigidas a desprestigiar o difamar a personas.
2. Utilización del sistema por parte de agresores de violencia machista para rastrear el paradero de mujeres que han huido de situaciones de violencia intrafamiliar.
3. Publicación de fotografías inapropiadas o que revelen domicilios protegidos.

Por ello, en **Encuéntrame Nicaragua**, todo reporte recién creado se asigna indefectiblemente al estado `pending_review` (`is_public = False`). Solo los usuarios con rol `moderator` o `admin` pueden autorizar su publicación cívica tras examinar la coherencia de la narrativa, la verosimilitud de los datos y la ausencia de riesgos a terceros.

---

### 11. SEGURIDAD DE APLICACIONES WEB (OWASP ASVS V5.0.0)

La seguridad técnica del sistema fue contrastada contra el *Application Security Verification Standard* (ASVS) versión 5.0.0 de la OWASP Foundation (2025):

#### 11.1. Manejo Seguro de Archivos Multimedia (Capítulo V12)
El riesgo de que una imagen contenga código malicioso o exponga metadatos EXIF fue neutralizado mediante el servicio `storage_service.py`:
- Validación binaria de firma MIME (solo `image/jpeg`, `image/png`, `image/webp`).
- Uso de la librería Pillow para reconstruir la imagen en memoria, eliminando cabeceras EXIF con coordenadas GPS y marcas de tiempo del teléfono.
- Conversión forzada a WebP con calidad 85% y límite de 800x800 píxeles.
- Asignación de nombre aleatorio criptográfico MD5/SHA256 (`<hash>.webp`) para impedir ataques de Path Traversal o nombres de archivo ejecutables.

#### 11.2. Autenticación y Criptografía (Capítulos V2 y V6)
- **Hashing de Contraseñas:** Se descartaron algoritmos débiles y se implementó **Argon2id** (`passlib.hash.argon2`), estándar recomendado por OWASP por su resistencia contra ataques de fuerza bruta asistidos por GPU.
- **Sesiones:** Emisión de tokens firmados mediante JSON Web Token (JWT) con expiración corta y lista negra de revocación en base de datos (`token_revocations`).

#### 11.3. Control de Acceso por Roles - RBAC (Capítulo V4)
- Jerarquía estricta de 4 roles (`admin`, `moderator`, `reporter`, `citizen`) aplicada a nivel de middleware en FastAPI (`deps.py`).
- Los ciudadanos anónimos o autenticados carecen de permisos para consultar el endpoint administrativo de pistas (`/api/v1/admin/tips`) arrojando HTTP 403 Forbidden.

#### 11.4. Auditoría Inmutable (Capítulo V8)
- Registro forense en la tabla `audit_logs` que almacena cada evento sensible (`REPORT_CREATED`, `REPORT_MODERATED_APPROVE`, `CASE_CLOSED`, etc.), garantizando no-repudio.

---

### 12. PARTICIPACIÓN CIUDADANA RESPONSABLE

El CICR (2021) destaca que la solidaridad de la comunidad es a menudo el factor determinante para localizar a una persona extraviada. Sin embargo, esta participación debe canalizarse de forma estructurada para evitar la difusión de rumores o la interferencia imprudente.

En la plataforma:
- El módulo `/pistas` permite a cualquier ciudadano aportar datos sobre un avistamiento.
- Se ofrece la opción de anonimato absoluto (`strict_anonymous`) para personas que temen comprometer su seguridad.
- Al informante se le genera un código único de seguimiento (`tip_code`) alfanumérico, que le permite conocer si su testimonio fue evaluado por los moderadores sin necesidad de identificarse públicamente.
- Las pistas no se publican en el muro público; se depositan directamente en la bandeja privada de moderación.

---

### 13. UTILIDAD DE LOS SISTEMAS DE INFORMACIÓN GEOGRÁFICA (SIG)

La búsqueda de personas es una actividad inherentemente espacial. La delimitación territorial orienta los esfuerzos comunitarios hacia las regiones con mayor probabilidad de avistamiento.

#### 13.1. División Político-Administrativa Oficial de Nicaragua
Conforme a la cartografía del INIDE (2021), el sistema modela de forma exacta:
- 15 departamentos y 2 regiones autónomas (RACCN y RACCS).
- 153 municipios oficiales con centroides y geometrías GeoJSON integradas localmente.

#### 13.2. Georreferenciación Ética y Privacidad Diferencial
La plataforma no expone coordenadas satelitales milimétricas de domicilios familiares. En su lugar, el mapa nacional (`NationalMap.tsx`) agrupa y proyecta los casos sobre centroides municipales o coordenadas aproximadas de zonas públicas de avistamiento (`approximate_latitude` y `approximate_longitude`), balanceando la utilidad cartográfica con la seguridad física de los afectados.

---

### 14. JUSTIFICACIÓN DE UNA PLATAFORMA TECNOLÓGICA CENTRALIZADA

Frente a la dispersión de esfuerzos, una plataforma web centralizada proporciona ventajas operativas insustituibles:
1. **Punto Único de Verdad:** Un repositorio oficial previene versiones contradictorias y datos desactualizados.
2. **Arquitectura Híbrida Desacoplada:** El uso de Next.js como generador estático (SSG) garantiza tiempos de carga casi instantáneos y alta disponibilidad ante picos de tráfico, mientras que la API en FastAPI encapsula las reglas de negocio, criptografía y persistencia relacional.
3. **Autonomía y Desacoplamiento de Terceros:** La paquetería local (estilos, Leaflet, iconografía sin CDN) garantiza que el sistema funcione en redes cerradas o entornos de contingencia nacional sin dependencias externas.

---

### 15. LIMITACIONES DE LA INVESTIGACIÓN

Para mantener el rigor académico, se declaran explícitamente las limitaciones de este estudio:
1. **Falta de Series Estadísticas Públicas Desagregadas:** Debido a que el Estado de Nicaragua no publica boletines epidemiológicos o estadísticos abiertos y continuos sobre personas no localizadas por municipio, las cifras de incidencia no pudieron modelarse sobre datos cuantitativos oficiales recientes.
2. **Inoperatividad de la DIPRODAP:** No fue posible evaluar resoluciones, circulares vinculantes o dictámenes de la autoridad de protección de datos de Nicaragua, obligando a fundar las decisiones de diseño en el texto literal de la Ley 787 y doctrina regional comparada.
3. **Brecha de Conectividad en Comunidades Rurales:** Aunque la plataforma está optimizada para bajo consumo de datos, la persistencia de zonas sin cobertura celular en la Costa Caribe limita el alcance de cualquier aplicación basada en navegador web, señalando la necesidad de esquemas PWA offline en etapas futuras.

---

### 16. CONCLUSIONES

1. **Viabilidad y Relevancia Social:** La investigación documental demuestra que **Encuéntrame Nicaragua** responde a una necesidad humanitaria apremiante y no resuelta en el país, ofreciendo a las familias una alternativa cívica digna, estructurada y protectora de sus derechos fundamentales.
2. **Alineamiento Jurídico Riguroso:** La arquitectura del sistema cumple con los mandatos esenciales de la Ley N.° 787 de Nicaragua: consentimiento informado obligatorio, no almacenamiento de documentos en texto plano (hashing SHA-256), principios de minimización y despublicación inmediata ante la resolución del caso (artículo 16).
3. **Adopción de Buenas Prácticas Humanitarias:** La implementación de expedientes tipo "Carpetas Vivas" mediante líneas de tiempo dinámicas (`timeline`) y buzones confidenciales de pistas traduce fielmente las directrices del Comité Internacional de la Cruz Roja (CICR).
4. **Seguridad y Privacidad por Diseño:** La aplicación estricta de controles OWASP ASVS v5.0.0 —especialmente la sanitización automática de metadatos EXIF con Pillow y el control de acceso RBAC jerárquico— previene vectores de extorsión, secuestro de datos o vulneración física de las víctimas.
5. **Autonomía Operativa:** El desacoplamiento de dependencias externas en la compilación de Next.js y el servido unificado con FastAPI aseguran que la plataforma sea tecnológicamente soberana, robusta y escalable.

---
**Fin del Documento de Investigación Académica.**