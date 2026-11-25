# MATRIZ INTEGRAL DE VALIDACIONES CAMPO POR CAMPO
## PROYECTO: ENCUÉNTRAME NICARAGUA
### Auditoría de Validación Cruzada: Frontend vs Backend vs Base de Datos

**Fecha de Evaluación:** 18 de Noviembre de 2026  
**Objetivo:** Verificar la simetría de validaciones entre lo que exige el navegador (HTML/React), lo que rechaza el servidor (FastAPI/Pydantic) y lo que restringe el motor relacional (SQLAlchemy/SQLite/PostgreSQL).

---

## 1. FORMULARIO DE REGISTRO DE REPORTES DE PERSONAS NO LOCALIZADAS

| Campo | Tipo | Oblig. | Long. Mín/Máx | Validación Frontend | Validación Backend (Pydantic) | Restricción Base de Datos | Mensaje de Error / Estado |
| :--- | :--- | :---: | :---: | :--- | :--- | :--- | :--- |
| `first_name` | String | Sí | 2 / 100 | `required` (HTML) | `Field(..., min_length=2)`, `strip()` | `String(100)`, `nullable=False` | ✅ Simétrico y validado |
| `last_name` | String | Sí | 2 / 100 | `required` (HTML) | `Field(..., min_length=2)`, `strip()` | `String(100)`, `nullable=False` | ✅ Simétrico y validado |
| `nickname` | String | No | 0 / 100 | Sin validación | `strip() if nickname else None` | `String(100)`, `nullable=True` | ✅ Consistente |
| `age_at_disappearance` | Integer | Sí | 0 / 120 | `type="number"`, `min=0`, `max=120` | `Field(..., ge=0, le=120)` | `Integer`, `nullable=False` | ✅ Coherente en ambos extremos |
| `gender` | String | Sí | Enum (4) | `<select>` con 4 opciones | Validado contra `GenderEnum` | `String(32)`, `nullable=False` | ✅ Consistente |
| `disappearance_date` | DateTime | Sí | 1920 a Hoy | `<input type="date">` **(No bloquea fecha futura)** | `@field_validator`: rechaza fechas futuras (> now + 5m) y < 1920 | `DateTime`, `nullable=False` | ⚠️ **Falta bloqueo en Frontend antes de avanzar de paso** |
| `department` | String | Sí | 2 / 100 | `<select>` poblado desde API | `@field_validator`: chequea existencia en catálogo oficial | `String(100)`, `nullable=False` | ✅ Simétrico y validado |
| `municipality` | String | Sí | 2 / 100 | `<select>` dependiente filtrado | `@model_validator`: valida pertenencia territorial estricta al departamento | `String(100)`, `nullable=False` | ✅ Blindado contra inconsistencias |
| `neighborhood_zone` | String | No | 0 / 150 | Sin restricción | `strip() if zone else None` | `String(150)`, `nullable=True` | ✅ Consistente |
| `physical_description` | Text | Sí | 10 / inf | `<textarea>` **(No valida min. 10 chars en paso 3)** | `Field(..., min_length=10)` | `Text`, `nullable=False` | ⚠️ **Falta validación temprana de longitud en UI** |
| `clothing_description` | Text | Sí | 5 / inf | `<textarea>` **(No valida min. 5 chars en paso 3)** | `Field(..., min_length=5)` | `Text`, `nullable=False` | ⚠️ **Falta validación temprana de longitud en UI** |
| `circumstances` | Text | Sí | 15 / inf | `<textarea>` **(No valida min. 15 chars en paso 2)** | `Field(..., min_length=15)` | `Text`, `nullable=False` | ⚠️ **Falta validación temprana de longitud en UI** |
| `relationship_to_victim` | String | Sí | 2 / 100 | Bloquea botón si está vacío | `Field(..., min_length=2)` | En `ConsentRecord`: `String(100)`, `nullable=False` | ✅ Validado |
| `identity_doc_number` | String | Sí | 5 / 64 | Bloquea botón si está vacío | `Field(..., min_length=5)`, hash SHA-256 | `identity_doc_hash String(64)`, `nullable=False` | ✅ Cifrado y protegido |
| `accepted_terms` | Boolean | Sí | True | Checkbox obligatorio | `@field_validator`: solo acepta `True` explícito | `accepted_terms_timestamp DateTime` | ✅ Cumple Ley N.° 787 |
| `photo` (archivo) | File | No | 0 / 5 MB | `accept="image/*"` | Valida firmas mágicas, Pillow verify, strip EXIF, máx. 5MB | `ReportPhoto` `storage_key String(255)` | ⚠️ **Falta manejo de fallo de subida en cliente** |

---

## 2. FORMULARIO DE PISTAS CONFIDENCIALES CIUDADANAS

| Campo | Tipo | Oblig. | Validación Frontend | Validación Backend | Restricción Base de Datos | Estado |
| :--- | :--- | :---: | :--- | :--- | :--- | :--- |
| `report_id` | String | Sí | Asociado por contexto de URL | Valida existencia de reporte y que NO esté cerrado | `ForeignKey("missing_person_reports.id")` | ✅ Blindado |
| `description` | Text | Sí | `required`, min 10 caracteres | `Field(..., min_length=10)` | `Text`, `nullable=False` | ✅ Simétrico |
| `sighting_date` | DateTime | No | `<input type="date">` | Rechaza fechas futuras (> now + 5 min) | `DateTime`, `nullable=True` | ✅ Validado |
| `sighting_department` | String | No | Input de texto libre | Geocodificación aproximada a nivel municipal | `GeographicLocation.id` | ⚠️ Se recomienda `<select>` de departamentos |
| `informant_contact` | String | No | Input de texto opcional | Texto opcional limpio con `strip()` | `String(255)`, `nullable=True` | ✅ Confidencial |
| `confidentiality_level` | Enum | Sí | Seleccionable | `ConfidentialityLevel.STRICT_ANONYMOUS` | `String(32)`, `nullable=False` | ✅ Seguro |

---

## 3. FORMULARIO DE AUTENTICACIÓN Y REGISTRO

| Campo | Tipo | Oblig. | Validación Frontend | Validación Backend | Restricción Base de Datos | Estado |
| :--- | :--- | :---: | :--- | :--- | :--- | :--- |
| `email` (Login/Reg) | EmailStr | Sí | `type="email"` (HTML5) | `EmailStr` (Pydantic con email-validator) | `String(255)`, `unique=True`, `index=True` | ✅ Validado |
| `password` (Login) | String | Sí | `type="password"` | Verificación con Argon2 / Bcrypt | `password_hash String(255)` | ✅ Seguro |
| `password` (Registro) | String | Sí | `type="password"`, placeholder guía | 8+ chars, mayúscula, minúscula, número y símbolo especial | `password_hash String(255)` | ⚠️ **Falta medidor de fortaleza en UI** |
| `confirm_password` | String | Sí | Valida igualdad en submit | `@model_validator`: valida coincidencia con `password` | No se persiste en BD | ✅ Validado |
| `full_name` | String | Sí | `required` | `Field(..., min_length=3)` | `String(255)`, `nullable=False` | ✅ Validado |
| `phone_number` | String | No | Opcional | Opcional con `strip()` | `String(100)`, `nullable=True` | ✅ Opcional |

---

## 4. FORMULARIO DE ADMINISTRACIÓN TERRITORIAL (DEPARTAMENTOS Y MUNICIPIOS)

| Campo | Tipo | Oblig. | Validación Frontend | Validación Backend | Restricción Base de Datos | Estado |
| :--- | :--- | :---: | :--- | :--- | :--- | :--- |
| `name` (Depto) | String | Sí | Min 2 chars | 2-100 chars, unicidad insensitive | `name String(100) UNIQUE` | ✅ Validado |
| `code` (Depto) | String | Sí | Min 2 chars | Formato `^[A-Z0-9_-]+$`, unicidad | `code String(10) UNIQUE` | ✅ Validado |
| `type` (Depto) | Enum | Sí | Select (2 opciones) | `^(department\|autonomous_region)$` | `String(32)` | ✅ Validado |
| `latitude` (Depto/Mun) | Float | Sí | Coordenadas decimales | Geofencing nacional: 10.70 a 15.10 | `Float`, `nullable=False` | ✅ Geofencing activo |
| `longitude` (Depto/Mun) | Float | Sí | Coordenadas decimales | Geofencing nacional: -87.70 a -82.50 | `Float`, `nullable=False` | ✅ Geofencing activo |
| `department_id` (Mun) | String | Sí | Selección de padre | Valida existencia previa de departamento | `ForeignKey("departments.id")` | ✅ Integridad referencial |
| `code` (Mun) | String | Sí | Min 2 chars | Formato `^[A-Z0-9_-]+$`, unicidad | `code String(15) UNIQUE` | ✅ Validado |
| `name` (Mun) | String | Sí | Min 2 chars | Unicidad por departamento padre | `UniqueConstraint("department_id", "name")` | ✅ Sin duplicados |

---

## 5. ESCENARIOS EXCEPCIONALES Y PRUEBAS DE FRONTERA

1. **Campo vacío / nulo:** Rechazado en backend con HTTP 422 Unprocessable Entity mediante Pydantic schemas.
2. **Espacios en blanco al inicio o final:** Todos los endpoints aplican `.strip()` antes de validar y almacenar en la base de datos.
3. **Caracteres Unicode / Acentos nicaragüenses (ñ, á, é, í, ó, ú):** Soportados de forma nativa en nombres propios, municipios (ej. *El Cuá*, *Waslala*, *Totogalpa*) y descripciones.
4. **Fechas futuras:** Rechazadas en el backend por `validate_disappearance_date_not_future` (HTTP 422). Falta advertencia inmediata en UI.
5. **Archivos maliciosos / no-imagen:** Pillow y `VALID_IMAGE_SIGNATURES` validan cabeceras binarias reales (magic bytes), rechazando ejecutables con extensión `.jpg` simulada.
6. **Archivos de más de 5 MB:** Rechazados en backend con HTTP 400 antes de procesar bytes en memoria.
7. **Peticiones concurrentes repetidas:** Mitigadas en el frontend mediante `inFlightGetRequests` y en el backend mediante control de transacciones ACID en SQLAlchemy.
