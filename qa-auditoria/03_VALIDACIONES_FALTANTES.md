# 03 — MATRIZ EXHAUSTIVA DE VALIDACIONES
## Proyecto: ENCUÉNTRAME NICARAGUA
### Comparativa de Validaciones por Campo: Frontend vs. Backend vs. Base de Datos
**Auditor:** Senior QA Engineer & SDET  
**Fecha:** 19 de Noviembre de 2026  

---

## 1. FORMULARIO: REGISTRO DE REPORTE DE PERSONA DESAPARECIDA (`/reportar`)

| Campo | Obligatorio | Tipo de Dato | Validación Frontend | Validación Backend (Pydantic) | Restricción Base de Datos | Brecha / Validación Faltante Detectada |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| `first_name` | Sí | `String` | HTML `required`, `trim()` en submit. | `min_length=2`, sanitización de espacios. | `Column(String(100), nullable=False)` | En frontend falta regex para evitar caracteres numéricos aislados o símbolos matemáticos ("12345"). Backend sí tolera Unicode/tildes correctamente. |
| `last_name` | Sí | `String` | HTML `required`, `trim()` en submit. | `min_length=2`, sanitización de espacios. | `Column(String(100), nullable=False)` | Adecuado. |
| `nickname` | No | `String` | Opcional, `trim()`. | `Optional[str] = None`, `max_length=100`. | `Column(String(100), nullable=True)` | Adecuado. |
| `age_at_disappearance`| Sí | `Integer` | `<input type="number">`, `min="0"`, `max="120"`. | `Field(..., ge=0, le=120)`. | `Column(Integer, nullable=False)` | En frontend, el campo de texto permite escribir caracteres de exponente ("e", "+") por comportamiento nativo HTML number sin sanitizar en `onChange`. |
| `gender` | Sí | `Enum` | `<select>` con opciones fijas (`male`, `female`, `other`, `unspecified`). | `GenderEnum` validado estrictamente. | `Column(String(20), nullable=False)` | Adecuado. |
| `disappearance_date` | Sí | `DateTime` | `<input type="datetime-local">`, `max={now}`. | `@field_validator`: Rechazo de fechas futuras (> now + 5m) y fechas anteriores a 1920. | `Column(DateTime(timezone=True), nullable=False)` | Validado robustamente en backend (HTTP 422 si se envía fecha futura). En frontend, `max` en el input previene selección en navegadores modernos. |
| `department` | Sí | `String` | `<select>` cargado desde `/api/v1/locations/departments`. | Validación contra los 17 nombres oficiales. | `Column(String(100), nullable=False)` | Adecuado. |
| `municipality` | Sí | `String` | `<select>` dinámico filtrado por departamento. | `@field_validator`: Valida existencia y pertenencia estricta al departamento seleccionado. | `Column(String(100), nullable=False)` | Validado robustamente. Backend rechaza combinaciones inconsistentes (ej. Managua + León) con HTTP 422. |
| `neighborhood_zone` | No | `String` | `<input>`, `trim()`. | `Optional[str]`, `max_length=200`. | `Column(String(200), nullable=True)` | Adecuado. |
| `physical_description`| Sí | `Text` | `textarea`, `minLength={10}`. | `Field(..., min_length=10)`. | `Column(Text, nullable=False)` | Adecuado. |
| `clothing_description`| Sí | `Text` | `textarea`, `minLength={5}`. | `Field(..., min_length=5)`. | `Column(Text, nullable=False)` | Adecuado. |
| `circumstances` | Sí | `Text` | `textarea`, `minLength={15}`. | `Field(..., min_length=15)`. | `Column(Text, nullable=False)` | Adecuado. |
| `consent.accepted_terms`| Sí | `Boolean` | `<input type="checkbox">` requerido. | `@field_validator`: Debe ser estrictamente `True`. | `Column(Boolean, nullable=False)` | Validado robustamente. Si se envía `False`, backend responde `HTTP 422: Debe aceptar expresamente los términos de consentimiento informado y la Ley 787`. |
| `consent.relationship_to_victim` | Sí | `String` | Input de parentesco en modal de consentimiento. | `Field(..., min_length=2)`. | `Column(String(100), nullable=False)` | Adecuado. |
| `consent.identity_doc_number` | Sí | `String` | Input de cédula o documento. | `Field(..., min_length=5)`. | `Column(String(50), nullable=False)` | **Mejora:** Falta validador de formato de Cédula de Identidad de Nicaragua (`000-000000-0000X`). Actualmente acepta cualquier cadena >= 5 caracteres. |
| Fotografía adjunta | No | `File / Image`| Validado en cliente: `<input type="file" accept="image/*">`. | Valida extensiones (`.jpg, .jpeg, .png, .webp`), tamaño máx 5MB y cabecera MIME con PIL. | `report_photos` tabla relacional con SHA-256. | **DEF-07:** El backend valida el formato pero no purga explícitamente los metadatos EXIF de geolocalización de la cámara antes de guardar en disco. |

---

## 2. FORMULARIO: APORTE DE PISTAS CONFIDENCIALES (`/pistas`)

| Campo | Obligatorio | Tipo de Dato | Validación Frontend | Validación Backend (Pydantic) | Restricción Base de Datos | Brecha / Validación Faltante Detectada |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| `case_number` / `report_id` | Sí | `String` | Input con autocompletado y validación de existencia. | Valida que el caso exista y se encuentre en estado `published`. | `ForeignKey("missing_person_reports.id")` | Adecuado. Rechaza pistas para reportes cerrados o no publicados. |
| `tip_text` | Sí | `Text` | `textarea` requerido, min 10 caracteres. | `Field(..., min_length=10)`. | `Column(Text, nullable=False)` | Adecuado. |
| `sighting_date` | No | `DateTime` | Input datetime-local opcional. | No permite fechas futuras mayores a la actual. | `Column(DateTime(timezone=True), nullable=True)` | Adecuado. |
| `location_description` | No | `String` | Input opcional de texto. | `Optional[str] = None`, `max_length=255`. | `Column(String(255), nullable=True)` | Adecuado. |
| `is_anonymous` | Sí | `Boolean` | Switch / Checkbox. | `bool = True`. | `Column(Boolean, default=True)` | Adecuado. Si es anónimo, los datos de contacto se omiten o cifran. |
| `informant_contact` | No (Cond.) | `String` | Opcional si `is_anonymous=False`. | Teléfono o correo opcional. | `Column(String(200), nullable=True)` | **Mejora:** En caso de no ser anónimo, no se aplica validación estricta de formato telefónico de Nicaragua (`+505 \d{8}`) en backend. |

---

## 3. FORMULARIO: AUTENTICACIÓN CIUDADANA Y ACCESO (`/auth/login` y `/auth/registro`)

| Campo | Obligatorio | Tipo de Dato | Validación Frontend | Validación Backend (Pydantic) | Restricción Base de Datos | Brecha / Validación Faltante Detectada |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| `email` | Sí | `EmailStr` | `<input type="email">` nativo. | `EmailStr` con normalización `.lower().strip()`. | `Column(String(150), unique=True, index=True)` | Robusto. Duplicados rechazan con HTTP 409 / HTTP 422. |
| `password` | Sí | `String` | `<input type="password">`, `minLength={8}`. | `Field(..., min_length=8)` con verificación Bcrypt. | `Column(String(255), nullable=False)` | **Mejora:** En registro no se impone regla de complejidad de contraseña (ej. al menos una mayúscula y un número) en el validador Pydantic de `UserRegister`. |
| `full_name` (Registro) | Sí | `String` | Input con `trim()`. | `Field(..., min_length=3)`. | `Column(String(150), nullable=False)` | Adecuado. |
| `phone_number` (Registro)| Sí | `String` | Input telefónico con placeholder `8888-0000`. | `Field(..., min_length=8)`. | `Column(String(30), nullable=False)` | Falta máscara de entrada y normalización estricta al prefijo internacional `+505`. |

---

## 4. FORMULARIO: BÚSQUEDA Y FILTRADO DE EXPEDIENTES (`/casos`)

| Parámetro | Tipo | Valores Permitidos | Validación Frontend | Validación Backend | Riesgo de Seguridad / Inyección |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `q` (texto libre) | `String` | Alfanumérico, espacios, tildes | Sanitizado en cliente. | Consulta parametrizada en SQLAlchemy ORM (`ilike(:pattern)`). | Protegido contra SQL Injection gracias a ORM parametrizado. |
| `department` | `String` | 17 nombres oficiales | Seleccionado vía dropdown. | Filtrado exacto en query `filter(department == depto)`. | Protegido. |
| `municipality` | `String` | 153 municipios | Dropdown dependiente. | Filtrado exacto en query. | Protegido. |
| `gender` | `String` | `male`, `female`, `other` | Dropdown fijo. | Validación contra `GenderEnum`. | Protegido. |
| `limit` | `Integer` | 1 a N | Paginador frontend envía 20 por página. | `limit: int = 50`. | **DEF-06:** No tiene límite superior estricto `le=100`, riesgo menor de DoS por memoria. |
| `skip` | `Integer` | >= 0 | Paginador frontend calcula offset. | `skip: int = 0, ge=0`. | Protegido. |
