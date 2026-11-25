# ESTUDIO INTEGRAL DE VIABILIDAD DEL PROYECTO

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