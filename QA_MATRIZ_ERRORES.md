# MATRIZ PROFESIONAL DE DEFECTOS Y HALLAZGOS — QA SENIOR
## PROYECTO: ENCUÉNTRAME NICARAGUA

**Fecha de Evaluación:** 18 de Noviembre de 2026  
**Criterio de Severidad:**
- **P0 — Crítico:** Compromete la seguridad, privacidad de las víctimas, integridad de datos o detiene la operación de módulos principales.
- **P1 — Alto:** Impide flujos funcionales relevantes o carece de validaciones de frontera esenciales.
- **P2 — Medio:** Afecta parcialmente la usabilidad, experiencia de usuario o genera inconsistencias menores.
- **P3 — Bajo:** Oportunidades de mejora, optimizaciones de código o mantenimiento.

---

## 1. MATRIZ CONSOLIDADA DE HALLAZGOS

| ID | Módulo | Defecto / Hallazgo | Sev. | Archivo y Línea | Evidencia | Causa Raíz | Propuesta de Corrección | Estado |
| :--- | :--- | :--- | :---: | :--- | :--- | :--- | :--- | :---: |
| **DEF-01** | Seguridad / Fotos | Riesgo de Path Traversal en descarga de imágenes | **P0** | [backend/app/api/v1/reports.py:412](file:///c:/Users/User/Documents/Valor%20IA/EncuentrameNicaragua/backend/app/api/v1/reports.py#L412-L418) | Endpoint `/photos/{storage_key}` recibe parámetro sin validar formato `hex.webp` | `os.path.join(settings.STORAGE_DIR, storage_key)` permite secuencias relativas `..` | Validar `storage_key` con regex `^[a-f0-9]{32}\.webp$` o verificar `os.path.commonpath` | **Confirmado** |
| **DEF-02** | Seguridad / API | Exposición de trazas internas en excepciones no controladas | **P0** | [backend/app/main.py:59](file:///c:/Users/User/Documents/Valor%20IA/EncuentrameNicaragua/backend/app/main.py#L59-L63) | Respuesta JSON contiene `"detail": f"Error interno en el servidor: {str(exc)}"` | Fuga de nombres de tablas, paths o variables internas hacia clientes HTTP (OWASP A05) | Enmascarar mensaje a texto genérico institucional y mantener `str(exc)` solo en logs internos | **Confirmado** |
| **DEF-03** | Auth / Seguridad | Ausencia de Rate Limiting en endpoint de registro de usuarios | **P1** | [backend/app/api/v1/auth.py:52](file:///c:/Users/User/Documents/Valor%20IA/EncuentrameNicaragua/backend/app/api/v1/auth.py#L52-L57) | `POST /auth/register` no tiene inyección de dependencias `rate_limit` | Omisión de política de limitación de solicitudes ante registros automatizados | Agregar `dependencies=[Depends(rate_limit_register)]` (máx. 3 registros por IP cada 10 min) | **Confirmado** |
| **DEF-04** | Auth / Sesiones | Ausencia de revocación o lista negra de tokens JWT en logout | **P1** | [backend/app/api/v1/auth.py:97](file:///c:/Users/User/Documents/Valor%20IA/EncuentrameNicaragua/backend/app/api/v1/auth.py#L97-L99) | `POST /auth/logout` solo devuelve mensaje estático; el token permanece válido 24 horas | Stateless JWT no guarda estado de invalidación en servidor ni blacklist | Implementar tabla de revocación o blacklist de `jti`/token hash o reducir vida a 60 min con refresh tokens | **Confirmado** |
| **DEF-05** | Frontend / Reportes | Falta de control de error y ausencia de cliente tipado al subir foto | **P1** | [frontend/src/app/reportar/page.tsx:138](file:///c:/Users/User/Documents/Valor%20IA/EncuentrameNicaragua/frontend/src/app/reportar/page.tsx#L138-L144) | `fetch("${apiBase}/reports/${result.id}/photos")` no valida `res.ok` ni errores | Código `fetch` crudo desacoplado de `src/lib/api.ts` sin alertar si la foto falló | Crear función `uploadReportPhoto` en `src/lib/api.ts` y presentar retroalimentación visual al reportante | **Confirmado** |
| **DEF-06** | Frontend / Stepper | Validación tardía de fecha futura y longitudes en formulario de reporte | **P2** | [frontend/src/app/reportar/page.tsx:568](file:///c:/Users/User/Documents/Valor%20IA/EncuentrameNicaragua/frontend/src/app/reportar/page.tsx#L568-L583) | Permite avanzar al Paso 4 con fecha de desaparición futura o texto de menos de 10 caracteres | La función `onClick` de siguiente paso no valida el rango de fechas ni longitudes mínimas | Validar fecha no futura y `min_length` de descripciones en cada paso antes de permitir avanzar | **Confirmado** |
| **DEF-07** | Funcionalidad | Inexistencia de endpoint para suscripción a alertas ciudadanas | **P2** | [backend/app/api/v1/notifications.py](file:///c:/Users/User/Documents/Valor%20IA/EncuentrameNicaragua/backend/app/api/v1/notifications.py) | Solo existe `/unsubscribe/{token}`; no existe `POST /notifications/subscribe` | Se creó el modelo `NotificationSubscription` pero se omitió el endpoint de registro | Implementar `POST /notifications/subscribe` con validación de correo y departamento de interés | **Confirmado** |
| **DEF-08** | Privacidad / Ley 787 | Modelo `DeletionRequest` huérfano sin endpoints de consumo | **P2** | [backend/app/models/entities.py:259](file:///c:/Users/User/Documents/Valor%20IA/EncuentrameNicaragua/backend/app/models/entities.py#L259-L272) | Tabla `deletion_requests` existe pero no hay rutas en `reports.py` ni en `admin.py` | La funcionalidad de derecho al olvido / supresión no fue expuesta en la API | Crear endpoints `POST /reports/{id}/request-deletion` y `GET/PATCH /admin/deletion-requests` | **Confirmado** |
| **DEF-09** | Frontend / Calidad | Ausencia de suite de pruebas automatizadas en Frontend (`npm test`) | **P2** | [frontend/package.json:5](file:///c:/Users/User/Documents/Valor%20IA/EncuentrameNicaragua/frontend/package.json#L5-L10) | `npm test` arroja error `Missing script: "test"` | No se instalaron ni configuraron librerías de prueba (Jest, Vitest o Playwright) | Instalar `vitest` / `@testing-library/react` y configurar script de pruebas en CI/CD | **Confirmado** |
| **DEF-10** | Accesibilidad / HTML | Advertencias de ESLint por uso de etiquetas `<img>` nativas | **P3** | [ReportCard.tsx:22](file:///c:/Users/User/Documents/Valor%20IA/EncuentrameNicaragua/frontend/src/components/reports/ReportCard.tsx#L22), [casos/[id]/page.tsx:124](file:///c:/Users/User/Documents/Valor%20IA/EncuentrameNicaragua/frontend/src/app/casos/[id]/page.tsx#L124) | `next build` genera advertencia `@next/next/no-img-element` | Uso de `<img>` en lugar del componente optimizado `<Image />` de Next.js | Migrar a `<Image />` con dominios autorizados y fallbacks accesibles | **Confirmado** |
| **DEF-11** | Accesibilidad / A11y | Ausencia de vinculación semántica `htmlFor` - `id` en controles de formulario | **P3** | [login/page.tsx:146](file:///c:/Users/User/Documents/Valor%20IA/EncuentrameNicaragua/frontend/src/app/login/page.tsx#L146), [reportar/page.tsx:265](file:///c:/Users/User/Documents/Valor%20IA/EncuentrameNicaragua/frontend/src/app/reportar/page.tsx#L265) | `<label>` no posee atributo `htmlFor` ni los inputs poseen `id` coincidente | Omisión de directrices WCAG 2.1 AA para lectores de pantalla | Agregar atributos `id` y `htmlFor` a todos los campos de entrada de datos | **Confirmado** |
| **DEF-12** | Seguridad / Config | `SECRET_KEY` en `config.py` utiliza clave de desarrollo por defecto | **P1** | [backend/app/core/config.py:15](file:///c:/Users/User/Documents/Valor%20IA/EncuentrameNicaragua/backend/app/core/config.py#L15) | Si no se pasa variable de entorno, se utiliza string harcodeado de desarrollo | No existe validación de arranque que impida iniciar en modo `production` con la clave default | Agregar validador en `Settings` que arroje excepción si `ENVIRONMENT == "production"` y se usa la clave default | **Confirmado** |

---

## 2. DISTRIBUCIÓN DE DEFECTOS POR SEVERIDAD

- **Total de Defectos Confirmados:** 12
- **P0 — Críticos:** 2 (16.7%) — Path Traversal en imágenes y fuga de datos en excepciones 500.
- **P1 — Altos:** 3 (25.0%) — Rate limiting en registro, falta de blacklist de tokens y `SECRET_KEY` permisiva.
- **P2 — Medios:** 4 (33.3%) — Manejo de fotos en frontend, validaciones tempranas en stepper, alertas y derecho al olvido.
- **P3 — Bajos:** 3 (25.0%) — Pruebas en frontend, etiquetas de imagen y accesibilidad de etiquetas de formulario.

---

## 3. DIFERENCIACIÓN TÉCNICA DE ESTADOS
- **Defecto Confirmado:** 12 incidencias reproducibles directamente en el código fuente.
- **Riesgo Potencial:** Ataques de fuerza bruta sobre el registro de cuentas debido a la falta de rate limiting en `/auth/register`.
- **Validación Faltante:** Validación en cliente de fechas futuras y longitudes mínimas en el formulario multipaso de reportes.
- **Funcionalidad Incompleta:** Suscripción a alertas ciudadanas (`POST /notifications/subscribe`) y trámite de derecho al olvido (`DeletionRequest`).
- **Mejora Recomendada:** Migración de `<img>` a `next/image` y vinculación estricta de accesibilidad WCAG.
