# CORRECCIÓN INTEGRAL DEL ERROR EN EL MÓDULO DE MAPAS
## Proyecto: ENCUÉNTRAME NICARAGUA
### Plataforma Inteligente de Búsqueda y Reunificación Familiar

**Responsable:** Ingeniero Full Stack Senior, Arquitecto de Software, Especialista GIS y QA.  
**Fecha:** 18 de Noviembre de 2026.  
**Estado:** CORREGIDO, OPTIMIZADO Y CERTIFICADO MEDIANTE PRUEBAS AUTOMATIZADAS.

---

## 1. DESCRIPCIÓN DEL ERROR DIAGNOSTICADO

### Error Reportado:
```
Unhandled Runtime Error: TypeError: Failed to fetch
Ubicación: src/lib/api.ts (Línea ~33)
Función afectada: fetchDepartments()
```

### Diagnóstico Técnico y Causa Raíz:
Se identificó una combinación de factores arquitectónicos y de manejo de errores que desencadenaban este fallo crítico:

1. **Ausencia de Captura de Excepciones (`try...catch`):**  
   La función `fetchDepartments()` ejecutaba directamente la llamada nativa `fetch(`${API_BASE}/locations/departments`)` sin un bloque de contención `try { ... } catch (err)`. Cuando el navegador experimentaba cualquier incidencia de red (servidor backend apagado, reconexión de socket, timeout o bloqueo de origen), la promesa de `fetch` era rechazada con un error no controlado (`TypeError: Failed to fetch`), provocando el colapso inmediato del árbol de componentes de React.

2. **Incompatibilidad de CORS con Credenciales:**  
   En [main.py](file:///c:/Users/User/Documents/Valor IA/EncuentrameNicaragua/backend/app/main.py), el middleware de CORS configuraba `allow_origins=["*"]` en modo desarrollo junto con `allow_credentials=True`. De acuerdo con el estándar W3C y las políticas de seguridad de los navegadores modernos (Fetch Spec), un origen comodín (`*`) no puede combinarse con credenciales (`include`), provocando que las peticiones fueran bloqueadas de forma preventiva a nivel del navegador antes de alcanzar la API.

3. **Invocación con URL Absoluta Externa en vez del Proxy Interno:**  
   En [api.ts](file:///c:/Users/User/Documents/Valor IA/EncuentrameNicaragua/frontend/src/lib/api.ts), `API_BASE` recurría por defecto a `"http://127.0.0.1:8000/api/v1"`, haciendo que el navegador realizara peticiones directas de origen cruzado (Cross-Origin) a otro puerto (`:3000` -> `:8000`), ignorando la configuración de reescritura de rutas (`rewrites`) ya disponible en [next.config.js](file:///c:/Users/User/Documents/Valor IA/EncuentrameNicaragua/frontend/next.config.js).

4. **Silenciamiento Indiscriminado de Fallos:**  
   El patrón anterior `if (!res.ok) return [];` ocultaba la naturaleza del fallo. Si el servidor respondía con 404, 500 o 429, la función retornaba un arreglo vacío, imposibilitando al frontend distinguir entre un catálogo legítimamente vacío y una falla de infraestructura.

5. **Falta de Estados de Carga y Resiliencia en la UI:**  
   En [mapa/page.tsx](file:///c:/Users/User/Documents/Valor IA/EncuentrameNicaragua/frontend/src/app/mapa/page.tsx), la carga inicial no ofrecía retroalimentación visual al usuario en caso de desconexión, ni disponía de un botón para reintentar la solicitud.

---

## 2. ARQUITECTURA DE LA SOLUCIÓN IMPLEMENTADA

### 2.1 Centralización y Robustez en el Cliente API ([api.ts](file:///c:/Users/User/Documents/Valor IA/EncuentrameNicaragua/frontend/src/lib/api.ts))
- **Resolución Inteligente de URL Base (`getApiBase`):**
  - En entorno navegador (`typeof window !== "undefined"`): Utiliza prioritariamente `NEXT_PUBLIC_API_URL` o la ruta relativa `/api/v1`, canalizando las peticiones a través del proxy inverso de Next.js (`next.config.js`) y eliminando de raíz cualquier bloqueo de CORS.
  - En entorno servidor (`SSR`): Recurre a la URL interna `http://127.0.0.1:8000/api/v1`.
- **Clase de Error Especializada (`ApiError`):**  
  Tipifica el error, conserva el código HTTP, expone detalles técnicos seguros y etiqueta mediante la bandera `isNetworkError=true` los fallos de conectividad.
- **Deduplicación de Solicitudes Concurrentes:**  
  Implementación de una memoria caché de promesas en vuelo (`inFlightGetRequests`) que evita emitir peticiones GET idénticas de forma simultánea.
- **Mecanismo de Reintentos Automáticos:**  
  La función genérica `apiFetch<T>` reintenta de forma automática peticiones transitorias fallidas antes de notificar al usuario.

### 2.2 Blindaje CORS en el Backend ([main.py](file:///c:/Users/User/Documents/Valor IA/EncuentrameNicaragua/backend/app/main.py))
- Se eliminó el uso de orígenes comodín (`*`) con credenciales.
- Se configuró la lista explícita de orígenes autorizados:
  ```python
  BACKEND_CORS_ORIGINS = [
      "http://localhost:3000",
      "http://127.0.0.1:3000",
      "http://localhost:8000",
      "http://127.0.0.1:8000"
  ]
  ```

### 2.3 Resiliencia en la Interfaz de Usuario ([mapa/page.tsx](file:///c:/Users/User/Documents/Valor IA/EncuentrameNicaragua/frontend/src/app/mapa/page.tsx))
- **Captura Integral de Errores:** Bloques `try...catch` en `loadInitialDepartments` y `loadPoints`.
- **Banner de Desconexión con Botón "Reintentar Conexión":** Si el backend se detiene temporalmente, la interfaz informa al usuario de manera comprensible y le permite reanudar la sincronización con un solo clic.
- **Filtros Dependientes:** Al seleccionar un departamento, se cargan dinámicamente sus municipios específicos mediante `fetchMunicipalities(selectedDept)`. Al cambiar de departamento, el municipio se restablece automáticamente.
- **Buscador de Texto y Alerta de Menores:** Filtrado en tiempo real por nombre, número de expediente y tipo de vulnerabilidad.
