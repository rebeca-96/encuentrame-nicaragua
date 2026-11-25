import { ReportPublicItem, ReportDetail, CaseMilestone } from "../types";

export interface ExtendedReportDetail extends ReportDetail {
  resolution_notes?: string;
  is_active_case: boolean;
  timeline?: CaseMilestone[];
}

export function getCasePhotoUrl(caseNumber: string, fallback?: string): string {
  // Prioridad 1: Si se proporcionó una fotografía real subida del caso (Data URL, blob, endpoint API o archivo), USARLA DIRECTAMENTE
  if (fallback && 
      !fallback.includes("avatar-placeholder") && 
      !fallback.includes("/images/avatars/avatar_en-2026-")) {
    return fallback;
  }
  if (!caseNumber) return fallback || "/images/avatar-placeholder.svg";
  const clean = caseNumber.toLowerCase().replace(/[^a-z0-9]/g, "-");
  const map: Record<string, string> = {
    "en-2026-0001": "/images/avatars/avatar_en-2026-0001.webp",
    "en-2026-0002": "/images/avatars/avatar_en-2026-0002.webp",
    "en-2026-0003": "/images/avatars/avatar_en-2026-0003.webp",
    "en-2026-0004": "/images/avatars/avatar_en-2026-0004.webp",
    "en-2026-0005": "/images/avatars/avatar_en-2026-0005.webp",
    "en-2026-0006": "/images/avatars/avatar_en-2026-0006.webp",
    "en-2026-0007": "/images/avatars/avatar_en-2026-0007.webp",
    "en-2026-0008": "/images/avatars/avatar_en-2026-0008.webp",
    "en-2026-0009": "/images/avatars/avatar_en-2026-0009.webp",
    "en-2026-0010": "/images/avatars/avatar_en-2026-00010.webp",
    "en-2026-0011": "/images/avatars/avatar_en-2026-00011.webp",
    "en-2026-0012": "/images/avatars/avatar_en-2026-00012.webp",
    "en-2026-0013": "/images/avatars/avatar_en-2026-00013.webp",
    "en-2026-0014": "/images/avatars/avatar_en-2026-00014.webp",
    "en-2026-0015": "/images/avatars/avatar_en-2026-00015.webp",
    "en-2026-0016": "/images/avatars/avatar_en-2026-00016.webp",
    "en-2026-0017": "/images/avatars/avatar_en-2026-00017.webp",
    "en-2026-0018": "/images/avatars/avatar_en-2026-00018.webp",
    "en-2026-0019": "/images/avatars/avatar_en-2026-00019.webp",
    "en-2026-0020": "/images/avatars/avatar_en-2026-00020.webp",
  };
  if (map[clean]) return `${map[clean]}?v=1`;

  // Mapear cíclicamente para cualquier caso 1..61 a uno de los 20 avatares fotográficos oficiales
  const match = caseNumber.match(/(\d+)$/);
  if (match) {
    const num = parseInt(match[1], 10);
    const mod = ((num - 1) % 20) + 1;
    const pad = mod < 10 ? `000${mod}` : `000${mod}`;
    return `/images/avatars/avatar_en-2026-${pad}.webp?v=1`;
  }

  return fallback || "/images/avatars/avatar_en-2026-0001.webp?v=1";
}

export function generateDefaultTimeline(report: any): CaseMilestone[] {
  const dDate = new Date(report.disappearance_date || "2026-11-10T12:00:00Z");
  const dStr = isNaN(dDate.getTime()) 
    ? "Nov 2026" 
    : dDate.toLocaleDateString("es-NI", { day: "2-digit", month: "short", year: "numeric" });
  const isResolved = 
    report.status === "closed" || 
    report.status === "closed_found" || 
    report.status === "closed_resolved" || 
    report.status === "resolved";

  const timeline: CaseMilestone[] = [
    {
      date: `${dStr}, 16:30`,
      title: "Registro de Denuncia y Consentimiento Informado",
      description: `Reporte de desaparición formalizado ante el sistema de búsqueda en ${report.municipality || "Nicaragua"} bajo Ley N.° 787.`,
      status: "completed"
    },
    {
      date: `${dStr}, 18:45`,
      title: "Validación Documental y Aprobación Ética",
      description: "El equipo de moderación revisó la autenticidad del reporte, documentación y ausencia de riesgos a terceros.",
      status: "completed"
    },
    {
      date: `${dStr}, 20:00`,
      title: "Activación de Ficha Pública y Difusión Nacional",
      description: `Alerta oficial incorporada al Directorio Nacional y georreferenciada en ${report.department}.`,
      status: "completed"
    },
    {
      date: "Seguimiento en Vivo",
      title: "Monitoreo Territorial y Recepción de Pistas",
      description: "Canal seguro y confidencial activo 24/7 para el procesamiento de indicios y testimonios comunitarios.",
      status: isResolved ? "completed" : "current"
    }
  ];

  if (isResolved) {
    timeline.push({
      date: "Caso Concluido",
      title: "Localización Exitosa y Restablecimiento Familiar",
      description: report.resolution_notes || "Persona localizada y bajo resguardo seguro. El expediente cívico se encuentra formalmente cerrado.",
      status: "completed"
    });
  }

  return timeline;
}

export const OFFICIAL_SEED_REPORTS: Array<ExtendedReportDetail> = [
  // --- CASOS ACTIVOS (BÚSQUEDA EN CURSO) ---
  {
    id: "case-01",
    case_number: "EN-2026-0001",
    first_name: "Mateo Andrés",
    last_name: "García Centeno",
    nickname: "Mateíto",
    age_at_disappearance: 14,
    gender: "male",
    department: "Managua",
    municipality: "Ciudad Sandino",
    neighborhood_zone: "Zona 4, cerca del parque central",
    disappearance_date: "2026-11-16T15:30:00Z",
    approximate_latitude: 12.1583,
    approximate_longitude: -86.3444,
    physical_description: "Estatura 1.55m, contextura delgada, tez morena clara, cabello negro lacio corto, lunar visible cerca de la ceja derecha.",
    clothing_description: "Camiseta azul marino con estampado deportivo, jeans color celeste, tenis blancos marca Converse.",
    medical_conditions: "Padece asma leve; requiere inhalador de salbutamol.",
    circumstances: "Salió en horas de la tarde hacia la pulpería del barrio a comprar víveres y no regresó a su domicilio familiar.",
    vulnerability_flag: true,
    primary_photo_url: "/images/avatars/avatar_en-2026-0001.webp",
    photos: [
      {
        id: "p1",
        storage_key: "case-01-avatar",
        url: "/images/avatars/avatar_en-2026-0001.webp",
        is_primary: true,
        original_filename: "mateo_garcia.webp"
      }
    ],
    is_minor: true,
    status: "published",
    is_active_case: true,
    published_at: "2026-11-17T08:00:00Z",
    timeline: [
      {
        date: "16 Nov 2026, 17:00",
        title: "Recepción de Denuncia Ciudadana",
        description: "Familiares presentan reporte formal con consentimiento informado y cédula de identidad.",
        status: "completed"
      },
      {
        date: "16 Nov 2026, 18:30",
        title: "Validación y Moderación Ética",
        description: "Equipo de moderación aprueba la ficha tras comprobar identidad y ausencia de riesgo de terceros.",
        status: "completed"
      },
      {
        date: "17 Nov 2026, 08:00",
        title: "Difusión en Plataforma y Mapa Departamental",
        description: "Alerta publicada en Directorio Nacional y georreferenciada en Ciudad Sandino.",
        status: "completed"
      },
      {
        date: "18 Nov 2026, 14:15",
        title: "Pistas Confidenciales Canalizadas",
        description: "Se procesaron 2 testimonios anónimos de avistamiento en el mercado municipal de Ciudad Sandino.",
        status: "completed"
      },
      {
        date: "Actualidad",
        title: "Búsqueda Activa en Desarrollo",
        description: "Coordinación comunitaria y canal de pistas abierto para recibir información verificable.",
        status: "current"
      }
    ]
  },
  {
    id: "case-02",
    case_number: "EN-2026-0002",
    first_name: "Valeria Nicole",
    last_name: "Pérez Fonseca",
    nickname: "Vale",
    age_at_disappearance: 17,
    gender: "female",
    department: "Matagalpa",
    municipality: "Sébaco",
    neighborhood_zone: "Sector La Báscula",
    disappearance_date: "2026-11-14T09:15:00Z",
    approximate_latitude: 12.8550,
    approximate_longitude: -86.0967,
    physical_description: "Estatura 1.62m, complexión delgada, piel blanca, ojos castaños claros, cabello castaño largo ondulado.",
    clothing_description: "Blusa blanca de manga corta, pantalón negro de mezclilla, mochila escolar gris.",
    medical_conditions: "Ninguna condición médica relevante reportada.",
    circumstances: "Vista por última vez abordando una unidad de transporte colectivo interlocal hacia la ciudad de Matagalpa.",
    vulnerability_flag: true,
    primary_photo_url: "/images/avatar-placeholder.svg",
    photos: [
      {
        id: "p2",
        storage_key: "case-02-avatar",
        url: "/images/avatar-placeholder.svg",
        is_primary: true,
        original_filename: "valeria_perez.webp"
      }
    ],
    is_minor: true,
    status: "published",
    is_active_case: true,
    published_at: "2026-11-15T10:00:00Z",
    timeline: [
      {
        date: "14 Nov 2026, 12:00",
        title: "Registro de Caso de Búsqueda",
        description: "Tía materna ingresa solicitud de búsqueda responsable.",
        status: "completed"
      },
      {
        date: "14 Nov 2026, 14:00",
        title: "Aprobación y Publicación Oficial",
        description: "Se autoriza difusión pública con fotografía sanitizada sin metadatos EXIF.",
        status: "completed"
      },
      {
        date: "16 Nov 2026, 10:30",
        title: "Verificación en Terminales de Transporte",
        description: "Colaboradores cívicos comparten alerta en paradas de autobuses de Sébaco y Matagalpa.",
        status: "completed"
      },
      {
        date: "Actualidad",
        title: "Seguimiento en Territorio",
        description: "Se continúa rastreando el trayecto intermunicipal.",
        status: "current"
      }
    ]
  },
  {
    id: "case-04",
    case_number: "EN-2026-0004",
    first_name: "Yader Francisco",
    last_name: "Gutiérrez Marenco",
    nickname: "El Capi",
    age_at_disappearance: 29,
    gender: "male",
    department: "Chinandega",
    municipality: "Corinto",
    neighborhood_zone: "Zona Portuaria, muelle pesquero",
    disappearance_date: "2026-11-12T18:00:00Z",
    approximate_latitude: 12.4833,
    approximate_longitude: -87.1667,
    physical_description: "Estatura 1.74m, piel morena, complexión atlética, cicatriz de 4 cm en antebrazo izquierdo, tatuaje de ancla en hombro derecho.",
    clothing_description: "Camisa manga larga a cuadros verde y blanca, pantalón de lona azul, botas de hule negras.",
    medical_conditions: "Ninguna condición médica reportada.",
    circumstances: "Pescador artesanal; salió en una faena corta en estero local y la embarcación retornó a la orilla sin tripulantes.",
    vulnerability_flag: false,
    primary_photo_url: "/images/avatar-placeholder.svg",
    photos: [
      {
        id: "p4",
        storage_key: "case-04-avatar",
        url: "/images/avatar-placeholder.svg",
        is_primary: true,
        original_filename: "yader_gutierrez.webp"
      }
    ],
    is_minor: false,
    status: "published",
    is_active_case: true,
    published_at: "2026-11-13T12:00:00Z",
    timeline: [
      {
        date: "13 Nov 2026, 06:00",
        title: "Reporte de Desaparición Costera",
        description: "Compañeros de pesca y familiares emiten reporte por embarcación desatendida.",
        status: "completed"
      },
      {
        date: "13 Nov 2026, 09:00",
        title: "Activación de Alerta Fluvial y Marítima",
        description: "Publicación de ficha en línea con foco en la costa pacífica de Chinandega.",
        status: "completed"
      },
      {
        date: "15 Nov 2026, 15:00",
        title: "Búsqueda en Bancos Costeros",
        description: "Pescadores de Corinto y Poneloya coordinan inspección visual en litoral.",
        status: "completed"
      },
      {
        date: "Actualidad",
        title: "Búsqueda Activa en Vigilancia",
        description: "Se mantiene alerta comunitaria con cooperativas pesqueras de la zona.",
        status: "current"
      }
    ]
  },
  {
    id: "case-05",
    case_number: "EN-2026-0005",
    first_name: "Lucía Esperanza",
    last_name: "Solís Jarquín",
    nickname: "Lucy",
    age_at_disappearance: 16,
    gender: "female",
    department: "Estelí",
    municipality: "Estelí",
    neighborhood_zone: "Barrio El Rosario",
    disappearance_date: "2026-11-15T13:45:00Z",
    approximate_latitude: 13.0919,
    approximate_longitude: -86.3538,
    physical_description: "Estatura 1.58m, contextura media, tez trigueña, cabello castaño hasta los hombros, tatuaje pequeño de mariposa en muñeca izquierda.",
    clothing_description: "Suéter negro con capucha, jeans rotos azules, tenis deportivos negros.",
    medical_conditions: "Ninguna condición médica conocida.",
    circumstances: "Salió de clases universitarias nocturnas hacia la parada de autobuses y su teléfono móvil quedó fuera de servicio.",
    vulnerability_flag: true,
    primary_photo_url: "/images/avatar-placeholder.svg",
    photos: [
      {
        id: "p5",
        storage_key: "case-05-avatar",
        url: "/images/avatar-placeholder.svg",
        is_primary: true,
        original_filename: "lucia_solis.webp"
      }
    ],
    is_minor: true,
    status: "published",
    is_active_case: true,
    published_at: "2026-11-16T09:00:00Z",
    timeline: [
      {
        date: "15 Nov 2026, 22:30",
        title: "Ingreso de Reporte Urgente",
        description: "Familiares reportan falta de llegada tras horario de clases nocturnas.",
        status: "completed"
      },
      {
        date: "16 Nov 2026, 08:30",
        title: "Verificación y Publicación",
        description: "Moderador asignado verifica matrícula y confirma consentimiento parental.",
        status: "completed"
      },
      {
        date: "Actualidad",
        title: "Recepción de Testimonios",
        description: "Se recopilan testimonios de compañeros de aula y transeúntes del sector.",
        status: "current"
      }
    ]
  },
  {
    id: "case-06",
    case_number: "EN-2026-0006",
    first_name: "José Ramón",
    last_name: "Calero Bermúdez",
    nickname: "Moncho",
    age_at_disappearance: 42,
    gender: "male",
    department: "Carazo",
    municipality: "Jinotepe",
    neighborhood_zone: "Sector El Calvario",
    disappearance_date: "2026-11-11T16:20:00Z",
    approximate_latitude: 11.8541,
    approximate_longitude: -86.1994,
    physical_description: "Estatura 1.70m, complexión robusta, piel trigueña clara, lunar pronunciado en mejilla izquierda, cabello negro crespo con canas en los laterales.",
    clothing_description: "Camisa roja tipo polo, jeans azul oscuro, botas camperas de cuero café.",
    medical_conditions: "Hipertensión tratada; requiere losartán diario.",
    circumstances: "Se dirigía a negociar una cosecha en comarcas aledañas en su motocicleta roja y no regresó a su hogar.",
    vulnerability_flag: false,
    primary_photo_url: "/images/avatar-placeholder.svg",
    photos: [
      {
        id: "p6",
        storage_key: "case-06-avatar",
        url: "/images/avatar-placeholder.svg",
        is_primary: true,
        original_filename: "jose_calero.webp"
      }
    ],
    is_minor: false,
    status: "published",
    is_active_case: true,
    published_at: "2026-11-12T14:30:00Z",
    timeline: [
      {
        date: "12 Nov 2026, 09:00",
        title: "Recepción de Denuncia",
        description: "Cónyuge registra el reporte de no localización tras 24 horas sin comunicación.",
        status: "completed"
      },
      {
        date: "12 Nov 2026, 14:30",
        title: "Publicación Departamental",
        description: "Ficha activada con descripción vehicular y datos médicos relevantes.",
        status: "completed"
      },
      {
        date: "Actualidad",
        title: "Búsqueda Comunitaria",
        description: "Seguimiento en talleres mecánicos y caminos vecinales entre Jinotepe y Diriamba.",
        status: "current"
      }
    ]
  },
  {
    id: "case-08",
    case_number: "EN-2026-0008",
    first_name: "Carlos Alberto",
    last_name: "Membreño Ruiz",
    nickname: "Carlitos",
    age_at_disappearance: 35,
    gender: "male",
    department: "Granada",
    municipality: "Granada",
    neighborhood_zone: "Sector Calle La Calzada hacia el malecón",
    disappearance_date: "2026-11-13T20:10:00Z",
    approximate_latitude: 11.9299,
    approximate_longitude: -85.9560,
    physical_description: "Estatura 1.76m, complexión gruesa, cabello negro con entradas, cicatriz en labio superior, portaba sombrero y camisa a cuadros.",
    clothing_description: "Camisa a cuadros azul y blanco, jeans clásicos, sombrero de palma, botas vaqueras.",
    medical_conditions: "Ninguna condición reportada.",
    circumstances: "Comerciante regional, fue visto por compañeros conversando en la plazoleta y no retornó a su lugar de estancia.",
    vulnerability_flag: false,
    primary_photo_url: "/images/avatar-placeholder.svg",
    photos: [
      {
        id: "p8",
        storage_key: "case-08-avatar",
        url: "/images/avatar-placeholder.svg",
        is_primary: true,
        original_filename: "carlos_membreno.webp"
      }
    ],
    is_minor: false,
    status: "published",
    is_active_case: true,
    published_at: "2026-11-14T11:00:00Z",
    timeline: [
      {
        date: "14 Nov 2026, 08:00",
        title: "Registro de Caso",
        description: "Familiares solicitan apoyo cívico para difusión de fotografía.",
        status: "completed"
      },
      {
        date: "14 Nov 2026, 11:00",
        title: "Difusión en Granada",
        description: "Publicado en el directorio y compartido con el sector turístico de Granada.",
        status: "completed"
      },
      {
        date: "Actualidad",
        title: "Procesamiento de Información",
        description: "Canal abierto para recepción de pistas sobre su trayecto.",
        status: "current"
      }
    ]
  },
  {
    id: "case-10",
    case_number: "EN-2026-0010",
    first_name: "Byron Antonio",
    last_name: "Zeledón Castro",
    nickname: "Byron",
    age_at_disappearance: 24,
    gender: "male",
    department: "Jinotega",
    municipality: "Jinotega",
    neighborhood_zone: "Comarca Sabana Grande",
    disappearance_date: "2026-11-09T08:00:00Z",
    approximate_latitude: 13.0991,
    approximate_longitude: -85.9992,
    physical_description: "Estatura 1.68m, tez trigueña, contextura delgada, ojos café oscuros, cicatriz en rodilla derecha.",
    clothing_description: "Camisa manga larga azul celeste, pantalón de tela café, botas de hule.",
    medical_conditions: "Ninguna médica relevante.",
    circumstances: "Salió temprano a labores agrícolas en finca comunal y no regresó al mediodía.",
    vulnerability_flag: false,
    primary_photo_url: "/images/avatar-placeholder.svg",
    photos: [
      {
        id: "p10",
        storage_key: "case-10-avatar",
        url: "/images/avatar-placeholder.svg",
        is_primary: true,
        original_filename: "byron_zeledon.webp"
      }
    ],
    is_minor: false,
    status: "published",
    is_active_case: true,
    published_at: "2026-11-10T16:00:00Z",
    timeline: [
      {
        date: "10 Nov 2026, 10:00",
        title: "Alerta Rural Ingresada",
        description: "Cooperativa cafetalera y familiares presentan reporte formal.",
        status: "completed"
      },
      {
        date: "10 Nov 2026, 16:00",
        title: "Ficha Aprobada",
        description: "Publicación autorizada en plataforma para búsqueda comunitaria.",
        status: "completed"
      },
      {
        date: "Actualidad",
        title: "Coordinación en Zona Rural",
        description: "Equipos locales recorren senderos entre Jinotega y San Rafael del Norte.",
        status: "current"
      }
    ]
  },
  {
    id: "case-11",
    case_number: "EN-2026-0011",
    first_name: "Clara Inés",
    last_name: "Chow González",
    nickname: "Clarita",
    age_at_disappearance: 23,
    gender: "female",
    department: "Región Autónoma de la Costa Caribe Norte",
    municipality: "Puerto Cabezas (Bilwi)",
    neighborhood_zone: "Sector El Muelle / Barrio Peter Ferrera",
    disappearance_date: "2026-11-08T14:00:00Z",
    approximate_latitude: 14.0351,
    approximate_longitude: -83.3888,
    physical_description: "Estatura 1.65m, piel morena clara, cabello negro lacio hasta la cintura, bilingüe español-miskito.",
    clothing_description: "Camisa amarilla sin mangas, pantalón capri blanco, zapatillas de lona rojas.",
    medical_conditions: "Ninguna condición reportada.",
    circumstances: "Fue vista en las cercanías del muelle municipal esperando una panga de pasajeros.",
    vulnerability_flag: false,
    primary_photo_url: "/images/avatar-placeholder.svg",
    photos: [
      {
        id: "p11",
        storage_key: "case-11-avatar",
        url: "/images/avatar-placeholder.svg",
        is_primary: true,
        original_filename: "clara_chow.webp"
      }
    ],
    is_minor: false,
    status: "published",
    is_active_case: true,
    published_at: "2026-11-09T18:00:00Z",
    timeline: [
      {
        date: "09 Nov 2026, 11:00",
        title: "Denuncia Recibida en Bilwi",
        description: "Registro en plataforma con asistencia de moderador bilingüe miskito.",
        status: "completed"
      },
      {
        date: "09 Nov 2026, 18:00",
        title: "Publicación Multilingüe",
        description: "Ficha habilitada con cobertura regional en la Costa Caribe Norte.",
        status: "completed"
      },
      {
        date: "Actualidad",
        title: "Búsqueda Fluvial y Costera",
        description: "Monitoreo permanente de comunidades ribereñas y puertos fluviales.",
        status: "current"
      }
    ]
  },
  {
    id: "case-12",
    case_number: "EN-2026-0012",
    first_name: "Deyvin Omar",
    last_name: "Campbell Hodgson",
    nickname: "Deyvin",
    age_at_disappearance: 31,
    gender: "male",
    department: "Región Autónoma de la Costa Caribe Sur",
    municipality: "Bluefields",
    neighborhood_zone: "Barrio Beholden",
    disappearance_date: "2026-11-07T19:00:00Z",
    approximate_latitude: 12.0131,
    approximate_longitude: -83.7635,
    physical_description: "Estatura 1.78m, tez morena oscura, complexión atlética, tatuaje con brújula marina en hombro izquierdo.",
    clothing_description: "Camiseta de básquetbol azul con número 7, pantalón deportivo negro, gorra azul.",
    medical_conditions: "Ninguna médica reportada.",
    circumstances: "Se dirigía a laborar en una bodega cercana a la bahía de Bluefields y no llegó a su turno.",
    vulnerability_flag: false,
    primary_photo_url: "/images/avatar-placeholder.svg",
    photos: [
      {
        id: "p12",
        storage_key: "case-12-avatar",
        url: "/images/avatar-placeholder.svg",
        is_primary: true,
        original_filename: "deyvin_campbell.webp"
      }
    ],
    is_minor: false,
    status: "published",
    is_active_case: true,
    published_at: "2026-11-08T12:00:00Z",
    timeline: [
      {
        date: "08 Nov 2026, 08:30",
        title: "Reporte Registrado",
        description: "Familiares presentan información sobre trayecto en bahía.",
        status: "completed"
      },
      {
        date: "08 Nov 2026, 12:00",
        title: "Alerta en RACCS",
        description: "Publicación oficial en el Directorio Nacional.",
        status: "completed"
      },
      {
        date: "Actualidad",
        title: "Indagación Comunitaria",
        description: "Recepción de información de estibadores y transportistas acuáticos.",
        status: "current"
      }
    ]
  },
  {
    id: "case-13",
    case_number: "EN-2026-0013",
    first_name: "Wilmer Enrique",
    last_name: "Aragón Borge",
    nickname: "Wilmita",
    age_at_disappearance: 15,
    gender: "male",
    department: "Carazo",
    municipality: "Diriamba",
    neighborhood_zone: "Sector La Salle",
    disappearance_date: "2026-11-12T16:40:00Z",
    approximate_latitude: 11.8541,
    approximate_longitude: -86.2394,
    physical_description: "Estatura 1.64m, tez trigueña, complexión delgada, brackets dentales metálicos, cabello corto.",
    clothing_description: "Camiseta negra deportiva con logo de fútbol, short gris, zapatillas deportivas negras.",
    medical_conditions: "Sin condiciones médicas reportadas.",
    circumstances: "Salió a una práctica deportiva en cancha comunitaria y no regresó al anochecer.",
    vulnerability_flag: true,
    primary_photo_url: "/images/avatar-placeholder.svg",
    photos: [
      {
        id: "p13",
        storage_key: "case-13-avatar",
        url: "/images/avatar-placeholder.svg",
        is_primary: true,
        original_filename: "wilmer_aragon.webp"
      }
    ],
    is_minor: true,
    status: "published",
    is_active_case: true,
    published_at: "2026-11-13T10:00:00Z",
    timeline: [
      {
        date: "12 Nov 2026, 21:00",
        title: "Reporte de Menor no Localizado",
        description: "Familiares informan que no retornó de cancha comunal.",
        status: "completed"
      },
      {
        date: "13 Nov 2026, 10:00",
        title: "Alerta Prioritaria Publicada",
        description: "Activada alerta prioritaria por minoría de edad.",
        status: "completed"
      },
      {
        date: "Actualidad",
        title: "Búsqueda Activa",
        description: "Colaboración con directivos escolares y entrenadores deportivos de Carazo.",
        status: "current"
      }
    ]
  },
  {
    id: "case-15",
    case_number: "EN-2026-0015",
    first_name: "Erick Jayson",
    last_name: "Finley Dixon",
    nickname: "Erick",
    age_at_disappearance: 21,
    gender: "male",
    department: "Región Autónoma de la Costa Caribe Norte",
    municipality: "Puerto Cabezas (Bilwi)",
    neighborhood_zone: "Sector El Muelle",
    disappearance_date: "2026-11-11T10:00:00Z",
    approximate_latitude: 14.0351,
    approximate_longitude: -83.3888,
    physical_description: "Estatura 1.75m, tez morena, complexión delgada, tatuaje de compás náutico en el pecho, gorra deportiva azul.",
    clothing_description: "Camisa polo gris, jeans oscuros, sandalias de cuero.",
    medical_conditions: "Ninguna reportada.",
    circumstances: "Desplazamiento matutino hacia embarcadero para trámites comerciales.",
    vulnerability_flag: false,
    primary_photo_url: "/images/avatar-placeholder.svg",
    photos: [
      {
        id: "p15",
        storage_key: "case-15-avatar",
        url: "/images/avatar-placeholder.svg",
        is_primary: true,
        original_filename: "erick_finley.webp"
      }
    ],
    is_minor: false,
    status: "published",
    is_active_case: true,
    published_at: "2026-11-12T15:00:00Z",
    timeline: [
      {
        date: "12 Nov 2026, 10:00",
        title: "Recepción de Caso",
        description: "Familiares reportan pérdida de señal celular tras salida matutina.",
        status: "completed"
      },
      {
        date: "12 Nov 2026, 15:00",
        title: "Publicación en Directorio",
        description: "Ficha oficial verificada y georreferenciada.",
        status: "completed"
      },
      {
        date: "Actualidad",
        title: "Búsqueda en Curso",
        description: "Se reciben pistas de cooperativas marítimas locales.",
        status: "current"
      }
    ]
  },
  {
    id: "case-16",
    case_number: "EN-2026-0016",
    first_name: "Francisco Javier",
    last_name: "Cruz Pastrana",
    nickname: "Chico",
    age_at_disappearance: 31,
    gender: "male",
    department: "Nueva Segovia",
    municipality: "Jalapa",
    neighborhood_zone: "Comarca Teotecacinte",
    disappearance_date: "2026-11-05T07:30:00Z",
    approximate_latitude: 13.9167,
    approximate_longitude: -86.1333,
    physical_description: "Estatura 1.72m, contextura fuerte, cabello lacio negro, mancha de nacimiento oscura en la parte posterior del cuello.",
    clothing_description: "Camisa vaquera azul, pantalón vaquero negro, cinturón de cuero con hebilla metálica.",
    medical_conditions: "Ninguna médica relevante.",
    circumstances: "Agricultor de tabaco y granos; se trasladaba a inspeccionar tierras de cultivo en sector fronterizo.",
    vulnerability_flag: false,
    primary_photo_url: "/images/avatar-placeholder.svg",
    photos: [
      {
        id: "p16",
        storage_key: "case-16-avatar",
        url: "/images/avatar-placeholder.svg",
        is_primary: true,
        original_filename: "francisco_cruz.webp"
      }
    ],
    is_minor: false,
    status: "published",
    is_active_case: true,
    published_at: "2026-11-06T11:00:00Z",
    timeline: [
      {
        date: "06 Nov 2026, 07:00",
        title: "Reporte Registrado",
        description: "Hermana presenta reporte formal con consentimiento y documentación de identidad.",
        status: "completed"
      },
      {
        date: "06 Nov 2026, 11:00",
        title: "Alerta en Nueva Segovia",
        description: "Publicado en el directorio nacional con alerta en Jalapa y municipios limítrofes.",
        status: "completed"
      },
      {
        date: "Actualidad",
        title: "Rastreo en Zona Agrícola",
        description: "Comité cívico local continúa búsqueda en comunidades productoras.",
        status: "current"
      }
    ]
  },

  // --- CASOS NO ACTIVOS (LOCALIZADOS / RESUELTOS / CERRADOS) ---
  {
    id: "case-03",
    case_number: "EN-2026-0003",
    first_name: "Don Manuel de Jesús",
    last_name: "Rocha Blandón",
    nickname: "Don Manuelito",
    age_at_disappearance: 73,
    gender: "male",
    department: "León",
    municipality: "León",
    neighborhood_zone: "Barrio Sutiaba, costado oeste de la iglesia",
    disappearance_date: "2026-11-10T07:00:00Z",
    approximate_latitude: 12.4379,
    approximate_longitude: -86.8780,
    physical_description: "Estatura 1.68m, cabello canoso escaso, contextura delgada, anteojos de marco metálico, bigote blanco.",
    clothing_description: "Camisa guayabera beige de manga larga, pantalón de vestir café, zapatos negros de cuero.",
    medical_conditions: "Presenta desorientación por principio de pérdida de memoria senil.",
    circumstances: "Salió a dar una caminata matutina en el barrio Sutiaba y perdió la orientación espacial.",
    vulnerability_flag: true,
    primary_photo_url: "/images/avatar-placeholder.svg",
    photos: [
      {
        id: "p3",
        storage_key: "case-03-avatar",
        url: "/images/avatar-placeholder.svg",
        is_primary: true,
        original_filename: "manuel_rocha.webp"
      }
    ],
    is_minor: false,
    status: "closed",
    is_active_case: false,
    published_at: "2026-11-11T09:00:00Z",
    resolution_notes: "Localizado sano y salvo en el sector de Poneloya gracias a aviso ciudadano anónimo y reunificado con su familia.",
    timeline: [
      {
        date: "10 Nov 2026, 11:00",
        title: "Reporte de Adulto Mayor Desorientado",
        description: "Hijos reportan salida matutina sin retorno de Don Manuel.",
        status: "completed"
      },
      {
        date: "10 Nov 2026, 12:30",
        title: "Alerta Prioritaria de Salud Publicada",
        description: "Activada alerta urgente por condición de memoria senil.",
        status: "completed"
      },
      {
        date: "11 Nov 2026, 14:10",
        title: "Pista Ciudadana Certera",
        description: "Comerciante reporta a Don Manuel descansando en una parada hacia Poneloya.",
        status: "completed"
      },
      {
        date: "11 Nov 2026, 16:30",
        title: "Localización y Asistencia Médica",
        description: "Equipo de socorro verifica estado de salud estable e hidratación.",
        status: "completed"
      },
      {
        date: "11 Nov 2026, 18:00",
        title: "Caso Cerrado: Reunificación Exitosa",
        description: "Entregado a su familia en su domicilio de Sutiaba. Expediente formalmente concluido.",
        status: "completed"
      }
    ]
  },
  {
    id: "case-07",
    case_number: "EN-2026-0007",
    first_name: "Adriana Marcela",
    last_name: "Tinoco Rivas",
    nickname: "Marce",
    age_at_disappearance: 21,
    gender: "female",
    department: "Chontales",
    municipality: "Juigalpa",
    neighborhood_zone: "Salida a La Libertad",
    disappearance_date: "2026-11-06T11:00:00Z",
    approximate_latitude: 12.0620,
    approximate_longitude: -85.3644,
    physical_description: "Estatura 1.63m, piel morena clara, cabello castaño amarrado en coleta, ojos café oscuros.",
    clothing_description: "Camisa deportiva manga larga gris, pantalón de senderismo caqui, botas de montaña.",
    medical_conditions: "Alergia a picaduras de abejas.",
    circumstances: "Realizaba recorrido por senderos regionales y se separó del grupo por avería de señal de comunicación.",
    vulnerability_flag: false,
    primary_photo_url: "/images/avatar-placeholder.svg",
    photos: [
      {
        id: "p7",
        storage_key: "case-07-avatar",
        url: "/images/avatar-placeholder.svg",
        is_primary: true,
        original_filename: "adriana_tinoco.webp"
      }
    ],
    is_minor: false,
    status: "closed",
    is_active_case: false,
    published_at: "2026-11-07T13:00:00Z",
    resolution_notes: "Caso resuelto satisfactoriamente. Se confirmó su localización segura y restablecimiento de contacto.",
    timeline: [
      {
        date: "06 Nov 2026, 19:00",
        title: "Reporte de Extravío Temporal",
        description: "Compañeros de senderismo registran reporte por retraso en retorno.",
        status: "completed"
      },
      {
        date: "07 Nov 2026, 08:00",
        title: "Publicación en Plataforma",
        description: "Difusión en comunidades rurales entre Juigalpa y La Libertad.",
        status: "completed"
      },
      {
        date: "07 Nov 2026, 12:45",
        title: "Localización Positiva",
        description: "Ubicada en albergue comunitario tras resguardarse de lluvia.",
        status: "completed"
      },
      {
        date: "07 Nov 2026, 15:00",
        title: "Caso Cerrado",
        description: "Comunicación familiar restablecida y expediente archivado con éxito.",
        status: "completed"
      }
    ]
  },
  {
    id: "case-09",
    case_number: "EN-2026-0009",
    first_name: "Kenia Jamileth",
    last_name: "López Obando",
    nickname: "Kenita",
    age_at_disappearance: 19,
    gender: "female",
    department: "Masaya",
    municipality: "Nindirí",
    neighborhood_zone: "Sector El Empalme",
    disappearance_date: "2026-11-08T17:30:00Z",
    approximate_latitude: 12.0000,
    approximate_longitude: -86.1167,
    physical_description: "Estatura 1.60m, piel morena clara, cabello castaño lacio a la cintura, hoyuelos en ambas mejillas al sonreír.",
    clothing_description: "Vestido floreado de verano fondo oscuro, sandalias bajas color camel.",
    medical_conditions: "Ninguna condición médica reportada.",
    circumstances: "Reportada no localizada temporalmente tras pérdida de contacto por corte eléctrico y batería agotada.",
    vulnerability_flag: false,
    primary_photo_url: "/images/avatar-placeholder.svg",
    photos: [
      {
        id: "p9",
        storage_key: "case-09-avatar",
        url: "/images/avatar-placeholder.svg",
        is_primary: true,
        original_filename: "kenia_lopez.webp"
      }
    ],
    is_minor: false,
    status: "closed",
    is_active_case: false,
    published_at: "2026-11-09T08:30:00Z",
    resolution_notes: "Localizada de forma segura por autoridades comunitarias y entregada bajo resguardo a su núcleo familiar.",
    timeline: [
      {
        date: "08 Nov 2026, 21:00",
        title: "Alerta Presentada",
        description: "Madre de familia solicita apoyo para búsqueda.",
        status: "completed"
      },
      {
        date: "09 Nov 2026, 08:30",
        title: "Publicación Autorizada",
        description: "Ficha divulgada en Masaya y Managua.",
        status: "completed"
      },
      {
        date: "09 Nov 2026, 14:00",
        title: "Contacto Restablecido",
        description: "Kenia se comunica con su familia y confirma encontrarse en resguardo seguro.",
        status: "completed"
      },
      {
        date: "09 Nov 2026, 16:00",
        title: "Cierre de Caso",
        description: "Reunificación presencial verificada. Caso cerrado.",
        status: "completed"
      }
    ]
  },
  {
    id: "case-20",
    case_number: "EN-2026-0020",
    first_name: "Gerardo Antonio",
    last_name: "Mendoza Espinoza",
    nickname: "Don Gerardo",
    age_at_disappearance: 52,
    gender: "male",
    department: "Managua",
    municipality: "Managua",
    neighborhood_zone: "Distrito 5",
    disappearance_date: "2026-11-01T12:00:00Z",
    approximate_latitude: 12.1364,
    approximate_longitude: -86.2514,
    physical_description: "Estatura 1.70m, tez morena, bigote poblado, anteojos de lectura, contextura fuerte.",
    clothing_description: "Camisa azul manga corta, jeans celestes, zapatos negros de trabajo.",
    medical_conditions: "Tratamiento de tensión arterial.",
    circumstances: "Reportado no localizado temporalmente tras pérdida de contacto por avería de vehículo en zona rural.",
    vulnerability_flag: false,
    primary_photo_url: "/images/avatar-placeholder.svg",
    photos: [
      {
        id: "p20",
        storage_key: "case-20-avatar",
        url: "/images/avatar-placeholder.svg",
        is_primary: true,
        original_filename: "gerardo_mendoza.webp"
      }
    ],
    is_minor: false,
    status: "closed",
    is_active_case: false,
    published_at: "2026-11-02T10:00:00Z",
    resolution_notes: "Localizado sin afectaciones físicas tras superar percance mecánico en zona rural. Caso cerrado exitosamente.",
    timeline: [
      {
        date: "01 Nov 2026, 20:00",
        title: "Reporte por Ausencia de Llegada",
        description: "Familiares reportan vehículo no retornado de viaje rural.",
        status: "completed"
      },
      {
        date: "02 Nov 2026, 10:00",
        title: "Alerta Emitida",
        description: "Publicación de ficha para reporte de vehículo.",
        status: "completed"
      },
      {
        date: "02 Nov 2026, 18:20",
        title: "Retorno y Localización Segura",
        description: "El señor Mendoza arriba a Managua tras recibir auxilio vial.",
        status: "completed"
      },
      {
        date: "02 Nov 2026, 19:00",
        title: "Cierre Definitivo",
        description: "Expediente formalmente archivado y cerrado.",
        status: "completed"
      }
    ]
  }
];

export function getLocalPublicReports(params: Record<string, any> = {}): ReportPublicItem[] {
  let list: Array<ExtendedReportDetail> = [...OFFICIAL_SEED_REPORTS];

  // Integrar reportes creados dinámicamente en el navegador
  if (typeof window !== "undefined") {
    try {
      const raw = localStorage.getItem("encuentrame_created_reports");
      if (raw) {
        const localCreated = JSON.parse(raw);
        for (const rep of localCreated) {
          list.unshift({
            id: rep.id,
            case_number: rep.case_number,
            first_name: rep.first_name,
            last_name: rep.last_name,
            nickname: rep.nickname,
            age_at_disappearance: Number(rep.age_at_disappearance),
            gender: rep.gender || "unspecified",
            disappearance_date: rep.disappearance_date || new Date().toISOString(),
            department: rep.department,
            municipality: rep.municipality,
            neighborhood_zone: rep.neighborhood_zone,
            approximate_latitude: rep.approximate_latitude || 12.1364,
            approximate_longitude: rep.approximate_longitude || -86.2514,
            physical_description: rep.physical_description || "Sin descripción proporcionada",
            clothing_description: rep.clothing_description || "Vestimenta no detallada",
            circumstances: rep.circumstances || "Circunstancias reportadas por familiar",
            medical_conditions: rep.medical_conditions,
            vulnerability_flag: Boolean(rep.vulnerability_flag || rep.is_minor),
            primary_photo_url: rep.primary_photo_url || "/images/avatar-placeholder.svg",
            photos: [
              {
                id: `p_${rep.id}`,
                storage_key: "local",
                url: rep.primary_photo_url || "/images/avatar-placeholder.svg",
                is_primary: true,
                original_filename: "foto_subida.webp"
              }
            ],
            is_minor: Boolean(rep.is_minor),
            status: rep.status || "published",
            is_active_case: rep.status !== "closed" && rep.status !== "resolved",
            published_at: rep.created_at || new Date().toISOString(),
            timeline: [
              {
                date: "Hoy",
                title: "Reporte Registrado",
                description: "Ingresado recientemente por usuario reportante.",
                status: "completed"
              },
              {
                date: "Hoy",
                title: "En Revisión y Difusión",
                description: "Disponible en la plataforma para seguimiento ciudadano.",
                status: "current"
              }
            ]
          });
        }
      }
    } catch (e) {
      console.warn("Error leyendo reportes locales:", e);
    }
  }

  // Filtro por Estado (activos / no activos / todos)
  const statusFilter = params.status || params.status_filter || "all";
  if (statusFilter === "active" || statusFilter === "activos") {
    list = list.filter((r) => r.is_active_case || r.status === "published" || r.status === "under_investigation" || r.status === "approved_published");
  } else if (statusFilter === "inactive" || statusFilter === "no_activos" || statusFilter === "closed" || statusFilter === "resolved") {
    list = list.filter((r) => !r.is_active_case || r.status === "closed" || r.status === "resolved" || r.status === "closed_found" || r.status === "closed_resolved");
  }

  // Filtro de búsqueda por texto (q)
  if (params.q && typeof params.q === "string" && params.q.trim()) {
    const qTerm = params.q.toLowerCase().trim();
    list = list.filter((r) =>
      r.first_name.toLowerCase().includes(qTerm) ||
      r.last_name.toLowerCase().includes(qTerm) ||
      r.case_number.toLowerCase().includes(qTerm) ||
      (r.physical_description && r.physical_description.toLowerCase().includes(qTerm)) ||
      (r.municipality && r.municipality.toLowerCase().includes(qTerm)) ||
      (r.department && r.department.toLowerCase().includes(qTerm))
    );
  }

  // Filtro por Departamento
  if (params.department && params.department !== "all") {
    list = list.filter((r) => r.department.toLowerCase() === params.department.toLowerCase());
  }

  // Filtro por Municipio
  if (params.municipality && params.municipality !== "all") {
    list = list.filter((r) => r.municipality.toLowerCase() === params.municipality.toLowerCase());
  }

  // Filtro por Género
  if (params.gender && params.gender !== "all") {
    list = list.filter((r) => r.gender.toLowerCase() === params.gender.toLowerCase());
  }

  // Filtro solo menores
  if (params.is_minor === true || params.is_minor === "true") {
    list = list.filter((r) => r.is_minor);
  }

  // Filtro rango de edad
  if (params.age_min !== undefined && params.age_min !== null && params.age_min !== "") {
    list = list.filter((r) => r.age_at_disappearance >= Number(params.age_min));
  }
  if (params.age_max !== undefined && params.age_max !== null && params.age_max !== "") {
    list = list.filter((r) => r.age_at_disappearance <= Number(params.age_max));
  }

  // Límite opcional
  if (params.limit && Number(params.limit) > 0) {
    list = list.slice(0, Number(params.limit));
  }

  // Priorizar siempre la fotografía real cargada del caso; sólo recurrir a avatar si no existe imagen
  return list.map((r) => {
    const isRealUploaded = r.primary_photo_url && 
      !r.primary_photo_url.includes("avatar-placeholder") && 
      !r.primary_photo_url.includes("/images/avatars/");
    return {
      ...r,
      primary_photo_url: isRealUploaded 
        ? r.primary_photo_url 
        : getCasePhotoUrl(r.case_number, r.primary_photo_url)
    };
  });
}

export function getLocalReportDetail(idOrCase: string): ExtendedReportDetail {
  const allReports = getLocalPublicReports({ status: "all" }) as ExtendedReportDetail[];
  const found = allReports.find(
    (r) => r.id === idOrCase || r.case_number.toLowerCase() === idOrCase.toLowerCase()
  ) || OFFICIAL_SEED_REPORTS[0];

  const isRealPhoto = found.primary_photo_url && 
    !found.primary_photo_url.includes("avatar-placeholder") && 
    !found.primary_photo_url.includes("/images/avatars/");
  const photo = (isRealPhoto 
    ? found.primary_photo_url 
    : getCasePhotoUrl(found.case_number, found.primary_photo_url)) || "/images/avatar-placeholder.svg";
  const timeline = found.timeline && found.timeline.length > 0
    ? found.timeline
    : generateDefaultTimeline(found);

  return {
    ...found,
    primary_photo_url: photo,
    timeline,
    photos: [
      {
        id: `photo_${found.id}`,
        storage_key: found.case_number.toLowerCase(),
        url: photo,
        is_primary: true,
        original_filename: `${found.case_number}.webp`
      }
    ]
  };
}
