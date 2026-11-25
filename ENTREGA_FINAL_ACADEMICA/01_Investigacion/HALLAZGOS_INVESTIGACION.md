# SÍNTESIS DE HALLAZGOS DE LA INVESTIGACIÓN DOCUMENTAL

## PROYECTO: ENCUÉNTRAME NICARAGUA
### Plataforma Cívica de Búsqueda y Reunificación Familiar
**Investigador:** Especialista en Derechos Humanos, Metodología y Ciberseguridad  
**Fecha:** 24 de noviembre de 2026

---

### INTRODUCCIÓN Y ENFOQUE METODOLÓGICO

El presente informe sintetiza los hallazgos documentales, empíricos y técnicos obtenidos tras la revisión sistemática de las tres fuentes principales de referencia:
1. **Fuente Jurídica:** Ley N.° 787 de Protección de Datos Personales de Nicaragua (Asamblea Nacional de Nicaragua, 2012) y su Decreto Reglamentario N.° 36-2012 (Poder Ejecutivo de Nicaragua, 2012).
2. **Fuente Humanitaria:** Directrices globales sobre el proceso de búsqueda y reporte regional para México y Centroamérica del Comité Internacional de la Cruz Roja (CICR, 2021, 2023).
3. **Fuente Tecnológica:** Estándar de Verificación de Seguridad en Aplicaciones Web ASVS versión 5.0.0 de la OWASP Foundation (2025).

Complementariamente, se integraron análisis territoriales del Instituto Nicaragüense de Información de Desarrollo (INIDE, 2021) y diagnósticos de privacidad digital regional (IPANDETEC, 2021).

Los hallazgos se estructuran en cuatro ejes temáticos fundamentales:

---

### EJE 1: HALLAZGOS JURÍDICOS Y NORMATIVOS (LEY N.° 787 DE NICARAGUA)

#### 1.1. Principio de Autodeterminación Informativa y Consentimiento Previo
- **Hallazgo:** Los artículos 1 y 3 de la Ley N.° 787 establecen que el tratamiento de datos personales en cualquier fichero público o privado solo es lícito si se respeta el derecho de la persona a conocer quién, con qué fines y en qué circunstancias se tratan sus datos. El artículo 5 instituye como regla general el **consentimiento libre, expreso e informado**.
- **Aplicación al Proyecto:** Ningún reporte de desaparición puede ser creado de forma automatizada o arbitraria sin un consentimiento expreso del familiar directo o representante legal. En el formulario `/reportar` se exige la aceptación explícita de los términos bajo la Ley 787.
- **Minimización de Datos y Criptografía:** El artículo 6 consagra el principio de calidad de datos y proporcionalidad. Almacenar el número de cédula física del declarante en texto claro representaría un riesgo inaceptable de filtración. Se determinó convertir la cédula y la IP en un hash unidireccional SHA-256 (`ConsentRecord`), permitiendo verificar unicidad y trazabilidad legal sin almacenar el dato de identidad en crudo.

#### 1.2. Derechos ARCO y Derecho al Olvido (Artículos 13 al 17)
- **Hallazgo:** La normativa nicaragüense otorga a los titulares los derechos de Acceso, Rectificación, Cancelación (Supresión) y Oposición (derechos ARCO). El artículo 16 dispone que los datos personales deben cancelarse o bloquearse cuando hayan dejado de ser necesarios o pertinentes para la finalidad con que fueron recabados.
- **Aplicación al Proyecto:** Cuando una persona reportada es localizada o sus familiares solicitan formalmente el cese de la búsqueda, la ficha debe ser **despublicada de inmediato** (`is_public = False`). No es ético ni legal que la imagen y datos de una persona localizada sigan expuestos públicamente en internet indexados por motores de búsqueda. Se implementaron los endpoints formales `POST /api/v1/reports/{id}/request-close` y `POST /api/v1/reports/{id}/request-deletion`.

#### 1.3. Régimen Institucional y Realidad Práctica (DIPRODAP)
- **Hallazgo:** Aunque la Ley 787 contempló la creación de la Dirección de Protección de Datos Personales (DIPRODAP) bajo el Ministerio de Hacienda y Crédito Público (artículo 29), los estudios de sociedad civil (IPANDETEC, 2021) constatan que dicho órgano no se encuentra plenamente operativo ni ofrece una ventanilla pública de fiscalización accesible.
- **Impacto:** La plataforma debe operar bajo el principio de **autorregulación proactiva y Privacidad desde el Diseño (*Privacy by Design*)**, implementando mecanismos internos verificables de seguridad y auditoría sin depender de requerimientos de un ente regulador externo inactivo.

---

### EJE 2: HALLAZGOS HUMANITARIOS Y SOCIALES (CICR)

#### 2.1. La Centralidad de las Familias en la Búsqueda
- **Hallazgo:** El Comité Internacional de la Cruz Roja (CICR, 2021) estipula que los familiares no son meros informantes pasivos, sino el núcleo del proceso de búsqueda. La angustia provocada por la desaparición genera un "limbo humanitario" (CICR, 2023) que impacta la salud física, emocional y la estabilidad económica del hogar.
- **Aplicación al Proyecto:** El sistema debe proporcionar a la familia acceso permanente a su expediente, control sobre los datos publicados y un estado visible del avance de las indagaciones.

#### 2.2. Metodología de "Carpetas Vivas" vs. Expedientes Burocráticos Estáticos
- **Hallazgo:** El CICR (2023) denuncia que en América Central muchas investigaciones fracasan porque los reportes se archivan como "carpetas muertas", desarticuladas y sin seguimiento activo. La metodología humanitaria exige "Carpetas Vivas": expedientes dinámicos, multidisciplinarios y abiertos a la incorporación continua de nueva información.
- **Aplicación al Proyecto:** En lugar de una base de datos estática, cada ficha (`/casos/[id]`) integra una **Línea de Tiempo Dinámica (`timeline`)** que registra hitos cronológicos (recepción de denuncia, validación documental, activación cívica territorial, procesamiento de testimonios y conclusión del caso).

#### 2.3. Búsqueda Humanitaria Desvinculada de la Sanción Penal
- **Hallazgo:** El proceso de búsqueda humanitaria persigue esclarecer la suerte y paradero de la persona para aliviar el sufrimiento de sus seres queridos, distinguiéndose de la investigación penal destinada a sancionar culpables (CICR, 2021).
- **Aplicación al Proyecto:** El canal de recepción de pistas (`/pistas`) permite aportaciones anónimas y confidenciales bajo secreto de testimonio, protegiendo a ciudadanos que poseen datos valiosos pero temen represalias si acuden a una sede policial convencional.

#### 2.4. Protección Contra el Fraude y la Extorsión
- **Hallazgo:** En contextos de desaparición en Centroamérica, las familias son frecuentemente blanco de extorsionistas y estafadores que exigen dinero a cambio de supuesta información sobre la persona ausente (CICR, 2023).
- **Aplicación al Proyecto:** No se publican teléfonos personales directos ni números de cuentas de los familiares en las fichas públicas. Todas las pistas se canalizan a través de un buzón institucional moderado por el sistema.

---

### EJE 3: HALLAZGOS TECNOLÓGICOS Y CIBERSEGURIDAD (OWASP ASVS V5.0.0)

#### 3.1. Gestión Segura de Archivos Multimedia y Peligro de Metadatos EXIF
- **Hallazgo:** Las fotografías tomadas con teléfonos inteligentes contienen metadatos Exchangeable Image File Format (EXIF) que almacenan coordenadas geográficas satelitales (latitud, longitud, altitud), marca y modelo del dispositivo, fecha y hora exacta. Si un familiar sube una foto tomada en su domicilio o en la escuela de sus otros hijos y se publica sin sanitización, se exponen puntos neurálgicos de vulnerabilidad física.
- **Aplicación al Proyecto (Capítulo V12 ASVS):** El servicio `storage_service.py` intercepta cada imagen subida mediante FastAPI y Pillow:
  1. Descarta todas las cabeceras EXIF y metadatos incrustados.
  2. Transcodifica la imagen a formato WebP optimizado (calidad 85).
  3. Redimensiona a dimensiones máximas controladas (800x800 píxeles).
  4. Asigna un nombre criptográfico único e impredecible (`<hash>.webp`) para prevenir ataques de enumeración o ejecución de código.

#### 3.2. Control de Acceso Riguroso (RBAC) y Seguridad en APIs
- **Hallazgo:** El estándar ASVS v5.0.0 (Capítulo V4) exige que las decisiones de autorización se tomen en el lado del servidor y no dependan de la interfaz de usuario.
- **Aplicación al Proyecto:**
  - Usuarios con rol `citizen` o anónimos no pueden consultar el listado de pistas confidenciales (HTTP 401/403).
  - Un usuario con rol `reporter` únicamente puede editar reportes creados por él mismo mientras estén en estado `draft` o `pending_review`.
  - Solo los roles `moderator` y `admin` tienen facultades para cambiar estados del caso a `approved_published`, archivar o despublicar.

#### 3.3. Autenticación Robusta y Protección Contra Ataques de Fuerza Bruta
- **Hallazgo:** ASVS v5.0.0 (Capítulos V2 y V3) desaconseja algoritmos obsoletos como MD5 o SHA-1 para contraseñas, recomendando algoritmos con coste de memoria elevado como Argon2id, además de rate limiting en endpoints de acceso.
- **Aplicación al Proyecto:**
  - Hasheo de contraseñas mediante **Argon2id** (`passlib.hash.argon2`).
  - Emisión de tokens de acceso firmados mediante **JWT (JSON Web Token)** con algoritmo HS256 y expiración temporal.
  - Limitador de tasa en memoria (`rate_limit.py`) para los endpoints críticos `/auth/login` y `/auth/register`.

#### 3.4. Registro Inmutable de Auditoría Forense
- **Hallazgo:** ASVS v5.0.0 (Capítulo V8) demanda el registro inalterable de eventos de seguridad y modificaciones de datos sensibles para garantizar no-repudio y trazabilidad.
- **Aplicación al Proyecto:** Implementación de la tabla `audit_logs` y `audit_service.py`, donde se registra la acción realizada, entidad afectada, ID de usuario ejecutor, dirección IP anonimizada y timestamp UTC inmutable.

---

### EJE 4: HALLAZGOS OPERATIVOS, GEOGRÁFICOS Y DE MODERACIÓN

#### 4.1. Cobertura Cartográfica Integral de Nicaragua (INIDE / INETER)
- **Hallazgo:** La división político-administrativa de Nicaragua comprende 15 departamentos y 2 regiones autónomas (RACCN y RACCS), con un total de 153 municipios oficiales (INIDE, 2021). Las herramientas comerciales de mapas a menudo presentan discrepancias tipográficas en nombres de municipios caribeños o fronterizos.
- **Aplicación al Proyecto:** Se integró el catálogo exhaustivo de 153 municipios y GeoJSON oficial validado, garantizando que comunidades de la Costa Caribe Norte y Sur tengan la misma representatividad y precisión de búsqueda que los departamentos del Pacífico y Centro.

#### 4.2. Privacidad Diferencial y Georreferenciación Aproximada
- **Hallazgo:** Publicar la ubicación exacta del domicilio o lugar de último avistamiento puede poner en riesgo la seguridad de testigos o de los propios familiares.
- **Aplicación al Proyecto:** La georreferenciación pública en el mapa (`NationalMap.tsx`) utiliza centroides municipales o coordenadas aproximadas con un radio de dispersión de zona, protegiendo direcciones domiciliarias exactas.

#### 4.3. Obligatoriedad Ineludible de la Moderación Humana
- **Hallazgo:** Permitir que cualquier persona publique de forma instantánea una alerta de desaparición en internet sin supervisión abre la puerta a difamaciones, cobros ilegítimos de deudas, violencia de género vicaria o engaños maliciosos.
- **Aplicación al Proyecto:** Todos los reportes creados ingresan estrictamente con estado `pending_review` (`is_public = False`). Solo un operador humano con rol `moderator` puede autorizar su paso a `approved_published` tras validar la autenticidad del reporte, el consentimiento y la documentación de respaldo.