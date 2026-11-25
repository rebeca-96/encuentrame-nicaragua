"""
Catálogo Oficial de la División Político-Administrativa de la República de Nicaragua
Fuente: Instituto Nicaragüense de Estudios Territoriales (INETER) y Ley N.° 59 de División Política Administrativa.
Fecha de actualización del catálogo: Noviembre 2026.
Total: 15 Departamentos + 2 Regiones Autónomas (17 entidades) y 153 Municipios.
"""

from typing import Dict, List, Any
from sqlalchemy.orm import Session
from app.models.entities import Department, Municipality, TerritorialType

OFFICIAL_DIVISIONS: List[Dict[str, Any]] = [
    {
        "name": "Boaco",
        "code": "BOA",
        "type": TerritorialType.DEPARTMENT.value,
        "latitude": 12.4722,
        "longitude": -85.6586,
        "municipalities": [
            {"name": "Boaco", "code": "BOA-01", "latitude": 12.4722, "longitude": -85.6586},
            {"name": "Camoapa", "code": "BOA-02", "latitude": 12.3839, "longitude": -85.5122},
            {"name": "San José de los Remates", "code": "BOA-03", "latitude": 12.6000, "longitude": -85.7600},
            {"name": "San Lorenzo", "code": "BOA-04", "latitude": 12.3781, "longitude": -85.6667},
            {"name": "Santa Lucía", "code": "BOA-05", "latitude": 12.5333, "longitude": -85.7167},
            {"name": "Teustepe", "code": "BOA-06", "latitude": 12.4200, "longitude": -85.7981},
        ]
    },
    {
        "name": "Carazo",
        "code": "CAR",
        "type": TerritorialType.DEPARTMENT.value,
        "latitude": 11.8541,
        "longitude": -86.1994,
        "municipalities": [
            {"name": "Diriamba", "code": "CAR-01", "latitude": 11.8581, "longitude": -86.2392},
            {"name": "Dolores", "code": "CAR-02", "latitude": 11.8558, "longitude": -86.2153},
            {"name": "El Rosario", "code": "CAR-03", "latitude": 11.8419, "longitude": -86.1733},
            {"name": "Jinotepe", "code": "CAR-04", "latitude": 11.8541, "longitude": -86.1994},
            {"name": "La Conquista", "code": "CAR-05", "latitude": 11.7333, "longitude": -86.1928},
            {"name": "La Paz de Carazo", "code": "CAR-06", "latitude": 11.8236, "longitude": -86.1278},
            {"name": "San Marcos", "code": "CAR-07", "latitude": 11.9094, "longitude": -86.2036},
            {"name": "Santa Teresa", "code": "CAR-08", "latitude": 11.8028, "longitude": -86.2144},
        ]
    },
    {
        "name": "Chinandega",
        "code": "CHI",
        "type": TerritorialType.DEPARTMENT.value,
        "latitude": 12.6294,
        "longitude": -87.1311,
        "municipalities": [
            {"name": "Chichigalpa", "code": "CHI-01", "latitude": 12.5775, "longitude": -87.0275},
            {"name": "Chinandega", "code": "CHI-02", "latitude": 12.6294, "longitude": -87.1311},
            {"name": "Cinco Pinos", "code": "CHI-03", "latitude": 13.2300, "longitude": -86.8667},
            {"name": "Corinto", "code": "CHI-04", "latitude": 12.4817, "longitude": -87.1733},
            {"name": "El Realejo", "code": "CHI-05", "latitude": 12.5400, "longitude": -87.1667},
            {"name": "El Viejo", "code": "CHI-06", "latitude": 12.6633, "longitude": -87.1689},
            {"name": "Posoltega", "code": "CHI-07", "latitude": 12.5447, "longitude": -86.9797},
            {"name": "Puerto Morazán", "code": "CHI-08", "latitude": 12.8500, "longitude": -87.1833},
            {"name": "San Francisco del Norte", "code": "CHI-09", "latitude": 13.2000, "longitude": -86.7667},
            {"name": "San Pedro del Norte", "code": "CHI-10", "latitude": 13.2833, "longitude": -86.8833},
            {"name": "Santo Tomás del Norte", "code": "CHI-11", "latitude": 13.1833, "longitude": -86.9167},
            {"name": "Somotillo", "code": "CHI-12", "latitude": 13.0439, "longitude": -86.9069},
            {"name": "Villa Nueva", "code": "CHI-13", "latitude": 12.9667, "longitude": -86.8167},
        ]
    },
    {
        "name": "Chontales",
        "code": "CHO",
        "type": TerritorialType.DEPARTMENT.value,
        "latitude": 12.0620,
        "longitude": -85.3644,
        "municipalities": [
            {"name": "Acoyapa", "code": "CHO-01", "latitude": 11.9703, "longitude": -85.1711},
            {"name": "Comalapa", "code": "CHO-02", "latitude": 12.2833, "longitude": -85.5167},
            {"name": "El Coral", "code": "CHO-03", "latitude": 11.9167, "longitude": -84.5167},
            {"name": "Juigalpa", "code": "CHO-04", "latitude": 12.0620, "longitude": -85.3644},
            {"name": "La Libertad", "code": "CHO-05", "latitude": 12.2167, "longitude": -85.1667},
            {"name": "San Francisco de Cuapa", "code": "CHO-06", "latitude": 12.2667, "longitude": -85.3833},
            {"name": "San Pedro de Lóvago", "code": "CHO-07", "latitude": 12.1333, "longitude": -85.1167},
            {"name": "Santo Domingo", "code": "CHO-08", "latitude": 12.2667, "longitude": -85.0833},
            {"name": "Santo Tomás", "code": "CHO-09", "latitude": 12.0667, "longitude": -85.0833},
            {"name": "Villa Sandino", "code": "CHO-10", "latitude": 12.0500, "longitude": -84.9833},
        ]
    },
    {
        "name": "Estelí",
        "code": "EST",
        "type": TerritorialType.DEPARTMENT.value,
        "latitude": 13.0919,
        "longitude": -86.3538,
        "municipalities": [
            {"name": "Condega", "code": "EST-01", "latitude": 13.3500, "longitude": -86.4000},
            {"name": "Estelí", "code": "EST-02", "latitude": 13.0919, "longitude": -86.3538},
            {"name": "La Trinidad", "code": "EST-03", "latitude": 12.9667, "longitude": -86.2333},
            {"name": "Pueblo Nuevo", "code": "EST-04", "latitude": 13.3833, "longitude": -86.4833},
            {"name": "San Juan de Limay", "code": "EST-05", "latitude": 13.1833, "longitude": -86.6167},
            {"name": "San Nicolás", "code": "EST-06", "latitude": 12.9333, "longitude": -86.3500},
        ]
    },
    {
        "name": "Granada",
        "code": "GRA",
        "type": TerritorialType.DEPARTMENT.value,
        "latitude": 11.9299,
        "longitude": -85.9560,
        "municipalities": [
            {"name": "Diriá", "code": "GRA-01", "latitude": 11.8833, "longitude": -86.0500},
            {"name": "Diriomo", "code": "GRA-02", "latitude": 11.8767, "longitude": -86.0519},
            {"name": "Granada", "code": "GRA-03", "latitude": 11.9299, "longitude": -85.9560},
            {"name": "Nandaime", "code": "GRA-04", "latitude": 11.7569, "longitude": -86.0528},
        ]
    },
    {
        "name": "Jinotega",
        "code": "JIN",
        "type": TerritorialType.DEPARTMENT.value,
        "latitude": 13.0991,
        "longitude": -85.9992,
        "municipalities": [
            {"name": "El Cuá", "code": "JIN-01", "latitude": 13.3667, "longitude": -85.6667},
            {"name": "Jinotega", "code": "JIN-02", "latitude": 13.0991, "longitude": -85.9992},
            {"name": "La Concordia", "code": "JIN-03", "latitude": 13.2000, "longitude": -86.1667},
            {"name": "San José de Bocay", "code": "JIN-04", "latitude": 13.5417, "longitude": -85.5392},
            {"name": "San Rafael del Norte", "code": "JIN-05", "latitude": 13.2167, "longitude": -86.1167},
            {"name": "San Sebastián de Yalí", "code": "JIN-06", "latitude": 13.3000, "longitude": -86.1833},
            {"name": "Santa María de Pantasma", "code": "JIN-07", "latitude": 13.3500, "longitude": -85.9500},
            {"name": "Wiwilí de Jinotega", "code": "JIN-08", "latitude": 13.6167, "longitude": -85.8333},
        ]
    },
    {
        "name": "León",
        "code": "LEO",
        "type": TerritorialType.DEPARTMENT.value,
        "latitude": 12.4379,
        "longitude": -86.8780,
        "municipalities": [
            {"name": "Achuapa", "code": "LEO-01", "latitude": 13.0500, "longitude": -86.5833},
            {"name": "El Jicaral", "code": "LEO-02", "latitude": 12.7333, "longitude": -86.3833},
            {"name": "El Sauce", "code": "LEO-03", "latitude": 12.9333, "longitude": -86.5333},
            {"name": "La Paz Centro", "code": "LEO-04", "latitude": 12.3397, "longitude": -86.6742},
            {"name": "Larreynaga", "code": "LEO-05", "latitude": 12.6833, "longitude": -86.5667},
            {"name": "León", "code": "LEO-06", "latitude": 12.4379, "longitude": -86.8780},
            {"name": "Nagarote", "code": "LEO-07", "latitude": 12.2667, "longitude": -86.5667},
            {"name": "Quezalguaque", "code": "LEO-08", "latitude": 12.5167, "longitude": -86.9000},
            {"name": "Santa Rosa del Peñón", "code": "LEO-09", "latitude": 12.8000, "longitude": -86.3667},
            {"name": "Telica", "code": "LEO-10", "latitude": 12.5167, "longitude": -86.8500},
        ]
    },
    {
        "name": "Madriz",
        "code": "MAD",
        "type": TerritorialType.DEPARTMENT.value,
        "latitude": 13.4862,
        "longitude": -86.5822,
        "municipalities": [
            {"name": "Las Sabanas", "code": "MAD-01", "latitude": 13.3500, "longitude": -86.6167},
            {"name": "Palacagüina", "code": "MAD-02", "latitude": 13.4564, "longitude": -86.4069},
            {"name": "San José de Cusmapa", "code": "MAD-03", "latitude": 13.2833, "longitude": -86.6500},
            {"name": "San Juan de Río Coco", "code": "MAD-04", "latitude": 13.5500, "longitude": -86.1667},
            {"name": "San Lucas", "code": "MAD-05", "latitude": 13.4167, "longitude": -86.6000},
            {"name": "Somoto", "code": "MAD-06", "latitude": 13.4862, "longitude": -86.5822},
            {"name": "Telpaneca", "code": "MAD-07", "latitude": 13.5333, "longitude": -86.2833},
            {"name": "Totogalpa", "code": "MAD-08", "latitude": 13.5628, "longitude": -86.4917},
            {"name": "Yalagüina", "code": "MAD-09", "latitude": 13.4833, "longitude": -86.4833},
        ]
    },
    {
        "name": "Managua",
        "code": "MGA",
        "type": TerritorialType.DEPARTMENT.value,
        "latitude": 12.1364,
        "longitude": -86.2514,
        "municipalities": [
            {"name": "Ciudad Sandino", "code": "MGA-01", "latitude": 12.1583, "longitude": -86.3444},
            {"name": "El Crucero", "code": "MGA-02", "latitude": 11.9833, "longitude": -86.3167},
            {"name": "Managua", "code": "MGA-03", "latitude": 12.1364, "longitude": -86.2514},
            {"name": "Mateare", "code": "MGA-04", "latitude": 12.2333, "longitude": -86.4333},
            {"name": "San Francisco Libre", "code": "MGA-05", "latitude": 12.5000, "longitude": -86.3000},
            {"name": "San Rafael del Sur", "code": "MGA-06", "latitude": 11.8500, "longitude": -86.4333},
            {"name": "Ticuantepe", "code": "MGA-07", "latitude": 12.0225, "longitude": -86.2050},
            {"name": "Tipitapa", "code": "MGA-08", "latitude": 12.1978, "longitude": -86.0967},
            {"name": "Villa El Carmen", "code": "MGA-09", "latitude": 11.9833, "longitude": -86.5000},
        ]
    },
    {
        "name": "Masaya",
        "code": "MAS",
        "type": TerritorialType.DEPARTMENT.value,
        "latitude": 11.9744,
        "longitude": -86.0942,
        "municipalities": [
            {"name": "Catarina", "code": "MAS-01", "latitude": 11.9167, "longitude": -86.0833},
            {"name": "La Concepción", "code": "MAS-02", "latitude": 11.9333, "longitude": -86.1833},
            {"name": "Masatepe", "code": "MAS-03", "latitude": 11.9167, "longitude": -86.1500},
            {"name": "Masaya", "code": "MAS-04", "latitude": 11.9744, "longitude": -86.0942},
            {"name": "Nandasmo", "code": "MAS-05", "latitude": 11.9236, "longitude": -86.1206},
            {"name": "Nindirí", "code": "MAS-06", "latitude": 12.0000, "longitude": -86.1167},
            {"name": "Niquinohomo", "code": "MAS-07", "latitude": 11.9000, "longitude": -86.1000},
            {"name": "San Juan de Oriente", "code": "MAS-08", "latitude": 11.9056, "longitude": -86.0750},
            {"name": "Tisma", "code": "MAS-09", "latitude": 12.0833, "longitude": -86.0167},
        ]
    },
    {
        "name": "Matagalpa",
        "code": "MAT",
        "type": TerritorialType.DEPARTMENT.value,
        "latitude": 12.9256,
        "longitude": -85.9178,
        "municipalities": [
            {"name": "Ciudad Darío", "code": "MAT-01", "latitude": 12.7317, "longitude": -86.1239},
            {"name": "El Tuma - La Dalia", "code": "MAT-02", "latitude": 13.0667, "longitude": -85.7500},
            {"name": "Esquipulas", "code": "MAT-03", "latitude": 12.6667, "longitude": -85.7833},
            {"name": "Matagalpa", "code": "MAT-04", "latitude": 12.9256, "longitude": -85.9178},
            {"name": "Matiguás", "code": "MAT-05", "latitude": 12.8333, "longitude": -85.4667},
            {"name": "Muy Muy", "code": "MAT-06", "latitude": 12.7667, "longitude": -85.6333},
            {"name": "Rancho Grande", "code": "MAT-07", "latitude": 13.2333, "longitude": -85.5500},
            {"name": "Río Blanco", "code": "MAT-08", "latitude": 12.9333, "longitude": -85.2167},
            {"name": "San Dionisio", "code": "MAT-09", "latitude": 12.7667, "longitude": -85.8500},
            {"name": "San Isidro", "code": "MAT-10", "latitude": 12.9333, "longitude": -86.2000},
            {"name": "San Ramón", "code": "MAT-11", "latitude": 12.9228, "longitude": -85.8389},
            {"name": "Sébaco", "code": "MAT-12", "latitude": 12.8550, "longitude": -86.0967},
            {"name": "Terrabona", "code": "MAT-13", "latitude": 12.7333, "longitude": -85.9833},
        ]
    },
    {
        "name": "Nueva Segovia",
        "code": "NSE",
        "type": TerritorialType.DEPARTMENT.value,
        "latitude": 13.6322,
        "longitude": -86.4756,
        "municipalities": [
            {"name": "Ciudad Antigua", "code": "NSE-01", "latitude": 13.6333, "longitude": -86.3000},
            {"name": "Dipilto", "code": "NSE-02", "latitude": 13.7167, "longitude": -86.5167},
            {"name": "El Jícaro", "code": "NSE-03", "latitude": 13.7167, "longitude": -86.1333},
            {"name": "Jalapa", "code": "NSE-04", "latitude": 13.9167, "longitude": -86.1333},
            {"name": "Macuelizo", "code": "NSE-05", "latitude": 13.6500, "longitude": -86.6167},
            {"name": "Mozonte", "code": "NSE-06", "latitude": 13.6667, "longitude": -86.4500},
            {"name": "Murra", "code": "NSE-07", "latitude": 13.7667, "longitude": -86.0167},
            {"name": "Ocotal", "code": "NSE-08", "latitude": 13.6322, "longitude": -86.4756},
            {"name": "Quilalí", "code": "NSE-09", "latitude": 13.5667, "longitude": -86.0333},
            {"name": "San Fernando", "code": "NSE-10", "latitude": 13.6833, "longitude": -86.3167},
            {"name": "Santa María", "code": "NSE-11", "latitude": 13.7500, "longitude": -86.7167},
            {"name": "Wiwilí de Nueva Segovia", "code": "NSE-12", "latitude": 13.6167, "longitude": -85.8333},
        ]
    },
    {
        "name": "Río San Juan",
        "code": "RSJ",
        "type": TerritorialType.DEPARTMENT.value,
        "latitude": 11.1300,
        "longitude": -84.7789,
        "municipalities": [
            {"name": "El Almendro", "code": "RSJ-01", "latitude": 11.6833, "longitude": -84.7167},
            {"name": "El Castillo", "code": "RSJ-02", "latitude": 11.0167, "longitude": -84.3833},
            {"name": "Morrito", "code": "RSJ-03", "latitude": 11.6167, "longitude": -85.0833},
            {"name": "San Carlos", "code": "RSJ-04", "latitude": 11.1300, "longitude": -84.7789},
            {"name": "San Juan de Nicaragua", "code": "RSJ-05", "latitude": 10.9167, "longitude": -83.7000},
            {"name": "San Miguelito", "code": "RSJ-06", "latitude": 11.4000, "longitude": -84.9000},
        ]
    },
    {
        "name": "Rivas",
        "code": "RIV",
        "type": TerritorialType.DEPARTMENT.value,
        "latitude": 11.4372,
        "longitude": -85.8263,
        "municipalities": [
            {"name": "Altagracia", "code": "RIV-01", "latitude": 11.5667, "longitude": -85.5833},
            {"name": "Belén", "code": "RIV-02", "latitude": 11.5000, "longitude": -85.8833},
            {"name": "Buenos Aires", "code": "RIV-03", "latitude": 11.4667, "longitude": -85.8167},
            {"name": "Cárdenas", "code": "RIV-04", "latitude": 11.2000, "longitude": -85.5167},
            {"name": "Moyogalpa", "code": "RIV-05", "latitude": 11.5333, "longitude": -85.6967},
            {"name": "Potosí", "code": "RIV-06", "latitude": 11.4833, "longitude": -85.8500},
            {"name": "Rivas", "code": "RIV-07", "latitude": 11.4372, "longitude": -85.8263},
            {"name": "San Jorge", "code": "RIV-08", "latitude": 11.4556, "longitude": -85.8031},
            {"name": "San Juan del Sur", "code": "RIV-09", "latitude": 11.2500, "longitude": -85.8700},
            {"name": "Tola", "code": "RIV-10", "latitude": 11.3833, "longitude": -85.9333},
        ]
    },
    {
        "name": "Región Autónoma de la Costa Caribe Norte",
        "code": "CCN",
        "type": TerritorialType.AUTONOMOUS_REGION.value,
        "latitude": 14.0351,
        "longitude": -83.3888,
        "municipalities": [
            {"name": "Bonanza", "code": "CCN-01", "latitude": 14.0167, "longitude": -84.5833},
            {"name": "Mulukukú", "code": "CCN-02", "latitude": 13.1667, "longitude": -84.9667},
            {"name": "Prinzapolka", "code": "CCN-03", "latitude": 13.4000, "longitude": -83.5667},
            {"name": "Puerto Cabezas (Bilwi)", "code": "CCN-04", "latitude": 14.0351, "longitude": -83.3888},
            {"name": "Rosita", "code": "CCN-05", "latitude": 13.9167, "longitude": -84.4000},
            {"name": "Siuna", "code": "CCN-06", "latitude": 13.7333, "longitude": -84.7833},
            {"name": "Waslala", "code": "CCN-07", "latitude": 13.3333, "longitude": -85.3833},
            {"name": "Waspam", "code": "CCN-08", "latitude": 14.7333, "longitude": -83.9667},
        ]
    },
    {
        "name": "Región Autónoma de la Costa Caribe Sur",
        "code": "CCS",
        "type": TerritorialType.AUTONOMOUS_REGION.value,
        "latitude": 12.0131,
        "longitude": -83.7635,
        "municipalities": [
            {"name": "Bluefields", "code": "CCS-01", "latitude": 12.0131, "longitude": -83.7635},
            {"name": "Bocana de Paiwas", "code": "CCS-02", "latitude": 12.7833, "longitude": -85.1167},
            {"name": "Corn Island", "code": "CCS-03", "latitude": 12.1667, "longitude": -83.0500},
            {"name": "Desembocadura de Río Grande", "code": "CCS-04", "latitude": 13.0000, "longitude": -83.7667},
            {"name": "El Ayote", "code": "CCS-05", "latitude": 12.1833, "longitude": -84.8667},
            {"name": "El Rama", "code": "CCS-06", "latitude": 12.1594, "longitude": -84.2194},
            {"name": "El Tortuguero", "code": "CCS-07", "latitude": 12.8167, "longitude": -84.2000},
            {"name": "Kukra Hill", "code": "CCS-08", "latitude": 12.2333, "longitude": -83.7500},
            {"name": "La Cruz de Río Grande", "code": "CCS-09", "latitude": 13.1167, "longitude": -84.1833},
            {"name": "Laguna de Perlas", "code": "CCS-10", "latitude": 12.3500, "longitude": -83.6667},
            {"name": "Muelle de los Bueyes", "code": "CCS-11", "latitude": 12.0667, "longitude": -84.5333},
            {"name": "Nueva Guinea", "code": "CCS-12", "latitude": 11.6875, "longitude": -84.4561},
        ]
    }
]

def seed_nicaragua_geography(db: Session) -> Dict[str, int]:
    """
    Carga inicial y sincronización idempotente del catálogo territorial nacional.
    Inserta o actualiza departamentos y municipios sin generar duplicados.
    """
    departments_synced = 0
    municipalities_synced = 0

    for div_data in OFFICIAL_DIVISIONS:
        # Check or create Department
        dept = db.query(Department).filter(
            (Department.code == div_data["code"]) | (Department.name == div_data["name"])
        ).first()

        if not dept:
            dept = Department(
                name=div_data["name"],
                code=div_data["code"],
                type=div_data["type"],
                latitude=div_data["latitude"],
                longitude=div_data["longitude"],
                is_active=True
            )
            db.add(dept)
            db.flush()
            departments_synced += 1
        else:
            # Update metadata to ensure official correctness
            dept.name = div_data["name"]
            dept.code = div_data["code"]
            dept.type = div_data["type"]
            dept.latitude = div_data["latitude"]
            dept.longitude = div_data["longitude"]
            dept.is_active = True
            db.flush()
            departments_synced += 1

        # Process municipalities
        for mun_data in div_data["municipalities"]:
            mun = db.query(Municipality).filter(
                (Municipality.code == mun_data["code"]) |
                ((Municipality.department_id == dept.id) & (Municipality.name == mun_data["name"]))
            ).first()

            if not mun:
                mun = Municipality(
                    department_id=dept.id,
                    name=mun_data["name"],
                    code=mun_data["code"],
                    latitude=mun_data["latitude"],
                    longitude=mun_data["longitude"],
                    is_active=True
                )
                db.add(mun)
                municipalities_synced += 1
            else:
                mun.name = mun_data["name"]
                mun.code = mun_data["code"]
                mun.latitude = mun_data["latitude"]
                mun.longitude = mun_data["longitude"]
                mun.is_active = True
                municipalities_synced += 1

    db.commit()
    return {
        "departments_count": departments_synced,
        "municipalities_count": municipalities_synced
    }
