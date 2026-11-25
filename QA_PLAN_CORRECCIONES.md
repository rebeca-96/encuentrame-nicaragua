# PLAN PRIORIZADO DE CORRECCIONES TÉCNICAS — ARCHITECT & LEAD QA
## PROYECTO: ENCUÉNTRAME NICARAGUA

**Fecha de Formulación:** 18 de Noviembre de 2026  
**Regla de Ejecución:** Este plan establece las intervenciones técnicas ordenadas por impacto y severidad. **No se aplicará ninguna modificación sobre el código fuente hasta contar con la autorización explícita del usuario.**

---

## 1. ORDEN DE ATENCIÓN PRIORIZADO

### FASE 1: VULNERABILIDADES CRÍTICAS Y CONFIGURACIONES DE SEGURIDAD (P0)

#### Corrección 1.1: Blindaje contra Path Traversal en Descarga de Fotografías
- **Archivo afectado:** [backend/app/api/v1/reports.py:412](file:///c:/Users/User/Documents/Valor%20IA/EncuentrameNicaragua/backend/app/api/v1/reports.py#L412) y [backend/app/services/storage_service.py:84](file:///c:/Users/User/Documents/Valor%20IA/EncuentrameNicaragua/backend/app/services/storage_service.py#L84).
- **Acción:**
  - Validar mediante expresión regular estricta que `storage_key` corresponda únicamente al patrón `^[a-f0-9]{32}\.webp$`.
  - Asegurar que la ruta canónica absoluta pertenezca al directorio `settings.STORAGE_DIR` mediante `os.path.commonpath`.
- **Complejidad:** Baja (1 hora).
- **Impacto:** Crítico (Previene fuga de archivos del servidor).
- **Riesgo de Regresión:** Mínimo.
- **Pruebas necesarias:** Test unitario pasando cadenas con `../`, `%2e%2e/` y nombres válidos.
- **Estrategia de reversión:** Restauración de la versión previa de `reports.py`.

#### Corrección 1.2: Enmascaramiento de Trazas en Manejador Global de Error 500
- **Archivo afectado:** [backend/app/main.py:59](file:///c:/Users/User/Documents/Valor%20IA/EncuentrameNicaragua/backend/app/main.py#L59-L63).
- **Acción:**
  - Sustituir `"detail": f"Error interno en el servidor: {str(exc)}"` por `"detail": "Ha ocurrido un error interno en el servidor. El incidente ha sido registrado para diagnóstico."`.
  - Mantener el detalle de la excepción `{str(exc)}` y `exc_info=True` únicamente en `logger.error()`.
- **Complejidad:** Baja (30 minutos).
- **Impacto:** Crítico (Cumplimiento OWASP A05 - Information Disclosure).
- **Riesgo de Regresión:** Nulo.
- **Pruebas necesarias:** Test provocando una excepción artificial y validando que el JSON de respuesta no contenga información del sistema.
- **Estrategia de reversión:** Git revert sobre `main.py`.

#### Corrección 1.3: Validación Estricta de `SECRET_KEY` en Modo Producción
- **Archivo afectado:** [backend/app/core/config.py:15](file:///c:/Users/User/Documents/Valor%20IA/EncuentrameNicaragua/backend/app/core/config.py#L15).
- **Acción:**
  - Agregar un validador en la clase `Settings` que arroje una excepción fatal si `ENVIRONMENT == "production"` y `SECRET_KEY` contiene el valor por defecto de desarrollo.
- **Complejidad:** Baja (30 minutos).
- **Impacto:** Alto (Evita falsificación de tokens en entornos desplegados).
- **Riesgo de Regresión:** Nulo.
- **Pruebas necesarias:** Test de inicio de configuración con `ENVIRONMENT=production`.
- **Estrategia de reversión:** Revertir `config.py`.

---

### FASE 2: AUTENTICACIÓN, PERMISOS Y CONTROL DE ABUSO (P1)

#### Corrección 2.1: Implementación de Rate Limiting en Registro de Cuentas
- **Archivo afectado:** [backend/app/api/v1/auth.py:52](file:///c:/Users/User/Documents/Valor%20IA/EncuentrameNicaragua/backend/app/api/v1/auth.py#L52) y [backend/app/core/rate_limit.py](file:///c:/Users/User/Documents/Valor%20IA/EncuentrameNicaragua/backend/app/core/rate_limit.py).
- **Acción:**
  - Crear función de dependencia `rate_limit_register` (máximo 3 registros por IP cada 10 minutos).
  - Inyectar la dependencia en `POST /auth/register`.
- **Complejidad:** Baja (45 minutos).
- **Impacto:** Alto (Protección contra bots y spam de cuentas).
- **Riesgo de Regresión:** Mínimo.
- **Pruebas necesarias:** Test automatizado con 4 peticiones seguidas esperando HTTP 429.
- **Estrategia de reversión:** Eliminar dependencia del router `auth.py`.

#### Corrección 2.2: Reducción de Expiración de Token y Mecanismo de Revocación
- **Archivo afectado:** [backend/app/core/config.py:17](file:///c:/Users/User/Documents/Valor%20IA/EncuentrameNicaragua/backend/app/core/config.py#L17) y [backend/app/api/v1/auth.py:97](file:///c:/Users/User/Documents/Valor%20IA/EncuentrameNicaragua/backend/app/api/v1/auth.py#L97).
- **Acción:**
  - Configurar tiempo de vida del access token a 120 minutos (2 horas) en lugar de 24 horas continuas.
  - Implementar set en memoria de tokens invalidados en logout para sesiones activas.
- **Complejidad:** Media (2 horas).
- **Impacto:** Alto (Reduce ventana de riesgo ante tokens sustraídos).
- **Riesgo de Regresión:** Bajo.
- **Pruebas necesarias:** Test de uso de token posterior a llamada a `/auth/logout`.
- **Estrategia de reversión:** Revertir configuración a tokens estándar.

---

### FASE 3: VALIDACIONES DE CLIENTE Y EXPERIENCIA DE FORMULARIOS (P2)

#### Corrección 3.1: Validación Temprana en Stepper de Registro de Reportes
- **Archivo afectado:** [frontend/src/app/reportar/page.tsx:568](file:///c:/Users/User/Documents/Valor%20IA/EncuentrameNicaragua/frontend/src/app/reportar/page.tsx#L568-L585).
- **Acción:**
  - En Paso 1: validar que `age` esté entre 0 y 120 años.
  - En Paso 2: validar que `disappearanceDate` no sea una fecha futura y que `circumstances` tenga al menos 15 caracteres.
  - En Paso 3: validar que `physicalDesc` tenga al menos 10 caracteres y `clothingDesc` al menos 5 caracteres.
  - Mostrar mensajes de advertencia específicos antes de permitir pulsar "Siguiente Paso".
- **Complejidad:** Baja (1 hora).
- **Impacto:** Medio-Alto (Evita que el usuario llene los 4 pasos y reciba un error al final).
- **Riesgo de Regresión:** Nulo.
- **Pruebas necesarias:** Navegación por el formulario con datos inválidos verificando el bloqueo temprano.
- **Estrategia de reversión:** Revertir handler `onClick` en `reportar/page.tsx`.

#### Corrección 3.2: Creación de Helper Tipado para Subida de Fotos
- **Archivo afectado:** [frontend/src/lib/api.ts](file:///c:/Users/User/Documents/Valor%20IA/EncuentrameNicaragua/frontend/src/lib/api.ts) y [frontend/src/app/reportar/page.tsx:135](file:///c:/Users/User/Documents/Valor%20IA/EncuentrameNicaragua/frontend/src/app/reportar/page.tsx#L135-L145).
- **Acción:**
  - Exportar `uploadReportPhoto(reportId: string, file: File, token: string)` en `src/lib/api.ts`.
  - Capturar errores de tipo de archivo o tamaño en `reportar/page.tsx` para informar al usuario si la foto falló pero el reporte fue creado.
- **Complejidad:** Baja (1 hora).
- **Impacto:** Medio (Consistencia en la capa de red del frontend).
- **Riesgo de Regresión:** Nulo.
- **Pruebas necesarias:** Prueba de subida de imagen en formato JPEG, PNG y prueba de subida de archivo corrupto.
- **Estrategia de reversión:** Revertir cambios en `api.ts` y `reportar/page.tsx`.

---

### FASE 4: FUNCIONALIDADES INCOMPLETAS Y DERECHO AL OLVIDO (P2)

#### Corrección 4.1: Endpoint de Suscripción a Notificaciones y Alertas
- **Archivo afectado:** [backend/app/api/v1/notifications.py](file:///c:/Users/User/Documents/Valor%20IA/EncuentrameNicaragua/backend/app/api/v1/notifications.py) y [backend/app/schemas/schemas.py](file:///c:/Users/User/Documents/Valor%20IA/EncuentrameNicaragua/backend/app/schemas/schemas.py).
- **Acción:**
  - Crear schema `NotificationSubscribeRequest` (correo electrónico, departamento opcional).
  - Implementar endpoint `POST /api/v1/notifications/subscribe` generando token criptográfico de desuscripción.
- **Complejidad:** Media (1.5 horas).
- **Impacto:** Medio (Completa el módulo de difusión ciudadana).
- **Riesgo de Regresión:** Nulo.
- **Pruebas necesarias:** Test unitario de suscripción y posterior desuscripción mediante token.
- **Estrategia de reversión:** Deshabilitar la ruta `POST` en `notifications.py`.

#### Corrección 4.2: Endpoints para Trámite de Supresión de Datos (Ley N.° 787)
- **Archivo afectado:** [backend/app/api/v1/reports.py](file:///c:/Users/User/Documents/Valor%20IA/EncuentrameNicaragua/backend/app/api/v1/reports.py) y [backend/app/api/v1/admin.py](file:///c:/Users/User/Documents/Valor%20IA/EncuentrameNicaragua/backend/app/api/v1/admin.py).
- **Acción:**
  - Implementar `POST /api/v1/reports/{report_id}/request-deletion` para que el reportante pueda solicitar la supresión de datos conforme al marco legal.
  - Implementar `GET /api/v1/admin/deletion-requests` y `PATCH /api/v1/admin/deletion-requests/{id}` para el procesamiento de solicitudes por parte de moderación.
- **Complejidad:** Media-Alta (2.5 horas).
- **Impacto:** Alto (Garantía de cumplimiento legal de la Ley N.° 787 de Nicaragua).
- **Riesgo de Regresión:** Bajo.
- **Pruebas necesarias:** Test de creación de solicitud de borrado y resolución administrativa.
- **Estrategia de reversión:** Retirar controladores en `reports.py` y `admin.py`.

---

### FASE 5: ACCESIBILIDAD, LINTING Y CALIDAD DE CÓDIGO (P3)

#### Corrección 5.1: Migración de Etiquetas `<img>` a `<Image />` de Next.js
- **Archivos afectados:** `ReportCard.tsx`, `casos/[id]/page.tsx`, `reportar/page.tsx`.
- **Acción:** Reemplazar etiquetas `<img>` directas por `<Image />` con dimensiones explícitas, `alt` descriptivo y soporte de optimización.
- **Complejidad:** Baja (1 hora).
- **Impacto:** Mejora de rendimiento LCP y eliminación de advertencias en `npm run build`.

#### Corrección 5.2: Atributos Semánticos de Accesibilidad (`htmlFor` y `id`)
- **Archivos afectados:** `login/page.tsx`, `reportar/page.tsx`, `pistas/page.tsx`.
- **Acción:** Enlazar todos los `<label htmlFor="id_campo">` con sus correspondientes `<input id="id_campo">`.
- **Complejidad:** Baja (1 hora).
- **Impacto:** Cumplimiento de pautas WCAG 2.1 AA para lectores de pantalla de personas con discapacidad visual.

---

## 2. MATRIZ DE RIESGO DE REGRESIÓN Y ESTIMACIÓN DE TIEMPO

| Fase | Tareas | Tiempo Estimado | Riesgo de Regresión | Pruebas de Regresión Obligatorias |
| :---: | :--- | :---: | :---: | :--- |
| **Fase 1** | Path Traversal, Manejador 500, SECRET_KEY | 2.0 horas | Muy Bajo | Pytest suites 1, 2 y 3 completas |
| **Fase 2** | Rate limiting registro, revocación JWT | 2.5 horas | Bajo | Tests de autenticación y carga de login |
| **Fase 3** | Validaciones tempranas UI, helper de fotos | 2.0 horas | Muy Bajo | Pruebas de navegación en formulario y subida de foto |
| **Fase 4** | Suscripciones alertas, Derecho al olvido | 4.0 horas | Bajo | Pruebas de creación de registros y flujo de aprobación |
| **Fase 5** | Accesibilidad A11y, Next Image, Linting | 2.0 horas | Nulo | `npm run lint` y `npm run build` |
| **TOTAL** | **11 Intervenciones Planificadas** | **12.5 horas** | **Controlado** | **Regresión 100% automatizada** |

> [!IMPORTANT]
> **COMPROMISO DE SEGURIDAD Y CONTROL:** Ningún archivo de código ha sido modificado durante la elaboración de este plan. Todas las intervenciones esperan la confirmación del usuario para proceder de manera incremental y controlada.
