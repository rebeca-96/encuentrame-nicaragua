# MATRIZ DE PRUEBAS FUNCIONALES Y DE EXPERIENCIA DE USUARIO
## PROYECTO: ENCUÉNTRAME NICARAGUA
### Verificación End-to-End de Flujos Funcionales y Casos de Uso

**Fecha de Ejecución:** 18 de Noviembre de 2026  
**Entorno de Pruebas:** Local Host Windows 11 / Node.js 20 / Python 3.12 / SQLite 3 & PostgreSQL  
**Resultado Global:** 16 Escenarios Ejecutados | **14 PASS** | **2 CONDICIONALES / PENDIENTES**

---

## 1. FLUJO 1: CIUDADANÍA PÚBLICA (CONSULTA, BÚSQUEDA Y MAPA)

| ID | Escenario | Datos de Entrada | Resultado Esperado | Resultado Real | Estado |
| :--- | :--- | :--- | :--- | :--- | :---: |
| **TC-FUNC-01** | Búsqueda por palabra clave en directorio de casos | `q="Mateo"` | Devuelve reportes aprobados cuyo nombre, apodo o rasgos contengan "Mateo" | Devuelve registros aprobados coincidentes | **PASS** |
| **TC-FUNC-02** | Filtro dependiente Departamento - Municipio | Seleccionar Departamento "Managua" | El selector de municipios se actualiza mostrando únicamente los municipios de Managua | Carga los municipios de Managua en tiempo real vía API | **PASS** |
| **TC-FUNC-03** | Visualización de expediente público de persona desaparecida | Caso publicado `EN-2026-0001` | Muestra fotografía sanitizada, datos físicos, vestimenta, fecha y coordenadas aproximadas | Muestra ficha completa sin exponer domicilio privado | **PASS** |
| **TC-FUNC-04** | Aportar pista confidencial anónima sobre un caso | Descripción con más de 10 caracteres, departamento y fecha | Registra la pista de forma privada y devuelve código único `PISTA-XXXX-XXXX` | Devuelve HTTP 201 con `tip_code` aleatorio no predecible | **PASS** |
| **TC-FUNC-05** | Seguimiento de pista ciudadana con código de rastreo | Código `PISTA-9A4K-2B7Z` | Retorna estado actual del trámite ("En cola de moderación", "Triaged", etc.) sin divulgar datos de investigación | Muestra mensaje de estado institucional protegido | **PASS** |
| **TC-FUNC-06** | Navegación e interacción con el Mapa GIS Nacional | Clic en marcadores y zoom en Nicaragua | Muestra casos agrupados con badges diferenciados para menores de edad; geofencing respetado | Mapa Leaflet renderiza marcadores en coordenadas aproximadas | **PASS** |

---

## 2. FLUJO 2: USUARIO REPORTANTE (FAMILIAR / TUTOR)

| ID | Escenario | Datos de Entrada | Resultado Esperado | Resultado Real | Estado |
| :--- | :--- | :--- | :--- | :--- | :---: |
| **TC-FUNC-07** | Registro de cuenta con contraseña compleja | Correo válido, nombre, contraseña `Segura2026#` | Crea la cuenta con rol `reporter` y devuelve perfil sin contraseña | HTTP 201 creado exitosamente con contraseña hasheada en Argon2 | **PASS** |
| **TC-FUNC-08** | Inicio de sesión con credenciales correctas | `reportante@encuentrame.ni` / `Reportante2026#` | Autentica y guarda sesión `encuentrame_session` con token JWT | Genera token válido y redirige al panel correspondiente | **PASS** |
| **TC-FUNC-09** | Intento de registro con contraseña simple | Contraseña `123456` | Rechaza la solicitud indicando requisitos de complejidad | HTTP 422 con detalle de mayúscula, número y símbolo | **PASS** |
| **TC-FUNC-10** | Registro de reporte de desaparición multipaso | 4 pasos completos + aceptación expresa Ley 787 | Crea el reporte en estado `pending_review`, `is_public=False` y genera número de expediente | Caso creado confidencialmente; no visible en el portal público | **PASS** |
| **TC-FUNC-11** | Intento de reportar con fecha de desaparición futura | Fecha: Mañana o próximo mes | El backend rechaza la creación del caso con error de validación temporal | HTTP 422 `La fecha de desaparición no puede ser una fecha en el futuro` | **PASS (Backend)** / ⚠️ **Falta alerta previa en UI** |
| **TC-FUNC-12** | Solicitud de cierre de caso por localización pacífica | Razón: "Persona localizada sana y salva" | El estado cambia a `closed_found` y se retira inmediatamente de la vista pública | Caso despublicado (`is_public=False`) en milisegundos | **PASS** |

---

## 3. FLUJO 3: EQUIPO DE MODERACIÓN Y ADMINISTRACIÓN

| ID | Escenario | Datos de Entrada | Resultado Esperado | Resultado Real | Estado |
| :--- | :--- | :--- | :--- | :--- | :---: |
| **TC-FUNC-13** | Acceso a la cola de reportes pendientes de validación | Sesión con rol `moderator` | Muestra lista de casos en `pending_review` con datos del reportante y documento | Retorna expedientes completos para revisión humana | **PASS** |
| **TC-FUNC-14** | Decisión humana de aprobación de reporte | Acción `approve` con notas internas | El caso pasa a `approved_published`, `is_public=True` y se registra en `audit_logs` | Caso publicado y accesible en el buscador público | **PASS** |
| **TC-FUNC-15** | Triaje de pistas confidenciales ciudadanas | Sesión de moderador | Lista todas las pistas recibidas y permite actualizar estado a `triaged` o `escalated` | Estado actualizado y registrado en auditoría | **PASS** |
| **TC-FUNC-16** | Gestión territorial administrativa (Crear municipio) | Rol `admin`, datos de municipio dentro de Nicaragua | Crea el municipio asociado al departamento y valida coordenadas | Municipio persistido en el catálogo oficial | **PASS** |

---

## 4. EVALUACIÓN DE ESTADOS DE INTERFAZ

- **Loading:** Indicadores giratorios de carga presentes en carga de mapa (`NicaraguaMap`), carga de casos y botones de envío (`disabled` durante la operación).
- **Empty State:** Mensajes claros cuando no hay casos coincidentes en filtros o la cola de moderación está vacía.
- **Error State:** Banners con estilo Tailwind (`bg-red-50 border-red-500 text-red-900`) con opción de **"Reintentar Conexión"** en el mapa y casos.
- **Offline / Network Failure:** Captura de `TypeError: Failed to fetch` transformada en `ApiError` con mensaje explicativo para el usuario.
