# 10 — PLAN DE ACCIÓN Y CORRECCIÓN FULL STACK
## Proyecto: ENCUÉNTRAME NICARAGUA
### Guía Técnica Priorizada para el Ingeniero Full Stack Senior
**Auditor:** Senior QA Engineer & SDET  
**Fecha:** 19 de Noviembre de 2026  

---

## 1. RUTA CRÍTICA DE REMEDIACIÓN (SPRINT DE ESTABILIZACIÓN)

Para habilitar la plataforma en el entorno público de producción de manera segura y funcional, se debe seguir el siguiente orden estricto de tareas:

```
[FASE 1: INFRAESTRUCTURA (P0 / P1)]
  ├── Tarea 1.1: Conectar Proxy Reverso Nginx hacia Backend FastAPI (DEF-01)
  └── Tarea 1.2: Resolver Enrutamiento de URLs Limpias en Next.js (DEF-02)
         │
[FASE 2: BACKEND Y SEGURIDAD (P2 / P3)]
  ├── Tarea 2.1: Implementar Endpoint Global `GET /api/v1/admin/reports` (DEF-03)
  ├── Tarea 2.2: Purgar Metadatos EXIF / GPS en Subida de Fotos (DEF-07)
  └── Tarea 2.3: Restringir Paginación Máxima `le=100` (DEF-06)
         │
[FASE 3: BASE DE DATOS Y RENDIMIENTO (P2)]
  └── Tarea 3.1: Crear Índice Compuesto B-tree para Consultas de Casos Activos (DEF-05)
         │
[FASE 4: FRONTEND, ACCESIBILIDAD Y RESILIENCIA (P2 / P3)]
  ├── Tarea 4.1: Subsanar Brechas de Accesibilidad WCAG 2.2 en Formularios (DEF-04)
  └── Tarea 4.2: Componente de Tolerancia a Fallos y Reintento de Red (DEF-08)
```

---

## 2. DETALLE DE TAREAS TÉCNICAS

### Tarea 1.1: Conexión de API Backend en Hosting Público (DEF-01) [P0 - CRÍTICA]
- **Objetivo:** Permitir que las peticiones a `/api/v1/*` alcancen la API de FastAPI.
- **Archivos / Configuración Afectada:** Configuración del servidor web Nginx en el host.
- **Solución Propuesta:**
  En el archivo de configuración del sitio Nginx (`/etc/nginx/sites-available/...`):
  ```nginx
  server {
      server_name creacionvaloria.tradescanner.online;

      # Frontend estático compilado
      location / {
          root /var/www/encuentrame/frontend/out;
          index index.html;
          try_files $uri $uri.html $uri/ /index.html;
      }

      # Proxy reverso hacia el Backend FastAPI
      location /api/ {
          proxy_pass http://127.0.0.1:8000/api/;
          proxy_set_header Host $host;
          proxy_set_header X-Real-IP $remote_addr;
          proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
          proxy_set_header X-Forwarded-Proto $scheme;
      }

      # Almacenamiento de fotos estáticas
      location /storage/ {
          alias /var/www/encuentrame/backend/storage/;
          expires 30d;
          add_header Cache-Control "public, no-transform";
      }
  }
  ```
- **Criterio de Aceptación:** `curl -s -o /dev/null -w "%{http_code}" https://creacionvaloria.tradescanner.online/api/v1/health` debe devolver `200`.

---

### Tarea 1.2: Enrutamiento de URLs Limpias en Next.js (DEF-02) [P1 - ALTA]
- **Objetivo:** Evitar que URLs directas como `/casos` o `/mapa` devuelvan 404 al refrescar la pantalla.
- **Archivos Afectados:** `frontend/next.config.ts`.
- **Solución Propuesta:**
  Habilitar `trailingSlash: true`:
  ```typescript
  import type { NextConfig } from "next";

  const nextConfig: NextConfig = {
    output: "export",
    trailingSlash: true, // Exporta /casos/index.html en lugar de /casos.html
    images: {
      unoptimized: true,
    },
  };

  export default nextConfig;
  ```
  Al compilar con `trailingSlash: true`, cualquier servidor web estático sirve la página sin necesidad de configuraciones complejas de reescritura.
- **Criterio de Aceptación:** Acceder directamente a `https://creacionvaloria.tradescanner.online/casos/` responde con HTTP 200 y renderiza el catálogo.

---

### Tarea 2.1: Implementar Endpoint Global de Reportes Administrativos (DEF-03) [P2 - MEDIA]
- **Objetivo:** Estandarizar la API REST para el panel administrativo.
- **Archivos Afectados:** `backend/app/api/v1/admin.py`.
- **Solución Propuesta:**
  Implementar el handler `GET /api/v1/admin/reports` que soporte filtrado por estado (`pending_review`, `published`, `closed`, `rejected`).
- **Criterio de Aceptación:** Petición GET a `/api/v1/admin/reports` con credenciales de administrador retorna código 200 y el listado consolidado.

---

### Tarea 2.2: Purga de Metadatos EXIF / GPS en Fotografías (DEF-07) [P2 - PRIVACIDAD]
- **Objetivo:** Cumplir con el Artículo 6 de la Ley N.° 787 impidiendo la exposición indirecta de ubicaciones privadas mediante tags EXIF.
- **Archivos Afectados:** `backend/app/services/storage_service.py`.
- **Solución Propuesta:**
  Al abrir la imagen con PIL, regenerar un canvas limpio sin metadatos antes de guardar:
  ```python
  from PIL import Image

  def sanitize_and_save_photo(file_bytes: bytes, destination_path: str):
      with Image.open(io.BytesIO(file_bytes)) as img:
          # Recrear los datos de píxeles sin el diccionario info/exif
          clean_img = Image.new(img.mode, img.size)
          clean_img.putdata(list(img.getdata()))
          clean_img.save(destination_path, format="WEBP", quality=85)
  ```
- **Criterio de Aceptación:** Inspeccionar la imagen guardada con `exiftool` o `PIL._getexif()` y verificar que el diccionario EXIF es nulo o vacío.

---

### Tarea 2.3: Restringir Límite Máximo de Paginación (DEF-06) [P3 - SEGURIDAD]
- **Objetivo:** Evitar sobrecarga de memoria por consultas desmedidas.
- **Archivos Afectados:** `backend/app/api/v1/reports.py`.
- **Solución Propuesta:**
  ```python
  limit: int = Query(default=50, ge=1, le=100, description="Cantidad máxima de expedientes por página")
  ```
- **Criterio de Aceptación:** `GET /api/v1/reports/?limit=500` debe responder `HTTP 422 Unprocessable Entity`.

---

### Tarea 3.1: Índice Compuesto en Base de Datos (DEF-05) [P2 - RENDIMIENTO]
- **Objetivo:** Acelerar el filtrado de casos activos por departamento y orden cronológico.
- **Archivos Afectados:** `backend/app/models/entities.py`.
- **Solución Propuesta:**
  Agregar en la clase `MissingPersonReport`:
  ```python
  __table_args__ = (
      Index("ix_reports_active_feed", "status", "department", "disappearance_date"),
  )
  ```
- **Criterio de Aceptación:** Ejecutar `EXPLAIN QUERY PLAN` en SQLite/PostgreSQL y comprobar el uso del índice `ix_reports_active_feed`.

---

### Tarea 4.1: Accesibilidad WCAG 2.2 y Formularios (DEF-04) [P2 - UX]
- **Objetivo:** Garantizar uso universal para personas con discapacidad visual y de motricidad.
- **Archivos Afectados:**
  - `frontend/src/components/layout/Navbar.tsx`: Agregar `aria-label="Menú principal"` y `aria-expanded`.
  - `frontend/src/app/reportar/page.tsx`: Asociar `<label htmlFor="id_campo">` a cada `<input id="id_campo">`.
  - Agregar `role="alert"` y `aria-live="polite"` en los contenedores de mensajes de error.
- **Criterio de Aceptación:** Pasar auditoría automatizada con axe-core / Lighthouse Accessibility con puntaje superior a 95/100.
