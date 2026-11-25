import subprocess
import os
import time

EDGE_PATH = r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"
BASE_URL = "https://creacionvaloria.tradescanner.online"

DESKTOP_DIR = r"C:\Users\User\Documents\Valor IA\EncuentrameNicaragua\ENTREGA_FINAL_ACADEMICA\04_Diseno_Visual\Capturas_Escritorio"
MOVIL_DIR = r"C:\Users\User\Documents\Valor IA\EncuentrameNicaragua\ENTREGA_FINAL_ACADEMICA\04_Diseno_Visual\Capturas_Movil"

PAGES = [
    ("01_Inicio", ""),
    ("02_Catalogo", "casos.html"),
    ("03_Ficha_Detalle", "casos/EN-2026-0001.html"),
    ("04_Mapa", "mapa.html"),
    ("05_Reportar", "reportar.html"),
    ("06_Pistas", "pistas.html"),
    ("07_Login", "login.html"),
    ("08_Admin", "admin.html")
]

def capture():
    print("Iniciando captura de pantallas...")
    
    # 1. Desktop 1280x800
    for name, route in PAGES:
        target_file = os.path.join(DESKTOP_DIR, f"{name}_Desktop.png")
        url = f"{BASE_URL}/{route}" if route else BASE_URL
        print(f"Capturando Desktop: {name} -> {url}")
        args = [
            EDGE_PATH,
            "--headless",
            "--disable-gpu",
            "--hide-scrollbars",
            f"--window-size=1280,800",
            f"--screenshot={target_file}",
            url
        ]
        res = subprocess.run(args, capture_output=True, timeout=30)
        if os.path.exists(target_file):
            print(f"  OK ({os.path.getsize(target_file):,} bytes)")
        else:
            print(f"  FALLÓ {name}")
        time.sleep(1)

    # 2. Movil 375x812 (iPhone X/12/13/14 viewport)
    for name, route in PAGES:
        target_file = os.path.join(MOVIL_DIR, f"{name}_Movil.png")
        url = f"{BASE_URL}/{route}" if route else BASE_URL
        print(f"Capturando Movil: {name} -> {url}")
        args = [
            EDGE_PATH,
            "--headless",
            "--disable-gpu",
            "--hide-scrollbars",
            f"--window-size=375,812",
            f"--screenshot={target_file}",
            url
        ]
        res = subprocess.run(args, capture_output=True, timeout=30)
        if os.path.exists(target_file):
            print(f"  OK ({os.path.getsize(target_file):,} bytes)")
        else:
            print(f"  FALLÓ {name}")
        time.sleep(1)

    print("Captura finalizada exitosamente.")

if __name__ == "__main__":
    capture()
