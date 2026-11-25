"use client";

import { useEffect, useState, useMemo, useCallback } from "react";
import dynamic from "next/dynamic";
import { 
  MapPin, Filter, AlertCircle, Info, ChevronRight, 
  RotateCcw, Search, Shield, Plus, Edit2, CheckCircle2, 
  Layers, Map as MapIcon, X, Check, Globe
} from "lucide-react";
import { 
  fetchMapPoints, fetchDepartments, fetchMunicipalities,
  fetchDepartmentObjects, fetchMunicipalityObjects, fetchGeographicSummary,
  createDepartment, updateDepartment, createMunicipality, updateMunicipality,
  ApiError
} from "../../lib/api";
import { MapPoint, DepartmentItem, MunicipalityItem, GeographicSummary, UserSession } from "../../types";
import { getLocalDepartments, getLocalMunicipalities, getLocalMapPoints } from "../../lib/geography";
import Link from "next/link";

// Dynamic import with SSR disabled for Leaflet map
const NicaraguaMap = dynamic(() => import("../../components/map/NicaraguaMap"), {
  ssr: false,
  loading: () => (
    <div className="w-full h-full min-h-[500px] bg-slate-100 flex items-center justify-center text-slate-500 font-medium">
      <div className="text-center space-y-2">
        <div className="animate-spin w-8 h-8 border-4 border-[#0D9488] border-t-transparent rounded-full mx-auto"></div>
        <p>Cargando visualización geoespacial de Nicaragua...</p>
      </div>
    </div>
  ),
});

export default function MapaPage() {
  // Data states
  const [points, setPoints] = useState<MapPoint[]>([]);
  const [departments, setDepartments] = useState<string[]>([]);
  const [municipalities, setMunicipalities] = useState<string[]>([]);
  
  // Filter states
  const [selectedDept, setSelectedDept] = useState("all");
  const [selectedMun, setSelectedMun] = useState("all");
  const [searchTerm, setSearchTerm] = useState("");
  const [minorFilter, setMinorFilter] = useState("all"); // 'all' | 'minors' | 'adults'

  // Loading and Error states
  const [loadingPoints, setLoadingPoints] = useState(true);
  const [loadingDepts, setLoadingDepts] = useState(true);
  const [loadingMuns, setLoadingMuns] = useState(false);
  const [errorMessage, setErrorMessage] = useState<string | null>(null);
  const [isNetworkFailure, setIsNetworkFailure] = useState(false);

  // Administrative Geographic Management states
  const [currentUser, setCurrentUser] = useState<UserSession | null>(null);
  const [showAdminPanel, setShowAdminPanel] = useState(false);
  const [geoSummary, setGeoSummary] = useState<GeographicSummary | null>(null);
  const [adminDepartments, setAdminDepartments] = useState<DepartmentItem[]>([]);
  const [adminMunicipalities, setAdminMunicipalities] = useState<MunicipalityItem[]>([]);
  const [adminSelectedDeptId, setAdminSelectedDeptId] = useState<string>("");
  const [adminLoading, setAdminLoading] = useState(false);
  const [adminFeedback, setAdminFeedback] = useState<{ type: "success" | "error"; text: string } | null>(null);

  // Modal forms for adding/editing
  const [showDeptModal, setShowDeptModal] = useState(false);
  const [editingDept, setEditingDept] = useState<DepartmentItem | null>(null);
  const [deptForm, setDeptForm] = useState<{
    name: string;
    code: string;
    type: "department" | "autonomous_region";
    latitude: number;
    longitude: number;
  }>({
    name: "",
    code: "",
    type: "department",
    latitude: 12.1364,
    longitude: -86.2514,
  });

  const [showMunModal, setShowMunModal] = useState(false);
  const [editingMun, setEditingMun] = useState<MunicipalityItem | null>(null);
  const [munForm, setMunForm] = useState({
    department_id: "",
    name: "",
    code: "",
    latitude: 12.1364,
    longitude: -86.2514,
  });

  // Check logged user session
  useEffect(() => {
    try {
      const rawSession = localStorage.getItem("encuentrame_session") || localStorage.getItem("encuentrame_user");
      if (rawSession) {
        const parsed = JSON.parse(rawSession);
        if (parsed.user_id) {
          setCurrentUser({
            user_id: parsed.user_id,
            role: parsed.role,
            full_name: parsed.full_name,
            access_token: parsed.access_token,
          } as UserSession);
        } else if (parsed.user) {
          setCurrentUser(parsed.user);
        } else {
          setCurrentUser(parsed);
        }
      }
    } catch {
      // Ignore parse error
    }
  }, []);

  // 1. Initial Load: Departments
  const loadInitialDepartments = useCallback(async () => {
    setLoadingDepts(true);
    setErrorMessage(null);
    setIsNetworkFailure(false);
    try {
      const depts = await fetchDepartments();
      if (depts && depts.length > 0) {
        setDepartments(depts);
      } else {
        setDepartments(getLocalDepartments());
      }
    } catch (err: any) {
      console.warn("Utilizando catálogo local de departamentos:", err);
      setDepartments(getLocalDepartments());
    } finally {
      setLoadingDepts(false);
    }
  }, []);

  useEffect(() => {
    loadInitialDepartments();
  }, [loadInitialDepartments]);

  // 2. Dependent Municipalities Load
  useEffect(() => {
    async function loadDependentMuns() {
      if (selectedDept === "all") {
        setMunicipalities([]);
        setSelectedMun("all");
        return;
      }
      setLoadingMuns(true);
      try {
        const muns = await fetchMunicipalities(selectedDept);
        if (muns && muns.length > 0) {
          setMunicipalities(muns);
        } else {
          setMunicipalities(getLocalMunicipalities(selectedDept));
        }
        setSelectedMun("all"); // Reset dependent selection on department change
      } catch (err) {
        setMunicipalities(getLocalMunicipalities(selectedDept));
        setSelectedMun("all");
      } finally {
        setLoadingMuns(false);
      }
    }
    loadDependentMuns();
  }, [selectedDept]);

  // 3. Load Map Points
  const loadPoints = useCallback(async () => {
    setLoadingPoints(true);
    setErrorMessage(null);
    try {
      const deptFilter = selectedDept === "all" ? undefined : selectedDept;
      const munFilter = selectedMun === "all" ? undefined : selectedMun;
      const data = await fetchMapPoints(deptFilter, munFilter);
      if (data && data.length > 0) {
        setPoints(data);
      } else {
        setPoints(getLocalMapPoints(deptFilter, munFilter));
      }
    } catch (err: any) {
      console.warn("Utilizando puntos geoespaciales locales:", err);
      const deptFilter = selectedDept === "all" ? undefined : selectedDept;
      const munFilter = selectedMun === "all" ? undefined : selectedMun;
      setPoints(getLocalMapPoints(deptFilter, munFilter));
    } finally {
      setLoadingPoints(false);
    }
  }, [selectedDept, selectedMun]);

  useEffect(() => {
    loadPoints();
  }, [loadPoints]);

  // 4. Load Admin Geographic Data
  const loadAdminGeographicData = useCallback(async () => {
    if (!currentUser || currentUser.role !== "admin") return;
    setAdminLoading(true);
    try {
      const [summary, depts] = await Promise.all([
        fetchGeographicSummary(),
        fetchDepartmentObjects(false),
      ]);
      setGeoSummary(summary);
      setAdminDepartments(depts);
      if (depts.length > 0 && !adminSelectedDeptId) {
        setAdminSelectedDeptId(depts[0].id);
      }
    } catch (err: any) {
      console.error("Error al cargar administración territorial:", err);
    } finally {
      setAdminLoading(false);
    }
  }, [currentUser, adminSelectedDeptId]);

  useEffect(() => {
    if (showAdminPanel && currentUser?.role === "admin") {
      loadAdminGeographicData();
    }
  }, [showAdminPanel, currentUser, loadAdminGeographicData]);

  // Load municipalities for admin selected department
  useEffect(() => {
    async function loadAdminMuns() {
      if (!adminSelectedDeptId) return;
      try {
        const muns = await fetchMunicipalityObjects(adminSelectedDeptId);
        setAdminMunicipalities(muns);
      } catch (err) {
        console.error("Error al cargar municipios administrativos:", err);
      }
    }
    if (showAdminPanel && adminSelectedDeptId) {
      loadAdminMuns();
    }
  }, [showAdminPanel, adminSelectedDeptId]);

  // Filtered Points in memory (Search Term and Minor filter)
  const filteredPoints = useMemo(() => {
    return points.filter((pt) => {
      // Search term
      if (searchTerm.trim()) {
        const term = searchTerm.toLowerCase();
        const matchName = pt.full_name.toLowerCase().includes(term);
        const matchCase = pt.case_number.toLowerCase().includes(term);
        const matchMun = pt.municipality.toLowerCase().includes(term);
        if (!matchName && !matchCase && !matchMun) return false;
      }
      // Minor filter
      if (minorFilter === "minors" && !pt.is_minor) return false;
      if (minorFilter === "adults" && pt.is_minor) return false;

      return true;
    });
  }, [points, searchTerm, minorFilter]);

  // Reset Filters handler
  const handleResetFilters = () => {
    setSelectedDept("all");
    setSelectedMun("all");
    setSearchTerm("");
    setMinorFilter("all");
  };

  // Administration Handlers
  const handleSaveDepartment = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!currentUser?.access_token) return;
    setAdminFeedback(null);
    try {
      if (editingDept) {
        await updateDepartment(editingDept.id, deptForm, currentUser.access_token);
        setAdminFeedback({ type: "success", text: `Departamento '${deptForm.name}' actualizado correctamente.` });
      } else {
        await createDepartment(deptForm, currentUser.access_token);
        setAdminFeedback({ type: "success", text: `Departamento '${deptForm.name}' creado exitosamente.` });
      }
      setShowDeptModal(false);
      setEditingDept(null);
      loadAdminGeographicData();
      loadInitialDepartments();
    } catch (err: any) {
      setAdminFeedback({ type: "error", text: err.detail || err.message || "Error al guardar departamento" });
    }
  };

  const handleToggleDeptStatus = async (dept: DepartmentItem) => {
    if (!currentUser?.access_token) return;
    try {
      await updateDepartment(dept.id, { is_active: !dept.is_active }, currentUser.access_token);
      loadAdminGeographicData();
      loadInitialDepartments();
    } catch (err: any) {
      alert(err.message || "Error al cambiar estado");
    }
  };

  const handleSaveMunicipality = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!currentUser?.access_token) return;
    setAdminFeedback(null);
    try {
      if (editingMun) {
        await updateMunicipality(editingMun.id, munForm, currentUser.access_token);
        setAdminFeedback({ type: "success", text: `Municipio '${munForm.name}' actualizado correctamente.` });
      } else {
        await createMunicipality(munForm, currentUser.access_token);
        setAdminFeedback({ type: "success", text: `Municipio '${munForm.name}' creado exitosamente.` });
      }
      setShowMunModal(false);
      setEditingMun(null);
      // Reload municipalities
      if (adminSelectedDeptId) {
        const muns = await fetchMunicipalityObjects(adminSelectedDeptId);
        setAdminMunicipalities(muns);
      }
      loadInitialDepartments();
    } catch (err: any) {
      setAdminFeedback({ type: "error", text: err.detail || err.message || "Error al guardar municipio" });
    }
  };

  const handleToggleMunStatus = async (mun: MunicipalityItem) => {
    if (!currentUser?.access_token) return;
    try {
      await updateMunicipality(mun.id, { is_active: !mun.is_active }, currentUser.access_token);
      if (adminSelectedDeptId) {
        const muns = await fetchMunicipalityObjects(adminSelectedDeptId);
        setAdminMunicipalities(muns);
      }
    } catch (err: any) {
      alert(err.message || "Error al cambiar estado");
    }
  };

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8 space-y-6">
      {/* Header and Quick Stats */}
      <div className="flex flex-col md:flex-row md:items-end justify-between gap-4 border-b border-slate-200 pb-5">
        <div>
          <div className="flex items-center gap-2">
            <span className="text-xs font-bold text-[#0D9488] tracking-wider uppercase bg-teal-50 px-2.5 py-1 rounded-full border border-teal-200">
              Sistemas de Información Geográfica (GIS)
            </span>
            {currentUser?.role === "admin" && (
              <button
                onClick={() => setShowAdminPanel(!showAdminPanel)}
                className="text-xs font-bold text-[#0F2A4A] bg-slate-100 hover:bg-slate-200 px-2.5 py-1 rounded-full border border-slate-300 transition flex items-center gap-1.5"
              >
                <Shield className="w-3.5 h-3.5 text-[#0D9488]" />
                {showAdminPanel ? "Ocultar Administración Territorial" : "Gestionar División Territorial"}
              </button>
            )}
          </div>
          <h1 className="text-3xl font-extrabold text-slate-900 mt-2">
            Mapa Interactivo de Búsqueda Nacional
          </h1>
          <p className="text-xs sm:text-sm text-slate-600 max-w-3xl mt-1">
            Visualización geoespacial de casos activos sobre los 15 departamentos y 2 regiones autónomas de Nicaragua.
          </p>
        </div>

        {/* Status Pills */}
        <div className="flex items-center gap-3">
          <div className="bg-white border border-slate-200 rounded-xl px-4 py-2 text-center shadow-xs">
            <span className="text-[10px] text-slate-500 uppercase font-bold block">Casos en Mapa</span>
            <span className="text-base font-extrabold text-[#0F2A4A]">{filteredPoints.length}</span>
          </div>
          <div className="bg-white border border-slate-200 rounded-xl px-4 py-2 text-center shadow-xs">
            <span className="text-[10px] text-slate-500 uppercase font-bold block">Alertas Menores</span>
            <span className="text-base font-extrabold text-red-600">
              {filteredPoints.filter((p) => p.is_minor).length}
            </span>
          </div>
        </div>
      </div>

      {/* Error and Offline Banner with Retry Option */}
      {errorMessage && (
        <div className="bg-red-50 border-l-4 border-red-500 p-4 rounded-xl flex flex-col sm:flex-row items-start sm:items-center justify-between gap-3 text-red-900 text-xs shadow-sm">
          <div className="flex items-center gap-3">
            <AlertCircle className="w-5 h-5 text-red-600 shrink-0" />
            <div>
              <p className="font-bold">Error de sincronización con la base de datos geográfica</p>
              <p className="text-red-700 mt-0.5">{errorMessage}</p>
            </div>
          </div>
          <button
            onClick={() => {
              loadInitialDepartments();
              loadPoints();
            }}
            className="bg-red-600 hover:bg-red-700 text-white font-bold px-3.5 py-1.5 rounded-lg transition shrink-0 flex items-center gap-1.5"
          >
            <RotateCcw className="w-3.5 h-3.5" />
            Reintentar Conexión
          </button>
        </div>
      )}

      {/* Safety Notice Banner */}
      <div className="bg-blue-50 border border-blue-200 rounded-xl p-3.5 flex items-center gap-3 text-xs text-blue-900">
        <Info className="w-5 h-5 text-blue-600 shrink-0" />
        <p>
          <strong>Protección de Privacidad (Ley N.° 787):</strong> Este mapa emplea <strong>coordenadas de cuadrante aproximadas a nivel de municipio</strong>. Jamás se exponen domicilios particulares ni ubicaciones sensibles de refugio.
        </p>
      </div>

      {/* Administration Panel (Conditional for Admin) */}
      {showAdminPanel && currentUser?.role === "admin" && (
        <div className="bg-slate-900 text-white rounded-2xl p-6 shadow-md border border-slate-700 space-y-6">
          <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-3 border-b border-slate-800 pb-4">
            <div className="flex items-center gap-3">
              <div className="w-10 h-10 rounded-xl bg-teal-500/20 text-[#14B8A6] flex items-center justify-center font-bold">
                <Globe className="w-5 h-5" />
              </div>
              <div>
                <h2 className="text-lg font-bold text-white flex items-center gap-2">
                  Gestión del Catálogo Territorial Nacional
                  <span className="text-[10px] bg-teal-900/60 text-teal-300 font-bold px-2 py-0.5 rounded border border-teal-700">
                    Oficial INETER
                  </span>
                </h2>
                <p className="text-xs text-slate-400">
                  Administre los 15 departamentos, 2 regiones autónomas y 153 municipios oficiales de Nicaragua.
                </p>
              </div>
            </div>

            {geoSummary && (
              <div className="text-right text-xs text-slate-400">
                <span>Fuente: {geoSummary.source}</span>
                <span className="block text-[11px] text-teal-400">
                  {geoSummary.active_departments} Entidades • {geoSummary.active_municipalities} Municipios Activos
                </span>
              </div>
            )}
          </div>

          {/* Feedback message */}
          {adminFeedback && (
            <div className={`p-3 rounded-lg text-xs font-semibold flex items-center gap-2 ${
              adminFeedback.type === "success" 
                ? "bg-teal-950 border border-teal-700 text-teal-200" 
                : "bg-red-950 border border-red-700 text-red-200"
            }`}>
              {adminFeedback.type === "success" ? <CheckCircle2 className="w-4 h-4" /> : <AlertCircle className="w-4 h-4" />}
              {adminFeedback.text}
            </div>
          )}

          {/* Admin Sub-navigation & Actions */}
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6 items-start">
            {/* Left: Department List Table */}
            <div className="bg-slate-800/80 rounded-xl p-4 border border-slate-700 space-y-3">
              <div className="flex items-center justify-between">
                <h3 className="font-bold text-sm text-slate-200 flex items-center gap-2">
                  <Layers className="w-4 h-4 text-[#14B8A6]" />
                  Departamentos y Regiones ({adminDepartments.length})
                </h3>
                <button
                  onClick={() => {
                    setEditingDept(null);
                    setDeptForm({
                      name: "",
                      code: "",
                      type: "department",
                      latitude: 12.1364,
                      longitude: -86.2514,
                    });
                    setShowDeptModal(true);
                  }}
                  className="bg-[#0D9488] hover:bg-[#14B8A6] text-white text-xs font-bold px-2.5 py-1 rounded-md transition flex items-center gap-1"
                >
                  <Plus className="w-3.5 h-3.5" /> Agregar
                </button>
              </div>

              <div className="max-h-[300px] overflow-y-auto divide-y divide-slate-700 text-xs">
                {adminDepartments.map((dept) => (
                  <div 
                    key={dept.id} 
                    className={`py-2 px-2.5 rounded-lg flex items-center justify-between transition cursor-pointer ${
                      adminSelectedDeptId === dept.id ? "bg-teal-900/40 border border-teal-600" : "hover:bg-slate-700/50"
                    }`}
                    onClick={() => setAdminSelectedDeptId(dept.id)}
                  >
                    <div>
                      <span className="font-bold text-white block">{dept.name}</span>
                      <span className="text-[10px] text-slate-400 font-mono">
                        {dept.code} • {dept.type === "autonomous_region" ? "Región Autónoma" : "Departamento"} • {dept.municipalities_count} muns
                      </span>
                    </div>

                    <div className="flex items-center gap-1.5" onClick={(e) => e.stopPropagation()}>
                      <button
                        onClick={() => handleToggleDeptStatus(dept)}
                        className={`px-2 py-0.5 rounded text-[10px] font-bold ${
                          dept.is_active ? "bg-emerald-900 text-emerald-300" : "bg-red-900 text-red-300"
                        }`}
                        title="Activar / Desactivar"
                      >
                        {dept.is_active ? "Activo" : "Inactivo"}
                      </button>
                      <button
                        onClick={() => {
                          setEditingDept(dept);
                          setDeptForm({
                            name: dept.name,
                            code: dept.code,
                            type: dept.type,
                            latitude: dept.latitude,
                            longitude: dept.longitude,
                          });
                          setShowDeptModal(true);
                        }}
                        className="p-1 hover:bg-slate-600 rounded text-slate-300"
                        title="Editar departamento"
                      >
                        <Edit2 className="w-3.5 h-3.5" />
                      </button>
                    </div>
                  </div>
                ))}
              </div>
            </div>

            {/* Right: Municipalities Table */}
            <div className="bg-slate-800/80 rounded-xl p-4 border border-slate-700 space-y-3">
              <div className="flex items-center justify-between">
                <div>
                  <h3 className="font-bold text-sm text-slate-200 flex items-center gap-2">
                    <MapPin className="w-4 h-4 text-[#14B8A6]" />
                    Municipios ({adminMunicipalities.length})
                  </h3>
                  <span className="text-[11px] text-slate-400">
                    Departamento: {adminDepartments.find((d) => d.id === adminSelectedDeptId)?.name || "Seleccione uno"}
                  </span>
                </div>
                <button
                  onClick={() => {
                    setEditingMun(null);
                    setMunForm({
                      department_id: adminSelectedDeptId,
                      name: "",
                      code: "",
                      latitude: 12.1364,
                      longitude: -86.2514,
                    });
                    setShowMunModal(true);
                  }}
                  className="bg-[#0D9488] hover:bg-[#14B8A6] text-white text-xs font-bold px-2.5 py-1 rounded-md transition flex items-center gap-1"
                >
                  <Plus className="w-3.5 h-3.5" /> Agregar
                </button>
              </div>

              <div className="max-h-[300px] overflow-y-auto divide-y divide-slate-700 text-xs">
                {adminMunicipalities.length === 0 ? (
                  <div className="text-center py-8 text-slate-500 text-xs">
                    No hay municipios cargados o seleccione un departamento.
                  </div>
                ) : (
                  adminMunicipalities.map((mun) => (
                    <div key={mun.id} className="py-2 px-2 flex items-center justify-between hover:bg-slate-700/40 rounded-lg">
                      <div>
                        <span className="font-bold text-white block">{mun.name}</span>
                        <span className="text-[10px] text-slate-400 font-mono">
                          {mun.code} • Lat: {mun.latitude.toFixed(4)}, Lon: {mun.longitude.toFixed(4)}
                        </span>
                      </div>

                      <div className="flex items-center gap-1.5">
                        <button
                          onClick={() => handleToggleMunStatus(mun)}
                          className={`px-2 py-0.5 rounded text-[10px] font-bold ${
                            mun.is_active ? "bg-emerald-900 text-emerald-300" : "bg-red-900 text-red-300"
                          }`}
                        >
                          {mun.is_active ? "Activo" : "Inactivo"}
                        </button>
                        <button
                          onClick={() => {
                            setEditingMun(mun);
                            setMunForm({
                              department_id: mun.department_id,
                              name: mun.name,
                              code: mun.code,
                              latitude: mun.latitude,
                              longitude: mun.longitude,
                            });
                            setShowMunModal(true);
                          }}
                          className="p-1 hover:bg-slate-600 rounded text-slate-300"
                        >
                          <Edit2 className="w-3.5 h-3.5" />
                        </button>
                      </div>
                    </div>
                  ))
                )}
              </div>
            </div>
          </div>
        </div>
      )}

      {/* Interactive Filter Bar */}
      <div className="bg-white rounded-2xl border border-slate-200 p-5 shadow-xs space-y-4">
        <div className="flex items-center justify-between border-b border-slate-100 pb-3">
          <div className="flex items-center gap-2 text-xs font-bold text-slate-800">
            <Filter className="w-4 h-4 text-[#0D9488]" />
            Panel de Búsqueda y Filtros Geoespaciales
          </div>
          <button
            onClick={handleResetFilters}
            className="text-xs font-bold text-slate-500 hover:text-slate-800 flex items-center gap-1 transition"
          >
            <RotateCcw className="w-3 h-3" />
            Restablecer Filtros
          </button>
        </div>

        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4 text-xs">
          {/* Department Filter */}
          <div>
            <label className="block font-bold text-slate-700 mb-1">
              Departamento / Región:
            </label>
            <select
              value={selectedDept}
              onChange={(e) => setSelectedDept(e.target.value)}
              disabled={loadingDepts}
              className="w-full p-2.5 bg-slate-50 border border-slate-300 rounded-xl font-semibold text-slate-800 focus:ring-2 focus:ring-[#0D9488] focus:bg-white outline-none cursor-pointer transition"
            >
              <option value="all">
                {loadingDepts ? "Cargando catálogo..." : `Nacional (${departments.length} zonas)`}
              </option>
              {departments.map((d) => (
                <option key={d} value={d}>
                  {d}
                </option>
              ))}
            </select>
          </div>

          {/* Dependent Municipality Filter */}
          <div>
            <label className="block font-bold text-slate-700 mb-1">
              Municipio (Dependiente):
            </label>
            <select
              value={selectedMun}
              onChange={(e) => setSelectedMun(e.target.value)}
              disabled={selectedDept === "all" || loadingMuns}
              className="w-full p-2.5 bg-slate-50 border border-slate-300 rounded-xl font-semibold text-slate-800 focus:ring-2 focus:ring-[#0D9488] focus:bg-white outline-none cursor-pointer transition disabled:opacity-50"
            >
              <option value="all">
                {selectedDept === "all" 
                  ? "Seleccione un depto primero" 
                  : loadingMuns 
                  ? "Cargando municipios..." 
                  : `Todos los municipios (${municipalities.length})`}
              </option>
              {municipalities.map((m) => (
                <option key={m} value={m}>
                  {m}
                </option>
              ))}
            </select>
          </div>

          {/* Name / Case Search */}
          <div>
            <label className="block font-bold text-slate-700 mb-1">
              Buscar Persona o Expediente:
            </label>
            <div className="relative">
              <Search className="w-3.5 h-3.5 text-slate-400 absolute left-3 top-3" />
              <input
                type="text"
                value={searchTerm}
                onChange={(e) => setSearchTerm(e.target.value)}
                placeholder="Nombre, apellido o número de caso..."
                className="w-full pl-8 pr-3 py-2 bg-slate-50 border border-slate-300 rounded-xl text-slate-800 focus:ring-2 focus:ring-[#0D9488] focus:bg-white outline-none transition"
              />
            </div>
          </div>

          {/* Minor / Vulnerability Filter */}
          <div>
            <label className="block font-bold text-slate-700 mb-1">
              Filtro de Edad / Prioridad:
            </label>
            <select
              value={minorFilter}
              onChange={(e) => setMinorFilter(e.target.value)}
              className="w-full p-2.5 bg-slate-50 border border-slate-300 rounded-xl font-semibold text-slate-800 focus:ring-2 focus:ring-[#0D9488] focus:bg-white outline-none cursor-pointer transition"
            >
              <option value="all">Todas las edades</option>
              <option value="minors">Solo Alertas de Menores de Edad</option>
              <option value="adults">Solo Personas Adultas</option>
            </select>
          </div>
        </div>
      </div>

      {/* Map Layout */}
      <div className="grid grid-cols-1 lg:grid-cols-4 gap-6 items-start">
        {/* Map Container */}
        <div className="lg:col-span-3 bg-white rounded-2xl shadow-sm border border-slate-200 overflow-hidden h-[580px] relative">
          <NicaraguaMap points={filteredPoints} />

          {/* Map Legend Floating Box */}
          <div className="absolute bottom-4 left-4 bg-white/95 backdrop-blur-xs p-3 rounded-xl border border-slate-200 shadow-md text-xs space-y-1.5 z-1000 max-w-[200px]">
            <span className="font-bold text-slate-800 block text-[11px] border-b pb-1">
              Simbología Cartográfica
            </span>
            <div className="flex items-center gap-2 text-[10px] text-slate-700">
              <span className="w-3.5 h-3.5 rounded-full bg-red-600 border-2 border-white inline-block shadow-xs"></span>
              <span>Alerta Menor de Edad</span>
            </div>
            <div className="flex items-center gap-2 text-[10px] text-slate-700">
              <span className="w-3.5 h-3.5 rounded-full bg-[#0F2A4A] border-2 border-[#14B8A6] inline-block shadow-xs"></span>
              <span>Caso Adulto Autorizado</span>
            </div>
            <span className="text-[9px] text-slate-400 block pt-1 italic">
              * Cuadrantes agregados
            </span>
          </div>
        </div>

        {/* Sidebar with Filtered Cases List */}
        <div className="bg-white rounded-2xl shadow-sm border border-slate-200 p-5 space-y-4 max-h-[580px] overflow-y-auto">
          <div className="flex items-center justify-between border-b pb-3">
            <h3 className="font-bold text-slate-900 text-sm flex items-center gap-1.5">
              <MapIcon className="w-4 h-4 text-[#0D9488]" />
              Casos ({filteredPoints.length})
            </h3>
            <span className="text-[11px] text-[#0D9488] font-bold bg-teal-50 px-2 py-0.5 rounded-md border border-teal-200">
              Verificados
            </span>
          </div>

          {loadingPoints ? (
            <div className="text-center py-12 text-xs text-slate-400 space-y-2">
              <div className="animate-spin w-6 h-6 border-2 border-[#0D9488] border-t-transparent rounded-full mx-auto"></div>
              <p>Actualizando puntos...</p>
            </div>
          ) : filteredPoints.length === 0 ? (
            <div className="text-center py-12 text-xs text-slate-500 space-y-2">
              <AlertCircle className="w-8 h-8 text-slate-300 mx-auto" />
              <p className="font-bold text-slate-700">Sin casos con los criterios actuales</p>
              <p className="text-[11px] text-slate-400">
                Pruebe cambiando de municipio o restableciendo los filtros.
              </p>
              <button
                onClick={handleResetFilters}
                className="mt-2 text-xs bg-slate-100 hover:bg-slate-200 text-[#0F2A4A] font-bold px-3 py-1.5 rounded-lg transition"
              >
                Limpiar filtros
              </button>
            </div>
          ) : (
            <div className="space-y-3">
              {filteredPoints.map((pt) => (
                <Link
                  key={pt.id}
                  href={`/casos/${pt.id}`}
                  className="block p-3 rounded-xl border border-slate-100 bg-slate-50 hover:bg-slate-100 hover:border-[#14B8A6] transition group shadow-2xs"
                >
                  <div className="flex items-start justify-between">
                    <span className="font-bold text-xs text-slate-900 group-hover:text-[#0D9488]">
                      {pt.full_name}
                    </span>
                    {pt.is_minor && (
                      <span className="bg-red-600 text-white text-[9px] font-bold px-1.5 py-0.5 rounded shadow-2xs">
                        ALERTA MENOR
                      </span>
                    )}
                  </div>
                  <div className="text-[11px] text-slate-600 mt-1 flex items-center gap-1 font-medium">
                    <MapPin className="w-3 h-3 text-[#0D9488] shrink-0" />
                    <span className="truncate">{pt.municipality}, {pt.department}</span>
                  </div>
                  <div className="text-[10px] text-slate-400 mt-1 flex items-center justify-between">
                    <span>{pt.age_at_disappearance} años</span>
                    <span className="font-mono font-semibold">Exp: {pt.case_number}</span>
                  </div>
                </Link>
              ))}
            </div>
          )}
        </div>
      </div>

      {/* Modal: Department Create / Edit */}
      {showDeptModal && (
        <div className="fixed inset-0 z-50 bg-black/60 flex items-center justify-center p-4">
          <div className="bg-white rounded-2xl max-w-md w-full p-6 space-y-4 shadow-2xl">
            <div className="flex items-center justify-between border-b pb-3">
              <h3 className="font-bold text-slate-900 text-sm">
                {editingDept ? "Editar Departamento" : "Nuevo Departamento o Región"}
              </h3>
              <button onClick={() => setShowDeptModal(false)} className="text-slate-400 hover:text-slate-600">
                <X className="w-5 h-5" />
              </button>
            </div>

            <form onSubmit={handleSaveDepartment} className="space-y-3 text-xs">
              <div>
                <label className="block font-bold text-slate-700 mb-1">Nombre Oficial:</label>
                <input
                  type="text"
                  required
                  value={deptForm.name}
                  onChange={(e) => setDeptForm({ ...deptForm, name: e.target.value })}
                  placeholder="Ej: Matagalpa"
                  className="w-full p-2 border border-slate-300 rounded-lg outline-none focus:ring-2 focus:ring-[#0D9488]"
                />
              </div>

              <div>
                <label className="block font-bold text-slate-700 mb-1">Código Oficial (2-10 caracteres):</label>
                <input
                  type="text"
                  required
                  value={deptForm.code}
                  onChange={(e) => setDeptForm({ ...deptForm, code: e.target.value.toUpperCase() })}
                  placeholder="Ej: MAT"
                  className="w-full p-2 border border-slate-300 rounded-lg font-mono outline-none focus:ring-2 focus:ring-[#0D9488]"
                />
              </div>

              <div>
                <label className="block font-bold text-slate-700 mb-1">Tipo de Demarcación:</label>
                <select
                  value={deptForm.type}
                  onChange={(e) => setDeptForm({ ...deptForm, type: e.target.value as "department" | "autonomous_region" })}
                  className="w-full p-2 border border-slate-300 rounded-lg outline-none focus:ring-2 focus:ring-[#0D9488]"
                >
                  <option value="department">Departamento</option>
                  <option value="autonomous_region">Región Autónoma</option>
                </select>
              </div>

              <div className="grid grid-cols-2 gap-3">
                <div>
                  <label className="block font-bold text-slate-700 mb-1">Latitud (10.70 a 15.10):</label>
                  <input
                    type="number"
                    step="0.0001"
                    required
                    value={deptForm.latitude}
                    onChange={(e) => setDeptForm({ ...deptForm, latitude: parseFloat(e.target.value) })}
                    className="w-full p-2 border border-slate-300 rounded-lg outline-none focus:ring-2 focus:ring-[#0D9488]"
                  />
                </div>
                <div>
                  <label className="block font-bold text-slate-700 mb-1">Longitud (-87.70 a -82.50):</label>
                  <input
                    type="number"
                    step="0.0001"
                    required
                    value={deptForm.longitude}
                    onChange={(e) => setDeptForm({ ...deptForm, longitude: parseFloat(e.target.value) })}
                    className="w-full p-2 border border-slate-300 rounded-lg outline-none focus:ring-2 focus:ring-[#0D9488]"
                  />
                </div>
              </div>

              <div className="pt-3 flex justify-end gap-2 border-t">
                <button
                  type="button"
                  onClick={() => setShowDeptModal(false)}
                  className="px-3 py-1.5 rounded-lg border text-slate-600 font-semibold"
                >
                  Cancelar
                </button>
                <button
                  type="submit"
                  className="px-4 py-1.5 rounded-lg bg-[#0D9488] hover:bg-[#14B8A6] text-white font-bold"
                >
                  Guardar
                </button>
              </div>
            </form>
          </div>
        </div>
      )}

      {/* Modal: Municipality Create / Edit */}
      {showMunModal && (
        <div className="fixed inset-0 z-50 bg-black/60 flex items-center justify-center p-4">
          <div className="bg-white rounded-2xl max-w-md w-full p-6 space-y-4 shadow-2xl">
            <div className="flex items-center justify-between border-b pb-3">
              <h3 className="font-bold text-slate-900 text-sm">
                {editingMun ? "Editar Municipio" : "Nuevo Municipio Oficial"}
              </h3>
              <button onClick={() => setShowMunModal(false)} className="text-slate-400 hover:text-slate-600">
                <X className="w-5 h-5" />
              </button>
            </div>

            <form onSubmit={handleSaveMunicipality} className="space-y-3 text-xs">
              <div>
                <label className="block font-bold text-slate-700 mb-1">Departamento Perteneciente:</label>
                <select
                  value={munForm.department_id}
                  onChange={(e) => setMunForm({ ...munForm, department_id: e.target.value })}
                  required
                  className="w-full p-2 border border-slate-300 rounded-lg outline-none focus:ring-2 focus:ring-[#0D9488]"
                >
                  <option value="">Seleccione Departamento</option>
                  {adminDepartments.map((d) => (
                    <option key={d.id} value={d.id}>
                      {d.name}
                    </option>
                  ))}
                </select>
              </div>

              <div>
                <label className="block font-bold text-slate-700 mb-1">Nombre Oficial del Municipio:</label>
                <input
                  type="text"
                  required
                  value={munForm.name}
                  onChange={(e) => setMunForm({ ...munForm, name: e.target.value })}
                  placeholder="Ej: Sébaco"
                  className="w-full p-2 border border-slate-300 rounded-lg outline-none focus:ring-2 focus:ring-[#0D9488]"
                />
              </div>

              <div>
                <label className="block font-bold text-slate-700 mb-1">Código Municipal (Ej: MAT-12):</label>
                <input
                  type="text"
                  required
                  value={munForm.code}
                  onChange={(e) => setMunForm({ ...munForm, code: e.target.value.toUpperCase() })}
                  placeholder="Ej: MAT-12"
                  className="w-full p-2 border border-slate-300 rounded-lg font-mono outline-none focus:ring-2 focus:ring-[#0D9488]"
                />
              </div>

              <div className="grid grid-cols-2 gap-3">
                <div>
                  <label className="block font-bold text-slate-700 mb-1">Latitud (10.70 a 15.10):</label>
                  <input
                    type="number"
                    step="0.0001"
                    required
                    value={munForm.latitude}
                    onChange={(e) => setMunForm({ ...munForm, latitude: parseFloat(e.target.value) })}
                    className="w-full p-2 border border-slate-300 rounded-lg outline-none focus:ring-2 focus:ring-[#0D9488]"
                  />
                </div>
                <div>
                  <label className="block font-bold text-slate-700 mb-1">Longitud (-87.70 a -82.50):</label>
                  <input
                    type="number"
                    step="0.0001"
                    required
                    value={munForm.longitude}
                    onChange={(e) => setMunForm({ ...munForm, longitude: parseFloat(e.target.value) })}
                    className="w-full p-2 border border-slate-300 rounded-lg outline-none focus:ring-2 focus:ring-[#0D9488]"
                  />
                </div>
              </div>

              <div className="pt-3 flex justify-end gap-2 border-t">
                <button
                  type="button"
                  onClick={() => setShowMunModal(false)}
                  className="px-3 py-1.5 rounded-lg border text-slate-600 font-semibold"
                >
                  Cancelar
                </button>
                <button
                  type="submit"
                  className="px-4 py-1.5 rounded-lg bg-[#0D9488] hover:bg-[#14B8A6] text-white font-bold"
                >
                  Guardar
                </button>
              </div>
            </form>
          </div>
        </div>
      )}
    </div>
  );
}
