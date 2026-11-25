from typing import List, Dict, Optional, Tuple, Any
from app.core.seed_geography import OFFICIAL_DIVISIONS

# Source of truth: 15 Departments + 2 Autonomous Regions (17) and 153 Municipalities
# Verificado según INETER y Ley N.° 59 de División Política Administrativa de Nicaragua

NICARAGUA_GEOGRAPHY: Dict[str, Dict[str, Any]] = {}

# Build geography dictionary from official divisions
for div in OFFICIAL_DIVISIONS:
    dept_name = div["name"]
    NICARAGUA_GEOGRAPHY[dept_name] = {
        "code": div["code"],
        "type": div["type"],
        "lat": div["latitude"],
        "lng": div["longitude"],
        "municipalities": [m["name"] for m in div["municipalities"]],
        "municipality_details": div["municipalities"]
    }

# Department alias mapping for flexible lookups
DEPARTMENT_ALIASES: Dict[str, str] = {
    "costa caribe norte": "Región Autónoma de la Costa Caribe Norte",
    "costa caribe norte (raccn)": "Región Autónoma de la Costa Caribe Norte",
    "raccn": "Región Autónoma de la Costa Caribe Norte",
    "region autonoma de la costa caribe norte": "Región Autónoma de la Costa Caribe Norte",
    "costa caribe sur": "Región Autónoma de la Costa Caribe Sur",
    "costa caribe sur (raccs)": "Región Autónoma de la Costa Caribe Sur",
    "raccs": "Región Autónoma de la Costa Caribe Sur",
    "region autonoma de la costa caribe sur": "Región Autónoma de la Costa Caribe Sur",
    "rio san juan": "Río San Juan",
    "leon": "León",
    "esteli": "Estelí"
}

def normalize_department_name(department: str) -> Optional[str]:
    """Normaliza y resuelve el nombre canónico de una demarcación territorial."""
    if not department:
        return None
    cleaned = department.strip()
    if cleaned in NICARAGUA_GEOGRAPHY:
        return cleaned
    lower_cleaned = cleaned.lower()
    if lower_cleaned in DEPARTMENT_ALIASES:
        return DEPARTMENT_ALIASES[lower_cleaned]
    for official_name in NICARAGUA_GEOGRAPHY.keys():
        if official_name.lower() == lower_cleaned:
            return official_name
    return None

def get_departments() -> List[str]:
    """Retorna la lista de los 15 departamentos y 2 regiones autónomas oficiales."""
    return list(NICARAGUA_GEOGRAPHY.keys())

def get_municipalities(department: str) -> List[str]:
    """Retorna los municipios oficiales correspondientes a un departamento o región autónoma."""
    canonical_dept = normalize_department_name(department)
    if canonical_dept and canonical_dept in NICARAGUA_GEOGRAPHY:
        return NICARAGUA_GEOGRAPHY[canonical_dept]["municipalities"]
    return []

def get_approximate_coords(department: str, municipality: Optional[str] = None) -> Tuple[float, float]:
    """
    Retorna coordenadas aproximadas a nivel de municipio o departamento.
    Salvaguarda la privacidad de las personas al no emitir nunca coordenadas domiciliarias exactas.
    """
    canonical_dept = normalize_department_name(department)
    if not canonical_dept or canonical_dept not in NICARAGUA_GEOGRAPHY:
        return (12.1364, -86.2514)  # Default Managua

    dept_info = NICARAGUA_GEOGRAPHY[canonical_dept]
    if municipality:
        mun_clean = municipality.strip().lower()
        for m in dept_info.get("municipality_details", []):
            if m["name"].lower() == mun_clean:
                return (m["latitude"], m["longitude"])
                
    return (dept_info["lat"], dept_info["lng"])

def validate_nicaragua_coordinates(latitude: float, longitude: float) -> bool:
    """
    Verifica que las coordenadas se encuentren dentro de los límites territoriales de Nicaragua.
    Latitud: 10.70 a 15.10 | Longitud: -87.70 a -82.50
    """
    return (10.70 <= latitude <= 15.10) and (-87.70 <= longitude <= -82.50)
