/**
 * Catálogo Oficial de la División Político-Administrativa de la República de Nicaragua.
 * Total: 15 Departamentos + 2 Regiones Autónomas (17 entidades) y 153 Municipios.
 * Fuente: INETER / INIDE y Ley N.° 59 de Nicaragua.
 */

export const OFFICIAL_NICARAGUA_DEPARTMENTS: string[] = [
  "Boaco",
  "Carazo",
  "Chinandega",
  "Chontales",
  "Estelí",
  "Granada",
  "Jinotega",
  "León",
  "Madriz",
  "Managua",
  "Masaya",
  "Matagalpa",
  "Nueva Segovia",
  "Región Autónoma de la Costa Caribe Norte",
  "Región Autónoma de la Costa Caribe Sur",
  "Rivas",
  "Río San Juan"
];

export const OFFICIAL_NICARAGUA_MUNICIPALITIES: Record<string, string[]> = {
  "Boaco": [
    "Boaco",
    "Camoapa",
    "San José de los Remates",
    "San Lorenzo",
    "Santa Lucía",
    "Teustepe"
  ],
  "Carazo": [
    "Diriamba",
    "Dolores",
    "El Rosario",
    "Jinotepe",
    "La Conquista",
    "La Paz de Carazo",
    "San Marcos",
    "Santa Teresa"
  ],
  "Chinandega": [
    "Chichigalpa",
    "Chinandega",
    "Cinco Pinos",
    "Corinto",
    "El Realejo",
    "El Viejo",
    "Posoltega",
    "Puerto Morazán",
    "San Francisco del Norte",
    "San Pedro del Norte",
    "Santo Tomás del Norte",
    "Somotillo",
    "Villa Nueva"
  ],
  "Chontales": [
    "Acoyapa",
    "Comalapa",
    "El Coral",
    "Juigalpa",
    "La Libertad",
    "San Francisco de Cuapa",
    "San Pedro de Lóvago",
    "Santo Domingo",
    "Santo Tomás",
    "Villa Sandino"
  ],
  "Estelí": [
    "Condega",
    "Estelí",
    "La Trinidad",
    "Pueblo Nuevo",
    "San Juan de Limay",
    "San Nicolás"
  ],
  "Granada": [
    "Diriá",
    "Diriomo",
    "Granada",
    "Nandaime"
  ],
  "Jinotega": [
    "El Cuá",
    "Jinotega",
    "La Concordia",
    "San José de Bocay",
    "San Rafael del Norte",
    "San Sebastián de Yalí",
    "Santa María de Pantasma",
    "Wiwilí de Jinotega"
  ],
  "León": [
    "Achuapa",
    "El Jicaral",
    "El Sauce",
    "La Paz Centro",
    "Larreynaga",
    "León",
    "Nagarote",
    "Quezalguaque",
    "Santa Rosa del Peñón",
    "Telica"
  ],
  "Madriz": [
    "Las Sabanas",
    "Palacagüina",
    "San José de Cusmapa",
    "San Juan de Río Coco",
    "San Lucas",
    "Somoto",
    "Telpaneca",
    "Totogalpa",
    "Yalagüina"
  ],
  "Managua": [
    "Ciudad Sandino",
    "El Crucero",
    "Managua",
    "Mateare",
    "San Francisco Libre",
    "San Rafael del Sur",
    "Ticuantepe",
    "Tipitapa",
    "Villa El Carmen"
  ],
  "Masaya": [
    "Catarina",
    "La Concepción",
    "Masatepe",
    "Masaya",
    "Nandasmo",
    "Nindirí",
    "Niquinohomo",
    "San Juan de Oriente",
    "Tisma"
  ],
  "Matagalpa": [
    "Ciudad Darío",
    "El Tuma - La Dalia",
    "Esquipulas",
    "Matagalpa",
    "Matiguás",
    "Muy Muy",
    "Rancho Grande",
    "Río Blanco",
    "San Dionisio",
    "San Isidro",
    "San Ramón",
    "Sébaco",
    "Terrabona"
  ],
  "Nueva Segovia": [
    "Ciudad Antigua",
    "Dipilto",
    "El Jícaro",
    "Jalapa",
    "Macuelizo",
    "Mozonte",
    "Murra",
    "Ocotal",
    "Quilalí",
    "San Fernando",
    "Santa María",
    "Wiwilí de Nueva Segovia"
  ],
  "Región Autónoma de la Costa Caribe Norte": [
    "Bonanza",
    "Mulukukú",
    "Prinzapolka",
    "Puerto Cabezas (Bilwi)",
    "Rosita",
    "Siuna",
    "Waslala",
    "Waspam"
  ],
  "Región Autónoma de la Costa Caribe Sur": [
    "Bluefields",
    "Bocana de Paiwas",
    "Corn Island",
    "Desembocadura de Río Grande",
    "El Ayote",
    "El Rama",
    "El Tortuguero",
    "Kukra Hill",
    "La Cruz de Río Grande",
    "Laguna de Perlas",
    "Muelle de los Bueyes",
    "Nueva Guinea"
  ],
  "Rivas": [
    "Altagracia",
    "Belén",
    "Buenos Aires",
    "Cárdenas",
    "Moyogalpa",
    "Potosí",
    "Rivas",
    "San Jorge",
    "San Juan del Sur",
    "Tola"
  ],
  "Río San Juan": [
    "El Almendro",
    "El Castillo",
    "Morrito",
    "San Carlos",
    "San Juan de Nicaragua",
    "San Miguelito"
  ]
};

export function getLocalDepartments(): string[] {
  return [...OFFICIAL_NICARAGUA_DEPARTMENTS];
}

export function getLocalMunicipalities(department: string): string[] {
  if (!department) return [];
  // Búsqueda insensible a mayúsculas/minúsculas y espacios
  const cleanDept = department.trim().toLowerCase();
  for (const [deptName, munis] of Object.entries(OFFICIAL_NICARAGUA_MUNICIPALITIES)) {
    if (deptName.toLowerCase() === cleanDept) {
      return [...munis];
    }
  }
  return OFFICIAL_NICARAGUA_MUNICIPALITIES[department] || [];
}

export const DEPARTMENT_COORDINATES: Record<string, { lat: number; lng: number }> = {
  "Boaco": { lat: 12.4722, lng: -85.6586 },
  "Carazo": { lat: 11.8541, lng: -86.1994 },
  "Chinandega": { lat: 12.6294, lng: -87.1311 },
  "Chontales": { lat: 12.0620, lng: -85.3644 },
  "Estelí": { lat: 13.0919, lng: -86.3538 },
  "Granada": { lat: 11.9299, lng: -85.9560 },
  "Jinotega": { lat: 13.0991, lng: -85.9992 },
  "León": { lat: 12.4379, lng: -86.8780 },
  "Madriz": { lat: 13.4862, lng: -86.5822 },
  "Managua": { lat: 12.1364, lng: -86.2514 },
  "Masaya": { lat: 11.9744, lng: -86.0942 },
  "Matagalpa": { lat: 12.9256, lng: -85.9178 },
  "Nueva Segovia": { lat: 13.6322, lng: -86.4756 },
  "Región Autónoma de la Costa Caribe Norte": { lat: 14.0351, lng: -83.3888 },
  "Región Autónoma de la Costa Caribe Sur": { lat: 12.0131, lng: -83.7635 },
  "Rivas": { lat: 11.4372, lng: -85.8263 },
  "Río San Juan": { lat: 11.1300, lng: -84.7789 },
};

export const INITIAL_MAP_POINTS: Array<{
  id: string;
  case_number: string;
  full_name: string;
  age_at_disappearance: number;
  gender: string;
  department: string;
  municipality: string;
  disappearance_date: string;
  approximate_latitude: number;
  approximate_longitude: number;
  is_minor: boolean;
  status: string;
}> = [
  {
    id: "case-01",
    case_number: "EN-2026-0001",
    full_name: "Mateo Andrés García Centeno",
    age_at_disappearance: 14,
    gender: "male",
    department: "Managua",
    municipality: "Ciudad Sandino",
    disappearance_date: "2026-11-16T15:30:00Z",
    approximate_latitude: 12.1583,
    approximate_longitude: -86.3444,
    is_minor: true,
    status: "published"
  },
  {
    id: "case-02",
    case_number: "EN-2026-0002",
    full_name: "Valeria Nicole Pérez Fonseca",
    age_at_disappearance: 17,
    gender: "female",
    department: "Matagalpa",
    municipality: "Sébaco",
    disappearance_date: "2026-11-14T09:15:00Z",
    approximate_latitude: 12.8550,
    approximate_longitude: -86.0967,
    is_minor: true,
    status: "published"
  },
  {
    id: "case-03",
    case_number: "EN-2026-0003",
    full_name: "Don Manuel de Jesús Rocha Blandón",
    age_at_disappearance: 73,
    gender: "male",
    department: "León",
    municipality: "León",
    disappearance_date: "2026-11-17T07:00:00Z",
    approximate_latitude: 12.4379,
    approximate_longitude: -86.8780,
    is_minor: false,
    status: "published"
  },
  {
    id: "case-04",
    case_number: "EN-2026-0004",
    full_name: "Yader Francisco Gutiérrez Marenco",
    age_at_disappearance: 29,
    gender: "male",
    department: "Chinandega",
    municipality: "El Viejo",
    disappearance_date: "2026-11-12T18:00:00Z",
    approximate_latitude: 12.6633,
    approximate_longitude: -87.1689,
    is_minor: false,
    status: "published"
  },
  {
    id: "case-05",
    case_number: "EN-2026-0005",
    full_name: "Lucía Esperanza Solís Jarquín",
    age_at_disappearance: 16,
    gender: "female",
    department: "Estelí",
    municipality: "Estelí",
    disappearance_date: "2026-11-15T13:45:00Z",
    approximate_latitude: 13.0919,
    approximate_longitude: -86.3538,
    is_minor: true,
    status: "published"
  },
  {
    id: "case-06",
    case_number: "EN-2026-0006",
    full_name: "José Ramón Calero Bermúdez",
    age_at_disappearance: 42,
    gender: "male",
    department: "Carazo",
    municipality: "Jinotepe",
    disappearance_date: "2026-11-11T16:20:00Z",
    approximate_latitude: 11.8541,
    approximate_longitude: -86.1994,
    is_minor: false,
    status: "published"
  },
  {
    id: "case-07",
    case_number: "EN-2026-0007",
    full_name: "Adriana Marcela Tinoco Rivas",
    age_at_disappearance: 21,
    gender: "female",
    department: "Chontales",
    municipality: "Juigalpa",
    disappearance_date: "2026-11-10T11:00:00Z",
    approximate_latitude: 12.0620,
    approximate_longitude: -85.3644,
    is_minor: false,
    status: "published"
  },
  {
    id: "case-08",
    case_number: "EN-2026-0008",
    full_name: "Carlos Alberto Membreño Ruiz",
    age_at_disappearance: 35,
    gender: "male",
    department: "Granada",
    municipality: "Granada",
    disappearance_date: "2026-11-13T20:10:00Z",
    approximate_latitude: 11.9299,
    approximate_longitude: -85.9560,
    is_minor: false,
    status: "published"
  },
  {
    id: "case-09",
    case_number: "EN-2026-0009",
    full_name: "Kenia Jamileth López Obando",
    age_at_disappearance: 19,
    gender: "female",
    department: "Masaya",
    municipality: "Nindirí",
    disappearance_date: "2026-11-15T17:30:00Z",
    approximate_latitude: 12.0000,
    approximate_longitude: -86.1167,
    is_minor: false,
    status: "published"
  },
  {
    id: "case-10",
    case_number: "EN-2026-0010",
    full_name: "Byron Antonio Zeledón Castro",
    age_at_disappearance: 24,
    gender: "male",
    department: "Jinotega",
    municipality: "Jinotega",
    disappearance_date: "2026-11-09T08:00:00Z",
    approximate_latitude: 13.0991,
    approximate_longitude: -85.9992,
    is_minor: false,
    status: "published"
  },
  {
    id: "case-11",
    case_number: "EN-2026-0011",
    full_name: "Clara Inés Chow González",
    age_at_disappearance: 23,
    gender: "female",
    department: "Región Autónoma de la Costa Caribe Norte",
    municipality: "Puerto Cabezas (Bilwi)",
    disappearance_date: "2026-11-08T14:00:00Z",
    approximate_latitude: 14.0351,
    approximate_longitude: -83.3888,
    is_minor: false,
    status: "published"
  },
  {
    id: "case-12",
    case_number: "EN-2026-0012",
    full_name: "Deyvin Omar Campbell Hodgson",
    age_at_disappearance: 31,
    gender: "male",
    department: "Región Autónoma de la Costa Caribe Sur",
    municipality: "Bluefields",
    disappearance_date: "2026-11-07T19:00:00Z",
    approximate_latitude: 12.0131,
    approximate_longitude: -83.7635,
    is_minor: false,
    status: "published"
  }
];

export function getLocalMapPoints(department?: string, municipality?: string): any[] {
  let list = [...INITIAL_MAP_POINTS];

  // Integrar reportes creados localmente si existen
  if (typeof window !== "undefined") {
    try {
      const raw = localStorage.getItem("encuentrame_created_reports");
      if (raw) {
        const createdReports = JSON.parse(raw);
        for (const rep of createdReports) {
          const coords = DEPARTMENT_COORDINATES[rep.department] || { lat: 12.1364, lng: -86.2514 };
          // Pequeño desplazamiento determinista para no superponer exactamente
          const offsetLat = (Math.random() - 0.5) * 0.04;
          const offsetLng = (Math.random() - 0.5) * 0.04;
          list.unshift({
            id: rep.id,
            case_number: rep.case_number,
            full_name: `${rep.first_name} ${rep.last_name}`,
            age_at_disappearance: Number(rep.age_at_disappearance),
            gender: rep.gender || "unspecified",
            department: rep.department,
            municipality: rep.municipality,
            disappearance_date: rep.disappearance_date,
            approximate_latitude: rep.approximate_latitude || (coords.lat + offsetLat),
            approximate_longitude: rep.approximate_longitude || (coords.lng + offsetLng),
            is_minor: Boolean(rep.is_minor),
            status: rep.status || "published"
          });
        }
      }
    } catch {}
  }

  if (department && department !== "all") {
    list = list.filter((p) => p.department.toLowerCase() === department.toLowerCase());
  }
  if (municipality && municipality !== "all") {
    list = list.filter((p) => p.municipality.toLowerCase() === municipality.toLowerCase());
  }

  return list;
}

export function getLocalGeographicSummary() {
  return {
    total_departments: 17,
    total_municipalities: 153,
    active_departments: 17,
    active_municipalities: 153,
    source: "Instituto Nicaragüense de Estudios Territoriales (INETER) / Ley N.° 59 de Nicaragua",
    last_update: new Date().toISOString()
  };
}

export function getLocalMunicipalityObjects(departmentId?: string) {
  const list: any[] = [];
  let idCounter = 1;

  for (const [deptName, munis] of Object.entries(OFFICIAL_NICARAGUA_MUNICIPALITIES)) {
    const coords = DEPARTMENT_COORDINATES[deptName] || { lat: 12.1364, lng: -86.2514 };
    for (const munName of munis) {
      list.push({
        id: `mun_${idCounter++}`,
        department_id: deptName,
        department_name: deptName,
        name: munName,
        code: `${deptName.substring(0, 3).toUpperCase()}-${idCounter}`,
        latitude: coords.lat,
        longitude: coords.lng,
        is_active: true
      });
    }
  }

  if (departmentId && departmentId !== "all") {
    return list.filter((m) => m.department_id.toLowerCase() === departmentId.toLowerCase() || m.department_name.toLowerCase() === departmentId.toLowerCase());
  }

  return list;
}
