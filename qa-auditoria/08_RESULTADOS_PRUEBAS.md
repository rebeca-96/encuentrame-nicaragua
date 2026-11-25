# 08 — RESULTADOS CONSOLIDADOS DE EJECUCIÓN DE PRUEBAS
## Proyecto: ENCUÉNTRAME NICARAGUA
### Registro de Ejecución de Casos de Prueba Automatizados y Exploratorios
**Auditor:** Senior QA Engineer & SDET  
**Fecha:** 19 de Noviembre de 2026  
**Total Casos Ejecutados:** 18  
**Aprobados (PASS):** 16 | **Fallidos (FAIL):** 2 | **Bloqueados (BLOCKED):** 0  

---

## 1. TABLA RESUMEN DE EJECUCIÓN

| ID de Prueba | Módulo | Nombre del Caso de Prueba | Resultado | Severidad | Código Esperado | Código Obtenido |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **TC-AUTH-01** | Autenticación | Login exitoso de Administrador con credenciales válidas | **PASS** | — | HTTP 200 con JWT | HTTP 200 |
| **TC-AUTH-02** | Autenticación | Rechazo de credenciales incorrectas en login | **PASS** | — | HTTP 400/401 | HTTP 401 |
| **TC-AUTH-03** | Autenticación | Revocación de JWT en cierre de sesión (Logout Blacklist) | **PASS** | — | HTTP 401 con token revocado | HTTP 401 |
| **TC-AUTH-04** | Seguridad | Protección contra fuerza bruta en login (Rate Limiting) | **PASS** | — | HTTP 429 Too Many Requests | HTTP 429 |
| **TC-RBAC-01** | Autorización | Aislamiento de rol 'reporter' ante panel admin de reportes | **PASS** | — | HTTP 401/403 Prohibido | HTTP 403 |
| **TC-REP-01** | Reportes | Creación correcta en estado `pending_review` y oculto al público | **PASS** | — | HTTP 201 Created | HTTP 201 |
| **TC-REP-02** | Validaciones | Rechazo estricto de fecha de desaparición futura | **PASS** | — | HTTP 400/422 | HTTP 422 |
| **TC-REP-03** | Validaciones | Rechazo de municipio que no pertenece al departamento | **PASS** | — | HTTP 400/422 | HTTP 422 |
| **TC-REP-04** | Privacidad | Rechazo de reporte sin consentimiento legal expreso (Ley 787) | **PASS** | — | HTTP 400/422 | HTTP 422 |
| **TC-REP-05** | Seguridad | Bloqueo de archivos ejecutables / scripts en carga de fotos | **PASS** | — | HTTP 400 Bad Request | HTTP 400 |
| **TC-GEO-01** | Geografía | Presencia exacta de 17 entidades territoriales de Nicaragua | **PASS** | — | 17 departamentos/regiones | 17 entidades |
| **TC-GEO-02** | Geografía | Presencia exacta de 153 municipios oficiales de Nicaragua | **PASS** | — | 153 municipios oficiales | 153 municipios |
| **TC-GEO-03** | Mapas | Mapa utiliza coordenadas aproximadas agregadas sin filtrar domicilios | **PASS** | — | Coordenadas agregadas | Agregadas |
| **TC-TIP-01** | Pistas | Recepción segura de pista y generación de código de seguimiento anónimo | **PASS** | — | HTTP 201 con código anónimo | HTTP 201 |
| **TC-TIP-02** | Pistas | Consulta ciudadana de estado mediante código anónimo | **PASS** | — | HTTP 200 con estado de pista | HTTP 200 |
| **TC-LEY787-01**| Privacidad | Solicitud formal de cancelación / supresión de expediente por titular | **PASS** | — | HTTP 201 Solicitud creada | HTTP 201 |
| **TC-ENV-01** | Infraestructura | Rutas limpias de Next.js responden sin sufijo `.html` en hosting estático | **FAIL** | **P1** | HTTP 200 / SPA Index | HTTP 404 Not Found |
| **TC-ENV-02** | Infraestructura | API de Backend conectada y respondiendo en el hosting público | **FAIL** | **P0** | HTTP 200 en `/api/v1/health` | HTTP 404 Not Found |

---

## 2. DETALLE DE CASOS FALLIDOS

### TC-ENV-01: Rutas limpias de Next.js devuelven 404 en hosting estático
- **Condición de Entrada:** Solicitud GET HTTP directa a `https://creacionvaloria.tradescanner.online/casos`.
- **Resultado Esperado:** Servir el documento HTML de casos o redirigir internamente al layout SPA.
- **Resultado Obtenido:** `HTTP 404 Not Found`. El servidor web busca una carpeta `/casos/` o archivo físico sin extensión que no existe.
- **Acción Requerida:** Configurar `trailingSlash: true` en `next.config.ts` o agregar reglas de reescritura en Nginx / Caddy.

### TC-ENV-02: API de Backend no está conectada o proxied en Hosting Público
- **Condición de Entrada:** Solicitud GET HTTP a `https://creacionvaloria.tradescanner.online/api/v1/health`.
- **Resultado Esperado:** Respuesta JSON `{"status": "healthy", "service": "encuentrame_nicaragua"}` con código HTTP 200.
- **Resultado Obtenido:** `HTTP 404 Not Found`. El servidor web maneja el dominio como un directorio de archivos estáticos puros (`/static`), sin un bloque `proxy_pass` hacia el puerto `8000` donde corre Uvicorn.
- **Acción Requerida:** Configurar proxy reverso en el servidor web o desplegar el contenedor backend con un punto de enlace HTTPS público.
