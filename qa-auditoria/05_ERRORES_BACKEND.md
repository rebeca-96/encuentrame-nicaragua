# 05 — AUDITORÍA DE ERRORES Y DEFECTOS DE BACKEND Y APIS
## Proyecto: ENCUÉNTRAME NICARAGUA
### Arquitectura FastAPI, Manejo de Excepciones, Seguridad de Endpoints y Robustez
**Auditor:** Senior QA Engineer & SDET  
**Fecha:** 19 de Noviembre de 2026  

---

## 1. EVALUACIÓN GENERAL DE LA CAPA BACKEND

El backend está desarrollado con **FastAPI** y **Pydantic v2**, estructurado modularmente con routers por contexto (`auth`, `reports`, `tips`, `locations`, `admin`, `notifications`, `search`).
La arquitectura general presenta un estándar elevado de diseño defensivo, pero se detectaron inconsistencias específicas de contratos de API y configuraciones de enrutamiento que deben corregirse.

---

## 2. HALLAZGOS Y ANÁLISIS DE ENDPOINTS

### 2.1 Inconsistencia en Endpoints Administrativos (DEF-03)
- **Ruta Faltante:** `GET /api/v1/admin/reports`
- **Comportamiento:** Actualmente, el router en `backend/app/api/v1/admin.py` define únicamente:
  - `GET /api/v1/admin/reports/pending` (expedientes pendientes de moderación).
  - `POST /api/v1/admin/reports/{id}/review` (aprobar/rechazar).
- **Problema:** Si el panel administrativo o un cliente frontend intenta consultar la lista completa de reportes (incluyendo `published`, `closed`, `rejected`), el endpoint raíz `GET /api/v1/admin/reports` responde con **HTTP 404 Not Found**.
- **Recomendación:** Agregar el endpoint canónico en `admin.py`:
  ```python
  @router.get("/reports", response_model=List[ReportSummaryAdmin])
  def get_all_reports_for_admin(
      status: Optional[ReportStatus] = None,
      skip: int = 0,
      limit: int = 50,
      db: Session = Depends(get_db),
      current_user: User = Depends(require_moderator_or_admin)
  ):
      query = db.query(MissingPersonReport)
      if status:
          query = query.filter(MissingPersonReport.status == status)
      return query.order_by(MissingPersonReport.created_at.desc()).offset(skip).limit(limit).all()
  ```

### 2.2 Protección contra Ataques de Denegación de Servicio (DoS) en Parámetros de Consulta (DEF-06)
- **Endpoint:** `GET /api/v1/reports/`
- **Comportamiento Actual:**
  El endpoint acepta `limit: int = 50` y `skip: int = 0`.
  Al ejecutar pruebas de límites enviando `limit=100000`, la API no genera error de validación `HTTP 422 Unprocessable Entity` porque el parámetro no cuenta con la restricción `le=100` en Pydantic / Query.
- **Riesgo:** Si un atacante envía solicitudes masivas con `limit=500000`, la base de datos y la memoria RAM del servidor de backend se verán sobrecargadas intentando serializar decenas de miles de objetos ORM.
- **Recomendación:**
  ```python
  limit: int = Query(default=50, ge=1, le=100, description="Máximo 100 registros por página")
  ```

### 2.3 Manejo de Excepciones y Fuga de Información Técnica
- **Prueba de Inyección y Payloads Malformados:**
  Se enviaron JSONs sintácticamente inválidos, campos de fecha corruptos y caracteres Unicode no imprimibles.
- **Resultado:**
  - FastAPI y Pydantic interceptan los errores de tipado y devuelven `HTTP 422 Unprocessable Entity` con un cuerpo JSON normalizado (`{"detail": [...]}`).
  - **No se revelaron trazas de pila (Stack Traces)** internas de Python en las respuestas HTTP a clientes públicos.
  - La excepción genérica `500 Internal Server Error` está blindada en `main.py` mediante un middleware de captura global que registra el error en los logs del servidor y devuelve un mensaje amigable y seguro:
    ```json
    {
      "detail": "Ha ocurrido un error interno en el servidor. El incidente ha sido registrado para revisión por el equipo técnico."
    }
    ```

---

## 3. AUDITORÍA DE CONTROL DE ACCESO (RBAC)

Se ejecutaron pruebas de matrices de permisos cruzados entre los cuatro roles del sistema:

| Operación / Endpoint | Rol Probado | Código HTTP Esperado | Código HTTP Obtenido | Veredicto |
| :--- | :--- | :--- | :--- | :--- |
| `GET /api/v1/admin/reports/pending` | Sin Token (Anónimo) | 401 Unauthorized | 401 Unauthorized | **PASS** |
| `GET /api/v1/admin/reports/pending` | Rol `citizen` | 403 Forbidden | 403 Forbidden | **PASS** |
| `GET /api/v1/admin/reports/pending` | Rol `reporter` | 403 Forbidden | 403 Forbidden | **PASS** |
| `GET /api/v1/admin/reports/pending` | Rol `moderator` | 200 OK | 200 OK | **PASS** |
| `GET /api/v1/admin/reports/pending` | Rol `admin` | 200 OK | 200 OK | **PASS** |
| `GET /api/v1/admin/audit-logs` | Rol `moderator` | 403 Forbidden | 403 Forbidden | **PASS** (Solo Admin) |
| `GET /api/v1/admin/audit-logs` | Rol `admin` | 200 OK | 200 OK | **PASS** |
| `POST /api/v1/reports/` | Rol `citizen` | 403 Forbidden | 403 Forbidden | **PASS** |
| `POST /api/v1/reports/` | Rol `reporter` | 201 Created | 201 Created | **PASS** |

**Conclusión RBAC:** El modelo de autorización está rigurosamente implementado mediante las dependencias `require_role`, `require_moderator_or_admin` y `get_current_user`.
