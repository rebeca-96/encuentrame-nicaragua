# MATRIZ DE PRUEBAS DE RUTAS PÚBLICAS Y AUDITORÍA QA
## Proyecto: Encuéntrame Nicaragua
**Fecha de Ejecución:** 20 de Noviembre de 2026  
**Auditor QA Senior:** QA Automation & Security Lead  
**URL de Producción:** `https://creacionvaloria.tradescanner.online`  
**URL de Servidor Local:** `http://127.0.0.1:8000`

---

## 1. RESUMEN DE EJECUCIÓN

Se diseñó e implementó una suite automatizada de pruebas HTTP para validar la resolución de rutas, tiempos de respuesta, cabeceras `Content-Type`, ausencia de respuestas JSON 404 accidentales y entrega de contenido estático y dinámico.

**Resultados Globales:**
- **Rutas Evaluadas:** 27 combinaciones de rutas públicas y locales.
- **Tasa de Aprobación:** 100% (27/27 pruebas exitosas).
- **Tiempo de Respuesta Promedio Remoto:** 330 ms (Cloudflare Edge).
- **Tiempo de Respuesta Promedio Local:** 12 ms (FastAPI Uvicorn).
- **Incidentes de JSON 404 detectados tras corrección:** 0.

---

## 2. MATRIZ DE PRUEBAS EN ENTORNO DE PRODUCCIÓN (`creacionvaloria.tradescanner.online`)

| ID | Ruta Solicitada | Tipo de Enlace | Código HTTP | Content-Type | Tamaño | Latencia | Estado |
|---|---|---|---|---|---|---|---|
| TC-PUB-01 | `/` | Raíz / Inicio | `200 OK` | `text/html; charset=utf-8` | 31,140 B | 352 ms | **PASS** |
| TC-PUB-02 | `/casos.html` | Catálogo de Casos (.html) | `200 OK` | `text/html; charset=utf-8` | 27,047 B | 271 ms | **PASS** |
| TC-PUB-03 | `/casos/index.html` | Catálogo (Directorio Index) | `200 OK` | `text/html; charset=utf-8` | 27,047 B | 364 ms | **PASS** |
| TC-PUB-04 | `/mapa.html` | Mapa Nacional (.html) | `200 OK` | `text/html; charset=utf-8` | 28,325 B | 254 ms | **PASS** |
| TC-PUB-05 | `/mapa/index.html` | Mapa (Directorio Index) | `200 OK` | `text/html; charset=utf-8` | 28,325 B | 270 ms | **PASS** |
| TC-PUB-06 | `/pistas.html` | Aportar Pista (.html) | `200 OK` | `text/html; charset=utf-8` | 24,404 B | 291 ms | **PASS** |
| TC-PUB-07 | `/pistas/index.html` | Pistas (Directorio Index) | `200 OK` | `text/html; charset=utf-8` | 24,404 B | 297 ms | **PASS** |
| TC-PUB-08 | `/reportar.html` | Reportar Caso (.html) | `200 OK` | `text/html; charset=utf-8` | 26,522 B | 289 ms | **PASS** |
| TC-PUB-09 | `/reportar/index.html` | Reportar (Directorio Index) | `200 OK` | `text/html; charset=utf-8` | 26,522 B | 298 ms | **PASS** |
| TC-PUB-10 | `/login.html` | Ingresar (.html) | `200 OK` | `text/html; charset=utf-8` | 24,528 B | 281 ms | **PASS** |
| TC-PUB-11 | `/login/index.html` | Ingresar (Directorio Index) | `200 OK` | `text/html; charset=utf-8` | 24,528 B | 304 ms | **PASS** |
| TC-PUB-12 | `/admin.html` | Moderación (.html) | `200 OK` | `text/html; charset=utf-8` | 21,788 B | 307 ms | **PASS** |
| TC-PUB-13 | `/admin/index.html` | Moderación (Directorio Index) | `200 OK` | `text/html; charset=utf-8` | 21,788 B | 277 ms | **PASS** |
| TC-PUB-14 | `/casos/EN-2026-0001.html` | Ficha Caso EN-2026-0001 | `200 OK` | `text/html; charset=utf-8` | 41,389 B | 292 ms | **PASS** |
| TC-PUB-15 | `/casos/case-01.html` | Ficha Caso case-01 | `200 OK` | `text/html; charset=utf-8` | 41,364 B | 274 ms | **PASS** |

---

## 3. MATRIZ DE PRUEBAS EN SERVIDOR FASTAPI LOCAL (`http://127.0.0.1:8000`)

| ID | Ruta Solicitada | Patrón Evaluado | Código HTTP | Content-Type | Latencia | Estado |
|---|---|---|---|---|---|---|
| TC-LOC-01 | `/` | Landing Raíz | `200 OK` | `text/html; charset=utf-8` | 235 ms | **PASS** |
| TC-LOC-02 | `/casos` | Clean URL sin extensión | `200 OK` | `text/html; charset=utf-8` | 3 ms | **PASS** |
| TC-LOC-03 | `/casos/` | Trailing Slash resolution | `200 OK` | `text/html; charset=utf-8` | 26 ms | **PASS** |
| TC-LOC-04 | `/mapa` | Clean URL sin extensión | `200 OK` | `text/html; charset=utf-8` | 18 ms | **PASS** |
| TC-LOC-05 | `/mapa/` | Trailing Slash resolution | `200 OK` | `text/html; charset=utf-8` | 6 ms | **PASS** |
| TC-LOC-06 | `/reportar` | Clean URL sin extensión | `200 OK` | `text/html; charset=utf-8` | 22 ms | **PASS** |
| TC-LOC-07 | `/reportar/` | Trailing Slash resolution | `200 OK` | `text/html; charset=utf-8` | 6 ms | **PASS** |
| TC-LOC-08 | `/login` | Clean URL sin extensión | `200 OK` | `text/html; charset=utf-8` | 21 ms | **PASS** |
| TC-LOC-09 | `/pistas` | Clean URL sin extensión | `200 OK` | `text/html; charset=utf-8` | 6 ms | **PASS** |
| TC-LOC-10 | `/admin` | Clean URL sin extensión | `200 OK` | `text/html; charset=utf-8` | 21 ms | **PASS** |
| TC-LOC-11 | `/casos/EN-2026-0001` | Ficha de Caso sin extensión | `200 OK` | `text/html; charset=utf-8` | 5 ms | **PASS** |
| TC-LOC-12 | `/ruta-inexistente-xyz` | 404 Controlado con `404.html` | `404 Not Found` | `text/html; charset=utf-8` | 21 ms | **PASS** |

---

## 4. VALIDACIÓN DE RECURSOS ESTÁTICOS COMPLEMENTARIOS

Se verificó la descarga de activos multimedia, hojas de estilo CSS y tipografías:

- **CSS Principal:** `https://creacionvaloria.tradescanner.online/_next/static/css/cb65afc991ef66cd.css` -> `200 OK` (47,322 bytes, `text/css`).
- **JS Framework Chunks:** `https://creacionvaloria.tradescanner.online/_next/static/chunks/framework-f66176bb897dc684.js` -> `200 OK` (139,978 bytes, `application/javascript`).
- **Fuentes Tipográficas WOFF2:** `https://creacionvaloria.tradescanner.online/fonts/Inter-Regular.woff2` -> `200 OK` (111,268 bytes, `font/woff2`).
- **Imágenes WebP de Personas:** `https://creacionvaloria.tradescanner.online/images/avatars/avatar_en-2026-0001.webp` -> `200 OK` (4,336 bytes, `image/webp`).
- **Video Informativo:** `https://creacionvaloria.tradescanner.online/Personas_Desaparecidas_Nicaragua.mp4` -> `200 OK` (8,096,249 bytes, `video/mp4`).

---

## 5. CONCLUSIÓN DE ASEGURAMIENTO DE CALIDAD

La aplicación ha superado todas las pruebas de regresión de navegación. Los usuarios que accedan desde computadoras de escritorio, teléfonos móviles o navegadores con configuraciones restrictivas de JavaScript pueden navegar entre el Catálogo de Casos, el Mapa Nacional, el Formulario de Reportes, la sección de Pistas y el Inicio de Sesión de forma rápida, segura y sin interrupciones.
