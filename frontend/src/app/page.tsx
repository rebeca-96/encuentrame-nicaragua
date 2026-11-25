"use client";

import { useEffect, useState } from "react";
import Link from "next/link";
import { 
  Search, PlusCircle, Shield, HeartHandshake, MapPin, 
  AlertTriangle, CheckCircle2, PhoneCall, ChevronRight, Lock
} from "lucide-react";
import ReportCard from "../components/reports/ReportCard";
import { fetchPublicReports, fetchDepartments } from "../lib/api";
import { ReportPublicItem } from "../types";

export default function HomePage() {
  const [reports, setReports] = useState<ReportPublicItem[]>([]);
  const [departments, setDepartments] = useState<string[]>([]);
  const [searchQuery, setSearchQuery] = useState("");
  const [selectedDept, setSelectedDept] = useState("all");
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    async function loadInitialData() {
      try {
        const [repData, deptData] = await Promise.all([
          fetchPublicReports({ limit: 6 }),
          fetchDepartments(),
        ]);
        setReports(repData);
        setDepartments(deptData);
      } catch (err) {
        console.error(err);
      } finally {
        setLoading(false);
      }
    }
    loadInitialData();
  }, []);

  const handleSearchSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    const params = new URLSearchParams();
    if (searchQuery.trim()) params.append("q", searchQuery.trim());
    if (selectedDept !== "all") params.append("department", selectedDept);
    window.location.href = `/casos?${params.toString()}`;
  };

  return (
    <div className="space-y-16 pb-16">
      {/* 1. HERO SECTION */}
      <section className="relative bg-gradient-to-b from-[#0F2A4A] to-[#0A192F] text-white py-20 px-4 sm:px-6 lg:px-8 border-b border-slate-700">
        <div className="max-w-5xl mx-auto text-center space-y-6">
          <div className="inline-flex items-center gap-2 bg-[#0D9488]/20 border border-[#14B8A6]/40 px-3.5 py-1.5 rounded-full text-xs font-semibold text-[#14B8A6]">
            <HeartHandshake className="w-4 h-4" />
            <span>Plataforma Cívica de Apoyo y Reunificación Familiar</span>
          </div>

          <h1 className="text-3xl sm:text-5xl font-extrabold tracking-tight leading-tight">
            ENCUÉNTRAME NICARAGUA
          </h1>
          <p className="text-lg sm:text-xl text-slate-300 font-light max-w-2xl mx-auto">
            Centralización transparente, verificación responsable y colaboración ciudadana para la búsqueda de personas en Nicaragua.
          </p>

          {/* Quick Search Form */}
          <form
            onSubmit={handleSearchSubmit}
            className="max-w-3xl mx-auto bg-white p-3 rounded-2xl shadow-xl flex flex-col sm:flex-row gap-3 text-slate-800"
          >
            <div className="flex-1 flex items-center gap-2 px-3 py-1 bg-slate-50 rounded-xl border border-slate-200">
              <Search className="w-5 h-5 text-slate-400 shrink-0" />
              <input
                type="text"
                value={searchQuery}
                onChange={(e) => setSearchQuery(e.target.value)}
                placeholder="Nombre, características o número de caso..."
                className="w-full bg-transparent text-sm focus:outline-none placeholder-slate-400"
              />
            </div>

            <div className="sm:w-56 flex items-center px-3 py-1 bg-slate-50 rounded-xl border border-slate-200">
              <MapPin className="w-4 h-4 text-slate-400 shrink-0 mr-1.5" />
              <select
                value={selectedDept}
                onChange={(e) => setSelectedDept(e.target.value)}
                className="w-full bg-transparent text-sm focus:outline-none text-slate-700 cursor-pointer"
              >
                <option value="all">Todo Nicaragua</option>
                {departments.map((dept) => (
                  <option key={dept} value={dept}>
                    {dept}
                  </option>
                ))}
              </select>
            </div>

            <button
              type="submit"
              className="bg-[#0D9488] hover:bg-[#0f766e] text-white font-semibold text-sm px-6 py-3 rounded-xl transition flex items-center justify-center gap-2 shadow-sm shrink-0"
            >
              <Search className="w-4 h-4" />
              Buscar
            </button>
          </form>

          {/* Quick action badges */}
          <div className="flex flex-wrap items-center justify-center gap-4 pt-2 text-xs">
            <Link
              href="/reportar.html"
              className="inline-flex items-center gap-2 bg-emerald-600 hover:bg-emerald-700 text-white font-semibold px-4 py-2 rounded-lg transition shadow"
            >
              <PlusCircle className="w-4 h-4" />
              Registrar un caso de desaparición
            </Link>
            <Link
              href="/mapa.html"
              className="inline-flex items-center gap-2 bg-slate-800 hover:bg-slate-700 text-slate-200 px-4 py-2 rounded-lg transition border border-slate-600"
            >
              <MapPin className="w-4 h-4 text-[#14B8A6]" />
              Explorar mapa interactivo
            </Link>
          </div>
        </div>
      </section>

      {/* VIDEO INFORMATIVO: PERSONAS DESAPARECIDAS NICARAGUA */}
      <section className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 -mt-8 sm:-mt-10 relative z-10">
        <div className="bg-slate-900 rounded-2xl overflow-hidden shadow-2xl border-2 border-slate-700/80">
          <div className="relative aspect-video w-full bg-black">
            <video
              controls
              playsInline
              preload="metadata"
              className="w-full h-full object-contain"
              src="/Personas_Desaparecidas_Nicaragua.mp4"
            >
              Tu navegador no soporta la reproducción de video HTML5.
            </video>
          </div>
          <div className="p-3 sm:p-4 bg-slate-900 flex flex-col sm:flex-row sm:items-center justify-between gap-2 border-t border-slate-800 text-xs">
            <span className="font-semibold text-white flex items-center gap-2">
              <span className="w-2.5 h-2.5 rounded-full bg-emerald-500 animate-pulse"></span>
              Video Oficial: Personas Desaparecidas Nicaragua
            </span>
            <span className="text-slate-400 text-[11px]">Encuéntrame Nicaragua</span>
          </div>
        </div>
      </section>

      {/* 2. RECENT VERIFIED CASES */}
      <section className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 space-y-8">
        <div className="flex flex-col sm:flex-row sm:items-end justify-between gap-4 border-b border-slate-200 pb-4">
          <div>
            <span className="text-xs font-bold text-[#0D9488] tracking-wider uppercase">
              Difusión Autorizada
            </span>
            <h2 className="text-2xl font-bold text-slate-900 mt-1">
              Casos Publicados Recientemente
            </h2>
            <p className="text-sm text-slate-600">
              Reportes verificados con consentimiento previo para colaborar con su localización.
            </p>
          </div>

          <Link
            href="/casos.html"
            className="text-sm font-semibold text-[#0F2A4A] hover:text-[#0D9488] transition flex items-center gap-1 shrink-0"
          >
            Ver todos los casos ({reports.length}+)
            <ChevronRight className="w-4 h-4" />
          </Link>
        </div>

        {loading ? (
          <div className="text-center py-16 text-slate-500 font-medium">
            Cargando directorio de casos verificados...
          </div>
        ) : reports.length === 0 ? (
          <div className="text-center py-16 bg-white rounded-xl border border-slate-200 text-slate-500">
            No hay casos reportados actualmente en este criterio.
          </div>
        ) : (
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6">
            {reports.map((report) => (
              <ReportCard key={report.id} report={report} />
            ))}
          </div>
        )}
      </section>

      {/* 3. CÓMO FUNCIONA LA PLATAFORMA */}
      <section className="bg-slate-100 py-16 px-4 sm:px-6 lg:px-8 border-y border-slate-200">
        <div className="max-w-7xl mx-auto space-y-12">
          <div className="text-center max-w-2xl mx-auto space-y-2">
            <span className="text-xs font-bold text-[#0D9488] tracking-wider uppercase">
              Garantía de Seguridad
            </span>
            <h2 className="text-2xl sm:text-3xl font-bold text-slate-900">
              ¿Cómo opera Encuéntrame Nicaragua?
            </h2>
            <p className="text-sm text-slate-600">
              Diseñado con estrictos protocolos éticos para salvaguardar a las familias y evitar el mal uso de la información.
            </p>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-4 gap-6">
            <div className="bg-white p-6 rounded-xl shadow-sm border border-slate-200 space-y-3">
              <div className="w-10 h-10 rounded-lg bg-blue-50 text-[#0F2A4A] flex items-center justify-center font-bold">
                1
              </div>
              <h3 className="font-bold text-slate-900 text-base">Registro Consentido</h3>
              <p className="text-xs text-slate-600 leading-relaxed">
                El familiar aporta datos esenciales y consentimiento formal bajo la Ley N.° 787. Los datos personales del reportante permanecen estrictamente privados.
              </p>
            </div>

            <div className="bg-white p-6 rounded-xl shadow-sm border border-slate-200 space-y-3">
              <div className="w-10 h-10 rounded-lg bg-amber-50 text-amber-600 flex items-center justify-center font-bold">
                2
              </div>
              <h3 className="font-bold text-slate-900 text-base">Moderación Humana</h3>
              <p className="text-xs text-slate-600 leading-relaxed">
                Ningún caso se publica automáticamente. Un moderador revisa la veracidad para evitar usurpaciones, violencia doméstica o reportes falsos.
              </p>
            </div>

            <div className="bg-white p-6 rounded-xl shadow-sm border border-slate-200 space-y-3">
              <div className="w-10 h-10 rounded-lg bg-teal-50 text-[#0D9488] flex items-center justify-center font-bold">
                3
              </div>
              <h3 className="font-bold text-slate-900 text-base">Difusión Protegida</h3>
              <p className="text-xs text-slate-600 leading-relaxed">
                Se publican fotografías sin metadatos EXIF y zonas geográficas aproximadas, protegiendo domicilios particulares y refugios.
              </p>
            </div>

            <div className="bg-white p-6 rounded-xl shadow-sm border border-slate-200 space-y-3">
              <div className="w-10 h-10 rounded-lg bg-emerald-50 text-emerald-600 flex items-center justify-center font-bold">
                4
              </div>
              <h3 className="font-bold text-slate-900 text-base">Pistas Confidenciales</h3>
              <p className="text-xs text-slate-600 leading-relaxed">
                La ciudadanía envía información mediante canales cifrados con código de seguimiento anónimo. Las pistas jamás se hacen públicas.
              </p>
            </div>
          </div>
        </div>
      </section>

      {/* 4. RECOMENDACIONES DE SEGURIDAD PARA FAMILIARES */}
      <section className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="bg-[#0F2A4A] text-white rounded-2xl p-8 sm:p-10 shadow-lg flex flex-col md:flex-row items-center gap-8">
          <div className="md:w-2/3 space-y-4">
            <div className="inline-flex items-center gap-1.5 bg-amber-500/20 text-amber-300 px-3 py-1 rounded-full text-xs font-semibold border border-amber-500/30">
              <AlertTriangle className="w-4 h-4" />
              Protección contra Extorsiones y Estafas
            </div>
            <h3 className="text-2xl font-bold tracking-tight">
              Recomendación vital de seguridad para las familias
            </h3>
            <p className="text-sm text-slate-300 leading-relaxed">
              <strong>Nunca publique números telefónicos privados ni cuentas bancarias personales</strong> en redes sociales abiertas. 
              Los estafadores monitorean estas publicaciones para exigir dinero falsamente. Utilice el canal seguro de Encuéntrame Nicaragua para recibir pistas evaluadas por moderadores.
            </p>
          </div>

          <div className="md:w-1/3 flex flex-col gap-3 w-full">
            <Link
              href="/reportar.html"
              className="bg-[#0D9488] hover:bg-[#0f766e] text-white text-center font-semibold text-sm py-3 px-4 rounded-xl transition shadow"
            >
              Iniciar reporte protegido
            </Link>
            <div className="text-center text-xs text-slate-400 flex items-center justify-center gap-1.5">
              <Lock className="w-3.5 h-3.5 text-emerald-400" />
              <span>Privacidad garantizada por diseño</span>
            </div>
          </div>
        </div>
      </section>
    </div>
  );
}
