import os
import hashlib
import uuid
from datetime import datetime, timedelta, timezone, date
from PIL import Image, ImageDraw, ImageFont
from app.core.database import SessionLocal, Base, engine
from app.core.security import get_password_hash
from app.core.config import settings
from app.models.entities import (
    User, GeographicLocation, MissingPersonReport, ReportPhoto,
    ConfidentialTip, Sighting, ReportStatusHistory, ModerationReview,
    ConsentRecord, DeletionRequest, NotificationSubscription,
    Notification, AuditLog, AIAnalysisResult,
    UserRole, ReportStatus, GenderEnum, TipStatus,
    ConfidentialityLevel, ModerationDecision
)
from app.services.geo_service import get_approximate_coords

def generate_synthetic_avatar(name: str, gender: str, age: int, filename: str) -> str:
    """Generates a professional civic graphic avatar for synthetic demonstration data."""
    os.makedirs(settings.STORAGE_DIR, exist_ok=True)
    img = Image.new("RGB", (400, 400), color=(15, 42, 74)) # Deep Navy
    draw = ImageDraw.Draw(img)
    
    # Outer border
    draw.rectangle([10, 10, 390, 390], outline=(13, 148, 136), width=4) # Teal border
    
    # Silhouette Head & Shoulders
    avatar_color = (226, 232, 240)
    # Head
    draw.ellipse([140, 70, 260, 190], fill=avatar_color)
    # Shoulders
    draw.chord([90, 210, 310, 370], start=0, end=180, fill=avatar_color)
    
    # Watermark text
    draw.text((120, 20), "DEMOSTRACIÓN FICTICIA", fill=(245, 158, 11))
    draw.text((110, 330), f"{name}", fill=(255, 255, 255))
    draw.text((160, 355), f"{age} años", fill=(148, 163, 184))
    
    save_path = os.path.join(settings.STORAGE_DIR, filename)
    img.save(save_path, format="WEBP", quality=85)
    return filename

def run_seed():
    print("Iniciando creación de datos ficticios de demostración para ENCUÉNTRAME NICARAGUA...")
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    
    # Check if already seeded
    if db.query(User).filter(User.email == "admin@encuentrame.ni").first():
        print("La base de datos ya contiene registros. Omitiendo seed repetido.")
        db.close()
        return

    # 1. Crear Usuarios de Prueba
    users_data = [
        ("admin@encuentrame.ni", "AdminPass2026!", "Lic. Sofía Montenegro", "8888-1001", UserRole.ADMIN.value),
        ("moderador@encuentrame.ni", "ModPass2026!", "Lic. Carlos Jarquín", "8888-1002", UserRole.MODERATOR.value),
        ("reportante@encuentrame.ni", "ReportPass2026!", "Elena María Alvarado", "8888-1003", UserRole.REPORTER.value),
        ("ciudadano@encuentrame.ni", "CitizenPass2026!", "Juan José Morales", "8888-1004", UserRole.CITIZEN.value),
    ]
    
    user_instances = {}
    for email, password, full_name, phone, role in users_data:
        u = User(
            email=email,
            password_hash=get_password_hash(password),
            full_name=full_name,
            phone_number=phone,
            role=role,
            is_active=True,
            is_verified=True
        )
        db.add(u)
        user_instances[role] = u
        
    db.commit()
    for role, u in user_instances.items():
        db.refresh(u)
        
    admin_u = user_instances[UserRole.ADMIN.value]
    mod_u = user_instances[UserRole.MODERATOR.value]
    reporter_u = user_instances[UserRole.REPORTER.value]

    # 2. Catálogo de 20 casos sintéticos representativos de Nicaragua
    seed_cases = [
        {
            "case_number": "EN-2026-0001",
            "first_name": "Mateo Andrés",
            "last_name": "García Centeno",
            "age": 14,
            "gender": GenderEnum.MALE.value,
            "dept": "Managua",
            "mun": "Ciudad Sandino",
            "zone": "Zona 4, cerca del parque central",
            "days_ago": 3,
            "desc": "Estatura 1.55m, contextura delgada, tez morena clara, cabello negro lacio corto, lunar visible cerca de la ceja derecha.",
            "clothing": "Camiseta azul marino con estampado deportivo, jeans color celeste, tenis blancos marca Converse.",
            "med": "Padece asma leve, requiere inhalador.",
            "circ": "Salió en horas de la tarde hacia la pulpería del barrio y no regresó a su domicilio.",
            "is_minor": True,
            "vulnerability": True,
            "status": ReportStatus.APPROVED_PUBLISHED.value,
            "rel": "Madre de familia",
            "is_public": True
        },
        {
            "case_number": "EN-2026-0002",
            "first_name": "Valeria Nicole",
            "last_name": "Pérez Fonseca",
            "age": 17,
            "gender": GenderEnum.FEMALE.value,
            "dept": "Matagalpa",
            "mun": "Sébaco",
            "zone": "Sector La Báscula",
            "days_ago": 5,
            "desc": "Estatura 1.62m, complexión delgada, piel blanca, ojos castaños claros, cabello castaño largo ondulado.",
            "clothing": "Blusa blanca de manga corta, pantalón negro de mezclilla, mochila escolar gris.",
            "med": "Ninguna condición médica reportada.",
            "circ": "Vista por última vez abordando una unidad de transporte colectivo interlocal hacia Matagalpa.",
            "is_minor": True,
            "vulnerability": True,
            "status": ReportStatus.APPROVED_PUBLISHED.value,
            "rel": "Tía materna",
            "is_public": True
        },
        {
            "case_number": "EN-2026-0003",
            "first_name": "Don Manuel de Jesús",
            "last_name": "Rocha Blandón",
            "age": 73,
            "gender": GenderEnum.MALE.value,
            "dept": "León",
            "mun": "León",
            "zone": "Barrio Sutiaba, costado oeste de la iglesia",
            "days_ago": 2,
            "desc": "Estatura 1.68m, cabello canoso escaso, contextura delgada, utiliza anteojos de marco metálico, bigote blanco.",
            "clothing": "Camisa guayabera beige de manga larga, pantalón de vestir café, zapatos negros de cuero.",
            "med": "Presenta desorientación por principio de pérdida de memoria senil.",
            "circ": "Salió a dar una caminata matutina en el barrio Sutiaba y se presume que perdió la noción de orientación.",
            "is_minor": False,
            "vulnerability": True,
            "status": ReportStatus.APPROVED_PUBLISHED.value,
            "rel": "Hijo",
            "is_public": True
        },
        {
            "case_number": "EN-2026-0004",
            "first_name": "Yader Francisco",
            "last_name": "Gutiérrez Marenco",
            "age": 28,
            "gender": GenderEnum.MALE.value,
            "dept": "Chinandega",
            "mun": "Corinto",
            "zone": "Zona Portuaria, muelle pesquero",
            "days_ago": 8,
            "desc": "Estatura 1.74m, piel morena, complexión atlética, cicatriz de 4 cm en antebrazo izquierdo, tatuaje de ancla en hombro derecho.",
            "clothing": "Camisa manga larga a cuadros verde y blanca, pantalón de lona azul, botas de hule negras.",
            "med": "No reporta condiciones médicas.",
            "circ": "Pescador artesanal, salió en una faena corta en estero local y la embarcación retornó a la orilla sin tripulantes.",
            "is_minor": False,
            "vulnerability": False,
            "status": ReportStatus.UNDER_INVESTIGATION.value,
            "rel": "Hermano",
            "is_public": True
        },
        {
            "case_number": "EN-2026-0005",
            "first_name": "Katherin Amanda",
            "last_name": "Salgado Méndez",
            "age": 22,
            "gender": GenderEnum.FEMALE.value,
            "dept": "Estelí",
            "mun": "Estelí",
            "zone": "Barrio El Rosario",
            "days_ago": 4,
            "desc": "Estatura 1.58m, contextura media, tez trigueña, cabello teñido de cobrizo hasta los hombros, tatuaje de mariposa en muñeca izquierda.",
            "clothing": "Suéter negro con capucha, jeans rotos azules, tenis deportivos negros.",
            "med": "Ninguna reportada.",
            "circ": "Salió de clases universitarias nocturnas hacia la parada de autobuses y su teléfono quedó fuera de servicio.",
            "is_minor": False,
            "vulnerability": False,
            "status": ReportStatus.APPROVED_PUBLISHED.value,
            "rel": "Hermana mayor",
            "is_public": True
        },
        {
            "case_number": "EN-2026-0006",
            "first_name": "Luis Alberto",
            "last_name": "Torres Zeledón",
            "age": 35,
            "gender": GenderEnum.MALE.value,
            "dept": "Jinotega",
            "mun": "San Rafael del Norte",
            "zone": "Comarca Sabana Grande",
            "days_ago": 6,
            "desc": "Estatura 1.70m, complexión robusta, piel trigueña clara, lunar pronunciado en mejilla izquierda, cabello negro crespo.",
            "clothing": "Camisa roja tipo polo, jeans azul oscuro, botas camperas de cuero café.",
            "med": "Hipertensión tratada.",
            "circ": "Se dirigía a negociar una cosecha de café en comarcas aledañas en su motocicleta roja.",
            "is_minor": False,
            "vulnerability": False,
            "status": ReportStatus.APPROVED_PUBLISHED.value,
            "rel": "Esposa",
            "is_public": True
        },
        {
            "case_number": "EN-2026-0007",
            "first_name": "Mariana del Socorro",
            "last_name": "Aguilar Obando",
            "age": 16,
            "gender": GenderEnum.FEMALE.value,
            "dept": "Masaya",
            "mun": "Nindirí",
            "zone": "Cerca del empalme de Nindirí",
            "days_ago": 1,
            "desc": "Estatura 1.60m, piel morena clara, cabello castaño lacio a la cintura, hoyuelos en ambas mejillas al sonreír.",
            "clothing": "Uniforme escolar de falda azul marino plisada y camisa blanca con monograma.",
            "med": "Sin padecimientos crónicos.",
            "circ": "No ingresó al turno vespertino del colegio; familiares no logran comunicarse por su móvil.",
            "is_minor": True,
            "vulnerability": True,
            "status": ReportStatus.APPROVED_PUBLISHED.value,
            "rel": "Madre",
            "is_public": True
        },
        {
            "case_number": "EN-2026-0008",
            "first_name": "José Ramón",
            "last_name": "Chavarría Rivas",
            "age": 42,
            "gender": GenderEnum.MALE.value,
            "dept": "Chontales",
            "mun": "Juigalpa",
            "zone": "Salida a La Libertad",
            "days_ago": 10,
            "desc": "Estatura 1.76m, complexión gruesa, cabello negro con entradas, cicatriz pequeña en labio superior.",
            "clothing": "Camisa a cuadros azul y blanco, jeans clásicos, sombrero de palma.",
            "med": "Ninguna conocida.",
            "circ": "Comerciante de ganado, viajó a una subasta regional y no se tuvo más reporte de su paradero.",
            "is_minor": False,
            "vulnerability": False,
            "status": ReportStatus.APPROVED_PUBLISHED.value,
            "rel": "Hermano",
            "is_public": True
        },
        {
            "case_number": "EN-2026-0009",
            "first_name": "Brenda Liseth",
            "last_name": "Morales Hurtado",
            "age": 19,
            "gender": GenderEnum.FEMALE.value,
            "dept": "Granada",
            "mun": "Granada",
            "zone": "Calle La Calzada hacia el malecón",
            "days_ago": 3,
            "desc": "Estatura 1.65m, piel blanca, cabello negro ondulado, piercing discreto en la aleta nasal derecha.",
            "clothing": "Vestido floreado de verano fondo negro, sandalias bajas color camel.",
            "med": "Ninguna reportada.",
            "circ": "Estudiante de turismo, fue vista por compañeros conversando en la plazoleta y no retornó a casa.",
            "is_minor": False,
            "vulnerability": False,
            "status": ReportStatus.APPROVED_PUBLISHED.value,
            "rel": "Padre de familia",
            "is_public": True
        },
        {
            "case_number": "EN-2026-00010",
            "first_name": "Wilmer Enrique",
            "last_name": "Aragón Borge",
            "age": 15,
            "gender": GenderEnum.MALE.value,
            "dept": "Carazo",
            "mun": "Diriamba",
            "zone": "Sector La Salle",
            "days_ago": 4,
            "desc": "Estatura 1.64m, tez trigueña, complexión delgada, brackets metálicos en los dientes, cabello negro corto.",
            "clothing": "Camiseta negra deportiva con logo de fútbol, short gris deportivo, zapatillas deportivas negras.",
            "med": "Ninguna reportada.",
            "circ": "Salió a una práctica deportiva en cancha comunitaria y no regresó al anochecer.",
            "is_minor": True,
            "vulnerability": True,
            "status": ReportStatus.APPROVED_PUBLISHED.value,
            "rel": "Madre",
            "is_public": True
        },
        {
            "case_number": "EN-2026-00011",
            "first_name": "Carlos Fernando",
            "last_name": "Blandón Somarriba",
            "age": 29,
            "gender": GenderEnum.MALE.value,
            "dept": "Rivas",
            "mun": "San Juan del Sur",
            "zone": "Bahía de San Juan del Sur",
            "days_ago": 7,
            "desc": "Estatura 1.78m, tez trigueña clara, complexión atlética, tatuaje de ola y sol en la pantorrilla derecha.",
            "clothing": "Camiseta blanca sin mangas, bermudas de baño azules, sandalias de cuero.",
            "med": "No reporta.",
            "circ": "Instructor de surf y socorrista local; sus pertenencias quedaron en la estación de vigilancia costera.",
            "is_minor": False,
            "vulnerability": False,
            "status": ReportStatus.UNDER_INVESTIGATION.value,
            "rel": "Hermano",
            "is_public": True
        },
        {
            "case_number": "EN-2026-00012",
            "first_name": "Dayana Marcela",
            "last_name": "Tinoco Estrada",
            "age": 24,
            "gender": GenderEnum.FEMALE.value,
            "dept": "Madriz",
            "mun": "Somoto",
            "zone": "Entrada al Cañón de Somoto",
            "days_ago": 2,
            "desc": "Estatura 1.63m, piel morena clara, cabello castaño claro amarrado en coleta, ojos café oscuros.",
            "clothing": "Camisa deportiva manga larga gris protección UV, pantalón de senderismo caqui, botas de montaña.",
            "med": "Alergia a picaduras de abejas.",
            "circ": "Turista nacional que realizaba recorrido por senderos del cañón; se separó momentáneamente del grupo.",
            "is_minor": False,
            "vulnerability": False,
            "status": ReportStatus.APPROVED_PUBLISHED.value,
            "rel": "Prima",
            "is_public": True
        },
        {
            "case_number": "EN-2026-00013",
            "first_name": "Pedro Joaquín",
            "last_name": "López Urbina",
            "age": 68,
            "gender": GenderEnum.MALE.value,
            "dept": "Boaco",
            "mun": "Camoapa",
            "zone": "Sector La Embajada",
            "days_ago": 5,
            "desc": "Estatura 1.65m, piel morena tostada por el sol, cabello blanco ondulado, camina con ligera cojera en pierna izquierda.",
            "clothing": "Camisa azul celeste de botones, pantalón caqui de tela gruesa, sombrero de paja.",
            "med": "Sufre de diabetes e hipertensión.",
            "circ": "Salió de su finca a pie rumbo a Camoapa para comprar medicamentos.",
            "is_minor": False,
            "vulnerability": True,
            "status": ReportStatus.APPROVED_PUBLISHED.value,
            "rel": "Hija",
            "is_public": True
        },
        {
            "case_number": "EN-2026-00014",
            "first_name": "Keilynn Joyse",
            "last_name": "Hodgson Campbell",
            "age": 16,
            "gender": GenderEnum.FEMALE.value,
            "dept": "Costa Caribe Sur (RACCS)",
            "mun": "Bluefields",
            "zone": "Barrio Beholden",
            "days_ago": 3,
            "desc": "Estatura 1.67m, piel morena oscura, cabello afro negro trenzado con cuentas doradas, sonrisa amplia.",
            "clothing": "Camisa amarilla sin mangas, pantalón capri blanco, zapatillas de lona rojas.",
            "med": "Ninguna condición médica.",
            "circ": "Fue vista por última vez en las cercanías del muelle municipal esperando una panga de pasajeros.",
            "is_minor": True,
            "vulnerability": True,
            "status": ReportStatus.APPROVED_PUBLISHED.value,
            "rel": "Tía",
            "is_public": True
        },
        {
            "case_number": "EN-2026-00015",
            "first_name": "Erick Jayson",
            "last_name": "Finley Dixon",
            "age": 21,
            "gender": GenderEnum.MALE.value,
            "dept": "Costa Caribe Norte (RACCN)",
            "mun": "Puerto Cabezas (Bilwi)",
            "zone": "Sector El Muelle / Barrio Peter Ferrera",
            "days_ago": 4,
            "desc": "Estatura 1.75m, tez morena, complexión delgada y ágil, tatuaje de compás náutico en el pecho.",
            "clothing": "Camiseta de básquetbol azul con número 7, pantalón deportivo negro, gorra azul.",
            "med": "Sin enfermedades crónicas.",
            "circ": "Se dirigía a laborar en una bodega cercana a la costa marítima y no fue visto por sus compañeros.",
            "is_minor": False,
            "vulnerability": False,
            "status": ReportStatus.APPROVED_PUBLISHED.value,
            "rel": "Madre",
            "is_public": True
        },
        {
            "case_number": "EN-2026-00016",
            "first_name": "Francisco Javier",
            "last_name": "Cruz Pastrana",
            "age": 31,
            "gender": GenderEnum.MALE.value,
            "dept": "Nueva Segovia",
            "mun": "Jalapa",
            "zone": "Comarca Teotecacinte",
            "days_ago": 9,
            "desc": "Estatura 1.72m, contextura fuerte, cabello lacio negro, mancha de nacimiento oscura en cuello posterior.",
            "clothing": "Camisa vaquera azul, pantalón vaquero negro, cinturón de cuero con hebilla metálica.",
            "med": "Ninguna médica relevante.",
            "circ": "Agricultor de tabaco y granos básicos; se trasladaba a inspeccionar tierras de cultivo fronterizas.",
            "is_minor": False,
            "vulnerability": False,
            "status": ReportStatus.APPROVED_PUBLISHED.value,
            "rel": "Hermana",
            "is_public": True
        },
        {
            "case_number": "EN-2026-00017",
            "first_name": "Rosa Nelly",
            "last_name": "Castillo Oporta",
            "age": 38,
            "gender": GenderEnum.FEMALE.value,
            "dept": "Río San Juan",
            "mun": "San Carlos",
            "zone": "Malecón de San Carlos, cerca de la fortaleza",
            "days_ago": 6,
            "desc": "Estatura 1.57m, complexión mediana, piel trigueña clara, cabello negro recogido con gancho plástico café.",
            "clothing": "Blusa rosada de botones, falda de tela oscura por debajo de la rodilla, sandalias negras.",
            "med": "No reporta.",
            "circ": "Comerciante de artesanías fluviales; su teléfono celular no recibe llamadas desde el día señalado.",
            "is_minor": False,
            "vulnerability": False,
            "status": ReportStatus.APPROVED_PUBLISHED.value,
            "rel": "Cónyuge",
            "is_public": True
        },
        # 3 Casos PENDIENTES DE REVISIÓN (para verificar panel de moderación y seguridad)
        {
            "case_number": "EN-2026-00018",
            "first_name": "Kevin Josué",
            "last_name": "Moncada Rivera",
            "age": 16,
            "gender": GenderEnum.MALE.value,
            "dept": "Managua",
            "mun": "Tipitapa",
            "zone": "Barrio San Juan",
            "days_ago": 1,
            "desc": "Estatura 1.68m, piel morena clara, cabello negro corto estilo degradado, cicatriz en la ceja izquierda.",
            "clothing": "Camiseta blanca estampada, jeans negros, tenis deportivos rojos.",
            "med": "Ninguna condición médica.",
            "circ": "Salió en bicicleta roja hacia una librería y no ha retornado a su vivienda familiar.",
            "is_minor": True,
            "vulnerability": True,
            "status": ReportStatus.PENDING_REVIEW.value,
            "rel": "Hermano mayor",
            "is_public": False  # Not approved yet!
        },
        {
            "case_number": "EN-2026-00019",
            "first_name": "Sonia Elizabeth",
            "last_name": "Calero Solís",
            "age": 27,
            "gender": GenderEnum.FEMALE.value,
            "dept": "León",
            "mun": "Nagarote",
            "zone": "Sector Los Mangos",
            "days_ago": 2,
            "desc": "Estatura 1.60m, piel clara, contextura delgada, ojos pardos, cabello negro largo ondulado.",
            "clothing": "Blusa azul cielo, pantalón negro de vestir, zapatos bajos negros.",
            "med": "Migraña crónica.",
            "circ": "No se presentó a su centro laboral en horario matutino habitual.",
            "is_minor": False,
            "vulnerability": False,
            "status": ReportStatus.PENDING_REVIEW.value,
            "rel": "Madre",
            "is_public": False
        },
        # 1 Caso CERRADO LOCALIZADO (para verificar que los casos cerrados no revelan domicilios privados)
        {
            "case_number": "EN-2026-00020",
            "first_name": "Gerardo Antonio",
            "last_name": "Mendoza Espinoza",
            "age": 52,
            "gender": GenderEnum.MALE.value,
            "dept": "Managua",
            "mun": "Managua",
            "zone": "Distrito 5",
            "days_ago": 14,
            "desc": "Estatura 1.70m, tez morena, bigote poblado, anteojos de lectura.",
            "clothing": "Camisa azul manga corta, jeans celestes.",
            "med": "Tratamiento de tensión arterial.",
            "circ": "Reportado no localizado temporalmente tras pérdida de contacto por avería de vehículo en zona rural.",
            "is_minor": False,
            "vulnerability": False,
            "status": ReportStatus.CLOSED_FOUND.value,
            "rel": "Hermano",
            "is_public": False # De-published upon safe reunification
        }
    ]

    for case_data in seed_cases:
        lat, lng = get_approximate_coords(case_data["dept"], case_data["mun"])
        
        loc = GeographicLocation(
            department=case_data["dept"],
            municipality=case_data["mun"],
            neighborhood_zone=case_data["zone"],
            approximate_latitude=lat,
            approximate_longitude=lng,
            is_sensitive=True
        )
        db.add(loc)
        db.flush()
        
        disap_time = datetime.now(timezone.utc) - timedelta(days=case_data["days_ago"], hours=4)
        pub_time = disap_time + timedelta(hours=12) if case_data["is_public"] else None
        
        report = MissingPersonReport(
            case_number=case_data["case_number"],
            reporter_id=reporter_u.id,
            status=case_data["status"],
            first_name=case_data["first_name"],
            last_name=case_data["last_name"],
            nickname=None,
            age_at_disappearance=case_data["age"],
            birth_date=date(datetime.now().year - case_data["age"], 5, 15),
            gender=case_data["gender"],
            disappearance_date=disap_time,
            location_id=loc.id,
            physical_description=case_data["desc"],
            clothing_description=case_data["clothing"],
            medical_conditions=case_data["med"],
            circumstances=case_data["circ"],
            is_minor=case_data["is_minor"],
            vulnerability_flag=case_data["vulnerability"],
            is_public=case_data["is_public"],
            published_at=pub_time,
            created_at=disap_time - timedelta(hours=2)
        )
        db.add(report)
        db.flush()
        
        # Synthetic avatar generation
        avatar_file = f"avatar_{case_data['case_number'].lower()}.webp"
        generate_synthetic_avatar(
            name=f"{case_data['first_name']} {case_data['last_name']}",
            gender=case_data["gender"],
            age=case_data["age"],
            filename=avatar_file
        )
        
        photo = ReportPhoto(
            report_id=report.id,
            storage_key=avatar_file,
            is_primary=True,
            is_approved=True,
            blur_level=0,
            original_filename=f"{avatar_file}.png",
            file_hash_sha256=hashlib.sha256(avatar_file.encode()).hexdigest()
        )
        db.add(photo)
        
        # Consent record
        consent = ConsentRecord(
            report_id=report.id,
            reporter_id=reporter_u.id,
            relationship_to_victim=case_data["rel"],
            identity_doc_hash=hashlib.sha256(f"DOC-{case_data['case_number']}".encode()).hexdigest(),
            consent_text_version="v1.0-Ley787",
            ip_address_hash=hashlib.sha256("190.212.10.5".encode()).hexdigest(),
            accepted_terms_timestamp=disap_time - timedelta(hours=2)
        )
        db.add(consent)
        
        # Status history
        history = ReportStatusHistory(
            report_id=report.id,
            changed_by=reporter_u.id,
            previous_status="draft",
            new_status=case_data["status"],
            reason="Registro inicial validado con declaración jurada",
            created_at=disap_time
        )
        db.add(history)
        
        # If approved, add moderation review
        if case_data["is_public"]:
            mod_review = ModerationReview(
                report_id=report.id,
                moderator_id=mod_u.id,
                decision=ModerationDecision.APPROVE.value,
                notes_internal="Documentación de parentesco comprobada y consentimiento firmado.",
                created_at=pub_time
            )
            db.add(mod_review)
            
    db.commit()

    # 3. Pistas confidenciales simuladas de prueba (para casos 1 y 2)
    case_1 = db.query(MissingPersonReport).filter(MissingPersonReport.case_number == "EN-2026-0001").first()
    case_2 = db.query(MissingPersonReport).filter(MissingPersonReport.case_number == "EN-2026-0002").first()
    
    if case_1:
        tip1 = ConfidentialTip(
            report_id=case_1.id,
            tip_code="PISTA-8A12-9F01",
            description="Fue visto en la parada del bus interurbano de Ciudad Sandino con dirección al Mercado Israel Lewites.",
            sighting_date=datetime.now(timezone.utc) - timedelta(days=1),
            confidentiality_level=ConfidentialityLevel.STRICT_ANONYMOUS.value,
            status=TipStatus.TRIAGED.value,
            reviewed_by=mod_u.id
        )
        db.add(tip1)
        
    if case_2:
        tip2 = ConfidentialTip(
            report_id=case_2.id,
            tip_code="PISTA-7C34-2D99",
            description="Una joven con características similares fue vista en el parque central de Matagalpa acompañada de una compañera de estudios.",
            sighting_date=datetime.now(timezone.utc) - timedelta(days=2),
            informant_contact="8822-9911 (Solo WhatsApp)",
            confidentiality_level=ConfidentialityLevel.CONTACTABLE_MODERATOR_ONLY.value,
            status=TipStatus.RECEIVED.value
        )
        db.add(tip2)

    # 4. Suscripciones y notificaciones de prueba
    sub1 = NotificationSubscription(
        user_id=reporter_u.id,
        email="alertas.managua@demo.ni",
        department="Managua",
        is_active=True,
        token_unsubscribe=uuid.uuid4().hex
    )
    db.add(sub1)
    db.flush()
    
    notif1 = Notification(
        subscription_id=sub1.id,
        type="new_approved_case",
        title="Nueva Alerta Aprobada: Mateo Andrés García (Ciudad Sandino)",
        content="Se ha publicado un nuevo reporte de búsqueda verificado en el departamento de Managua.",
        status="sent"
    )
    db.add(notif1)

    # 5. Registro de auditoría inicial
    audit1 = AuditLog(
        user_id=admin_u.id,
        action="SYSTEM_INIT_SEED",
        entity_name="system",
        entity_id="GLOBAL",
        ip_address="127.0.0.1",
        details_json={"cases_seeded": 20, "environment": "DEMOSTRACION_CONTROLADA"}
    )
    db.add(audit1)
    
    db.commit()
    db.close()
    print("Seed completado exitosamente con 20 casos sintéticos representativos y datos de demostración.")

if __name__ == "__main__":
    run_seed()
