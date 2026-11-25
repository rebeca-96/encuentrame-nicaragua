import os
import sqlite3
import json

def inspect():
    print("=== INSPECCIÓN DE BASE DE DATOS ===")
    dbs = ["encuentrame_nicaragua.db", "backend/encuentrame_nicaragua.db"]
    for db_path in dbs:
        if os.path.exists(db_path):
            print(f"\nArchivo: {db_path} ({os.path.getsize(db_path):,} bytes)")
            conn = sqlite3.connect(db_path)
            cur = conn.cursor()
            cur.execute("SELECT name FROM sqlite_master WHERE type='table';")
            tables = [r[0] for r in cur.fetchall()]
            print("Tablas encontradas:", tables)
            for t in tables:
                if t != "sqlite_sequence":
                    cur.execute(f"SELECT COUNT(*) FROM [{t}]")
                    count = cur.fetchone()[0]
                    print(f"  [{t}]: {count} registros")
            
            # Verificación de casos
            if "cases" in tables:
                cur.execute("SELECT id, case_number, first_name, last_name, status, is_public FROM cases LIMIT 5")
                print("  Ejemplos de cases:")
                for r in cur.fetchall():
                    print("   ", r)

            # Verificación de usuarios
            if "users" in tables:
                cur.execute("SELECT id, email, role, is_active FROM users LIMIT 5")
                print("  Ejemplos de users:")
                for r in cur.fetchall():
                    print("   ", r)

            conn.close()

    print("\n=== INSPECCIÓN DE CATÁLOGO FRONTEND ===")
    cat_path = r"frontend/src/lib/catalogData.ts"
    if os.path.exists(cat_path):
        with open(cat_path, "r", encoding="utf-8") as f:
            lines = f.readlines()
        print(f"catalogData.ts: {len(lines)} líneas")
        # Chequear si tiene casos hardcoded
        case_ids = [line.strip() for line in lines if "case_number:" in line or "id:" in line]
        print(f"Muestras de identificadores en catalogData.ts: {len(case_ids)} entradas")

    print("\n=== INSPECCIÓN DE API FRONTEND (api.ts) ===")
    api_path = r"frontend/src/lib/api.ts"
    if os.path.exists(api_path):
        with open(api_path, "r", encoding="utf-8") as f:
            api_content = f.read()
        print(f"api.ts length: {len(api_content):,} bytes")
        endpoints = [line.strip() for line in api_content.splitlines() if "fetch(" in line or "axios" in line or "/api/" in line]
        print("Llamadas de API en api.ts:")
        for ep in endpoints[:10]:
            print("  ", ep)

    print("\n=== INSPECCIÓN DE BACKEND APIS ===")
    api_dir = r"backend/app/api/v1"
    if os.path.exists(api_dir):
        files = os.listdir(api_dir)
        print("Módulos en backend/app/api/v1:", files)

if __name__ == "__main__":
    inspect()
