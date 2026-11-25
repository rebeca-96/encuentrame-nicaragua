import os
import urllib.request
import urllib.parse
import time
import ssl

BASE_URL = "https://creacionvaloria.tradescanner.online"
OUT_DIR = r"C:\Users\User\Documents\Valor IA\EncuentrameNicaragua\frontend\out"
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Accept": "*/*",
}

def deploy():
    print(f"=== INICIANDO DESPLIEGUE A PRODUCCIÓN ===")
    print(f"Origen: {OUT_DIR}")
    print(f"Destino: {BASE_URL}")

    ctx = ssl.create_default_context()

    # 1. Recopilar carpetas y archivos
    dirs = []
    files = []
    for root, d_names, f_names in os.walk(OUT_DIR):
        for d in d_names:
            full_d = os.path.join(root, d)
            rel_d = os.path.relpath(full_d, OUT_DIR).replace("\\", "/")
            dirs.append(rel_d)
        for f in f_names:
            full_f = os.path.join(root, f)
            rel_f = os.path.relpath(full_f, OUT_DIR).replace("\\", "/")
            files.append((full_f, rel_f))

    dirs.sort(key=lambda x: (x.count("/"), len(x)))
    print(f"1. Creando/Verificando {len(dirs)} carpetas en el hosting...")
    created_dirs = 0
    for d in dirs:
        url = f"{BASE_URL}/api/static/folder?path={urllib.parse.quote(d)}"
        req = urllib.request.Request(url, data=b"", headers=HEADERS, method="POST")
        try:
            with urllib.request.urlopen(req, timeout=10, context=ctx) as resp:
                created_dirs += 1
        except Exception:
            pass
    print(f"   Carpetas sincronizadas: {created_dirs}/{len(dirs)}")

    # 2. Subir archivos
    total = len(files)
    print(f"\n2. Subiendo {total} archivos a producción...")
    success_count = 0
    skip_count = 0
    fail_count = 0

    for i, (full_f, rel_f) in enumerate(files, 1):
        if rel_f == "Personas_Desaparecidas_Nicaragua.mp4":
            print(f"[{i}/{total}] SKIP (archivo pesado ya existente): {rel_f}")
            skip_count += 1
            continue

        url = f"{BASE_URL}/api/static/file?path={urllib.parse.quote(rel_f)}"
        with open(full_f, "rb") as fp:
            data = fp.read()

        req = urllib.request.Request(url, data=data, headers=HEADERS, method="PUT")
        try:
            with urllib.request.urlopen(req, timeout=20, context=ctx) as resp:
                success_count += 1
                if i % 10 == 0 or i == total or not rel_f.startswith("_next"):
                    print(f"[{i}/{total}] OK: {rel_f} ({len(data):,} bytes)")
        except Exception as e:
            time.sleep(1)
            try:
                with urllib.request.urlopen(req, timeout=25, context=ctx) as resp:
                    success_count += 1
                    print(f"[{i}/{total}] REINTENTO OK: {rel_f}")
            except Exception as e2:
                fail_count += 1
                print(f"[{i}/{total}] FALLÓ: {rel_f} -> {e2}")

    print(f"\n=== RESUMEN DEL DESPLIEGUE ===")
    print(f"Total archivos: {total}")
    print(f"Exitosos: {success_count}")
    print(f"Omitidos: {skip_count}")
    print(f"Fallidos: {fail_count}")

    # 3. Verificación de rutas
    print("\n3. Verificando rutas en producción:")
    test_routes = [
        "",
        "casos.html",
        "mapa.html",
        "reportar.html",
        "pistas.html",
        "login.html",
        "admin.html",
        "casos/case-01.html",
        "casos/EN-2026-0001.html",
        "images/avatars/avatar_en-2026-0001.webp"
    ]
    for r in test_routes:
        test_url = f"{BASE_URL}/{r}"
        req = urllib.request.Request(test_url, headers=HEADERS, method="GET")
        try:
            with urllib.request.urlopen(req, timeout=10, context=ctx) as resp:
                print(f"   [GET] {test_url} -> {resp.status} OK")
        except Exception as e:
            print(f"   [GET] {test_url} -> ERROR: {e}")

if __name__ == "__main__":
    deploy()
