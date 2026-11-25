# DIAGNÓSTICO DE RUTAS Y ENRUTAMIENTO FASTAPI + NEXT.JS
## Proyecto: Encuéntrame Nicaragua
**Fecha de Auditoría:** 20 de Noviembre de 2026  
**Auditor:** Ingeniero Full Stack Senior & Arquitecto de Software  
**Ambiente Evaluado:** Producción (`https://creacionvaloria.tradescanner.online`) y Local (`http://127.0.0.1:8000`)

---

## 1. RESUMEN EJECUTIVO

Al navegar en el sitio web publicado en el entorno de producción (`https://creacionvaloria.tradescanner.online/`), los usuarios experimentaban un fallo crítico al hacer clic en los enlaces del menú principal o al recargar la página:

```json
{
  "detail": "Not Found"
}
```

El presente informe detalla la auditoría profunda de enrutamiento HTTP, la inspección de routers y endpoints de FastAPI, el comportamiento del servidor ASGI frente a Next.js Static Site Generation (SSG), la discrepancia entre el entorno local y el entorno de hosting remoto, y la identificación exacta de la causa raíz.

---

## 2. ANÁLISIS DE ENTORNO Y ARQUITECTURA DE SERVIDORES

### 2.1. Entorno de Hosting Remoto (`creacionvaloria.tradescanner.online`)
A través de inspección de cabeceras HTTP y endpoints OpenAPI (`/openapi.json`), se determinó la composición del servidor de producción:
- **Servidor Web / CDN Reverso:** Cloudflare (Edge Caching, TLS Termination).
- **Servidor de Aplicaciones ASGI:** FastAPI / Starlette (Identificado internamente como microservicio de almacenamiento y despacho de assets estáticos).
- **Endpoints de API registrados en OpenAPI remoto:**
  * `GET /api/images/{folder}`
  * `GET /api/static/files`
  * `GET /api/static/content`
  * `PUT /api/static/file`
  * `POST /api/static/folder`
  * `POST /api/static/move`
  * `DELETE /api/static/item`
  * `GET /salud` -> `{"estado":"floreciendo"}`
- **Despacho estático en raíz:**
  El servidor remoto expone el contenido estático montando el directorio directamente.

### 2.2. Entorno Local (`backend/app/main.py` y `main.py`)
- FastAPI 0.110+ con routers completos de dominio:
  * `/api/v1/auth`
  * `/api/v1/reports`
  * `/api/v1/search`
  * `/api/v1/locations`
  * `/api/v1/tips`
  * `/api/v1/admin`
  * `/api/v1/ai-assistance`
  * `/api/v1/statistics`
  * `/api/v1/notifications`
- Middleware de enrutamiento estático montando `frontend/out` mediante `StaticFiles` y un catch-all route `/{full_path:path}`.

---

## 3. AUDITORÍA DE RESPUESTAS HTTP Y EVIDENCIAS DE ERROR

Se ejecutaron pruebas automatizadas con peticiones HTTP dirigidas a los distintos patrones de URL en producción:

| Ruta Solicitada | Método | Código HTTP | Content-Type | Respuesta Obtenida | Diagnóstico |
|---|---|---|---|---|---|
| `https://creacionvaloria.tradescanner.online/` | GET | `200 OK` | `text/html; charset=utf-8` | HTML de `index.html` | Correcto |
| `https://creacionvaloria.tradescanner.online/casos.html` | GET | `200 OK` | `text/html; charset=utf-8` | HTML completo de casos | Archivo físico existe |
| `https://creacionvaloria.tradescanner.online/casos` | GET | `404 Not Found` | `application/json` | `{"detail":"Not Found"}` | **Fallo Crítico** |
| `https://creacionvaloria.tradescanner.online/casos/` | GET | `404 Not Found` | `application/json` | `{"detail":"Not Found"}` | **Fallo Crítico** |
| `https://creacionvaloria.tradescanner.online/mapa.html` | GET | `200 OK` | `text/html; charset=utf-8` | HTML completo del mapa | Archivo físico existe |
| `https://creacionvaloria.tradescanner.online/mapa` | GET | `404 Not Found` | `application/json` | `{"detail":"Not Found"}` | **Fallo Crítico** |
| `https://creacionvaloria.tradescanner.online/reportar.html` | GET | `200 OK` | `text/html; charset=utf-8` | HTML reporte de caso | Archivo físico existe |
| `https://creacionvaloria.tradescanner.online/reportar` | GET | `404 Not Found` | `application/json` | `{"detail":"Not Found"}` | **Fallo Crítico** |
| `https://creacionvaloria.tradescanner.online/login.html` | GET | `200 OK` | `text/html; charset=utf-8` | HTML inicio sesión | Archivo físico existe |
| `https://creacionvaloria.tradescanner.online/login` | GET | `404 Not Found` | `application/json` | `{"detail":"Not Found"}` | **Fallo Crítico** |
| `https://creacionvaloria.tradescanner.online/pistas.html` | GET | `200 OK` | `text/html; charset=utf-8` | HTML aportar pistas | Archivo físico existe |
| `https://creacionvaloria.tradescanner.online/pistas` | GET | `404 Not Found` | `application/json` | `{"detail":"Not Found"}` | **Fallo Crítico** |

---

## 4. CAUSA RAÍZ TÉCNICA

La causa del error radica en la conjunción de tres factores fundamentales de arquitectura:

### Factor 1: Configuración de Exportación SSG de Next.js
En `frontend/next.config.js`:
```javascript
const nextConfig = {
  output: "export",
  reactStrictMode: true,
  images: { unoptimized: true }
};
```
Por defecto, al no definir `trailingSlash: true`, Next.js compila las páginas estáticas generando archivos HTML individuales con el nombre de la ruta:
* `out/casos.html`
* `out/mapa.html`
* `out/reportar.html`
* `out/login.html`
* `out/pistas.html`

Sin embargo, los componentes de navegación en React (`<Link href="/casos">`, `<Link href="/mapa">`, etc.) generaban enlaces ancla `<a href="/casos">`.

### Factor 2: Comportamiento del Router de FastAPI en Producción
En un servidor Starlette/FastAPI estándar o montado sin middleware de reescritura de URLs limpias (clean URLs):
1. Cuando el cliente hace una petición HTTP GET a `/casos`, FastAPI recorre la tabla de rutas.
2. Como no existe ninguna función `@app.get("/casos")` ni ningún archivo con nombre exacto `casos` en el directorio estático (ya que en disco el archivo se llama `casos.html`), Starlette no puede resolver la ruta.
3. El manejador de excepciones por defecto de FastAPI (`HTTPException(status_code=404)`) se activa y genera la respuesta JSON predeterminada:
   ```json
   {
     "detail": "Not Found"
   }
   ```

### Factor 3: Comportamiento del Navegador y Re-hidratación de React
Cuando un usuario interactúa con la aplicación:
1. Al cargar la raíz `https://creacionvaloria.tradescanner.online/`, el navegador descarga `index.html` y los paquetes JS de Next.js.
2. Si el usuario hace clic en el enlace del menú antes de que React culmine la hidratación, o si el usuario hace clic secundario ("Abrir enlace en pestaña nueva"), o si presiona recargar (F5) mientras se encuentra en `/casos`:
3. El navegador emite una petición HTTP directa al servidor web solicitando el recurso `/casos`.
4. El servidor FastAPI remoto responde con `404 Not Found` en formato JSON en lugar de servir el documento HTML correspondiente.

---

## 5. COMPARACIÓN: LOCAL VS PRODUCCIÓN

| Aspecto | Servidor Local (`main.py`) | Servidor Remoto Producción |
|---|---|---|
| Catch-All Route | Implementado (`@app.get("/{full_path:path}")`) | Ausente / No reescribe extensionless a `.html` |
| Resolución `/casos` | Verifica `casos.html` y retorna `FileResponse` (200 OK) | Busca archivo exacto `casos` -> Falla -> Retorna JSON 404 |
| Resolución `/casos/` | Soporta trailing slash limpiando barra final | Retorna 404 |
| Manejo 404 estático | Retorna `404.html` con status 404 | Retorna JSON `{"detail":"Not Found"}` |

---

## 6. ESTRATEGIA DE SOLUCIÓN INTEGRAL

Para solventar este problema de raíz tanto en el hosting de producción como en el servidor backend local, se establecieron dos líneas de acción complementarias:

1. **Alineación de Enlaces en el Frontend Next.js:**
   Configurar los componentes de navegación (`Navbar.tsx`, `Footer.tsx`, `page.tsx`, etc.) para utilizar enlaces con extensión explícita `.html` (`/casos.html`, `/mapa.html`, etc.) y generar réplicas de carpetas con `index.html` (`casos/index.html`, `mapa/index.html`). Esto garantiza que **cualquier servidor estático o CDN** sirva la página con código `200 OK` y cabecera `Content-Type: text/html` sin requerir reescrituras complejas.

2. **Perfeccionamiento del Router FastAPI (`main.py` y `backend/app/main.py`):**
   Implementar un algoritmo de resolución en cascada en el manejador catch-all que:
   - Excluya rigurosamente prefijos técnicos (`api/`, `docs`, `redoc`, `openapi.json`).
   - Normalice la ruta eliminando barras inclinadas finales (`clean_path = full_path.strip("/")`).
   - Busque coincidencias directas en disco (`clean_path`).
   - Busque coincidencias con extensión HTML (`f"{clean_path}.html"`).
   - Busque archivos de índice de directorio (`f"{clean_path}/index.html"`).
   - Resuelva dinámicamente fichas de personas (`casos/{id}.html` o `casos/placeholder.html`).
   - Responda con `404.html` respetando el código de estado HTTP 404 cuando la página realmente no exista.
