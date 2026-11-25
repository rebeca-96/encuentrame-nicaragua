# JUSTIFICACIÓN DE LA ALTERNATIVA SELECCIONADA Y ACLARACIÓN RETROSPECTIVA

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