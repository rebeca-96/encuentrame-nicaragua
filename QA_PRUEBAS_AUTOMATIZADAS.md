# INFORME DE PRUEBAS AUTOMATIZADAS Y REGRESIÓN — SDET & QA SENIOR
## PROYECTO: ENCUÉNTRAME NICARAGUA

**Framework:** Pytest 9.2.0 + HTTPX 0.28.1 + AsyncIO 1.5.0 + Starlette TestClient  
**Python Runtime:** 3.12.10 (win32)  
**Fecha de Ejecución Oficial:** 18 de Noviembre de 2026, 21:12:13 CST  
**Resultado Global:** **33 PRUEBAS EJECUTADAS — 33 APROBADAS (100% PASS RATE) EN 2.15s**

---

## 1. REGISTRO DETALLADO DE PRUEBAS AUTOMATIZADAS EJECUTADAS

### Suite 1: Auditoría de Correcciones y Frontera (`test_audit_fixes.py` — 8 Pruebas)
| Test ID | Función de Prueba | Escenario y Caso de Prueba | Resultado Esperado | Resultado Real | Estado |
| :--- | :--- | :--- | :--- | :--- | :---: |
| **TEST-01** | `test_future_date_rejected` | Envío de fecha de desaparición posterior a la fecha actual (`now + 1 day`) | HTTP 422 Unprocessable Entity | HTTP 422 con detalle de fecha futura rechazada | **PASS** |
| **TEST-02** | `test_inconsistent_municipality_rejected` | Envío de municipio de Managua ("Tipitapa") bajo el departamento de León | HTTP 422 por inconsistencia territorial | HTTP 422 rechazado por validador de modelo | **PASS** |
| **TEST-03** | `test_invalid_image_upload_returns_400` | Subida de archivo `.txt` camuflado con nombre de imagen | HTTP 400 Bad Request por fallo de cabecera mágica | HTTP 400 rechazado antes de almacenar | **PASS** |
| **TEST-04** | `test_put_report_update_authorization` | Usuario común intentando modificar un reporte que ya fue aprobado | HTTP 400/403 prohibiendo modificación de casos publicados | HTTP 400 informando que debe canalizarse por moderación | **PASS** |
| **TEST-05** | `test_password_complexity_required` | Registro de usuario con contraseña débil sin mayúsculas ni números | HTTP 422 detallando requisitos de complejidad | HTTP 422 rechazando contraseña no segura | **PASS** |
| **TEST-06** | `test_rate_limiting_login_returns_429` | Ejecución de 6 intentos fallidos consecutivos de login en menos de 1 minuto | HTTP 429 Too Many Requests en el 6to intento | HTTP 429 con cabecera `Retry-After` activa | **PASS** |
| **TEST-07** | `test_tip_rejected_on_closed_case` | Intento de enviar una pista confidencial a un caso en estado `closed_found` | HTTP 400 indicando que el caso ya está resuelto | HTTP 400 impidiendo pistas en casos inactivos | **PASS** |
| **TEST-08** | `test_notification_unsubscribe_flow` | Cancelación de alertas mediante token único de desuscripción | HTTP 200 y marcado de suscripción a `is_active=False` | HTTP 200 desuscripción exitosa | **PASS** |

### Suite 2: Requerimientos Críticos de Negocio y Seguridad (`test_core_requirements.py` — 10 Pruebas)
| Test ID | Función de Prueba | Escenario y Caso de Prueba | Resultado Esperado | Resultado Real | Estado |
| :--- | :--- | :--- | :--- | :--- | :---: |
| **TEST-09** | `test_1_new_report_not_published_without_moderator_approval` | Creación de reporte nuevo por ciudadano | Estado inicial obligatorio `pending_review` y `is_public=False` | Reporte confidencial; ausente del catálogo público | **PASS** |
| **TEST-10** | `test_2_citizen_cannot_access_confidential_tips` | Ciudadano común intentando consultar la lista de pistas de un caso | HTTP 403 Forbidden por falta de rol moderador/admin | Acceso bloqueado estrictamente | **PASS** |
| **TEST-11** | `test_3_user_cannot_modify_or_close_others_reports` | Usuario B intentando modificar o cerrar reporte de Usuario A | HTTP 403 Forbidden por violación de propiedad | HTTP 403 protección IDOR confirmada | **PASS** |
| **TEST-12** | `test_4_search_filters_return_correct_results` | Búsqueda combinada por departamento, género y condición de menor | Solo devuelve casos coincidentes con todos los filtros | Coincidencia exacta de registros | **PASS** |
| **TEST-13** | `test_5_geographic_data_does_not_reveal_sensitive_coordinates` | Consulta de puntos del mapa interactivo | Coordenadas aproximadas; campos de dirección exacta ocultos | Coordenadas de protección municipal activas | **PASS** |
| **TEST-14** | `test_6_administrative_actions_are_audit_logged` | Moderación de un reporte | Inserción automática e inmutable en tabla `audit_logs` | Registro de auditoría persistido con timestamp UTC | **PASS** |
| **TEST-15** | `test_7_case_closure_is_processable_and_depublishes_case` | Solicitud de cierre por localización | El caso pasa a `is_public=False` y estado `closed_found` | Despublicación instantánea verificada | **PASS** |
| **TEST-16** | `test_8_error_handling_for_invalid_input_and_missing_consent` | Envío de reporte sin marcar la casilla de consentimiento Ley 787 | HTTP 400/422 rechazando creación sin consentimiento | Creación bloqueada sin consentimiento legal | **PASS** |
| **TEST-17** | `test_9_ai_acts_strictly_as_advisor_without_autonomous_state_changes` | Invocación del servicio de IA supervisada | Sugiere completitud y duplicados sin alterar el estado del caso | Solo retorna sugerencias; estado intacto | **PASS** |
| **TEST-18** | `test_10_secure_tip_submission_and_unpredictable_code` | Recepción de pista anónima | Código con formato `PISTA-XXXX-XXXX` con alta entropía | Código aleatorio generado exitosamente | **PASS** |

### Suite 3: División Territorial y Módulo de Mapas (`test_geography.py` — 15 Pruebas)
| Test ID | Función de Prueba | Escenario y Caso de Prueba | Resultado Esperado | Resultado Real | Estado |
| :--- | :--- | :--- | :--- | :--- | :---: |
| **TEST-19** | `test_01_backend_health_and_root` | Verificación de salud y conectividad de la API | HTTP 200 con estado `"status": "healthy"` | Respuesta en menos de 5ms | **PASS** |
| **TEST-20** | `test_02_get_departments_endpoint` | Consulta pública de departamentos | Retorna lista con los 15 departamentos y 2 regiones autónomas | 17 divisiones devueltas ordenadas | **PASS** |
| **TEST-21** | `test_03_get_municipalities_endpoint` | Consulta pública de municipios | Retorna catálogo de municipios oficiales | Catálogo oficial de Nicaragua devuelto | **PASS** |
| **TEST-22** | `test_04_seventeen_territorial_entities` | Conteo exacto de divisiones territoriales | Exactamente 17 entidades (15 departamentos + 2 RACs) | 17 entidades verificadas | **PASS** |
| **TEST-23** | `test_05_one_hundred_fifty_three_municipalities` | Conteo exacto de municipios de Nicaragua | Exactamente 153 municipios según INETER | 153 municipios verificados | **PASS** |
| **TEST-24** | `test_06_municipalities_belong_to_correct_entities` | Verificación de relación jerárquica padre-hijo | Cada municipio asociado a su departamento oficial | Integridad referencial 100% válida | **PASS** |
| **TEST-25** | `test_07_no_duplicate_codes_or_names` | Unicidad de códigos geográficos | Sin códigos de departamento ni municipio duplicados | Códigos únicos verificados | **PASS** |
| **TEST-26** | `test_08_selectors_load_real_data` | Simulación de carga de selectores en frontend | La API entrega datos enriquecidos con coordenadas | Datos completos para Leaflet | **PASS** |
| **TEST-27** | `test_09_dependent_filters` | Filtrado de municipios por departamento | Retorna solo los municipios del departamento consultado | Filtro dependiente exacto | **PASS** |
| **TEST-28** | `test_10_network_and_not_found_handling` | Solicitud de departamento inexistente | HTTP 404 con mensaje claro de recurso no encontrado | HTTP 404 estructurado en JSON | **PASS** |
| **TEST-29** | `test_11_form_validations_reject_invalid_geo_data` | Intento de crear municipio con coordenadas fuera de Nicaragua | HTTP 422 por violación de geofencing nacional | HTTP 422 rechazado por límites geográficos | **PASS** |
| **TEST-30** | `test_12_unauthorized_users_cannot_modify_catalog` | Usuario común intentando crear o editar un departamento | HTTP 403 Forbidden por restricción de rol administrador | Bloqueo RBAC confirmado | **PASS** |
| **TEST-31** | `test_13_map_aggregated_endpoint_and_filters` | Consulta de marcadores para mapa con filtro por departamento | Retorna solo puntos del departamento y oculta datos sensibles | Marcadores agregados devueltos | **PASS** |
| **TEST-32** | `test_14_reports_validate_territorial_consistency` | Creación de reporte con municipio inválido | Rechazo estricto con HTTP 422 | Inconsistencia territorial bloqueada | **PASS** |
| **TEST-33** | `test_15_geographic_summary_endpoint` | Resumen territorial cuantitativo para panel admin | Retorna totales: 17 departamentos y 153 municipios | Totales verificados contra Ley N.° 59 | **PASS** |

---

## 2. ESTADO DE LAS PRUEBAS EN EL FRONTEND

- **Comprobación:** Ejecución de `npm test` en `frontend/`.
- **Resultado:** `npm error Missing script: "test"`.
- **Diagnóstico:** El proyecto carece actualmente de arnés de pruebas automatizadas en cliente. La validación se realiza mediante compilación estricta de tipos (`npm run build`), la cual finalizó con éxito (`Exit Code 0`, 10/10 rutas generadas sin errores).
- **Recomendación SDET:** Instalar `vitest`, `@testing-library/react` y `@testing-library/jest-dom` para incorporar pruebas unitarias de componentes y validación de formularios en el cliente.
