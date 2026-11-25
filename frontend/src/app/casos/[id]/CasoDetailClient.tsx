"use client";

import { useEffect, useState } from "react";
import { useParams } from "next/navigation";
import Link from "next/link";
import { 
  MapPin, Calendar, AlertCircle, FileText, ArrowLeft, 
  Send, ShieldCheck, Heart, User, CheckCircle2, Lock,
  Activity, Clock, Eye, AlertTriangle, Shield, Check
} from "lucide-react";
import { fetchReportDetail, submitTip } from "../../../lib/api";
import { getLocalReportDetail, getCasePhotoUrl } from "../../../lib/catalogData";
import { ReportDetail, CaseMilestone } from "../../../types";

export default function CasoDetailClient() {
  const params = useParams();
  const rawParamId = params?.id as string;
  const initialId = (rawParamId && rawParamId !== "placeholder") ? rawParamId : "case-01";

  const [reportId, setReportId] = useState<string>(initialId);
  const [report, setReport] = useState<ReportDetail | null>(() => {
    return getLocalReportDetail(initialId);
  });
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [selectedPhoto, setSelectedPhoto] = useState<string | null>(null);
  const [lastSyncTime, setLastSyncTime] = useState<string>("");

  useEffect(() => {
    setLastSyncTime(new Date().toLocaleTimeString("es-NI", { hour: "2-digit", minute: "2-digit", second: "2-digit" }));
    const timer = setInterval(() => {
      setLastSyncTime(new Date().toLocaleTimeString("es-NI", { hour: "2-digit", minute: "2-digit", second: "2-digit" }));
    }, 30000);
    return () => clearInterval(timer);
  }, []);

  // Tip submission form state
  const [tipDescription, setTipDescription] = useState("");
  const [sightingDate, setSightingDate] = useState("");
  const [sightingDept, setSightingDept] = useState("");
  const [informantContact, setInformantContact] = useState("");
  const [confidentialityLevel, setConfidentialityLevel] = useState("strict_anonymous");
  const [submittingTip, setSubmittingTip] = useState(false);
  const [tipSuccessCode, setTipSuccessCode] = useState<string | null>(null);

  useEffect(() => {
    if (typeof window !== "undefined") {
      const urlParams = new URLSearchParams(window.location.search);
      const qId = urlParams.get("id") || urlParams.get("case");
      const pId = params?.id as string;
      if (qId) {
        setReportId(qId);
      } else if (pId && pId !== "placeholder") {
        setReportId(pId);
      } else {
        setReportId("case-01");
      }
    }
  }, [params]);

  useEffect(() => {
    async function load() {
      if (!reportId) return;
      setLoading(true);
      try {
        const data = await fetchReportDetail(reportId);
        setReport(data);
      } catch (err: any) {
        setError(err.message || "No fue posible cargar el caso");
      } finally {
        setLoading(false);
      }
    }
    load();
  }, [reportId]);

  const handleTipSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!report || tipDescription.trim().length < 10) return;

    setSubmittingTip(true);
    try {
      const res = await submitTip({
        report_id: report.id,
        description: tipDescription.trim(),
        sighting_date: sightingDate ? new Date(sightingDate).toISOString() : undefined,
        sighting_department: sightingDept || undefined,
        informant_contact: informantContact.trim() || undefined,
        confidentiality_level: confidentialityLevel,
      });

      setTipSuccessCode(res.tip_code);
      setTipDescription("");
      setInformantContact("");
    } catch (err: any) {
      alert(err.message || "Error al enviar la pista confidencial");
    } finally {
      setSubmittingTip(false);
    }
  };

  if (loading) {
    return (
      <div className="max-w-4xl mx-auto px-4 py-20 text-center text-slate-500">
        <div className="animate-spin w-8 h-8 border-4 border-[#0D9488] border-t-transparent rounded-full mx-auto mb-3"></div>
        Cargando expediente completo de la persona desaparecida...
      </div>
    );
  }

  if (error || !report) {
    return (
      <div className="max-w-2xl mx-auto px-4 py-20 text-center space-y-4">
        <div className="w-12 h-12 bg-red-100 text-red-600 rounded-full flex items-center justify-center mx-auto">
          <AlertCircle className="w-6 h-6" />
        </div>
        <h2 className="text-xl font-bold text-slate-900">Caso no disponible</h2>
        <p className="text-sm text-slate-600">
          El caso solicitado no existe o se encuentra bajo revisión y custodia confidencial.
        </p>
        <Link
          href="/casos.html"
          className="inline-flex items-center gap-1.5 text-sm font-semibold text-[#0F2A4A] hover:underline"
        >
          <ArrowLeft className="w-4 h-4" />
          Regresar al catálogo de casos
        </Link>
      </div>
    );
  }

  const primaryPhoto = report.photos?.find((p) => p.is_primary) || report.photos?.[0];
  const apiHost = process.env.NEXT_PUBLIC_API_URL ? process.env.NEXT_PUBLIC_API_URL.replace("/api/v1", "") : "";
  const photoUrl = primaryPhoto?.url && !primaryPhoto.url.includes("avatar-placeholder")
    ? (primaryPhoto.url.startsWith("http") || primaryPhoto.url.startsWith("/") || primaryPhoto.url.startsWith("data:")
        ? primaryPhoto.url
        : `${apiHost}/api/v1/reports/photos/${primaryPhoto.storage_key}`)
    : (report.primary_photo_url && !report.primary_photo_url.includes("avatar-placeholder")
        ? report.primary_photo_url
        : getCasePhotoUrl(report.case_number, report.primary_photo_url));

  const isClosed = 
    report.status === "closed" || 
    report.status === "closed_found" || 
    report.status === "closed_resolved" || 
    report.status === "resolved";

  return (
    <div className="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8 py-10 space-y-8">
      {/* Real-time Tracking Badge */}
      <div className="flex flex-wrap items-center justify-between gap-3 bg-slate-900 text-white px-4 py-2.5 rounded-xl shadow-xs text-xs border border-slate-800">
        <div className="flex items-center gap-2">
          <span className="relative flex h-2.5 w-2.5">
            <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-emerald-400 opacity-75"></span>
            <span className="relative inline-flex rounded-full h-2.5 w-2.5 bg-emerald-500"></span>
          </span>
          <span className="font-bold tracking-wide text-emerald-400 uppercase text-[11px]">
            Seguimiento en Tiempo Real Activo
          </span>
          <span className="text-slate-500 hidden sm:inline">•</span>
          <span className="text-slate-300 hidden sm:inline">
            Recepción y custodia inmediata de testimonios las 24 horas
          </span>
        </div>
        <div className="flex items-center gap-2 text-slate-400 text-[11px] font-mono">
          <span>Última sincronización:</span>
          <span className="text-slate-200 font-semibold">{lastSyncTime || "En vivo"}</span>
        </div>
      </div>

      {/* Back button & Action Header */}
      <div className="flex flex-wrap items-center justify-between gap-4">
        <Link
          href="/casos.html"
          className="inline-flex items-center gap-2 text-xs font-semibold text-slate-600 hover:text-[#0F2A4A] transition bg-white px-3 py-1.5 rounded-lg border border-slate-200 shadow-sm"
        >
          <ArrowLeft className="w-4 h-4" />
          Volver al Catálogo de Casos
        </Link>

        <span className="text-xs font-mono font-bold bg-[#0F2A4A] text-white px-3 py-1.5 rounded-lg shadow-sm">
          EXPEDIENTE OFICIAL: {report.case_number}
        </span>
      </div>

      {/* Case Status Banner */}
      {isClosed ? (
        <div className="bg-emerald-50 border border-emerald-300 rounded-2xl p-5 flex items-start gap-3.5 shadow-sm">
          <CheckCircle2 className="w-6 h-6 text-emerald-600 shrink-0 mt-0.5" />
          <div className="space-y-1">
            <h2 className="text-sm font-bold text-emerald-950 uppercase tracking-wide flex items-center gap-2">
              <span>Caso Concluido — Persona Localizada y Resguardada</span>
              <span className="bg-emerald-600 text-white text-[10px] px-2 py-0.5 rounded-full font-bold">
                CERRADO
              </span>
            </h2>
            <p className="text-xs text-emerald-800 leading-relaxed">
              {(report as any).resolution_notes || "Esta persona ha sido localizada de forma segura y se ha restablecido el contacto familiar. Agradecemos a toda la ciudadanía, brigadas y autoridades por su colaboración. El expediente se encuentra formalmente cerrado."}
            </p>
          </div>
        </div>
      ) : (
        <div className="bg-teal-50 border border-teal-200 rounded-2xl p-5 flex items-start gap-3.5 shadow-sm">
          <span className="w-3.5 h-3.5 rounded-full bg-emerald-500 animate-pulse shrink-0 mt-1" />
          <div className="space-y-1">
            <h2 className="text-sm font-bold text-teal-950 uppercase tracking-wide flex items-center gap-2">
              <span>Búsqueda Activa — Difusión Nacional Autorizada</span>
              <span className="bg-[#0D9488] text-white text-[10px] px-2 py-0.5 rounded-full font-bold animate-pulse">
                EN CURSO
              </span>
            </h2>
            <p className="text-xs text-teal-800 leading-relaxed">
              Expediente verificado con consentimiento informado bajo la Ley N.° 787 de Nicaragua. Se solicita el apoyo y la colaboración ciudadana ética y confidencial para su pronta localización.
            </p>
          </div>
        </div>
      )}

      {/* 1. MAIN PROFILE CARD */}
      <div className="bg-white rounded-2xl shadow-sm border border-slate-200 overflow-hidden grid grid-cols-1 md:grid-cols-3">
        {/* Column 1: Fotografía y Datos Primarios */}
        <div className="p-6 sm:p-8 bg-slate-50 border-b md:border-b-0 md:border-r border-slate-200 flex flex-col items-center text-center space-y-4">
          <div className="relative w-64 h-64 rounded-2xl overflow-hidden shadow-md border-4 border-white bg-slate-200 group">
            <img
              src={selectedPhoto || photoUrl}
              alt={`Fotografía oficial de ${report.first_name} ${report.last_name}`}
              className={`w-full h-full object-cover transition duration-300 ${isClosed ? "grayscale-[20%]" : "group-hover:scale-105"}`}
              onError={(e) => {
                (e.target as HTMLImageElement).src = "/images/avatar-placeholder.svg";
              }}
            />

            {report.is_minor && (
              <div className="absolute top-2 left-2 bg-red-600 text-white text-[10px] font-bold px-2.5 py-0.5 rounded-full shadow-md flex items-center gap-1">
                <AlertCircle className="w-3 h-3" />
                MENOR DE EDAD
              </div>
            )}

            <div className="absolute bottom-2 right-2 bg-slate-900/80 backdrop-blur-sm text-white text-[10px] font-mono px-2 py-0.5 rounded">
              {report.case_number}
            </div>
          </div>

          {/* Status Badge */}
          {isClosed ? (
            <span className="bg-emerald-700 text-white text-xs font-bold px-3.5 py-1.5 rounded-full shadow-sm flex items-center gap-1.5">
              <CheckCircle2 className="w-4 h-4" />
              LOCALIZADO / CASO RESUELTO
            </span>
          ) : (
            <span className="bg-[#0D9488] text-white text-xs font-bold px-3.5 py-1.5 rounded-full shadow-sm flex items-center gap-1.5">
              <span className="w-2 h-2 rounded-full bg-emerald-300 animate-pulse" />
              BÚSQUEDA ACTIVA
            </span>
          )}

          <div className="w-full space-y-1">
            <h1 className="text-2xl font-extrabold text-slate-900 leading-tight">
              {report.first_name} {report.last_name}
            </h1>
            {report.nickname && (
              <span className="text-xs text-slate-500 font-medium block">
                Conocido/a comúnmente como: &ldquo;{report.nickname}&rdquo;
              </span>
            )}
          </div>

          {/* Datos Vitales */}
          <div className="w-full pt-3 border-t border-slate-200 space-y-2 text-xs text-left">
            <div className="flex justify-between py-1 border-b border-slate-100">
              <span className="text-slate-500">Edad al desaparecer:</span>
              <span className="font-bold text-slate-800">{report.age_at_disappearance} años</span>
            </div>
            <div className="flex justify-between py-1 border-b border-slate-100">
              <span className="text-slate-500">Sexo / Género:</span>
              <span className="font-semibold text-slate-800 capitalize">
                {report.gender === "male" ? "Masculino" : report.gender === "female" ? "Femenino" : report.gender}
              </span>
            </div>
            <div className="flex justify-between py-1 border-b border-slate-100">
              <span className="text-slate-500">Departamento:</span>
              <span className="font-semibold text-slate-800">{report.department}</span>
            </div>
            <div className="flex justify-between py-1 border-b border-slate-100">
              <span className="text-slate-500">Municipio:</span>
              <span className="font-semibold text-slate-800">{report.municipality}</span>
            </div>
            <div className="flex justify-between py-1 border-b border-slate-100">
              <span className="text-slate-500">Fecha del hecho:</span>
              <span className="font-semibold text-slate-800">
                {new Date(report.disappearance_date).toLocaleDateString("es-NI", {
                  year: "numeric",
                  month: "long",
                  day: "numeric"
                })}
              </span>
            </div>
            {report.neighborhood_zone && (
              <div className="flex justify-between py-1">
                <span className="text-slate-500">Zona / Barrio:</span>
                <span className="font-semibold text-slate-800 text-right">{report.neighborhood_zone}</span>
              </div>
            )}
          </div>

          <div className="w-full pt-2">
            <div className="bg-slate-100 text-slate-600 p-2.5 rounded-lg text-[11px] text-center border border-slate-200 flex items-center justify-center gap-1.5">
              <Shield className="w-3.5 h-3.5 text-slate-500" />
              <span>Fotografía sanitizada bajo Ley N.° 787</span>
            </div>
          </div>
        </div>

        {/* Column 2 & 3: Descripción, Vestimenta y Circunstancias */}
        <div className="md:col-span-2 p-6 sm:p-8 space-y-6">
          {/* Medical / Vulnerability Alert Banner */}
          {report.medical_conditions && (
            <div className="bg-amber-50 border border-amber-200 rounded-xl p-4 text-xs flex gap-3 text-amber-900 shadow-sm">
              <AlertTriangle className="w-5 h-5 text-amber-600 shrink-0 mt-0.5" />
              <div>
                <strong className="block font-bold uppercase tracking-wider text-amber-950">
                  Condición Médica / Vulnerabilidad de Salud:
                </strong>
                <p className="mt-0.5 leading-relaxed font-medium">{report.medical_conditions}</p>
              </div>
            </div>
          )}

          {/* Rasgos Físicos */}
          <div className="space-y-2">
            <h3 className="text-xs font-bold text-slate-900 uppercase tracking-wider flex items-center gap-1.5">
              <User className="w-4 h-4 text-[#0D9488]" />
              Rasgos Físicos y Señas Particulares
            </h3>
            <div className="bg-slate-50 p-4 rounded-xl border border-slate-200 text-sm text-slate-800 leading-relaxed font-normal">
              {report.physical_description}
            </div>
          </div>

          {/* Vestimenta */}
          <div className="space-y-2">
            <h3 className="text-xs font-bold text-slate-900 uppercase tracking-wider flex items-center gap-1.5">
              <span className="w-2 h-2 rounded-full bg-[#0D9488]" />
              Vestimenta Reportada la Última Vez
            </h3>
            <div className="bg-slate-50 p-4 rounded-xl border border-slate-200 text-sm text-slate-800 leading-relaxed font-normal">
              {report.clothing_description || "Prendas de vestir no descritas en el reporte inicial."}
            </div>
          </div>

          {/* Circunstancias del Último Avistamiento */}
          <div className="space-y-2">
            <h3 className="text-xs font-bold text-slate-900 uppercase tracking-wider flex items-center gap-1.5">
              <MapPin className="w-4 h-4 text-[#0D9488]" />
              Circunstancias del Último Avistamiento
            </h3>
            <div className="bg-slate-50 p-4 rounded-xl border border-slate-200 text-sm text-slate-800 leading-relaxed font-normal">
              {report.circumstances}
              {report.neighborhood_zone && (
                <div className="mt-3 pt-2 border-t border-slate-200 text-xs font-semibold text-slate-600 flex items-center gap-1.5">
                  <MapPin className="w-3.5 h-3.5 text-[#0D9488]" />
                  <span>Ubicación territorial referencial: {report.neighborhood_zone}, {report.municipality}, {report.department}</span>
                </div>
              )}
            </div>
          </div>
        </div>
      </div>

      {/* 2. AVANCE Y CRONOLOGÍA DEL CASO (LÍNEA DE TIEMPO) */}
      <div className="bg-white rounded-2xl shadow-sm border border-slate-200 p-6 sm:p-8 space-y-6">
        <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-2 border-b border-slate-200 pb-4">
          <div className="space-y-1">
            <span className="text-xs font-bold text-[#0D9488] tracking-wider uppercase flex items-center gap-1.5">
              <Activity className="w-4 h-4" />
              Seguimiento Oficial de la Búsqueda
            </span>
            <h2 className="text-xl sm:text-2xl font-bold text-slate-900">
              Avance y Cronología del Caso
            </h2>
            <p className="text-xs text-slate-600">
              Registro histórico y trazabilidad de los hitos de recepción, validación documental, difusión pública y estado actual.
            </p>
          </div>
          <span className={`text-xs font-bold px-3.5 py-1.5 rounded-full border self-start sm:self-auto shadow-sm flex items-center gap-1.5 ${
            isClosed 
              ? "bg-emerald-50 text-emerald-800 border-emerald-300"
              : "bg-teal-50 text-[#0D9488] border-teal-200"
          }`}>
            {isClosed ? (
              <>
                <CheckCircle2 className="w-3.5 h-3.5 text-emerald-600" />
                <span>Caso Concluido / Localizado</span>
              </>
            ) : (
              <>
                <span className="w-2 h-2 rounded-full bg-emerald-400 animate-pulse" />
                <span>Búsqueda Activa en Desarrollo</span>
              </>
            )}
          </span>
        </div>

        {/* Timeline Items */}
        <div className="relative pl-6 sm:pl-8 border-l-2 border-slate-200 space-y-8 my-4 ml-3 sm:ml-4">
          {report.timeline && report.timeline.length > 0 ? (
            report.timeline.map((step, idx) => (
              <div key={idx} className="relative group">
                {/* Node icon */}
                <div className={`absolute -left-[31px] sm:-left-[39px] top-0.5 w-6 h-6 rounded-full flex items-center justify-center border-2 bg-white ${
                  step.status === "completed"
                    ? "border-emerald-500 text-emerald-600"
                    : step.status === "current"
                    ? "border-[#0D9488] text-[#0D9488] ring-4 ring-teal-100"
                    : "border-slate-300 text-slate-400"
                }`}>
                  {step.status === "completed" ? (
                    <Check className="w-3.5 h-3.5 stroke-[3]" />
                  ) : step.status === "current" ? (
                    <span className="w-2 h-2 rounded-full bg-[#0D9488] animate-ping" />
                  ) : (
                    <Clock className="w-3 h-3" />
                  )}
                </div>

                {/* Content */}
                <div className="space-y-1">
                  <div className="flex flex-wrap items-center gap-2">
                    <span className="text-xs font-semibold text-slate-500 font-mono">
                      {step.date}
                    </span>
                    <span className={`text-[10px] font-bold px-2 py-0.5 rounded uppercase tracking-wider ${
                      step.status === "completed"
                        ? "bg-emerald-50 text-emerald-700 border border-emerald-200"
                        : step.status === "current"
                        ? "bg-teal-50 text-[#0D9488] border border-teal-200 font-extrabold"
                        : "bg-slate-100 text-slate-500"
                    }`}>
                      {step.status === "completed" ? "Hito Completado" : step.status === "current" ? "Estado Actual" : "Pendiente"}
                    </span>
                  </div>

                  <h4 className="text-base font-bold text-slate-900">
                    {step.title}
                  </h4>
                  <p className="text-xs text-slate-600 leading-relaxed max-w-3xl">
                    {step.description}
                  </p>
                </div>
              </div>
            ))
          ) : (
            <div className="space-y-6">
              <div className="relative">
                <div className="absolute -left-[31px] sm:-left-[39px] top-0.5 w-6 h-6 rounded-full flex items-center justify-center border-2 border-emerald-500 bg-white text-emerald-600">
                  <Check className="w-3.5 h-3.5 stroke-[3]" />
                </div>
                <div className="space-y-1">
                  <span className="text-xs font-semibold text-slate-500 font-mono">
                    {new Date(report.disappearance_date).toLocaleDateString("es-NI")}
                  </span>
                  <h4 className="text-base font-bold text-slate-900">Recepción y Validación del Caso</h4>
                  <p className="text-xs text-slate-600">Registro verificado con consentimiento informado bajo Ley N.° 787.</p>
                </div>
              </div>

              <div className="relative">
                <div className="absolute -left-[31px] sm:-left-[39px] top-0.5 w-6 h-6 rounded-full flex items-center justify-center border-2 border-[#0D9488] bg-white text-[#0D9488] ring-4 ring-teal-100">
                  <span className="w-2 h-2 rounded-full bg-[#0D9488] animate-ping" />
                </div>
                <div className="space-y-1">
                  <span className="text-xs font-semibold text-slate-500 font-mono">Actualidad</span>
                  <h4 className="text-base font-bold text-slate-900">
                    {isClosed ? "Caso Concluido" : "Búsqueda Activa en Desarrollo"}
                  </h4>
                  <p className="text-xs text-slate-600">
                    {isClosed
                      ? "Persona localizada de forma segura. Expediente cerrado."
                      : "Coordinación comunitaria permanente y recepción de información anónima en curso."}
                  </p>
                </div>
              </div>
            </div>
          )}
        </div>
      </div>

      {/* 3. CANAL DE RECEPCIÓN DE PISTAS (MÓDULO E) */}
      <div id="pistas" className="bg-[#0F2A4A] text-white rounded-2xl p-6 sm:p-10 shadow-lg space-y-6">
        <div className="flex flex-col sm:flex-row justify-between sm:items-center gap-4 border-b border-slate-700 pb-4">
          <div className="space-y-1">
            <span className="text-xs font-bold text-[#14B8A6] tracking-wider uppercase flex items-center gap-1.5">
              <ShieldCheck className="w-4 h-4" />
              Canal de Recepción Protegido y Cifrado
            </span>
            <h2 className="text-xl sm:text-2xl font-bold">
              ¿Tiene información sobre {report.first_name}? Aporte una pista confidencial
            </h2>
            <p className="text-xs text-slate-300 max-w-2xl">
              Su aporte se transmite cifrado y es evaluado exclusivamente por moderadores profesionales. 
              <strong> Su identidad y su reporte jamás se harán públicos.</strong>
            </p>
          </div>
        </div>

        {isClosed ? (
          <div className="bg-emerald-950/80 border border-emerald-500/60 rounded-xl p-8 text-center space-y-3">
            <div className="w-12 h-12 bg-emerald-500/20 text-emerald-300 rounded-full flex items-center justify-center mx-auto border border-emerald-400">
              <CheckCircle2 className="w-7 h-7" />
            </div>
            <h3 className="text-lg font-bold text-emerald-200">
              Recepción de Pistas Concluida
            </h3>
            <p className="text-xs text-slate-300 max-w-lg mx-auto leading-relaxed">
              Este caso ha concluido satisfactoriamente con la localización de la persona. Por respeto y protección de la privacidad familiar (Ley N.° 787), ya no se reciben testimonios ni pistas adicionales para este expediente.
            </p>
          </div>
        ) : tipSuccessCode ? (
          <div className="bg-emerald-950/80 border border-emerald-500 rounded-xl p-6 text-center space-y-4">
            <div className="w-12 h-12 bg-emerald-500 text-slate-950 rounded-full flex items-center justify-center mx-auto">
              <CheckCircle2 className="w-7 h-7" />
            </div>
            <h3 className="text-lg font-bold text-emerald-300">
              ¡Pista Recibida Exitosamente!
            </h3>
            <p className="text-xs text-slate-300 max-w-lg mx-auto">
              Agradecemos su valiosa colaboración ciudadana. El equipo de moderación analizará estos datos de inmediato para apoyar la búsqueda.
            </p>
            <div className="bg-slate-900 p-4 rounded-lg inline-block border border-emerald-500/40">
              <span className="text-xs text-slate-400 block mb-1">Su código anónimo de seguimiento:</span>
              <span className="font-mono text-xl font-extrabold text-emerald-400 tracking-wider">
                {tipSuccessCode}
              </span>
            </div>
            <div className="text-[11px] text-slate-400">
              Guarde este código para consultar el estado de su pista en la sección <Link href="/pistas.html" className="text-emerald-400 underline font-semibold">Aportar Pista</Link>.
            </div>
          </div>
        ) : (
          <form onSubmit={handleTipSubmit} className="space-y-4 text-slate-900">
            {/* Description */}
            <div>
              <label className="block text-xs font-semibold text-slate-200 mb-1">
                Descripción detallada de la información o avistamiento: *
              </label>
              <textarea
                required
                rows={4}
                value={tipDescription}
                onChange={(e) => setTipDescription(e.target.value)}
                placeholder="Indique con claridad dónde fue vista la persona, fecha aproximada, vestimenta que llevaba, personas acompañantes o cualquier detalle de interés..."
                className="w-full p-3 rounded-xl bg-white text-sm border border-slate-300 focus:outline-none focus:ring-2 focus:ring-[#0D9488]"
              />
              <span className="text-[11px] text-slate-400">Mínimo 10 caracteres.</span>
            </div>

            <div className="grid grid-cols-1 sm:grid-cols-3 gap-3">
              {/* Sighting date */}
              <div>
                <label className="block text-xs font-semibold text-slate-200 mb-1">
                  Fecha del avistamiento:
                </label>
                <input
                  type="date"
                  value={sightingDate}
                  onChange={(e) => setSightingDate(e.target.value)}
                  className="w-full p-2.5 rounded-xl bg-white text-xs border border-slate-300 focus:outline-none"
                />
              </div>

              {/* Sighting department */}
              <div>
                <label className="block text-xs font-semibold text-slate-200 mb-1">
                  Departamento observado:
                </label>
                <input
                  type="text"
                  placeholder="Ej. Managua, Matagalpa..."
                  value={sightingDept}
                  onChange={(e) => setSightingDept(e.target.value)}
                  className="w-full p-2.5 rounded-xl bg-white text-xs border border-slate-300 focus:outline-none"
                />
              </div>

              {/* Informant contact (Optional) */}
              <div>
                <label className="block text-xs font-semibold text-slate-200 mb-1">
                  Teléfono / Contacto (Opcional):
                </label>
                <input
                  type="text"
                  placeholder="Solo si desea ser contactado"
                  value={informantContact}
                  onChange={(e) => setInformantContact(e.target.value)}
                  className="w-full p-2.5 rounded-xl bg-white text-xs border border-slate-300 focus:outline-none"
                />
              </div>
            </div>

            {/* Level of Confidentiality */}
            <div>
              <label className="block text-xs font-semibold text-slate-200 mb-1.5">
                Nivel de Confidencialidad Deseado:
              </label>
              <div className="grid grid-cols-1 sm:grid-cols-3 gap-3 text-xs">
                <label className="flex items-center gap-2 bg-slate-800 p-2.5 rounded-xl border border-slate-700 cursor-pointer text-slate-200 hover:bg-slate-700/60">
                  <input
                    type="radio"
                    name="conf"
                    value="strict_anonymous"
                    checked={confidentialityLevel === "strict_anonymous"}
                    onChange={(e) => setConfidentialityLevel(e.target.value)}
                    className="text-[#0D9488]"
                  />
                  <span>Estrictamente Anónimo</span>
                </label>
                <label className="flex items-center gap-2 bg-slate-800 p-2.5 rounded-xl border border-slate-700 cursor-pointer text-slate-200 hover:bg-slate-700/60">
                  <input
                    type="radio"
                    name="conf"
                    value="confidential_moderators"
                    checked={confidentialityLevel === "confidential_moderators"}
                    onChange={(e) => setConfidentialityLevel(e.target.value)}
                    className="text-[#0D9488]"
                  />
                  <span>Solo Moderadores</span>
                </label>
                <label className="flex items-center gap-2 bg-slate-800 p-2.5 rounded-xl border border-slate-700 cursor-pointer text-slate-200 hover:bg-slate-700/60">
                  <input
                    type="radio"
                    name="conf"
                    value="family_contact_authorized"
                    checked={confidentialityLevel === "family_contact_authorized"}
                    onChange={(e) => setConfidentialityLevel(e.target.value)}
                    className="text-[#0D9488]"
                  />
                  <span>Contacto Directo Familia</span>
                </label>
              </div>
            </div>

            <div className="pt-2 flex justify-end">
              <button
                type="submit"
                disabled={submittingTip}
                className="bg-[#0D9488] hover:bg-[#0f766e] text-white px-6 py-3 rounded-xl text-sm font-semibold transition flex items-center gap-2 shadow-md disabled:opacity-50"
              >
                <Send className="w-4 h-4" />
                {submittingTip ? "Transmitiendo pista cifrada..." : "Enviar Pista Confidencial"}
              </button>
            </div>
          </form>
        )}
      </div>
    </div>
  );
}
