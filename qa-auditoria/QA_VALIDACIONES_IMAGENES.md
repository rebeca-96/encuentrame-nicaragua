# AUDITORÍA TÉCNICA DE VALIDACIONES DE IMÁGENES
## Proyecto: ENCUÉNTRAME NICARAGUA
**Módulo:** Gestión Segura y Carga de Archivos Multimedia  
**Estándar de Referencia:** OWASP ASVS v4.0 (Sección V12: File and Resource Handling) / Ley N.° 787 de Nicaragua  

---

## 1. MATRIZ DE CONTROL DE VALIDACIONES DE SEGURIDAD

| Requisito de Validación | Estado Actual | Implementación / Evidencia Técnica | Nivel de Riesgo |
|---|---|---|---|
| **1. Formatos Permitidos (JPEG, PNG, WebP)** | **CONFORME (PASS)** | Validado en `backend/app/services/storage_service.py` mediante firmas de bytes mágicos. | Bajo |
| **2. Verificación de Firma Real (Magic Bytes)** | **CONFORME (PASS)** | Evaluado en `VALID_IMAGE_SIGNATURES`: `\xff\xd8\xff` (JPEG), `\x89PNG` (PNG), `RIFF` (WebP), `GIF87a/89a`. | Bajo |
| **3. Rechazo de Archivos Ejecutables / Scripts** | **CONFORME (PASS)** | Archivos `.exe`, `.sh`, `.php`, `.js` son rechazados antes del procesamiento por firma inválida. | Crítico |
| **4. Validación de Integridad contra Corrupción** | **CONFORME (PASS)** | Uso de `Image.open().verify()` de Pillow. Captura `UnidentifiedImageError` y arroja HTTP 400. | Medio |
| **5. Tamaño Máximo Configurable** | **CONFORME (PASS)** | Configurado en `settings.MAX_UPLOAD_SIZE_MB` (5 MB). Valida longitud de bytes antes de procesar. | Medio |
| **6. Dimensiones Máximas y Redimensionamiento** | **CONFORME (PASS)** | Si ancho o alto excede 1280px, aplica `img.thumbnail((1280, 1280), Image.Resampling.LANCZOS)`. | Bajo |
| **7. Eliminación Total de Metadatos EXIF** | **CONFORME (PASS)** | Transposición de orientación y re-creación en lienzo limpio `RGB` en WebP; elimina coordenadas GPS del dispositivo. | Crítico |
| **8. Sanitización de Nombres Peligrosos** | **CONFORME (PASS)** | El nombre del cliente se descarta; se genera un UUID determinista `uuid.uuid4().hex + ".webp"`. | Crítico |
| **9. Prevención de Sobrescritura de Archivos** | **CONFORME (PASS)** | Generación con entropía alta (128 bits UUID) impide colisiones en disco. | Medio |
| **10. Protección contra Path Traversal (CWE-22)** | **DEFECTO PARCIAL (OVER-RESTRICTIVE)** | `get_file_path()` valida `os.path.commonpath()` y expresión regular, pero la regex bloquea avatares legítimos de semilla. | Alto |
| **11. Hash Criptográfico para Trazabilidad** | **CONFORME (PASS)** | Se calcula `hashlib.sha256(file_bytes).hexdigest()` y se persiste en `ReportPhoto.file_hash_sha256`. | Bajo |
| **12. Control de Autorización y Moderación** | **CONFORME (PASS)** | `is_approved = True` requerido para que la API pública exponga la URL; imágenes sin aprobar quedan ocultas. | Crítico |

---

## 2. DETALLE DE DEFECTOS Y RECOMENDACIONES EN VALIDACIÓN

### Defecto V-01: Expresión Regular de Acceso Demasiado Restrictiva
* **Ubicación:** [backend/app/services/storage_service.py](file:///c:/Users/User/Documents/Valor%20IA/EncuentrameNicaragua/backend/app/services/storage_service.py#L14)
* **Código Actual:**
  ```python
  STORAGE_KEY_REGEX = re.compile(r"^[a-f0-9]{32}\.webp$")
  ```
* **Impacto:** Los identificadores generados para casos precargados (ej. `avatar_en-2026-0001.webp` hasta `avatar_en-2026-00020.webp`) son rechazados con HTTP 400 a pesar de ser archivos canónicos válidos que residen en el directorio seguro.
* **Solución Propuesta:** Ajustar la expresión regular permitida para incluir de forma controlada el patrón seguro de avatares oficiales sin comprometer la protección contra Path Traversal:
  ```python
  STORAGE_KEY_REGEX = re.compile(r"^(?:[a-f0-9]{32}|avatar_en-\d{4}-\d{4,5})\.webp$", re.IGNORECASE)
  ```

---

## 3. VALIDACIÓN EN EL FRONTEND

1. **Atributo `accept="image/jpeg,image/png,image/webp"`:** Debe reforzarse en el `<input type="file">` en [frontend/src/app/reportar/page.tsx](file:///c:/Users/User/Documents/Valor%20IA/EncuentrameNicaragua/frontend/src/app/reportar/page.tsx) para guiar al usuario.
2. **Validación Previa al Envío:** Validar en el cliente el tamaño del archivo (`file.size <= 5 * 1024 * 1024`) para evitar transferencias innecesarias de datos móviles.
3. **Manejo de Respuestas de Error:** Presentar mensajes amigables cuando el backend rechace una imagen por dimensiones o corrupción.
