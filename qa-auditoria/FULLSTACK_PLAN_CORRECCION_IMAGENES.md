# PLAN DE CORRECCIÓN FULL STACK — MÓDULO DE FOTOGRAFÍAS
## Proyecto: ENCUÉNTRAME NICARAGUA
**Arquitecto / Lead Full Stack:** Senior QA & Full Stack Engineer  
**Estado:** PENDIENTE DE AUTORIZACIÓN DEL USUARIO  

---

## 1. EXPLICACIÓN DE LA CAUSA RAÍZ

El problema por el cual las tarjetas de los 16 casos muestran siluetas genéricas en lugar de las fotografías reales tiene tres causas técnicas interconectadas:

1. **Expresión regular excesivamente restrictiva en el servicio de almacenamiento del Backend:**  
   En `backend/app/services/storage_service.py`, la constante `STORAGE_KEY_REGEX = re.compile(r"^[a-f0-9]{32}\.webp$")` solo acepta cadenas de 32 dígitos hexadecimales. Como los datos oficiales de los 16 casos fueron generados con nombres canónicos semánticos (`avatar_en-2026-0001.webp`), el backend rechaza cualquier petición a `GET /api/v1/reports/photos/avatar_en-2026-0001.webp` con un error `HTTP 400 Bad Request`.

2. **Captura y reemplazo por silueta en el Frontend:**  
   El componente `ReportCard.tsx` y `CasoDetailClient.tsx` tiene un controlador de evento `onError` en la etiqueta `<img>`. Al recibir el código HTTP 400 del backend, el navegador activa el callback y sustituye silenciosamente la imagen por `/images/avatar-placeholder.svg`.

3. **Compatibilidad en Hosting Público vs. Servidor Local:**  
   En el hosting público estático (`creacionvaloria.tradescanner.online`), la aplicación web corre sobre un servidor de archivos estáticos donde los endpoints dinámicos de `/api/v1/reports/photos/...` no existen. Por ello, el frontend debe contar con un mecanismo de resolución inteligente que verifique si la imagen está disponible vía API o directamente en el directorio público `/images/avatars/`.

---

## 2. ARCHIVOS AFECTADOS

| Componente | Archivo | Modificación Requerida |
|---|---|---|
| **Backend (Storage Service)** | [backend/app/services/storage_service.py](file:///c:/Users/User/Documents/Valor%20IA/EncuentrameNicaragua/backend/app/services/storage_service.py) | Ajustar `STORAGE_KEY_REGEX` para admitir de forma segura nombres UUID y nombres oficiales `avatar_en-2026-XXXX.webp`. |
| **Backend (Reports API)** | [backend/app/api/v1/reports.py](file:///c:/Users/User/Documents/Valor%20IA/EncuentrameNicaragua/backend/app/api/v1/reports.py) | Asegurar que `primary_photo_url` en la lista pública retorne una URL canónica válida y accesible. |
| **Frontend (ReportCard)** | [frontend/src/components/reports/ReportCard.tsx](file:///c:/Users/User/Documents/Valor%20IA/EncuentrameNicaragua/frontend/src/components/reports/ReportCard.tsx) | Optimizar la resolución de `photoSrc` para consultar la API o la ruta estática pública con reintento antes de recurrir a la silueta. |
| **Frontend (CasoDetailClient)** | [frontend/src/app/casos/[id]/CasoDetailClient.tsx](file:///c:/Users/User/Documents/Valor%20IA/EncuentrameNicaragua/frontend/src/app/casos/[id]/CasoDetailClient.tsx) | Asegurar la misma lógica robusta de visualización fotográfica y seguimiento. |
| **Pruebas de Seguridad** | [backend/tests/test_security_audit_v2.py](file:///c:/Users/User/Documents/Valor%20IA/EncuentrameNicaragua/backend/tests/test_security_audit_v2.py) | Añadir casos de prueba que validen que `avatar_en-2026-XXXX.webp` sea servido con HTTP 200 mientras que los intentos de *Path Traversal* sigan estrictamente bloqueados con HTTP 400. |

---

## 3. PROPUESTA DE CORRECCIÓN PASO A PASO

### Paso 1: Actualización de Expresión Regular Segura en `storage_service.py`
Sustituir:
```python
STORAGE_KEY_REGEX = re.compile(r"^[a-f0-9]{32}\.webp$")
```
Por:
```python
# Admite tanto UUIDs hexadecimales de 32 caracteres como avatares oficiales de expedientes pre-cargados
STORAGE_KEY_REGEX = re.compile(r"^(?:[a-f0-9]{32}|avatar_en-\d{4}-\d{4,5})\.webp$", re.IGNORECASE)
```
*Garantía de Seguridad:* Mantiene el bloqueo absoluto de caracteres peligrosos (`..`, `/`, `\`, caracteres nulos) y la verificación canónica de ruta con `os.path.commonpath([base_dir, full_path]) == base_dir`.

### Paso 2: Validación de la Suite de Pruebas Automatizadas de Pytest
Ejecutar `pytest backend/tests` para comprobar que todas las 38 pruebas existentes pasen al 100% sin regresiones y que el endpoint entregue la imagen física con `HTTP 200 OK`.

### Paso 3: Optimización del Manejo de Imágenes en el Frontend
En `ReportCard.tsx` y `CasoDetailClient.tsx`, asegurar que si el reporte cuenta con fotografía autorizada en el backend, se solicite primero a través de la ruta correspondiente, y si se encuentra en el hosting estático, consulte directamente `/images/avatars/{storage_key}`.

### Paso 4: Verificación Visual y Despliegue
Compilar con `npm run build` y sincronizar hacia `creacionvaloria.tradescanner.online` para certificar que las tarjetas muestren inmediatamente las imágenes correspondientes sin placeholders.

---

## 4. SOLICITUD DE AUTORIZACIÓN

> [!IMPORTANT]
> Siguiendo estrictamente las directrices de auditoría, **ninguna línea de código ha sido modificada** en este turno. El presente plan técnico se somete a revisión y espera tu aprobación explícita antes de proceder a la aplicación de cambios.
