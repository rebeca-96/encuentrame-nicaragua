# MATRIZ DE AUDITORÍA QA — 16 CASOS REGISTRADOS
## Proyecto: ENCUÉNTRAME NICARAGUA
**Módulo:** Verificación Individual de Fotografías por Expediente  
**Objetivo:** Determinar la disponibilidad, integridad, autorización y renderizado de la imagen de cada persona reportada.  

---

## 1. TABLA GENERAL DE AUDITORÍA DE LOS 16 CASOS

| N.° | ID Caso | Número Caso | Persona Reportada | Foto en BD | Archivo Físico | Autorizada | Endpoint API Backend | Visualización Observada | Diagnóstico QA |
|:---:|:---|:---|:---|:---:|:---:|:---:|:---|:---|:---|
| 1 | `30c12319...` | **EN-2026-0001** | Mateo Andrés García Centeno | Sí | Sí | Sí | HTTP 400 (Regex) | Placeholder Genérico | **BLOQUEO POR REGEX** |
| 2 | `81d0ddbf...` | **EN-2026-0002** | Valeria Nicole Pérez Fonseca | Sí | Sí | Sí | HTTP 400 (Regex) | Placeholder Genérico | **BLOQUEO POR REGEX** |
| 3 | `b716dac6...` | **EN-2026-0003** | Don Manuel de Jesús Rocha Blandón | Sí | Sí | Sí | HTTP 400 (Regex) | Placeholder Genérico | **BLOQUEO POR REGEX** |
| 4 | `5cd11745...` | **EN-2026-0004** | Yader Francisco Gutiérrez Marenco | Sí | Sí | Sí | HTTP 400 (Regex) | Placeholder Genérico | **BLOQUEO POR REGEX** |
| 5 | `7d322980...` | **EN-2026-0005** | Katherin Amanda Salgado Méndez | Sí | Sí | Sí | HTTP 400 (Regex) | Placeholder Genérico | **BLOQUEO POR REGEX** |
| 6 | `9395b915...` | **EN-2026-0006** | Luis Alberto Torres Zeledón | Sí | Sí | Sí | HTTP 400 (Regex) | Placeholder Genérico | **BLOQUEO POR REGEX** |
| 7 | `b16d1539...` | **EN-2026-0007** | Mariana del Socorro Aguilar Obando | Sí | Sí | Sí | HTTP 400 (Regex) | Placeholder Genérico | **BLOQUEO POR REGEX** |
| 8 | `4c6fabc8...` | **EN-2026-0008** | José Ramón Chavarría Rivas | Sí | Sí | Sí | HTTP 400 (Regex) | Placeholder Genérico | **BLOQUEO POR REGEX** |
| 9 | `f2ce1bd6...` | **EN-2026-0009** | Brenda Liseth Morales Hurtado | Sí | Sí | Sí | HTTP 400 (Regex) | Placeholder Genérico | **BLOQUEO POR REGEX** |
| 10 | `5e0a9e95...` | **EN-2026-00010** | Wilmer Enrique Aragón Borge | Sí | Sí | Sí | HTTP 400 (Regex) | Placeholder Genérico | **BLOQUEO POR REGEX** |
| 11 | `20f789cd...` | **EN-2026-00011** | Carlos Fernando Blandón Somarriba | Sí | Sí | Sí | HTTP 400 (Regex) | Placeholder Genérico | **BLOQUEO POR REGEX** |
| 12 | `37171e21...` | **EN-2026-00012** | Dayana Marcela Tinoco Estrada | Sí | Sí | Sí | HTTP 400 (Regex) | Placeholder Genérico | **BLOQUEO POR REGEX** |
| 13 | `8c971e14...` | **EN-2026-00013** | Pedro Joaquín López Urbina | Sí | Sí | Sí | HTTP 400 (Regex) | Placeholder Genérico | **BLOQUEO POR REGEX** |
| 14 | `c404ec67...` | **EN-2026-00014** | Keilynn Joyse Hodgson Campbell | Sí | Sí | Sí | HTTP 400 (Regex) | Placeholder Genérico | **BLOQUEO POR REGEX** |
| 15 | `48d3b2ee...` | **EN-2026-00015** | Erick Jayson Finley Dixon | Sí | Sí | Sí | HTTP 400 (Regex) | Placeholder Genérico | **BLOQUEO POR REGEX** |
| 16 | `9c43aabc...` | **EN-2026-00016** | Francisco Javier Cruz Pastrana | Sí | Sí | Sí | HTTP 400 (Regex) | Placeholder Genérico | **BLOQUEO POR REGEX** |

---

## 2. ANÁLISIS DE RESULTADOS DE LA MATRIZ

1. **Disponibilidad en Base de Datos (100%):** Los 16 casos poseen un registro hijo válido en la tabla `report_photos`. No existen expedientes con referencias huérfanas o nulas entre los 16 casos iniciales.
2. **Existencia Física de Archivos (100%):** Todos los archivos referenciados (`storage/uploads/avatar_en-2026-0001.webp` hasta `avatar_en-2026-00016.webp`) se encuentran alojados en el directorio de almacenamiento local del backend con tamaño aproximado de 4.3 KB cada uno.
3. **Estado de Aprobación Ética y Legal (100%):** Todos los registros tienen el indicador `is_approved = True` y `is_primary = True`, cumpliendo los criterios del equipo de moderación para su difusión pública.
4. **Falla en el Punto de Entrega (100% de los 16 casos):** Al solicitar la imagen a través del controlador `GET /api/v1/reports/photos/{storage_key}`, el backend responde con error `HTTP 400 Bad Request` debido a la validación de `STORAGE_KEY_REGEX`.
5. **Comportamiento en el Cliente Web:** El componente frontend `ReportCard` detecta el fallo HTTP mediante el evento `onError` del elemento HTML `<img>` y carga automáticamente el SVG de respaldo `/images/avatar-placeholder.svg`.

---

## 3. COMPROBACIÓN ADICIONAL DE CASO SIN FOTOGRAFÍA (CASO DE CONTROL)

* **Expediente de Control:** `EN-2026-0021` (Carlos García QA, creado durante pruebas exploratorias de registro sin adjuntar fotografía).
* **Foto en BD:** No.
* **Archivo Físico:** No aplica.
* **Comportamiento Esperado:** Mostrar el marcador de imagen `/images/avatar-placeholder.svg` de forma legítima.
* **Comportamiento Obtenido:** **PASS**. El sistema identifica la ausencia de fotografía y despliega el marcador de silueta oficial sin provocar errores de consola.
