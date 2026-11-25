# 09 — REGISTRO DE EVIDENCIAS TÉCNICAS Y PRUEBAS DE CONCEPTO (PoC)
## Proyecto: ENCUÉNTRAME NICARAGUA
### Comandos de Reproducción, Respuestas HTTP y Trazas Técnicas
**Auditor:** Senior QA Engineer & SDET  
**Fecha:** 19 de Noviembre de 2026  

---

## 1. EVIDENCIA DE DEFECTO P0: API DESCONECTADA EN HOSTING PÚBLICO (DEF-01)

### Comando cURL de Reproducción:
```bash
curl -i -X GET "https://creacionvaloria.tradescanner.online/api/v1/health"
```

### Respuesta Obtenida del Servidor:
```http
HTTP/1.1 404 Not Found
Server: nginx/1.24.0 (Ubuntu)
Date: Thu, 19 Nov 2026 19:35:00 GMT
Content-Type: text/html
Content-Length: 162
Connection: keep-alive

<html>
<head><title>404 Not Found</title></head>
<body>
<center><h1>404 Not Found</h1></center>
<hr><center>nginx</center>
</body>
</html>
```

### Análisis del Tráfico de Red en el Navegador:
Al interactuar con el formulario de búsqueda de casos en la página pública, la consola del navegador emite:
```
TypeError: Failed to fetch at api.ts:42
[API Error] GET https://creacionvaloria.tradescanner.online/api/v1/reports/?limit=20 net::ERR_ABORTED 404 (Not Found)
```
**Causa:** El servidor web `creacionvaloria.tradescanner.online` sirve el frontend compilado como carpeta estática (`/static`), pero no cuenta con la directiva `proxy_pass` que reenvíe las rutas `/api/v1/` al proceso FastAPI (Uvicorn).

---

## 2. EVIDENCIA DE DEFECTO P1: RUTAS LIMPIAS DEVUELVEN 404 (DEF-02)

### Comandos de Reproducción:
```bash
# 1. Petición directa a ruta limpia (Falla con 404)
curl -s -o /dev/null -w "%{http_code}\n" https://creacionvaloria.tradescanner.online/casos
# Output: 404

# 2. Petición con sufijo de archivo HTML físico (Funciona con 200)
curl -s -o /dev/null -w "%{http_code}\n" https://creacionvaloria.tradescanner.online/casos.html
# Output: 200
```

### Impacto en el Usuario Final:
Si un familiar comparte en WhatsApp o Facebook el enlace de un caso (`https://creacionvaloria.tradescanner.online/casos`), cualquier persona que abra el enlace directamente desde su teléfono recibirá la pantalla negra genérica de `404 Not Found`.

---

## 3. EVIDENCIA DE DEFECTO P2: INCONSISTENCIA EN ENDPOINTS ADMIN (DEF-03)

### Petición a Endpoint Raíz de Reportes Admin:
```bash
curl -i -X GET "http://127.0.0.1:8000/api/v1/admin/reports" \
     -H "Authorization: Bearer <TOKEN_ADMIN_VALIDO>"
```

### Respuesta Obtenida:
```json
HTTP/1.1 404 Not Found
Content-Type: application/json

{
  "detail": "Not Found"
}
```

### Contraste con Endpoint Específico:
```bash
curl -i -X GET "http://127.0.0.1:8000/api/v1/admin/reports/pending" \
     -H "Authorization: Bearer <TOKEN_ADMIN_VALIDO>"
```
```json
HTTP/1.1 200 OK
Content-Type: application/json

[
  {
    "id": "924afbce-66c4-41a5-bfa6-ecf82dabe8d0",
    "case_number": "EN-2026-0021",
    "status": "pending_review",
    "first_name": "Carlos",
    "last_name": "García QA"
  }
]
```

---

## 4. EVIDENCIA DE VALIDACIONES ROBUSTAS CONFIRMADAS (PASS)

### 4.1 Rechazo Estricto de Fecha Futura (`TC-REP-02`)
**Payload Enviado:**
```json
{
  "first_name": "Carlos",
  "last_name": "García",
  "disappearance_date": "2026-11-30T01:37:20+00:00",
  "department": "Managua",
  "municipality": "Ciudad Sandino",
  "physical_description": "Altura 1.75m, contextura delgada.",
  "clothing_description": "Camisa azul oscuro, pantalón jeans.",
  "circumstances": "Visto saliendo de su domicilio.",
  "consent": {
    "relationship_to_victim": "Madre",
    "identity_doc_number": "001-010190-0000A",
    "accepted_terms": true
  }
}
```
**Respuesta HTTP:**
```json
HTTP/1.1 422 Unprocessable Entity

{
  "detail": [
    {
      "type": "value_error",
      "loc": ["body", "disappearance_date"],
      "msg": "Value error, La fecha de desaparición no puede ser una fecha en el futuro."
    }
  ]
}
```

### 4.2 Inconsistencia Territorial Departamento-Municipio (`TC-REP-03`)
**Payload con Municipio de otro Departamento:**
```json
{
  "department": "Managua",
  "municipality": "León"
}
```
**Respuesta HTTP:**
```json
HTTP/1.1 422 Unprocessable Entity

{
  "detail": [
    {
      "type": "value_error",
      "loc": ["body", "municipality"],
      "msg": "Value error, El municipio 'León' no pertenece al departamento 'Managua'."
    }
  ]
}
```

### 4.3 Protección contra Fuerza Bruta en Login (`TC-AUTH-04`)
**Respuesta al 6.° intento fallido consecutivo:**
```json
HTTP/1.1 429 Too Many Requests
Retry-After: 60

{
  "detail": "Límite de solicitudes excedido. Por favor intente de nuevo en 60 segundos."
}
```
