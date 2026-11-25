# RESULTADOS DE PRUEBAS FUNCIONALES DE IMÁGENES (QA-IMG-001 A QA-IMG-018)
## Proyecto: ENCUÉNTRAME NICARAGUA
**Módulo:** Gestión, Almacenamiento, Sanitización y Despliegue de Fotografías  
**Auditor:** Senior SDET / QA Engineer  

---

## 1. TABLA RESUMEN DE PRUEBAS

| Caso de Prueba | Descripción | Resultado Esperado | Resultado Obtenido | Estado | Archivo Relacionado |
|---|---|---|---|:---:|---|
| **QA-IMG-001** | Subir fotografía válida (JPEG/PNG) | Imagen sanitizada en WebP sin EXIF guardada en disco | Generado UUID WebP en `./storage/uploads/` sin metadatos | **PASS** | `backend/app/services/storage_service.py` |
| **QA-IMG-002** | Rechazar formato no permitido (.exe, .sh) | HTTP 400 Bad Request por magic bytes inválidos | Rechazado con mensaje: `Formato de archivo no admitido` | **PASS** | `backend/app/services/storage_service.py` |
| **QA-IMG-003** | Rechazar archivo que excede 5MB | HTTP 400 Bad Request por exceso de tamaño | Rechazado con mensaje: `El archivo excede el tamaño máximo permitido` | **PASS** | `backend/app/api/v1/reports.py` |
| **QA-IMG-004** | Rechazar imagen corrupta | HTTP 400 por fallo de verificación en Pillow | Pillow `verify()` captura daño y arroja HTTP 400 | **PASS** | `backend/app/services/storage_service.py` |
| **QA-IMG-005** | Asociar fotografía al caso correcto | Clave foránea `report_id` apunta al expediente | `ReportPhoto.report_id == MissingPersonReport.id` confirmado | **PASS** | `backend/app/models/entities.py` |
| **QA-IMG-006** | Guardar fotografía de manera persistente | Archivos físicos conservados en volumen de almacenamiento | 21 archivos `.webp` presentes físicamente en disco | **PASS** | `storage/uploads/` |
| **QA-IMG-007** | Recuperar fotografía desde la API | HTTP 200 OK con `Content-Type: image/webp` | **HTTP 400 Bad Request** debido a `STORAGE_KEY_REGEX` | **FAIL** | `backend/app/services/storage_service.py` |
| **QA-IMG-008** | Mostrar fotografía en tarjeta | Tarjeta muestra la imagen individual de la persona | Se muestra `/images/avatar-placeholder.svg` por fallo 400 | **FAIL** | `frontend/src/components/reports/ReportCard.tsx` |
| **QA-IMG-009** | Mostrar fotografía en detalle del caso | Ficha `/casos/[id]` despliega la fotografía oficial | Se muestra `/images/avatar-placeholder.svg` por fallo 400 | **FAIL** | `frontend/src/app/casos/[id]/CasoDetailClient.tsx` |
| **QA-IMG-010** | Mostrar placeholder cuando no exista imagen | Expediente sin foto (ej. EN-2026-0021) muestra silueta | Muestra silueta oficial de forma controlada sin error | **PASS** | `frontend/src/components/reports/ReportCard.tsx` |
| **QA-IMG-011** | Evitar mostrar imágenes privadas | Fotos con `is_approved = False` no son públicas | Endpoint `/reports/` filtra `p.is_approved == True` | **PASS** | `backend/app/api/v1/reports.py` |
| **QA-IMG-012** | Validar fotografías de menores | Menores de edad muestran alerta visible | Insignia roja `ALERTA: MENOR DE EDAD` visible en tarjeta | **PASS** | `frontend/src/components/reports/ReportCard.tsx` |
| **QA-IMG-013** | Comprobar visualización móvil | Tarjeta no se deforma en pantallas pequeñas | Estilos Tailwind `w-full h-56 object-cover` probados | **PASS** | `frontend/src/components/reports/ReportCard.tsx` |
| **QA-IMG-014** | Comprobar carga desde el hosting público | Archivos WebP accesibles en dominio público | Sincronización en `creacionvaloria.tradescanner.online` responde 200 | **PASS** | `scratch_deploy.py` |
| **QA-IMG-015** | Comprobar que imágenes no se intercambien | Cada expediente tiene su imagen única | Mapeo 1:1 por `case_number` verificado | **PASS** | `backend/app/seed/seed_data.py` |
| **QA-IMG-016** | Comportamiento tras reiniciar el backend | Imágenes y base de datos conservan persistencia | Al reiniciar uvicorn, registros y archivos persisten | **PASS** | `backend/app/core/database.py` |
| **QA-IMG-017** | Comprobar retirada de imágenes autorizadas | Moderador puede revocar `is_approved` | Al pasar a `False`, la imagen deja de servirse públicamente | **PASS** | `backend/app/api/v1/admin.py` |
| **QA-IMG-018** | Verificar ausencia de errores de consola | Sin excepciones no capturadas de JavaScript | Fallbacks previenen errores fatales o pantalla blanca | **PASS** | `frontend/src/lib/catalogData.ts` |

---

## 2. BALANCE GENERAL DE LAS PRUEBAS

* **Total de Pruebas Ejecutadas:** 18
* **Pruebas Aprobadas (PASS):** 15 (83.3%)
* **Pruebas Fallidas (FAIL):** 3 (16.7%) — Corresponden a los casos de entrega y visualización afectados por el defecto de validación de clave de almacenamiento en el endpoint de la API (`QA-IMG-007`, `QA-IMG-008` y `QA-IMG-009`).
* **Pruebas Bloqueadas (BLOCKED):** 0
* **Pruebas No Ejecutadas (NOT RUN):** 0
