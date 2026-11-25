import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.core.security import create_access_token
from app.models.entities import Department, Municipality, User, UserRole
from app.core.security import get_password_hash
from tests.conftest import TestingSessionLocal

client = TestClient(app)

admin_user_id = None
citizen_user_id = None

@pytest.fixture(scope="module", autouse=True)
def setup_geo_users():
    global admin_user_id, citizen_user_id
    with TestingSessionLocal() as db:
        admin = db.query(User).filter(User.email == "admin_geo@encuentrame.ni").first()
        if not admin:
            admin = User(
                email="admin_geo@encuentrame.ni",
                password_hash=get_password_hash("AdminPass123!"),
                full_name="Admin Geo Test",
                role=UserRole.ADMIN.value,
                is_active=True,
                is_verified=True
            )
            db.add(admin)
            db.commit()
            db.refresh(admin)
        admin_user_id = admin.id

        citizen = db.query(User).filter(User.email == "citizen_geo@gmail.com").first()
        if not citizen:
            citizen = User(
                email="citizen_geo@gmail.com",
                password_hash=get_password_hash("CitizenPass123!"),
                full_name="Ciudadano Test",
                role=UserRole.CITIZEN.value,
                is_active=True,
                is_verified=True
            )
            db.add(citizen)
            db.commit()
            db.refresh(citizen)
        citizen_user_id = citizen.id

def get_admin_token() -> str:
    return create_access_token(
        subject=admin_user_id, 
        role=UserRole.ADMIN.value
    )

def get_citizen_token() -> str:
    return create_access_token(
        subject=citizen_user_id, 
        role=UserRole.CITIZEN.value
    )


def test_01_backend_health_and_root():
    """1. El backend responde correctamente."""
    res = client.get("/health")
    assert res.status_code == 200
    assert res.json()["status"] == "healthy"

    res_root = client.get("/")
    assert res_root.status_code == 200
    assert "Bienvenido" in res_root.json()["message"]


def test_02_get_departments_endpoint():
    """2. El endpoint de departamentos funciona y soporta formatos."""
    # Formato objetos
    res_obj = client.get("/api/v1/locations/departments")
    assert res_obj.status_code == 200
    departments = res_obj.json()
    assert isinstance(departments, list)
    assert len(departments) == 17
    assert "name" in departments[0]
    assert "code" in departments[0]
    assert "latitude" in departments[0]

    # Formato nombres planos
    res_names = client.get("/api/v1/locations/departments?format=names")
    assert res_names.status_code == 200
    dept_names = res_names.json()
    assert isinstance(dept_names, list)
    assert len(dept_names) == 17
    assert "Managua" in dept_names
    assert "Matagalpa" in dept_names


def test_03_get_municipalities_endpoint():
    """3. El endpoint de municipios funciona con filtros."""
    res = client.get("/api/v1/locations/municipalities?department=Matagalpa")
    assert res.status_code == 200
    muns = res.json()
    assert isinstance(muns, list)
    assert len(muns) == 13
    mun_names = [m["name"] if isinstance(m, dict) else m for m in muns]
    assert "Sébaco" in mun_names
    assert "Matagalpa" in mun_names


def test_04_seventeen_territorial_entities():
    """4. Existen exactamente 17 entidades territoriales de primer nivel en el catálogo oficial."""
    with TestingSessionLocal() as db:
        depts = db.query(Department).all()
        assert len(depts) == 17
        
        # 15 departamentos y 2 regiones autónomas
        standard_depts = [d for d in depts if d.type == "department"]
        auto_regions = [d for d in depts if d.type == "autonomous_region"]
        
        assert len(standard_depts) == 15
        assert len(auto_regions) == 2
        
        region_names = [r.name for r in auto_regions]
        assert "Región Autónoma de la Costa Caribe Norte" in region_names
        assert "Región Autónoma de la Costa Caribe Sur" in region_names


def test_05_one_hundred_fifty_three_municipalities():
    """5. El catálogo contiene exactamente 153 municipios válidos."""
    with TestingSessionLocal() as db:
        total_muns = db.query(Municipality).count()
        assert total_muns == 153


def test_06_municipalities_belong_to_correct_entities():
    """6. Cada municipio pertenece a la entidad territorial correcta."""
    with TestingSessionLocal() as db:
        # Masaya debe tener 9 municipios oficiales (incluyendo Nandasmo, sin Diriomo/Diriá)
        masaya = db.query(Department).filter(Department.name == "Masaya").first()
        assert masaya is not None
        masaya_muns = [m.name for m in masaya.municipalities]
        assert len(masaya_muns) == 9
        assert "Nandasmo" in masaya_muns
        assert "Diriomo" not in masaya_muns

        # Granada debe tener 4 municipios (Granada, Nandaime, Diriomo, Diriá)
        granada = db.query(Department).filter(Department.name == "Granada").first()
        assert granada is not None
        granada_muns = [m.name for m in granada.municipalities]
        assert len(granada_muns) == 4
        assert "Diriomo" in granada_muns
        assert "Diriá" in granada_muns

        # Costa Caribe Sur debe contener 12 municipios (incluyendo El Ayote)
        raccs = db.query(Department).filter(Department.code == "CCS").first()
        assert raccs is not None
        raccs_muns = [m.name for m in raccs.municipalities]
        assert len(raccs_muns) == 12
        assert "El Ayote" in raccs_muns


def test_07_no_duplicate_codes_or_names():
    """7. No existen códigos ni nombres duplicados dentro de la misma demarcación."""
    with TestingSessionLocal() as db:
        dept_codes = [d.code for d in db.query(Department).all()]
        assert len(dept_codes) == len(set(dept_codes))

        mun_codes = [m.code for m in db.query(Municipality).all()]
        assert len(mun_codes) == len(set(mun_codes))


def test_08_selectors_load_real_data():
    """8. Los selectores cargan información real tanto en formato plano como de objetos."""
    res = client.get("/api/v1/locations/departments?format=names")
    names = res.json()
    assert "Chinandega" in names
    assert "León" in names
    assert "Rivas" in names


def test_09_dependent_filters():
    """9. Los filtros dependientes funcionan correctamente."""
    # Al pedir Boaco retorna sus 6 municipios
    res_boaco = client.get("/api/v1/locations/municipalities?department=Boaco&format=names")
    assert res_boaco.status_code == 200
    boaco_muns = res_boaco.json()
    assert len(boaco_muns) == 6
    assert "Camoapa" in boaco_muns
    assert "Santa Lucía" in boaco_muns

    # Al pedir Estelí retorna sus 6 municipios
    res_esteli = client.get("/api/v1/locations/municipalities?department=Estelí&format=names")
    assert res_esteli.status_code == 200
    esteli_muns = res_esteli.json()
    assert len(esteli_muns) == 6
    assert "Condega" in esteli_muns


def test_10_network_and_not_found_handling():
    """10. Los errores de no encontrado o identificadores inválidos se manejan con códigos limpios."""
    res_404_dept = client.get("/api/v1/locations/departments/nonexistent-id-999")
    assert res_404_dept.status_code == 404

    res_404_mun = client.get("/api/v1/locations/municipalities/nonexistent-mun-999")
    assert res_404_mun.status_code == 404


def test_11_form_validations_reject_invalid_geo_data():
    """11. Los formularios rechazan coordenadas fuera de Nicaragua y códigos duplicados."""
    admin_token = get_admin_token()

    # Intento de crear departamento con coordenadas en Europa (lat 48, lon 2) -> debe ser rechazado
    res_invalid_coords = client.post(
        "/api/v1/locations/departments",
        headers={"Authorization": f"Bearer {admin_token}"},
        json={
            "name": "Departamento Ficticio",
            "code": "FIC",
            "type": "department",
            "latitude": 48.8566,
            "longitude": 2.3522
        }
    )
    assert res_invalid_coords.status_code == 422

    # Intento de duplicar código existente 'MGA'
    res_duplicate_code = client.post(
        "/api/v1/locations/departments",
        headers={"Authorization": f"Bearer {admin_token}"},
        json={
            "name": "Managua Clonada",
            "code": "MGA",
            "type": "department",
            "latitude": 12.1364,
            "longitude": -86.2514
        }
    )
    assert res_duplicate_code.status_code in [409, 422]


def test_12_unauthorized_users_cannot_modify_catalog():
    """12. Los usuarios anónimos o ciudadanos no pueden alterar el catálogo oficial (RBAC)."""
    # Anónimo intentando crear
    res_anon = client.post(
        "/api/v1/locations/departments",
        json={
            "name": "Hack Dept",
            "code": "HCK",
            "type": "department",
            "latitude": 12.1,
            "longitude": -86.2
        }
    )
    assert res_anon.status_code in [401, 403]

    # Ciudadano intentando crear
    citizen_token = get_citizen_token()
    res_citizen = client.post(
        "/api/v1/locations/departments",
        headers={"Authorization": f"Bearer {citizen_token}"},
        json={
            "name": "Hack Citizen Dept",
            "code": "HCK2",
            "type": "department",
            "latitude": 12.1,
            "longitude": -86.2
        }
    )
    assert res_citizen.status_code == 403


def test_13_map_aggregated_endpoint_and_filters():
    """13. El mapa carga correctamente y filtra por departamento y municipio."""
    res_map = client.get("/api/v1/locations/map-aggregated")
    assert res_map.status_code == 200
    points = res_map.json()
    assert isinstance(points, list)

    # Filtrar por departamento
    res_dept_map = client.get("/api/v1/locations/map-aggregated?department=Managua")
    assert res_dept_map.status_code == 200
    mga_points = res_dept_map.json()
    for pt in mga_points:
        assert pt["department"] == "Managua"


def test_14_reports_validate_territorial_consistency():
    """14. Los reportes exigen coherencia estricta entre departamento y municipio."""
    from datetime import datetime, timezone
    from app.schemas.schemas import ReportCreate
    
    # Incoherente: Managua con municipio Estelí -> debe fallar
    with pytest.raises(Exception):
        ReportCreate(
            first_name="Carlos",
            last_name="García",
            age_at_disappearance=25,
            gender="male",
            disappearance_date=datetime(2026, 1, 1, 12, 0, tzinfo=timezone.utc),
            department="Managua",
            municipality="Estelí", # Incoherente
            circumstances="Desapareció en viaje",
            reporter_relationship="Hermano",
            id_doc_number="001-010190-0001A",
            accepted_terms=True
        )


def test_15_geographic_summary_endpoint():
    """15. El resumen territorial devuelve estadísticas exactas de Nicaragua."""
    res = client.get("/api/v1/locations/summary")
    assert res.status_code == 200
    data = res.json()
    assert data["total_departments"] == 17
    assert data["total_municipalities"] == 153
    assert data["active_departments"] == 17
    assert data["active_municipalities"] == 153
    assert "INETER" in data["source"]
