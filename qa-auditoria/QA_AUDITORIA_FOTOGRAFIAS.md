# INFORME DE AUDITORÍA QA SENIOR — MÓDULO DE FOTOGRAFÍAS
## Proyecto: ENCUÉNTRAME NICARAGUA
**Fecha de Auditoría:** 19 de Noviembre de 2026  
**Auditor:** Senior QA Engineer & Full Stack Architect  
**Entorno:** Backend FastAPI / PostgreSQL (SQLite local) / Frontend Next.js / Hosting Público  

---

## 1. RESUMEN EJECUTIVO

Se ejecutó una auditoría forense y funcional de extremo a extremo (Frontend, Backend, Base de Datos, Sistema de Archivos y Red) sobre el módulo de fotografías de personas desaparecidas de la plataforma **Encuéntrame Nicaragua**.

### Hallazgo Principal (Causa Raíz Confirmada)
Las fotografías de los 16 casos no son genéricas por ausencia de datos ni por falta de archivos físicos. Las 20 fotografías sintéticas oficiales **existen físicamente** en `storage/uploads/` y están **correctamente registradas y autorizadas** en la base de datos (`report_photos.is_approved = True`). 

El motivo exacto por el cual la interfaz web muestra siluetas genéricas o marcadores visuales (`avatar-placeholder.svg`) se debe a un **bloqueo estricto por expresión regular en la capa de seguridad del backend**:

1. En [backend/app/services/storage_service.py](file:///c:/Users/User/Documents/Valor%20IA/EncuentrameNicaragua/backend/app/services/storage_service.py#L14), la validación de seguridad contra *Path Traversal* (CWE-22) definió:
   ```python
   STORAGE_KEY_REGEX = re.compile(r"^[a-f0-9]{32}\.webp$")
   ```
2. Los datos de inicialización oficial ([backend/app/seed/seed_data.py](file:///c:/Users/User/Documents/Valor%20IA/EncuentrameNicaragua/backend/app/seed/seed_data.py#L534)) asignaron identificadores con prefijo temático:
   ```python
   avatar_file = f"avatar_{case_data['case_number'].lower()}.webp"  # ej: avatar_en-2026-0001.webp
   ```
3. Al consultar el endpoint oficial de entrega de imágenes `GET /api/v1/reports/photos/{storage_key}`, la función `get_file_path()` rechaza el nombre `avatar_en-2026-0001.webp` por no ser exactamente un hash hexadecimal de 32 caracteres, arrojando **`HTTP 400 Bad Request: Identificador de fotografía inválido. Formato no admitido.`**
4. En el frontend, el componente [ReportCard.tsx](file:///c:/Users/User/Documents/Valor%20IA/EncuentrameNicaragua/frontend/src/components/reports/ReportCard.tsx#L37) y [CasoDetailClient.tsx](file:///c:/Users/User/Documents/Valor%20IA/EncuentrameNicaragua/frontend/src/app/casos/[id]/CasoDetailClient.tsx#L196) capturan el error HTTP mediante el evento `onError` del elemento `<img>` y sustituyen la imagen por el marcador por defecto `/images/avatar-placeholder.svg`.

---

## 2. DIAGNÓSTICO DETALLADO POR CAPA

### 2.1. Capa de Base de Datos
* **Tabla Auditada:** `report_photos` relacionada con `missing_person_reports`.
* **Integridad Referencial:** 100% íntegra. Cada uno de los 16 expedientes publicados tiene una fila correspondiente en `report_photos` con `is_primary = True` e `is_approved = True`.
* **Fotografías Huérfanas:** 0 fotografías huérfanas en la base de datos.
* **Archivos Inexistentes:** 0 referencias a archivos rotos; todos los archivos `avatar_en-2026-XXXX.webp` existen en el volumen de almacenamiento.

### 2.2. Capa de Almacenamiento Físico (Storage)
* **Directorio Configurado:** `settings.STORAGE_DIR = ./storage/uploads`.
* **Archivos Presentes:** 21 archivos WebP verificados en disco.
* **Formato:** WebP optimizado, 400x400 píxeles, sin metadatos EXIF sensibles, con marcas de agua civiles de prueba.

### 2.3. Capa de Backend (FastAPI)
* **Endpoints Evaluados:**
  - `POST /api/v1/reports/{report_id}/photos` (Subida de fotos): Funciona correctamente para nuevas subidas porque genera UUID de 32 hex (`uuid.uuid4().hex + ".webp"`).
  - `GET /api/v1/reports/photos/{storage_key}` (Servicio de fotos): **FALLA** con HTTP 400 para las fotos semilla pre-registradas debido a la restricción de `STORAGE_KEY_REGEX`.

### 2.4. Capa de Frontend (Next.js)
* **Construcción de URLs:**
  - El backend retorna URLs relativas `/api/v1/reports/photos/{storage_key}`.
  - En el entorno local (`localhost:3000`), el navegador intenta acceder a dicha ruta que devuelve HTTP 400.
  - En el hosting estático (`creacionvaloria.tradescanner.online`), la ruta `/api/v1/...` no existe en el servidor estático independiente, por lo que debe resolverse mediante el directorio estático sincronizado `/images/avatars/`.

---

## 3. CONCLUSIONES DE LA AUDITORÍA

1. Las fotografías individuales no aparecen **no porque falten o no existan**, sino por una discrepancia entre la regla de validación de nombres de archivo del servicio de almacenamiento y los nombres asignados en los datos oficiales de los casos.
2. La arquitectura de privacidad y sanitización (eliminación de EXIF y validación de tipos MIME) es robusta y cumple con los estándares exigidos por la Ley N.° 787 de Protección de Datos Personales de Nicaragua.
3. El plan de corrección debe armonizar la validación de `STORAGE_KEY_REGEX`, actualizar la correspondencia en los controladores y garantizar la sincronización transparente en ambos entornos (local y hosting público).
