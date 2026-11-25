"use client";

import { useState, useEffect, useMemo } from "react";
import { Search, Filter, X, MapPin, AlertCircle, RefreshCw, CheckCircle2, Radio } from "lucide-react";
import ReportCard from "../../components/reports/ReportCard";
import { fetchPublicReports, fetchDepartments, fetchMunicipalities } from "../../lib/api";
import { ReportPublicItem } from "../../types";

export default function CasosPage() {
  const [reports, setReports] = useState<ReportPublicItem[]>([]);
  const [departments, setDepartments] = useState<string[]>([]);
  const [loading, setLoading] = useState(true);

  // Filters state
  const [statusFilter, setStatusFilter] = useState<"all" | "active" | "inactive">("all");
  const [q, setQ] = useState("");
  const [department, setDepartment] = useState("all");
  const [municipality, setMunicipality] = useState("all");
  const [municipalities, setMunicipalities] = useState<string[]>([]);
  const [gender, setGender] = useState("all");
  const [onlyMinors, setOnlyMinors] = useState(false);
  const [ageMin, setAgeMin] = useState<number | "">("");
  const [ageMax, setAgeMax] = useState<number | "">("");

  // Load URL query params on initial mount
  useEffect(() => {
    if (typeof window !== "undefined") {
      const urlParams = new URLSearchParams(window.location.search);
      if (urlParams.get("q")) setQ(urlParams.get("q")!);
      if (urlParams.get("department")) setDepartment(urlParams.get("department")!);
      if (urlParams.get("municipality")) setMunicipality(urlParams.get("municipality")!);
      const statusParam = urlParams.get("status");
      if (statusParam === "active" || statusParam === "inactive" || statusParam === "all") {
        setStatusFilter(statusParam);
      }
    }
  }, []);

  useEffect(() => {
    async function init() {
      try {
        const depts = await fetchDepartments();
        setDepartments(depts);
      } catch (err) {
        console.error("Error al cargar departamentos en casos:", err);
      }
    }
    init();
  }, []);

  useEffect(() => {
    async function loadMuns() {
      if (department === "all") {
        setMunicipalities([]);
        setMunicipality("all");
        return;
      }
      try {
        const muns = await fetchMunicipalities(department);
        setMunicipalities(muns);
        setMunicipality("all");
      } catch (err) {
        console.error("Error al cargar municipios dependientes:", err);
      }
    }
    loadMuns();
  }, [department]);

  const loadReports = async () => {
    setLoading(true);
    try {
      const filters: any = {};
      if (statusFilter !== "all") filters.status = statusFilter;
      if (q.trim()) filters.q = q.trim();
      if (department !== "all") filters.department = department;
      if (municipality !== "all") filters.municipality = municipality;
      if (gender !== "all") filters.gender = gender;
      if (onlyMinors) filters.is_minor = true;
      if (ageMin !== "") filters.age_min = Number(ageMin);
      if (ageMax !== "") filters.age_max = Number(ageMax);

      const data = await fetchPublicReports(filters);
      setReports(data);
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadReports();
  }, [statusFilter, department, municipality, gender, onlyMinors]);

  const handleSearchSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    loadReports();
  };

  const handleResetFilters = () => {
    setQ("");
    setDepartment("all");
    setMunicipality("all");
    setGender("all");
    setOnlyMinors(false);
    setAgeMin("");
    setAgeMax("");
    setStatusFilter("all");
  };

  // Contadores calculados sobre la lista obtenida
  const activeCount = useMemo(() => {
    return reports.filter((r) => r.status !== "closed" && r.status !== "resolved" && r.status !== "closed_found" && r.status !== "closed_resolved").length;
  }, [reports]);

  const inactiveCount = useMemo(() => {
    return reports.filter((r) => r.status === "closed" || r.status === "resolved" || r.status === "closed_found" || r.status === "closed_resolved").length;
  }, [reports]);

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-10 space-y-8">
      {/* Header */}
      <div className="flex flex-col md:flex-row md:items-end justify-between gap-4">
        <div>
          <span className="text-xs font-bold text-[#0D9488] tracking-wider uppercase">
            Directorio Nacional Oficial
          </span>
          <h1 className="text-3xl font-extrabold text-slate-900 mt-1">
            Catálogo de Casos: Activos y No Activos
          </h1>
          <p className="text-sm text-slate-600 mt-1 max-w-2xl">
            Consulte reportes verificados de búsqueda en curso (casos activos) y personas localizadas o resueltas (casos concluidos) en toda Nicaragua.
          </p>
        </div>

        {/* Status Selector Tabs */}
        <div className="inline-flex bg-slate-100 p-1.5 rounded-xl border border-slate-200 self-start md:self-auto shadow-inner">
          <button
            onClick={() => setStatusFilter("all")}
            className={`px-4 py-2 rounded-lg text-xs font-bold transition flex items-center gap-1.5 ${
              statusFilter === "all"
                ? "bg-[#0F2A4A] text-white shadow-sm"
                : "text-slate-600 hover:text-slate-900 hover:bg-white/60"
            }`}
          >
            Todos los Casos
          </button>

          <button
            onClick={() => setStatusFilter("active")}
            className={`px-4 py-2 rounded-lg text-xs font-bold transition flex items-center gap-1.5 ${
              statusFilter === "active"
                ? "bg-[#0D9488] text-white shadow-sm"
                : "text-slate-600 hover:text-slate-900 hover:bg-white/60"
            }`}
          >
            <span className="w-2 h-2 rounded-full bg-emerald-400 animate-pulse" />
            Casos Activos
          </button>

          <button
            onClick={() => setStatusFilter("inactive")}
            className={`px-4 py-2 rounded-lg text-xs font-bold transition flex items-center gap-1.5 ${
              statusFilter === "inactive"
                ? "bg-emerald-700 text-white shadow-sm"
                : "text-slate-600 hover:text-slate-900 hover:bg-white/60"
            }`}
          >
            <CheckCircle2 className="w-3.5 h-3.5 text-white" />
            No Activos (Localizados)
          </button>
        </div>
      </div>

      {/* Filter Toolbar */}
      <div className="bg-white p-5 rounded-2xl shadow-sm border border-slate-200 space-y-4">
        {/* Main Search Input */}
        <form onSubmit={handleSearchSubmit} className="flex gap-3">
          <div className="flex-1 flex items-center gap-2 px-4 py-2.5 bg-slate-50 rounded-xl border border-slate-200 focus-within:border-[#0D9488] transition">
            <Search className="w-5 h-5 text-slate-400 shrink-0" />
            <input
              type="text"
              value={q}
              onChange={(e) => setQ(e.target.value)}
              placeholder="Buscar por nombre, apellidos, número de caso o rasgos particulares..."
              className="w-full bg-transparent text-sm focus:outline-none placeholder-slate-400"
            />
            {q && (
              <button
                type="button"
                onClick={() => setQ("")}
                className="text-slate-400 hover:text-slate-600"
              >
                <X className="w-4 h-4" />
              </button>
            )}
          </div>

          <button
            type="submit"
            className="bg-[#0D9488] hover:bg-[#0f766e] text-white px-5 py-2.5 rounded-xl text-sm font-semibold transition flex items-center gap-2 shrink-0 shadow-sm"
          >
            <Search className="w-4 h-4" />
            Buscar
          </button>
        </form>

        {/* Detailed Filters Row */}
        <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-5 gap-3 pt-2 text-xs">
          {/* Department */}
          <div>
            <label className="block text-slate-600 font-semibold mb-1">Departamento:</label>
            <select
              value={department}
              onChange={(e) => setDepartment(e.target.value)}
              className="w-full p-2 bg-slate-50 border border-slate-200 rounded-lg text-slate-800"
            >
              <option value="all">Todos los Departamentos</option>
              {departments.map((dept) => (
                <option key={dept} value={dept}>
                  {dept}
                </option>
              ))}
            </select>
          </div>

          {/* Municipality (Dependent) */}
          <div>
            <label className="block text-slate-600 font-semibold mb-1">Municipio:</label>
            <select
              value={municipality}
              onChange={(e) => setMunicipality(e.target.value)}
              disabled={department === "all"}
              className="w-full p-2 bg-slate-50 border border-slate-200 rounded-lg text-slate-800 disabled:opacity-50"
            >
              <option value="all">
                {department === "all" ? "Todos los municipios" : `Todos (${municipalities.length})`}
              </option>
              {municipalities.map((mun) => (
                <option key={mun} value={mun}>
                  {mun}
                </option>
              ))}
            </select>
          </div>

          {/* Gender */}
          <div>
            <label className="block text-slate-600 font-semibold mb-1">Sexo / Género:</label>
            <select
              value={gender}
              onChange={(e) => setGender(e.target.value)}
              className="w-full p-2 bg-slate-50 border border-slate-200 rounded-lg text-slate-800"
            >
              <option value="all">Cualquiera</option>
              <option value="male">Masculino</option>
              <option value="female">Femenino</option>
              <option value="non_binary">No binario</option>
            </select>
          </div>

          {/* Age range */}
          <div>
            <label className="block text-slate-600 font-semibold mb-1">Rango de Edad:</label>
            <div className="flex items-center gap-1.5">
              <input
                type="number"
                placeholder="Min"
                value={ageMin}
                onChange={(e) => setAgeMin(e.target.value === "" ? "" : Number(e.target.value))}
                className="w-full p-2 bg-slate-50 border border-slate-200 rounded-lg"
              />
              <span className="text-slate-400">-</span>
              <input
                type="number"
                placeholder="Max"
                value={ageMax}
                onChange={(e) => setAgeMax(e.target.value === "" ? "" : Number(e.target.value))}
                className="w-full p-2 bg-slate-50 border border-slate-200 rounded-lg"
              />
            </div>
          </div>

          {/* Minor toggle and reset */}
          <div className="flex flex-col justify-end space-y-2">
            <label className="flex items-center gap-2 cursor-pointer font-semibold text-slate-700 select-none">
              <input
                type="checkbox"
                checked={onlyMinors}
                onChange={(e) => setOnlyMinors(e.target.checked)}
                className="w-4 h-4 text-red-600 rounded border-slate-300 focus:ring-red-500"
              />
              <span className="text-red-700 flex items-center gap-1">
                <AlertCircle className="w-3.5 h-3.5" />
                Solo menores de edad
              </span>
            </label>

            <button
              type="button"
              onClick={handleResetFilters}
              className="text-xs text-slate-500 hover:text-slate-800 underline flex items-center gap-1"
            >
              <RefreshCw className="w-3 h-3" />
              Limpiar filtros
            </button>
          </div>
        </div>
      </div>

      {/* Results Header */}
      <div className="flex flex-wrap justify-between items-center gap-2 text-sm text-slate-600 px-1">
        <span>
          Mostrando <strong>{reports.length}</strong> casos registrados{" "}
          <span className="text-xs text-slate-500">
            ({activeCount} en búsqueda activa, {inactiveCount} localizados/concluidos)
          </span>
        </span>
        <span className="text-xs bg-slate-100 text-slate-700 px-3 py-1 rounded-full font-medium">
          Filtro actual:{" "}
          <strong>
            {statusFilter === "all"
              ? "Todos los casos"
              : statusFilter === "active"
              ? "Búsqueda Activa"
              : "No Activos (Localizados / Resueltos)"}
          </strong>
        </span>
      </div>

      {/* Results Grid */}
      {loading ? (
        <div className="text-center py-20 text-slate-500">
          <div className="animate-spin w-8 h-8 border-4 border-[#0D9488] border-t-transparent rounded-full mx-auto mb-3"></div>
          Cargando catálogo de casos...
        </div>
      ) : reports.length === 0 ? (
        <div className="text-center py-16 bg-white rounded-2xl border border-slate-200 p-8 space-y-3">
          <Search className="w-12 h-12 text-slate-300 mx-auto" />
          <h3 className="text-lg font-bold text-slate-800">
            No se encontraron casos con los criterios indicados
          </h3>
          <p className="text-xs text-slate-500 max-w-md mx-auto">
            Pruebe cambiando el filtro de estado a &ldquo;Todos los Casos&rdquo;, ampliando el rango de edad o restableciendo los filtros de búsqueda.
          </p>
          <button
            onClick={handleResetFilters}
            className="mt-2 bg-[#0F2A4A] text-white px-4 py-2 rounded-lg text-xs font-semibold hover:bg-slate-800 transition"
          >
            Restablecer todos los filtros
          </button>
        </div>
      ) : (
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6">
          {reports.map((report) => (
            <ReportCard key={report.id} report={report} />
          ))}
        </div>
      )}
    </div>
  );
}

