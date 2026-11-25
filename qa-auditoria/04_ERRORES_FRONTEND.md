# 04 — AUDITORÍA DE ERRORES DE FRONTEND, UI, UX Y ACCESIBILIDAD
## Proyecto: ENCUÉNTRAME NICARAGUA
### Pruebas Exploratorias, Navegación, Enrutamiento SPA, Responsive y WCAG 2.2
**Auditor:** Senior QA Engineer & SDET  
**Fecha:** 19 de Noviembre de 2026  

---

## 1. EVALUACIÓN DEL ENRUTAMIENTO Y ARQUITECTURA DE DESPLIEGUE

### 1.1 El problema de las URLs Limpias (DEF-02)
- **Diagnóstico:** El proyecto utiliza Next.js con modo de compilación estática `output: 'export'`.
  Al compilar mediante `npm run build`, Next.js genera un árbol de archivos estáticos en `frontend/out/`:
  - `casos.html`
  - `mapa.html`
  - `reportar.html`
  - `pistas.html`
  - `auth/login.html`
- **Comportamiento en Hosting:**
  Cuando un usuario navega desde la portada mediante los componentes `<Link>` de Next.js, la navegación es interceptada por el router de React en el cliente y funciona con fluidez.
  Sin embargo, **si el usuario recarga la página (F5)** o escribe directamente en la barra de direcciones `https://creacionvaloria.tradescanner.online/casos`, el servidor web (que no tiene reglas de reescritura configuradas) busca un archivo o directorio físico llamado `/casos` y responde con **HTTP 404 Not Found**.
- **Solución Recomendada para el Ingeniero Full Stack:**
  1. **Opción A (Recomendada en Next.js):** Agregar en `next.config.ts`:
     ```typescript
     const nextConfig: NextConfig = {
       output: 'export',
       trailingSlash: true, // Genera /casos/index.html en lugar de /casos.html
       // ...
     };
     ```
  2. **Opción B (Nginx / Web Server Rewrite):** Configurar en el bloque de servidor:
     ```nginx
     location / {
       try_files $uri $uri.html $uri/ /index.html;
     }
     ```

---

## 2. AUDITORÍA VISUAL Y DISEÑO RESPONSIVE

### 2.1 Carga de Hojas de Estilo y Tipografías
- **Estado de CSS:**
  - Tailwind CSS v3/v4 se compila correctamente dentro del bundle estático `_next/static/css/*.css`.
  - En la prueba en vivo sobre `https://creacionvaloria.tradescanner.online`, los colores institucionales (Azul Marino Cívico `#0f2a4a`, Dorado Ámbar `#f59e0b`, Blanco puro) renderizan correctamente sin FOUC (Flash of Unstyled Content).
  - Los archivos estáticos en `_next/static/` cargan con código HTTP 200 y cabeceras de compresión adecuadas.

### 2.2 Menú Móvil e Interacción Táctil
- **Comportamiento:** En resoluciones inferiores a 768px (Mobile Breakpoint), el menú de navegación se colapsa en un botón de hamburguesa.
- **Defecto Detectado:**
  - Al abrir el menú desplegable en pantallas pequeñas (360px a 414px), el botón de cierre carece de foco visual visible (`focus-visible:ring`).
  - Al hacer clic en un enlace del menú móvil, en algunos casos el drawer no se cierra automáticamente si la navegación es hacia una sub-sección con ancla.

---

## 3. AUDITORÍA DE ACCESIBILIDAD (WCAG 2.2 NIVEL AA)

Se ejecutó una inspección detallada de accesibilidad sobre los componentes principales:

| Criterio WCAG | Componente Evaluado | Estado | Detalle del Hallazgo |
| :--- | :--- | :--- | :--- |
| **1.1.1 Non-text Content** | `NationalMap.tsx`, `Navbar.tsx` | **Fallo Parcial** | El botón de alternancia de menú en `Navbar.tsx` no posee el atributo `aria-label="Abrir menú de navegación"`, lo que provoca que un lector de pantalla anuncie simplemente "Botón". |
| **1.3.1 Info and Relationships** | Formularios en `reportar` y `pistas` | **Fallo Parcial** | Múltiples etiquetas `<label>` no tienen la propiedad `htmlFor` vinculada al `id` del `<input>`. Se utilizan contenedores `<div>` como wrappers sin asociación semántica formal. |
| **1.4.3 Contrast (Minimum)** | Badges de estado en tarjetas de caso | **Cumple** | La relación de contraste entre el texto `#0f2a4a` sobre fondo blanco es 14.8:1 (supera el ratio mínimo de 4.5:1). Los badges de estado `published` (verde esmeralda sobre fondo claro) cumplen con ratio 5.1:1. |
| **2.1.1 Keyboard Navigation** | Filtros y Buscador de Casos | **Cumple** | Es posible tabular por todos los controles de filtro, inputs y botones de paginación. La tecla `Enter` activa la búsqueda. |
| **3.3.1 Error Identification** | Mensajes de validación en formularios | **Fallo Parcial** | Cuando un campo falla en validación, el mensaje de error aparece en un párrafo rojo pero el contenedor no cuenta con `role="alert"` ni `aria-live="polite"`, por lo que los usuarios con discapacidad visual no son notificados del error en tiempo real. |
| **4.1.2 Name, Role, Value** | Selectores de Departamento / Municipio | **Cumple** | Utilizan elementos nativos `<select>` que exponen correctamente su estado accesible a las tecnologías de asistencia. |

---

## 4. ESTADOS DE INTERFAZ Y MANEJO DE ERRORES DE CLIENTE

1. **Estado de Carga (Loading State):**
   - El catálogo de casos en `/casos` implementa tarjetas esqueleto (Skeletons) con animación `animate-pulse`, evitando saltos de maquetación (CLS - Cumulative Layout Shift).
2. **Estado Vacío (Empty State):**
   - Cuando una búsqueda de personas no arroja resultados con los filtros seleccionados, se muestra un mensaje informativo cívico claro: *"No se encontraron expedientes con los criterios seleccionados. Verifique el municipio o intente con términos más generales."*
3. **Estado de Error de Red (Error State):**
   - Si la API no responde (`Failed to fetch`), el frontend captura la excepción y muestra un banner de advertencia.
   - **Oportunidad de Mejora:** El mensaje actual en el modal de error es técnico. Se recomienda sustituirlo por: *"No pudimos sincronizar con el servidor central de búsqueda. Por favor verifique su conexión a internet y pulse 'Reintentar'."* con un botón activo de reintento.
