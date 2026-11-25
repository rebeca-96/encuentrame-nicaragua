# RESULTADOS DE PRUEBAS Y DIAGNÓSTICO EMPÍRICO
## Proyecto: ENCUÉNTRAME NICARAGUA

---

## 1. SUITE DE PRUEBAS AUTOMATIZADAS (BACKEND)

**Comando:** `pytest backend/tests/test_core_requirements.py -v`  
**Entorno:** Python 3.12.10, Pytest 9.2.0, SQLite en memoria aislada  
**Resultado:** **10/10 Pruebas Aprobadas (100%)**  
**Tiempo de Ejecución:** 2.07 segundos

| Test ID | Prueba Ejecutada | Objetivo | Resultado |
| :--- | :--- | :--- | :--- |
| **TEST-01** | `test_1_new_report_not_published_without_moderator_approval` | Comprobar que un nuevo reporte ingresa en `pending_review` y no es visible en catálogo público | **PASSED** |
| **TEST-02** | `test_2_citizen_cannot_access_confidential_tips` | Comprobar que ciudadanos o usuarios anónimos reciben 401/403 al intentar acceder a pistas | **PASSED** |
| **TEST-03** | `test_3_user_cannot_modify_or_close_others_reports` | Comprobar que un usuario no puede cerrar ni alterar reportes creados por otro usuario (403) | **PASSED** |
| **TEST-04** | `test_4_search_filters_return_correct_results` | Comprobar que los filtros departamentales devuelven resultados exactos y filtrados | **PASSED** |
| **TEST-05** | `test_5_geographic_data_does_not_reveal_sensitive_coordinates` | Comprobar que el endpoint del mapa no expone domicilios exactos ni teléfonos privados | **PASSED** |
| **TEST-06** | `test_6_administrative_actions_are_audit_logged` | Comprobar que la aprobación de reportes genera registros inmutables en `audit_logs` | **PASSED** |
| **TEST-07** | `test_7_case_closure_is_processable_and_depublishes_case` | Comprobar que el cierre de caso despublica inmediatamente el reporte del portal público | **PASSED** |
| **TEST-08** | `test_8_error_handling_for_invalid_input_and_missing_consent` | Comprobar rechazo con HTTP 400 ante omisión o rechazo de consentimiento informado | **PASSED** |
| **TEST-09** | `test_9_ai_acts_strictly_as_advisor_without_autonomous_state_changes` | Comprobar que el módulo de IA no modifica estados ni publica sin confirmación humana | **PASSED** |
| **TEST-10** | `test_10_secure_tip_submission_and_unpredictable_code` | Comprobar generación de código seguro `PISTA-XXXX-XXXX` y rastreo anónimo | **PASSED** |

---

## 2. PRUEBAS DE ESTRÉS Y COMPROBACIÓN DE VULNERABILIDADES (DIAGNÓSTICO)

Se ejecutaron scripts de prueba específicos para comprobar empíricamente los fallos potenciales detectados en la auditoría de código:

### Prueba de Inconsistencia Temporal y Geográfica (ERR-04 y ERR-05)
- **Precondición:** Usuario autenticado con rol `reporter`.
- **Payload:** `disappearance_date: 2099-01-01T00:00:00Z`, `department: Managua`, `municipality: Sébaco` (municipio de Matagalpa).
- **Resultado Obtenido:** HTTP 201 Created (`EN-2026-0021`).
- **Diagnóstico:** **VULNERABILIDAD CONFIRMADA.** El sistema admite fechas en el futuro y municipios incoherentes con el departamento. (El registro de prueba fue eliminado de inmediato de la base de datos).

### Prueba de Subida de Archivo No Gráfico (ERR-03)
- **Precondición:** Usuario autenticado como dueño del reporte.
- **Payload:** Archivo de texto plano con extensión `.exe` simulando binario o archivo dañado.
- **Resultado Obtenido:** `PIL.UnidentifiedImageError` no capturada en `storage_service.py` -> Excepción no controlada.
- **Diagnóstico:** **VULNERABILIDAD CONFIRMADA.** El endpoint no valida los magic bytes ni maneja la excepción de Pillow, provocando una falla interna de servidor.

---

## 3. PRUEBA DE COMPILACIÓN DE PRODUCCIÓN FRONTEND

**Comando:** `cd frontend; npm run build`  
**Entorno:** Next.js 14.2.35, Node.js v24.19.0  
**Resultado:** **Compilación Exitosa (10/10 rutas optimizadas)**

```
Route (app)                              Size     First Load JS
┌ ○ /                                    3.55 kB         103 kB
├ ○ /_not-found                          873 B          88.3 kB
├ ○ /admin                               6.35 kB         103 kB
├ ○ /casos                               2.41 kB         102 kB
├ ƒ /casos/[id]                          5.9 kB          102 kB
├ ○ /login                               3.93 kB        91.3 kB
├ ○ /mapa                                4.56 kB         101 kB
├ ○ /pistas                              3.95 kB         100 kB
└ ○ /reportar                            7.24 kB         104 kB
+ First Load JS shared by all            87.4 kB

✓ Compiled successfully
✓ Generating static pages (10/10)
```
