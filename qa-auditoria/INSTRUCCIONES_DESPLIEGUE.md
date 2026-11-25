# GUÍA OPERATIVA E INSTRUCCIONES DE DESPLIEGUE
## Proyecto: Encuéntrame Nicaragua
**Fecha:** 20 de Noviembre de 2026  
**Área:** DevOps & Arquitectura de Despliegue  
**Ambientes:** Servidor Local FastAPI / Producción Cloud Hosting

---

## 1. REQUISITOS PREVIOS

Asegúrese de contar con las siguientes herramientas en el entorno de despliegue:
- **Node.js:** Versión 18.x o 20.x LTS.
- **npm:** Versión 9.x o 10.x.
- **Python:** Versión 3.10 o superior (con `virtualenv` activado).
- **Dependencias Python:** Instaladas desde `backend/requirements.txt`.

---

## 2. PROCESO DE COMPILACIÓN DEL FRONTEND NEXT.JS

### Paso 1: Instalación de Dependencias
```bash
cd frontend
npm install
```

### Paso 2: Generación del Build Estático (SSG)
```bash
npm run build
```
Este comando compilará todas las rutas estáticas, optimizará los bundles de JavaScript y CSS, y generará los archivos en la carpeta `frontend/out`.

### Paso 3: Generación del Árbol Dual de Rutas (Dual Routing Mirror)
Para garantizar compatibilidad con servidores que utilicen tanto enlaces planos `.html` como directorios con `index.html`, ejecute el script de post-procesamiento:

```bash
python -c "
import os, shutil
OUT = r'frontend/out'
pages = ['casos', 'mapa', 'reportar', 'pistas', 'login', 'admin']
for p in pages:
    src = os.path.join(OUT, f'{p}.html')
    dest_dir = os.path.join(OUT, p)
    dest_file = os.path.join(dest_dir, 'index.html')
    if os.path.isfile(src):
        os.makedirs(dest_dir, exist_ok=True)
        shutil.copy2(src, dest_file)
print('Estructura dual generada exitosamente!')
"
```

---

## 3. DESPLIEGUE EN SERVIDOR FASTAPI UNIFICADO (PRODUCCIÓN / LOCAL)

### Opción A: Despliegue con Servidor Autónomo (`main.py`)
El archivo `main.py` en la raíz del proyecto está configurado para servir automáticamente los endpoints API y los archivos del frontend estático bajo un único puerto:

```bash
# Iniciar servidor en segundo plano o servicio systemd
uvicorn main:app --host 0.0.0.0 --port 8000 --workers 4
```

### Opción B: Despliegue con Aplicación de Dominio Completa (`backend/app/main.py`)
Si se ejecuta la suite completa con base de datos PostgreSQL:

```bash
cd backend
alembic upgrade head
uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 4
```

El servidor detecta automáticamente el directorio `frontend/out` mediante la variable de entorno `FRONTEND_STATIC_DIR` o por búsqueda en rutas candidatas.

---

## 4. DESPLIEGUE HACIA EL HOSTING REMOTO (`tradescanner.online`)

Para sincronizar la compilación de `frontend/out` con el entorno de alojamiento en `https://creacionvaloria.tradescanner.online`:

```bash
python scratch_deploy.py
```

El script realiza:
1. Creación de la estructura de carpetas en el servidor remoto (`/api/static/folder`).
2. Transmisión incremental de archivos (`/api/static/file`) con verificación de contenido e integridad.
3. Exclusión segura de archivos pesados ya presentes en el servidor (ej. video educativo de 8 MB).

---

## 5. VERIFICACIÓN POST-DESPLIEGUE (SANITY CHECKS)

Ejecute la suite de verificación automatizada:

```bash
python -c "
import urllib.request
urls = [
    'https://creacionvaloria.tradescanner.online/',
    'https://creacionvaloria.tradescanner.online/casos.html',
    'https://creacionvaloria.tradescanner.online/mapa.html',
    'https://creacionvaloria.tradescanner.online/reportar.html',
    'https://creacionvaloria.tradescanner.online/pistas.html',
    'https://creacionvaloria.tradescanner.online/login.html'
]
for u in urls:
    req = urllib.request.Request(u, headers={'User-Agent': 'Mozilla/5.0 SanityCheck'})
    with urllib.request.urlopen(req) as resp:
        print(f'{resp.status} OK: {u}')
"
```

Resultado esperado:
```text
200 OK: https://creacionvaloria.tradescanner.online/
200 OK: https://creacionvaloria.tradescanner.online/casos.html
200 OK: https://creacionvaloria.tradescanner.online/mapa.html
200 OK: https://creacionvaloria.tradescanner.online/reportar.html
200 OK: https://creacionvaloria.tradescanner.online/pistas.html
200 OK: https://creacionvaloria.tradescanner.online/login.html
```

---

## 6. PLAN DE CONTINGENCIA Y ROLLBACK

1. En caso de discrepancia en algún paquete compilado, el frontend puede ser regenerado en menos de 45 segundos con `npm --prefix frontend run build`.
2. Las imágenes y fotografías de personas permanecen custodiadas en `frontend/out/images/avatars` y `backend/app/services/storage_service.py`, conservando su identificador criptográfico inmutable.
3. El archivo `404.html` actúa como salvaguarda visual ante cualquier intento de acceso a rutas obsoletas.
