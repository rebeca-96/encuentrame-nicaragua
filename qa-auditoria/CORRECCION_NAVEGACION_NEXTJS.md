# CORRECCIÓN DE NAVEGACIÓN Y ENRUTAMIENTO NEXT.JS
## Proyecto: Encuéntrame Nicaragua
**Fecha de Corrección:** 20 de Noviembre de 2026  
**Auditor:** Especialista Frontend & Arquitecto Full Stack

---

## 1. OBJETIVO DE LA MODIFICACIÓN

Garantizar que la totalidad de los enlaces del menú de navegación, botones de llamada a la acción y enlaces internos en la aplicación Encuéntrame Nicaragua funcionen de manera infalible en cualquier infraestructura de alojamiento, eliminando la aparición de respuestas JSON `{"detail":"Not Found"}`.

---

## 2. MODIFICACIONES IMPLEMENTADAS EN EL FRONTEND

### 2.1. Normalización de Enlaces en la Barra de Navegación (`Navbar.tsx`)
Se actualizaron todas las rutas de escritorio y móviles para apuntar a los archivos estáticos correspondientes generados por Next.js SSG:

```tsx
// frontend/src/components/layout/Navbar.tsx
// Navegación de Escritorio y Móvil
<Link href="/" className="...">Inicio</Link>
<Link href="/casos.html" className="...">Catálogo de Casos</Link>
<Link href="/mapa.html" className="...">Mapa Nacional</Link>
<Link href="/pistas.html" className="...">Aportar Pista</Link>
<Link href="/reportar.html" className="...">Reportar Caso</Link>
<Link href="/login.html" className="...">Ingresar</Link>
<Link href="/admin.html" className="...">Moderación</Link>
```

### 2.2. Actualización de Enlaces en el Pie de Página (`Footer.tsx`)
```tsx
// frontend/src/components/layout/Footer.tsx
<Link href="/casos.html">Catálogo de Casos Activos</Link>
<Link href="/mapa.html">Mapa Geográfico Departamental</Link>
<Link href="/reportar.html">Registrar Reporte de Búsqueda</Link>
<Link href="/pistas.html">Aportar Información Confidencial</Link>
```

### 2.3. Actualización de Enlaces en la Página de Inicio (`page.tsx`)
- Botón "Registrar un caso de desaparición": `/reportar.html`
- Botón "Explorar mapa interactivo": `/mapa.html`
- Botón "Ver todos los casos": `/casos.html`
- Botón "Iniciar reporte protegido": `/reportar.html`

### 2.4. Enlaces de Retorno en Fichas de Casos (`CasoDetailClient.tsx` y `NicaraguaMap.tsx`)
- Botón "Volver al Catálogo": `/casos.html`
- Enlace en popup de marcadores geográficos: `/casos/${pt.id}.html`
- Enlace de consulta de pistas: `/pistas.html`

---

## 3. ESTRATEGIA DE EXPORTACIÓN Y COMPILACIÓN NEXT.JS

### 3.1. Archivo `next.config.js`
Se mantuvo la configuración de exportación estática desacoplada de servidores propietarios:

```javascript
/** @type {import('next').NextConfig} */
const nextConfig = {
  output: "export",
  reactStrictMode: true,
  images: {
    unoptimized: true,
  },
};

module.exports = nextConfig;
```

### 3.2. Generación Híbrida de Rutas Estáticas (Dual Routing)
Para asegurar compatibilidad con servidores que utilicen tanto convención de archivos planos (`/casos.html`) como servidores que resuelvan directorios indexados (`/casos/` -> `casos/index.html`), se implementó un script de post-compilación que duplica la estructura:

```text
out/
├── index.html
├── 404.html
├── casos.html  <-- Compatible con servidores de archivos directos
├── casos/
│   ├── index.html <-- Compatible con servidores con Directory Indexing
│   ├── case-01.html
│   ├── EN-2026-0001.html
│   └── ...
├── mapa.html
├── mapa/
│   └── index.html
├── reportar.html
├── reportar/
│   └── index.html
├── pistas.html
├── pistas/
│   └── index.html
├── login.html
├── login/
│   └── index.html
├── admin.html
└── admin/
    └── index.html
```

---

## 4. RESULTADOS DE LA VALIDACIÓN

1. **Navegación mediante Clic:** Al hacer clic en cualquier elemento del menú, el navegador solicita el archivo `.html`, el cual es servido inmediatamente con código HTTP `200 OK` y cabecera `Content-Type: text/html; charset=utf-8`.
2. **Recarga de Página (F5):** Al encontrarse en cualquier página interna y presionar F5, el navegador solicita el recurso exacto, eliminando completamente los errores 404 de FastAPI.
3. **Apertura en Pestaña Nueva:** El menú contextual del navegador ("Abrir en pestaña nueva") abre la URL completa con su extensión `.html` y renderiza el contenido de inmediato.
