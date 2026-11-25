import sqlite3

conn = sqlite3.connect("encuentrame_nicaragua.db")
cur = conn.cursor()

print("--- DETALLE DE missing_person_reports ---")
cur.execute("SELECT id, case_number, first_name, last_name, status, is_public, vulnerability_flag, disappearance_date FROM missing_person_reports LIMIT 10")
for r in cur.fetchall():
    print(r)

print("\n--- DISTRIBUCIÓN DE STATUS EN missing_person_reports ---")
cur.execute("SELECT status, count(*) FROM missing_person_reports GROUP BY status")
for r in cur.fetchall():
    print(r)

print("\n--- DETALLE DE report_photos ---")
cur.execute("SELECT id, report_id, file_path, is_primary, is_approved FROM report_photos LIMIT 5")
for r in cur.fetchall():
    print(r)

print("\n--- DETALLE DE confidential_tips ---")
cur.execute("SELECT id, report_id, sighting_date, sighting_location, is_anonymous, status FROM confidential_tips LIMIT 5")
for r in cur.fetchall():
    print(r)

print("\n--- DETALLE DE deletion_requests ---")
cur.execute("SELECT id, report_id, requester_email, reason, status FROM deletion_requests")
for r in cur.fetchall():
    print(r)

print("\n--- DETALLE DE audit_logs ---")
cur.execute("SELECT id, action, entity_type, created_at FROM audit_logs ORDER BY created_at DESC LIMIT 5")
for r in cur.fetchall():
    print(r)

conn.close()
