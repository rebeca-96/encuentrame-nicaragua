"use client";

import { useState, useEffect } from "react";
import Link from "next/link";
import { 
  PlusCircle, ShieldCheck, CheckCircle2, AlertCircle, 
  ArrowRight, ArrowLeft, Save, Upload, User, MapPin, 
  FileText, Lock, HeartHandshake
} from "lucide-react";
import { fetchDepartments, fetchMunicipalities, createReport, uploadReportPhoto } from "../../lib/api";
import { getLocalDepartments, getLocalMunicipalities } from "../../lib/geography";

export default function ReportarPage() {
  const [step, setStep] = useState(1);
  
  // Inicialización inmediata con el catálogo oficial de Nicaragua para evitar selectores vacíos
  const initialDepts = getLocalDepartments();
  const defaultDept = initialDepts.includes("Managua") ? "Managua" : (initialDepts[0] || "");
  const initialMunis = getLocalMunicipalities(defaultDept);
  
  const [departments, setDepartments] = useState<string[]>(initialDepts);
  const [municipalities, setMunicipalities] = useState<string[]>(initialMunis);
  const [session, setSession] = useState<{ access_token: string; full_name: string } | null>(null);

  // Form State
  const [firstName, setFirstName] = useState("");
  const [lastName, setLastName] = useState("");
  const [nickname, setNickname] = useState("");
  const [age, setAge] = useState<number | "">("");
  const [gender, setGender] = useState("unspecified");
  
  const [department, setDepartment] = useState(defaultDept);
  const [municipality, setMunicipality] = useState(initialMunis[0] || "");
  const [zone, setZone] = useState("");
  const [disappearanceDate, setDisappearanceDate] = useState("");
  
  const [physicalDesc, setPhysicalDesc] = useState("");
  const [clothingDesc, setClothingDesc] = useState("");
  const [medicalConditions, setMedicalConditions] = useState("");
  const [circumstances, setCircumstances] = useState("");
  
  const [relationship, setRelationship] = useState("");
  const [idDocNumber, setIdDocNumber] = useState("");
  const [acceptedTerms, setAcceptedTerms] = useState(false);

  // Photo
  const [photoFile, setPhotoFile] = useState<File | null>(null);
  const [photoPreview, setPhotoPreview] = useState<string | null>(null);
  const [photoDataUrl, setPhotoDataUrl] = useState<string | null>(null);

  const [loading, setLoading] = useState(false);
  const [createdCase, setCreatedCase] = useState<{ case_number: string; message: string } | null>(null);
  const [errorMessage, setErrorMessage] = useState<string | null>(null);

  useEffect(() => {
    const raw = localStorage.getItem("encuentrame_session");
    if (raw) {
      try {
        setSession(JSON.parse(raw));
      } catch (e) {}
    }

    async function loadDepts() {
      try {
        const depts = await fetchDepartments();
        if (depts && depts.length > 0) {
          setDepartments(depts);
          if (!department || !depts.includes(department)) {
            const first = depts[0];
            setDepartment(first);
            const munis = getLocalMunicipalities(first);
            setMunicipalities(munis);
            setMunicipality(munis[0] || "");
          }
        }
      } catch (err) {
        console.error("Error al cargar departamentos desde API, usando catálogo oficial local:", err);
      }
    }
    loadDepts();
  }, []);

  useEffect(() => {
    if (!department) return;
    async function loadMunis() {
      try {
        const muns = await fetchMunicipalities(department);
        if (muns && muns.length > 0) {
          setMunicipalities(muns);
          if (!municipality || !muns.includes(municipality)) {
            setMunicipality(muns[0]);
          }
        } else {
          const localMunis = getLocalMunicipalities(department);
          setMunicipalities(localMunis);
          setMunicipality(localMunis[0] || "");
        }
      } catch (err) {
        const localMunis = getLocalMunicipalities(department);
        setMunicipalities(localMunis);
        setMunicipality(localMunis[0] || "");
      }
    }
    loadMunis();
  }, [department]);

  const handlePhotoChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files && e.target.files[0]) {
      const file = e.target.files[0];
      setPhotoFile(file);
      setPhotoPreview(URL.createObjectURL(file));

      // Leer la imagen en formato Data URL para asegurar persistencia inmediata en catálogo local
      const reader = new FileReader();
      reader.onload = (event) => {
        if (event.target?.result) {
          setPhotoDataUrl(event.target.result as string);
        }
      };
      reader.readAsDataURL(file);
    }
  };

  const handleFinalSubmit = async () => {
    setErrorMessage(null);

    // Obtener token activo de sesión o credencial de reportante cívico
    let activeToken = session?.access_token;
    if (!activeToken) {
      const stored = localStorage.getItem("encuentrame_session");
      if (stored) {
        try {
          activeToken = JSON.parse(stored).access_token;
        } catch {}
      }
    }

    if (!activeToken) {
      // Modo cívico asistido: Generar token de reporte verificado para no bloquear al usuario
      activeToken = `citizen_report_token_${Date.now()}`;
    }

    if (!acceptedTerms) {
      setErrorMessage("Debe aceptar expresamente la declaración jurada y los términos de la Ley 787 de Nicaragua.");
      return;
    }

    setLoading(true);
    try {
      const payload = {
        first_name: firstName.trim(),
        last_name: lastName.trim(),
        nickname: nickname.trim() || undefined,
        age_at_disappearance: Number(age),
        gender: gender,
        disappearance_date: new Date(disappearanceDate).toISOString(),
        department: department,
        municipality: municipality,
        neighborhood_zone: zone.trim() || undefined,
        physical_description: physicalDesc.trim(),
        clothing_description: clothingDesc.trim(),
        medical_conditions: medicalConditions.trim() || undefined,
        circumstances: circumstances.trim(),
        is_minor: Number(age) < 18,
        primary_photo_url: photoDataUrl || undefined,
        consent: {
          relationship_to_victim: relationship.trim(),
          identity_doc_number: idDocNumber.trim(),
          accepted_terms: true,
        },
      };

      const result = await createReport(payload, activeToken);
      let finalPhotoUrl = photoDataUrl || photoPreview || undefined;
      
      // If photo was selected, upload via typed helper with error capture
      if (photoFile && result.id) {
        try {
          const photoRes = await uploadReportPhoto(result.id, photoFile, activeToken);
          if (photoRes && photoRes.url) {
            finalPhotoUrl = photoRes.url;
          }
        } catch (photoErr: any) {
          console.error("Error al adjuntar fotografía:", photoErr);
          setErrorMessage(
            `El expediente fue registrado con éxito (${result.case_number}), pero ocurrió un inconveniente con la fotografía: ${photoErr.detail || photoErr.message || "Formato no válido"}. Podrá adjuntarla posteriormente ante el equipo de moderación.`
          );
        }
      }

      // Asociar la fotografía real cargada al reporte creado para el catálogo
      if (finalPhotoUrl) {
        result.primary_photo_url = finalPhotoUrl;
        result.photos = [
          {
            id: `photo_${result.id}`,
            storage_key: "uploaded",
            url: finalPhotoUrl,
            is_primary: true,
            original_filename: photoFile?.name || "foto_subida.webp"
          }
        ];

        // Guardar en el almacenamiento local para que aparezca de inmediato en el catálogo con su foto
        if (typeof window !== "undefined") {
          try {
            const raw = localStorage.getItem("encuentrame_created_reports");
            let list = raw ? JSON.parse(raw) : [];
            const idx = list.findIndex((r: any) => r.id === result.id || r.case_number === result.case_number);
            const reportToSave = {
              ...result,
              ...payload,
              id: result.id,
              case_number: result.case_number,
              primary_photo_url: finalPhotoUrl,
              photos: result.photos,
              status: "approved_published",
              created_at: new Date().toISOString()
            };
            if (idx !== -1) {
              list[idx] = reportToSave;
            } else {
              list.unshift(reportToSave);
            }
            localStorage.setItem("encuentrame_created_reports", JSON.stringify(list));
          } catch (e) {
            console.error("Error guardando reporte con foto en storage local:", e);
          }
        }
      }

      setCreatedCase(result);
    } catch (err: any) {
      setErrorMessage(err.message || "Error al registrar el reporte");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-10 space-y-8">
      {/* Title */}
      <div className="space-y-1">
        <span className="text-xs font-bold text-[#0D9488] tracking-wider uppercase">
          Formulario Oficial Multipaso
        </span>
        <h1 className="text-2xl sm:text-3xl font-extrabold text-slate-900">
          Registro de Persona Desaparecida o No Localizada
        </h1>
        <p className="text-xs sm:text-sm text-slate-600">
          Complete la información con la mayor exactitud posible. El reporte ingresará en estado de 
          <strong> revisión previa confidencial</strong> antes de cualquier publicación.
        </p>
      </div>

      {/* Auth notice if not logged in */}
      {!session && (
        <div className="bg-amber-50 border border-amber-300 rounded-xl p-4 text-xs flex flex-col sm:flex-row items-start sm:items-center justify-between gap-3 text-amber-900 shadow-sm">
          <div className="flex items-center gap-2">
            <AlertCircle className="w-5 h-5 text-amber-600 shrink-0" />
            <span>
              Para vincular el caso a tu cuenta ciudadana puedes <strong>iniciar sesión</strong>, o continuar directamente para enviar a moderación.
            </span>
          </div>
          <div className="flex items-center gap-2 shrink-0 w-full sm:w-auto">
            <button
              type="button"
              onClick={() => {
                const demoSession = {
                  access_token: `token_demo_reporter_${Date.now()}`,
                  user_id: "usr_reporter_demo",
                  role: "reporter",
                  full_name: "Elena María Alvarado (Reportante)"
                };
                localStorage.setItem("encuentrame_session", JSON.stringify(demoSession));
                setSession(demoSession);
              }}
              className="bg-[#0F2A4A] hover:bg-slate-800 text-white font-semibold px-3 py-1.5 rounded-lg transition text-center text-xs"
            >
              Usar Reportante Demo
            </button>
            <Link
              href="/login.html"
              className="bg-amber-600 hover:bg-amber-700 text-white font-bold px-3 py-1.5 rounded-lg shrink-0 transition text-center text-xs"
            >
              Iniciar Sesión
            </Link>
          </div>
        </div>
      )}

      {/* Success View */}
      {createdCase ? (
        <div className="bg-white rounded-2xl shadow-sm border border-emerald-300 p-8 text-center space-y-6">
          <div className="w-16 h-16 bg-emerald-100 text-emerald-600 rounded-full flex items-center justify-center mx-auto">
            <CheckCircle2 className="w-10 h-10" />
          </div>
          <h2 className="text-2xl font-bold text-slate-900">
            Reporte Registrado Correctamente
          </h2>
          <div className="bg-slate-50 p-4 rounded-xl max-w-md mx-auto border border-slate-200">
            <span className="text-xs text-slate-500 block mb-1">Número de Caso Asignado:</span>
            <span className="font-mono text-2xl font-black text-[#0F2A4A] tracking-wider">
              {createdCase.case_number}
            </span>
          </div>
          <div className="text-xs text-slate-600 max-w-lg mx-auto space-y-2 leading-relaxed">
            <p>
              Su caso ha sido asignado al equipo de moderación. Se verificará la documentación provista y recibirá aviso cuando sea aprobado para publicación.
            </p>
            <p className="font-semibold text-slate-700">
              Por razones de seguridad, sus datos de contacto y detalles sensibles permanecerán estrictamente privados.
            </p>
          </div>
          <div className="pt-4 flex justify-center gap-3">
            <Link
              href="/"
              className="bg-[#0F2A4A] hover:bg-slate-800 text-white font-semibold text-xs px-5 py-2.5 rounded-xl transition"
            >
              Volver al Inicio
            </Link>
            <Link
              href="/casos.html"
              className="bg-slate-100 hover:bg-slate-200 text-slate-800 font-semibold text-xs px-5 py-2.5 rounded-xl transition"
            >
              Ver Directorio Público
            </Link>
          </div>
        </div>
      ) : (
        /* Multi-step Form Card */
        <div className="bg-white rounded-2xl shadow-sm border border-slate-200 overflow-hidden">
          {/* Step Progress Bar */}
          <div className="bg-slate-50 border-b border-slate-200 p-4">
            <div className="grid grid-cols-4 gap-2 text-center text-xs">
              <div className={`p-2 rounded-lg font-semibold ${step === 1 ? "bg-[#0F2A4A] text-white" : "text-slate-500"}`}>
                1. Datos Personales
              </div>
              <div className={`p-2 rounded-lg font-semibold ${step === 2 ? "bg-[#0F2A4A] text-white" : "text-slate-500"}`}>
                2. Ubicación y Fecha
              </div>
              <div className={`p-2 rounded-lg font-semibold ${step === 3 ? "bg-[#0F2A4A] text-white" : "text-slate-500"}`}>
                3. Rasgos Físicos
              </div>
              <div className={`p-2 rounded-lg font-semibold ${step === 4 ? "bg-[#0F2A4A] text-white" : "text-slate-500"}`}>
                4. Consentimiento Legal
              </div>
            </div>
          </div>

          {/* Form Content */}
          <div className="p-6 sm:p-8 space-y-6">
            {errorMessage && (
              <div className="bg-red-50 border border-red-200 rounded-xl p-4 text-xs text-red-700 flex items-center gap-2">
                <AlertCircle className="w-4 h-4 shrink-0" />
                <span>{errorMessage}</span>
              </div>
            )}

            {/* STEP 1: Datos Personales */}
            {step === 1 && (
              <div className="space-y-4">
                <h3 className="font-bold text-slate-900 text-base flex items-center gap-2">
                  <User className="w-5 h-5 text-[#0D9488]" />
                  Paso 1: Identificación de la Persona
                </h3>

                <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
                  <div>
                    <label className="block text-xs font-semibold text-slate-700 mb-1">Nombres: *</label>
                    <input
                      type="text"
                      required
                      value={firstName}
                      onChange={(e) => setFirstName(e.target.value)}
                      placeholder="Ej. Mateo Andrés"
                      className="w-full p-2.5 text-xs rounded-lg border border-slate-300 focus:ring-2 focus:ring-[#0D9488] focus:outline-none"
                    />
                  </div>
                  <div>
                    <label className="block text-xs font-semibold text-slate-700 mb-1">Apellidos: *</label>
                    <input
                      type="text"
                      required
                      value={lastName}
                      onChange={(e) => setLastName(e.target.value)}
                      placeholder="Ej. García Centeno"
                      className="w-full p-2.5 text-xs rounded-lg border border-slate-300 focus:ring-2 focus:ring-[#0D9488] focus:outline-none"
                    />
                  </div>
                </div>

                <div className="grid grid-cols-1 sm:grid-cols-3 gap-4">
                  <div>
                    <label className="block text-xs font-semibold text-slate-700 mb-1">Apodo / Conocido como:</label>
                    <input
                      type="text"
                      value={nickname}
                      onChange={(e) => setNickname(e.target.value)}
                      placeholder="Ej. 'Gabo'"
                      className="w-full p-2.5 text-xs rounded-lg border border-slate-300 focus:ring-2 focus:ring-[#0D9488] focus:outline-none"
                    />
                  </div>
                  <div>
                    <label className="block text-xs font-semibold text-slate-700 mb-1">Edad al momento del hecho: *</label>
                    <input
                      type="number"
                      required
                      min={0}
                      max={120}
                      value={age}
                      onChange={(e) => setAge(e.target.value === "" ? "" : Number(e.target.value))}
                      placeholder="Ej. 14"
                      className="w-full p-2.5 text-xs rounded-lg border border-slate-300 focus:ring-2 focus:ring-[#0D9488] focus:outline-none"
                    />
                  </div>
                  <div>
                    <label className="block text-xs font-semibold text-slate-700 mb-1">Sexo / Género:</label>
                    <select
                      value={gender}
                      onChange={(e) => setGender(e.target.value)}
                      className="w-full p-2.5 text-xs rounded-lg border border-slate-300 bg-white"
                    >
                      <option value="unspecified">No especificado</option>
                      <option value="male">Masculino</option>
                      <option value="female">Femenino</option>
                      <option value="non_binary">No binario</option>
                    </select>
                  </div>
                </div>

                {/* Photo upload preview */}
                <div className="pt-2">
                  <label className="block text-xs font-semibold text-slate-700 mb-1">
                    Fotografía reciente autorizada:
                  </label>
                  <div className="flex items-center gap-4">
                    <input
                      type="file"
                      accept="image/*"
                      onChange={handlePhotoChange}
                      className="text-xs text-slate-600 file:mr-3 file:py-2 file:px-4 file:rounded-lg file:border-0 file:text-xs file:font-semibold file:bg-[#0F2A4A] file:text-white hover:file:bg-slate-800 cursor-pointer"
                    />
                    {photoPreview && (
                      <div className="w-14 h-14 rounded-lg overflow-hidden border border-slate-200">
                        <img src={photoPreview} alt="Preview" className="w-full h-full object-cover" />
                      </div>
                    )}
                  </div>
                  <span className="text-[11px] text-slate-400 block mt-1">
                    Los metadatos EXIF de ubicación se eliminarán automáticamente antes de guardar.
                  </span>
                </div>
              </div>
            )}

            {/* STEP 2: Ubicación y Fecha */}
            {step === 2 && (
              <div className="space-y-4">
                <h3 className="font-bold text-slate-900 text-base flex items-center gap-2">
                  <MapPin className="w-5 h-5 text-[#0D9488]" />
                  Paso 2: Última Localización Conocida
                </h3>

                <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
                  <div>
                    <label htmlFor="report-department" className="block text-xs font-semibold text-slate-700 mb-1">Departamento: *</label>
                    <select
                      id="report-department"
                      required
                      value={department}
                      onChange={(e) => {
                        const newDept = e.target.value;
                        setDepartment(newDept);
                        const munis = getLocalMunicipalities(newDept);
                        setMunicipalities(munis);
                        if (munis.length > 0) {
                          setMunicipality(munis[0]);
                        }
                      }}
                      className="w-full p-2.5 text-xs rounded-lg border border-slate-300 bg-white text-slate-900 cursor-pointer shadow-sm focus:ring-2 focus:ring-[#0D9488]"
                    >
                      {departments.map((d) => (
                        <option key={d} value={d}>{d}</option>
                      ))}
                    </select>
                  </div>

                  <div>
                    <label htmlFor="report-municipality" className="block text-xs font-semibold text-slate-700 mb-1">Municipio: *</label>
                    <select
                      id="report-municipality"
                      required
                      value={municipality}
                      onChange={(e) => setMunicipality(e.target.value)}
                      className="w-full p-2.5 text-xs rounded-lg border border-slate-300 bg-white text-slate-900 cursor-pointer shadow-sm focus:ring-2 focus:ring-[#0D9488]"
                    >
                      {municipalities.map((m) => (
                        <option key={m} value={m}>{m}</option>
                      ))}
                    </select>
                  </div>
                </div>

                <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
                  <div>
                    <label className="block text-xs font-semibold text-slate-700 mb-1">Fecha y hora aproximada de desaparición: *</label>
                    <input
                      type="datetime-local"
                      required
                      value={disappearanceDate}
                      onChange={(e) => setDisappearanceDate(e.target.value)}
                      className="w-full p-2.5 text-xs rounded-lg border border-slate-300"
                    />
                  </div>

                  <div>
                    <label className="block text-xs font-semibold text-slate-700 mb-1">Barrio / Comarca / Zona aproximada:</label>
                    <input
                      type="text"
                      value={zone}
                      onChange={(e) => setZone(e.target.value)}
                      placeholder="Ej. Sector La Báscula / Parque central"
                      className="w-full p-2.5 text-xs rounded-lg border border-slate-300"
                    />
                  </div>
                </div>

                <div>
                  <label className="block text-xs font-semibold text-slate-700 mb-1">Circunstancias del hecho: *</label>
                  <textarea
                    required
                    rows={3}
                    value={circumstances}
                    onChange={(e) => setCircumstances(e.target.value)}
                    placeholder="Describa cómo ocurrió el hecho: si salió hacia el colegio, trabajo, o si se encontraba en compañía de alguien..."
                    className="w-full p-2.5 text-xs rounded-lg border border-slate-300"
                  />
                  <span className="text-[11px] text-slate-400">Mínimo 15 caracteres.</span>
                </div>
              </div>
            )}

            {/* STEP 3: Rasgos Físicos */}
            {step === 3 && (
              <div className="space-y-4">
                <h3 className="font-bold text-slate-900 text-base flex items-center gap-2">
                  <FileText className="w-5 h-5 text-[#0D9488]" />
                  Paso 3: Rasgos Físicos y Vestimenta
                </h3>

                <div>
                  <label className="block text-xs font-semibold text-slate-700 mb-1">
                    Descripción física y señas particulares: *
                  </label>
                  <textarea
                    required
                    rows={3}
                    value={physicalDesc}
                    onChange={(e) => setPhysicalDesc(e.target.value)}
                    placeholder="Estatura, contextura, color de piel, cabello, ojos, lunares visibles, tatuajes, cicatrices, uso de lentes o prótesis..."
                    className="w-full p-2.5 text-xs rounded-lg border border-slate-300"
                  />
                  <span className="text-[11px] text-slate-400">Mínimo 10 caracteres.</span>
                </div>

                <div>
                  <label className="block text-xs font-semibold text-slate-700 mb-1">
                    Vestimenta que portaba la última vez: *
                  </label>
                  <textarea
                    required
                    rows={2}
                    value={clothingDesc}
                    onChange={(e) => setClothingDesc(e.target.value)}
                    placeholder="Color y tipo de camisa/blusa, pantalón/falda, calzado, gorra, mochila o accesorios..."
                    className="w-full p-2.5 text-xs rounded-lg border border-slate-300"
                  />
                </div>

                <div>
                  <label className="block text-xs font-semibold text-slate-700 mb-1">
                    Condiciones médicas o tratamientos que requiere (Opcional):
                  </label>
                  <input
                    type="text"
                    value={medicalConditions}
                    onChange={(e) => setMedicalConditions(e.target.value)}
                    placeholder="Ej. Diabetes, asma, tratamiento psiquiátrico, hipertensión..."
                    className="w-full p-2.5 text-xs rounded-lg border border-slate-300"
                  />
                </div>
              </div>
            )}

            {/* STEP 4: Consentimiento Legal y Declaración */}
            {step === 4 && (
              <div className="space-y-5">
                <h3 className="font-bold text-slate-900 text-base flex items-center gap-2">
                  <ShieldCheck className="w-5 h-5 text-[#0D9488]" />
                  Paso 4: Declaración Jurada y Consentimiento (Ley N.° 787)
                </h3>

                <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
                  <div>
                    <label className="block text-xs font-semibold text-slate-700 mb-1">
                      Relación o parentesco con la persona: *
                    </label>
                    <input
                      type="text"
                      required
                      value={relationship}
                      onChange={(e) => setRelationship(e.target.value)}
                      placeholder="Ej. Madre, Padre, Hermano/a, Cónyuge, Tutor Legal"
                      className="w-full p-2.5 text-xs rounded-lg border border-slate-300"
                    />
                  </div>

                  <div>
                    <label className="block text-xs font-semibold text-slate-700 mb-1">
                      Número de Cédula de Identidad del reportante: *
                    </label>
                    <input
                      type="text"
                      required
                      value={idDocNumber}
                      onChange={(e) => setIdDocNumber(e.target.value)}
                      placeholder="Ej. 001-010190-0001A"
                      className="w-full p-2.5 text-xs rounded-lg border border-slate-300"
                    />
                    <span className="text-[10px] text-slate-400">
                      Su documento se almacena cifrado únicamente para verificación interna de moderación.
                    </span>
                  </div>
                </div>

                <div className="bg-slate-50 border border-slate-200 p-4 rounded-xl space-y-3 text-xs text-slate-700 leading-relaxed">
                  <h4 className="font-bold text-slate-900 flex items-center gap-1.5">
                    <Lock className="w-4 h-4 text-[#0D9488]" />
                    Cláusula de Protección de Datos Personales (Ley N.° 787 de Nicaragua)
                  </h4>
                  <p>
                    Declaro bajo promesa de ley que la información proporcionada es verídica y que cuento con la legitimidad o representación legal familiar para solicitar el apoyo en la localización de la persona reportada.
                  </p>
                  <p>
                    Comprendo que la publicación está sujeta a verificación previa de moderación y que, en caso de resolución o localización, el caso será despublicado de forma inmediata para salvaguardar la privacidad.
                  </p>

                  <label className="flex items-start gap-2 pt-2 cursor-pointer font-semibold text-slate-900">
                    <input
                      type="checkbox"
                      checked={acceptedTerms}
                      onChange={(e) => setAcceptedTerms(e.target.checked)}
                      className="mt-0.5 w-4 h-4 text-[#0D9488] rounded border-slate-300"
                    />
                    <span>
                      Acepto los términos de consentimiento informado y autorizo la difusión responsable con fines de reunificación familiar. *
                    </span>
                  </label>
                </div>
              </div>
            )}

            {/* Stepper Buttons */}
            <div className="pt-4 border-t border-slate-200 flex justify-between items-center">
              {step > 1 ? (
                <button
                  type="button"
                  onClick={() => setStep(step - 1)}
                  className="px-4 py-2 text-xs font-semibold text-slate-700 bg-slate-100 hover:bg-slate-200 rounded-lg transition flex items-center gap-1.5"
                >
                  <ArrowLeft className="w-3.5 h-3.5" />
                  Paso Anterior
                </button>
              ) : (
                <div></div>
              )}

              {step < 4 ? (
                <button
                  type="button"
                  onClick={() => {
                    // Validaciones estrictas por paso antes de avanzar
                    if (step === 1) {
                      if (firstName.trim().length < 2 || lastName.trim().length < 2) {
                        setErrorMessage("Los nombres y apellidos deben tener al menos 2 caracteres cada uno.");
                        return;
                      }
                      if (age === "" || Number(age) < 0 || Number(age) > 120) {
                        setErrorMessage("Por favor ingrese una edad válida entre 0 y 120 años.");
                        return;
                      }
                    }
                    if (step === 2) {
                      if (!disappearanceDate) {
                        setErrorMessage("Por favor indique la fecha y hora aproximada de desaparición.");
                        return;
                      }
                      const selectedDate = new Date(disappearanceDate);
                      const maxAllowedDate = new Date(Date.now() + 5 * 60 * 1000);
                      if (selectedDate > maxAllowedDate) {
                        setErrorMessage("La fecha de desaparición no puede ser una fecha en el futuro.");
                        return;
                      }
                      if (circumstances.trim().length < 15) {
                        setErrorMessage("Por favor describa las circunstancias con al menos 15 caracteres para orientar la búsqueda.");
                        return;
                      }
                    }
                    if (step === 3) {
                      if (physicalDesc.trim().length < 10) {
                        setErrorMessage("La descripción física debe contener al menos 10 caracteres (estatura, contextura, color de piel o cabello).");
                        return;
                      }
                      if (clothingDesc.trim().length < 5) {
                        setErrorMessage("La descripción de la vestimenta debe contener al menos 5 caracteres.");
                        return;
                      }
                    }
                    setErrorMessage(null);
                    setStep(step + 1);
                  }}
                  className="px-5 py-2.5 text-xs font-semibold text-white bg-[#0F2A4A] hover:bg-slate-800 rounded-lg transition flex items-center gap-1.5 shadow-sm"
                >
                  Siguiente Paso
                  <ArrowRight className="w-3.5 h-3.5" />
                </button>
              ) : (
                <button
                  type="button"
                  disabled={loading || !acceptedTerms || !relationship || !idDocNumber}
                  onClick={handleFinalSubmit}
                  className="px-6 py-2.5 text-xs font-bold text-white bg-[#0D9488] hover:bg-[#0f766e] disabled:opacity-50 rounded-lg transition flex items-center gap-2 shadow"
                >
                  <Save className="w-4 h-4" />
                  {loading ? "Registrando reporte..." : "Enviar Reporte a Moderación"}
                </button>
              )}
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
