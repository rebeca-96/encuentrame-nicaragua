# 02 — MATRIZ GENERAL DE DEFECTOS Y VULNERABILIDADES
## Proyecto: ENCUÉNTRAME NICARAGUA
### Auditoría QA Senior Full Stack — Clasificación por Severidad y Capa
**Auditor:** Senior QA Engineer & SDET  
**Fecha:** 19 de Noviembre de 2026  
**Total Defectos Identificados:** 8  

---

## 1. CRITERIOS DE SEVERIDAD UTILIZADOS

- **P0 (Bloqueante / Critical):** Impide el funcionamiento esencial de la plataforma en producción, fuga datos sensibles o bloquea totalmente a los usuarios sin alternativa.
- **P1 (Alta / High):** Afecta flujos clave del negocio (navegación directa por URL, carga de casos) con impacto directo en la experiencia o degradación de funciones críticas.
- **P2 (Media / Medium):** Inconsistencias en rutas de API, fallos de accesibilidad WCAG 2.2, optimización de base de datos o sanitización de metadatos secundarios.
- **P3 (Baja / Low):** Mejoras de robustez defensiva, límites de paginación o tolerancia a fallos en modo fuera de línea.

---

## 2. MATRIZ CONSOLIDADA DE DEFECTOS

| ID | Módulo | Descripción del Defecto | Severidad | Capa | Evidencia / Reproducción | Validación o Medida Faltante | Responsable Sugerido | Estado |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **DEF-01** | Infraestructura / Hosting | **Backend API desconectada en Hosting Público:** `https://creacionvaloria.tradescanner.online/api/v1/` devuelve `HTTP 404 Not Found`. El frontend estático no puede consultar casos, departamentos ni registrar reportes en producción. | **P0** | DevOps / Backend | `curl -s -o /dev/null -w "%{http_code}" https://creacionvaloria.tradescanner.online/api/v1/health` -> `404` | Falta configuración de reverse proxy en servidor web (Nginx/Traefik) hacia el proceso FastAPI (puerto 8000) o variable de entorno de API pública. | DevOps / Full Stack | **ABIERTO** |
| **DEF-02** | Frontend / Routing | **Rutas limpias devuelven 404 en Hosting Estático:** Al acceder directamente o refrescar URLs como `/casos`, `/mapa`, `/reportar` o `/pistas` se recibe un error 404 del servidor. Solo responden con sufijo `.html` (`/casos.html`). | **P1** | Frontend / DevOps | Petición HTTP a `https://creacionvaloria.tradescanner.online/casos` responde `404 Not Found` en lugar de servir `casos.html`. | Falta regla de reescritura en servidor web (`try_files $uri $uri.html $uri/ /index.html;`) o exportar con `trailingSlash: true` en `next.config.ts`. | Frontend / DevOps | **ABIERTO** |
| **DEF-03** | API / Admin | **Inconsistencia en Endpoint Raíz de Reportes Administrativos:** `GET /api/v1/admin/reports` devuelve `404 Not Found`. El endpoint implementado es exclusivamente `GET /api/v1/admin/reports/pending`. | **P2** | Backend REST | `client.get("/api/v1/admin/reports")` responde `HTTP 404`. No existe handler genérico de consulta de reportes para administradores. | Falta implementar handler RESTful estándar para listado global de reportes administrativos con filtro de estado (`?status=...`). | Backend Engineer | **ABIERTO** |
| **DEF-04** | Frontend / A11y | **Accesibilidad WCAG 2.2 Faltante en Formularios y Navegación:** Botones sin texto accesible (menú móvil en `Navbar.tsx`), campos de formulario sin asociación explícita `id`/`htmlFor` y falta de `aria-live` para alertar errores en pantalla. | **P2** | Frontend UI | Inspección de `Navbar.tsx` y `ReportWizard.tsx`: botones carecen de `aria-label`, inputs usan wrappers sin IDs coincidentes. | Cumplimiento WCAG 2.2 Criterios 1.3.1 (Info and Relationships) y 4.1.2 (Name, Role, Value). | Frontend Engineer | **ABIERTO** |
| **DEF-05** | Base de Datos / Rendimiento | **Falta de Índice Compuesto para Filtro de Casos Activos:** La tabla `missing_person_reports` tiene índices individuales en `status` y `department`, pero no un índice compuesto `(status, department, disappearance_date DESC)`. | **P2** | Database / ORM | Inspección de `backend/app/models/entities.py`: `__table_args__` no incluye índice multi-columna para las queries más frecuentes de la portada y buscador. | `Index('ix_reports_active_feed', 'status', 'department', 'disappearance_date')` en SQLAlchemy. | Database Engineer | **ABIERTO** |
| **DEF-06** | API / DoS | **Falta de Límite Máximo en Parámetro de Paginación (`limit`):** En `GET /api/v1/reports/`, el parámetro `limit` no define un valor máximo (`le=100`) en Query params, permitiendo solicitar hasta millones de registros. | **P3** | Backend Schemas | Petición `GET /api/v1/reports/?limit=500000` es aceptada por FastAPI sin generar `HTTP 422`. | Agregar validador Pydantic / Query: `limit: int = Query(default=50, ge=1, le=100)`. | Backend Engineer | **ABIERTO** |
| **DEF-07** | Privacidad / Almacenamiento | **Metadatos EXIF / GPS no purgados en Carga de Fotos:** `storage_service.py` almacena y procesa imágenes con PIL pero no elimina explícitamente los tags EXIF (geolocalización original de la cámara). | **P2** | Backend / Seguridad | Análisis de `storage_service.py`: al guardar la imagen no se reconstruye un canvas limpio sin metadatos EXIF. | Ley N.° 787 Art. 6: Garantía de no exposición de coordenadas privadas del domicilio o informante a través de metadatos de fotos. | Backend / Security | **ABIERTO** |
| **DEF-08** | Frontend / Resiliencia | **Ausencia de Estado Desconectado (Offline Graceful Degradation):** Si se interrumpe la conexión, la interfaz muestra errores técnicos sin un componente de reconexión o caché de datos de emergencia. | **P3** | Frontend UX | Desconectar interfaz en pruebas y pulsar "Buscar" muestra mensaje genérico no amigable sin botón de reintento. | Implementar Toast o Banner con botón "Reintentar" y captura centralizada de desconexión. | Frontend Engineer | **ABIERTO** |

---

## 3. RESUMEN ESTADÍSTICO DE DEFECTOS

```
+--------------------+-------+
| Nivel de Severidad | Total |
+--------------------+-------+
| P0 (Bloqueante)    |   1   |
| P1 (Alta)          |   1   |
| P2 (Media)         |   4   |
| P3 (Baja)          |   2   |
+--------------------+-------+
| TOTAL HALLAZGOS    |   8   |
+--------------------+-------+
```

```
+---------------------+-------+
| Capa Afectada       | Total |
+---------------------+-------+
| Infraestructura/Web |   2   |
| Backend / REST API  |   2   |
| Frontend / UI / UX  |   2   |
| Base de Datos       |   1   |
| Seguridad/Privacidad|   1   |
+---------------------+-------+
```
