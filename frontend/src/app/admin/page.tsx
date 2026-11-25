"use client";

import { useEffect, useState } from "react";
import Link from "next/link";
import { 
  Shield, CheckCircle, XCircle, AlertTriangle, FileText, 
  Users, Activity, Sparkles, RefreshCw, Eye, Lock
} from "lucide-react";
import { 
  fetchPendingReports, moderateReport, fetchMetrics, 
  fetchAdminTips, fetchAuditLogs, checkAIDuplicates, fetchAISummary 
} from "../../lib/api";

export default function AdminDashboardPage() {
  const [session, setSession] = useState<{ access_token: string; full_name: string; role: string } | null>(null);
  const [activeTab, setActiveTab] = useState<"pending" | "tips" | "audit">("pending");
  const [loading, setLoading] = useState(true);

  // Dashboard Data
  const [metrics, setMetrics] = useState<any>(null);
  const [pendingReports, setPendingReports] = useState<any[]>([]);
  const [tips, setTips] = useState<any[]>([]);
  const [auditLogs, setAuditLogs] = useState<any[]>([]);

  // AI Assistance Modal state
  const [aiModalReport, setAiModalReport] = useState<any | null>(null);
  const [aiDuplicates, setAiDuplicates] = useState<any | null>(null);
  const [aiSummary, setAiSummary] = useState<any | null>(null);
  const [aiLoading, setAiLoading] = useState(false);

  useEffect(() => {
    const raw = localStorage.getItem("encuentrame_session");
    if (raw) {
      try {
        const s = JSON.parse(raw);
        setSession(s);
        if (s.role === "admin" || s.role === "moderator") {
          loadData(s.access_token);
        }
      } catch (e) {}
    }
    setLoading(false);
  }, []);

  const loadData = async (token: string) => {
    try {
      const [m, pend, t] = await Promise.all([
        fetchMetrics(token),
        fetchPendingReports(token),
        fetchAdminTips(token),
      ]);
      setMetrics(m);
      setPendingReports(pend);
      setTips(t);

      if (token) {
        const logs = await fetchAuditLogs(token);
        setAuditLogs(logs);
      }
    } catch (e) {
      console.error(e);
    }
  };

  const handleModerate = async (reportId: string, decision: string) => {
    if (!session) return;
    const notes = prompt(`Ingrese notas internas de moderación para la acción (${decision}):`) || "";
    try {
      await moderateReport(reportId, decision, notes, session.access_token);
      alert(`Reporte procesado exitosamente (${decision}).`);
      loadData(session.access_token);
    } catch (err: any) {
      alert(err.message || "Error al moderar");
    }
  };

  const handleOpenAI = async (report: any) => {
    if (!session) return;
    setAiModalReport(report);
    setAiLoading(true);
    try {
      const [dupRes, sumRes] = await Promise.all([
        checkAIDuplicates(report.id, session.access_token),
        fetchAISummary(report.id, session.access_token),
      ]);
      setAiDuplicates(dupRes);
      setAiSummary(sumRes);
    } catch (err) {
      console.error(err);
    } finally {
      setAiLoading(false);
    }
  };

  if (!session || (session.role !== "admin" && session.role !== "moderator")) {
    return (
      <div className="max-w-md mx-auto px-4 py-20 text-center space-y-4">
        <div className="w-12 h-12 bg-amber-100 text-amber-600 rounded-full flex items-center justify-center mx-auto">
          <Lock className="w-6 h-6" />
        </div>
        <h2 className="text-xl font-bold text-slate-900">Acceso Restringido</h2>
        <p className="text-xs text-slate-600">
          Se requieren credenciales de moderador o administrador para acceder a esta área protegida.
        </p>
        <Link
          href="/login.html"
          className="inline-block bg-[#0F2A4A] text-white px-4 py-2 rounded-xl text-xs font-semibold"
        >
          Iniciar Sesión
        </Link>
      </div>
    );
  }

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-10 space-y-8">
      {/* Header */}
      <div className="flex flex-col sm:flex-row justify-between sm:items-center gap-4">
        <div>
          <span className="text-xs font-bold text-[#0D9488] tracking-wider uppercase flex items-center gap-1">
            <Shield className="w-4 h-4" />
            Panel de Seguridad y Control
          </span>
          <h1 className="text-2xl sm:text-3xl font-extrabold text-slate-900 mt-1">
            Centro de Moderación y Auditoría
          </h1>
          <p className="text-xs text-slate-600">
            Sesión activa como: <strong>{session.full_name}</strong> ({session.role.toUpperCase()})
          </p>
        </div>

        <button
          onClick={() => loadData(session.access_token)}
          className="bg-slate-100 hover:bg-slate-200 text-slate-700 text-xs font-semibold px-4 py-2 rounded-xl transition flex items-center gap-1.5 self-start"
        >
          <RefreshCw className="w-3.5 h-3.5" />
          Actualizar datos
        </button>
      </div>

      {/* Metrics Row */}
      {metrics && (
        <div className="grid grid-cols-2 sm:grid-cols-4 gap-4">
          <div className="bg-white p-4 rounded-xl shadow-sm border border-slate-200 space-y-1">
            <span className="text-xs text-slate-500 font-medium">Casos Pendientes</span>
            <div className="text-2xl font-black text-amber-600">{metrics.pending_review}</div>
          </div>
          <div className="bg-white p-4 rounded-xl shadow-sm border border-slate-200 space-y-1">
            <span className="text-xs text-slate-500 font-medium">Casos Publicados</span>
            <div className="text-2xl font-black text-[#0D9488]">{metrics.approved_published}</div>
          </div>
          <div className="bg-white p-4 rounded-xl shadow-sm border border-slate-200 space-y-1">
            <span className="text-xs text-slate-500 font-medium">Casos Resueltos</span>
            <div className="text-2xl font-black text-emerald-600">
              {metrics.closed_found + metrics.closed_resolved}
            </div>
          </div>
          <div className="bg-white p-4 rounded-xl shadow-sm border border-slate-200 space-y-1">
            <span className="text-xs text-slate-500 font-medium">Pistas Recibidas</span>
            <div className="text-2xl font-black text-blue-600">{metrics.total_tips}</div>
          </div>
        </div>
      )}

      {/* Navigation Tabs */}
      <div className="flex border-b border-slate-200 gap-4 text-xs font-semibold">
        <button
          onClick={() => setActiveTab("pending")}
          className={`pb-3 border-b-2 flex items-center gap-1.5 transition ${
            activeTab === "pending"
              ? "border-[#0D9488] text-[#0D9488]"
              : "border-transparent text-slate-500 hover:text-slate-800"
          }`}
        >
          <Activity className="w-4 h-4" />
          Cola de Moderación ({pendingReports.length})
        </button>
        <button
          onClick={() => setActiveTab("tips")}
          className={`pb-3 border-b-2 flex items-center gap-1.5 transition ${
            activeTab === "tips"
              ? "border-[#0D9488] text-[#0D9488]"
              : "border-transparent text-slate-500 hover:text-slate-800"
          }`}
        >
          <FileText className="w-4 h-4" />
          Pistas Confidenciales ({tips.length})
        </button>
        {session.role === "admin" && (
          <button
            onClick={() => setActiveTab("audit")}
            className={`pb-3 border-b-2 flex items-center gap-1.5 transition ${
              activeTab === "audit"
                ? "border-[#0D9488] text-[#0D9488]"
                : "border-transparent text-slate-500 hover:text-slate-800"
            }`}
          >
            <Shield className="w-4 h-4" />
            Registro de Auditoría ({auditLogs.length})
          </button>
        )}
      </div>

      {/* TAB 1: PENDING REPORTS */}
      {activeTab === "pending" && (
        <div className="space-y-4">
          {pendingReports.length === 0 ? (
            <div className="bg-white p-12 rounded-2xl text-center border border-slate-200 text-slate-500 text-xs">
              No hay reportes pendientes de revisión en este momento.
            </div>
          ) : (
            <div className="space-y-4">
              {pendingReports.map((r) => (
                <div
                  key={r.id}
                  className="bg-white p-6 rounded-2xl shadow-sm border border-slate-200 space-y-4"
                >
                  <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-2 border-b pb-3">
                    <div>
                      <span className="font-mono text-xs text-slate-500 font-bold">
                        Expediente: {r.case_number}
                      </span>
                      <h3 className="text-lg font-bold text-slate-900">
                        {r.first_name} {r.last_name} ({r.age_at_disappearance} años)
                      </h3>
                      <div className="text-xs text-slate-600">
                        📍 {r.municipality}, {r.department} • Fecha: {new Date(r.disappearance_date).toLocaleDateString("es-NI")}
                      </div>
                    </div>

                    <div className="flex items-center gap-2">
                      <button
                        onClick={() => handleOpenAI(r)}
                        className="bg-purple-50 text-purple-700 hover:bg-purple-100 border border-purple-200 px-3 py-1.5 rounded-lg text-xs font-semibold flex items-center gap-1.5 transition"
                      >
                        <Sparkles className="w-3.5 h-3.5" />
                        Asistente IA
                      </button>
                      <button
                        onClick={() => handleModerate(r.id, "approve")}
                        className="bg-emerald-600 hover:bg-emerald-700 text-white px-3 py-1.5 rounded-lg text-xs font-semibold flex items-center gap-1 transition"
                      >
                        <CheckCircle className="w-3.5 h-3.5" />
                        Aprobar y Publicar
                      </button>
                      <button
                        onClick={() => handleModerate(r.id, "reject")}
                        className="bg-red-600 hover:bg-red-700 text-white px-3 py-1.5 rounded-lg text-xs font-semibold flex items-center gap-1 transition"
                      >
                        <XCircle className="w-3.5 h-3.5" />
                        Rechazar
                      </button>
                    </div>
                  </div>

                  {/* Private verification details */}
                  <div className="bg-slate-50 p-3.5 rounded-xl border border-slate-200 text-xs space-y-2">
                    <span className="font-bold text-slate-800 block text-[11px] uppercase tracking-wider">
                      Datos de Validación del Reportante (Privados):
                    </span>
                    <div className="grid grid-cols-1 sm:grid-cols-3 gap-2 text-slate-600">
                      <div>
                        <strong>Reportante:</strong> {r.reporter_name}
                      </div>
                      <div>
                        <strong>Parentesco:</strong> {r.relationship_to_victim}
                      </div>
                      <div>
                        <strong>Contacto:</strong> {r.reporter_phone || r.reporter_email}
                      </div>
                    </div>
                  </div>

                  <div className="text-xs text-slate-700 space-y-1">
                    <p>
                      <strong>Descripción física:</strong> {r.physical_description}
                    </p>
                    <p>
                      <strong>Vestimenta:</strong> {r.clothing_description}
                    </p>
                    <p>
                      <strong>Circunstancias:</strong> {r.circumstances}
                    </p>
                  </div>
                </div>
              ))}
            </div>
          )}
        </div>
      )}

      {/* TAB 2: CONFIDENTIAL TIPS */}
      {activeTab === "tips" && (
        <div className="space-y-4">
          {tips.length === 0 ? (
            <div className="bg-white p-12 rounded-2xl text-center border border-slate-200 text-slate-500 text-xs">
              No hay pistas confidenciales registradas.
            </div>
          ) : (
            <div className="bg-white rounded-2xl shadow-sm border border-slate-200 overflow-x-auto">
              <table className="w-full text-left text-xs text-slate-700">
                <thead className="bg-slate-50 border-b border-slate-200 text-[11px] font-bold text-slate-600 uppercase">
                  <tr>
                    <th className="p-3.5">Código</th>
                    <th className="p-3.5">Caso Asociado</th>
                    <th className="p-3.5">Contenido de la Pista</th>
                    <th className="p-3.5">Contacto Informante</th>
                    <th className="p-3.5">Estado</th>
                    <th className="p-3.5">Fecha</th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-slate-100">
                  {tips.map((t) => (
                    <tr key={t.id} className="hover:bg-slate-50">
                      <td className="p-3.5 font-mono font-bold text-[#0F2A4A]">{t.tip_code}</td>
                      <td className="p-3.5">
                        <div className="font-bold">{t.missing_person_name}</div>
                        <div className="text-slate-400 font-mono">{t.case_number}</div>
                      </td>
                      <td className="p-3.5 max-w-xs leading-relaxed">{t.description}</td>
                      <td className="p-3.5 font-mono text-slate-500">
                        {t.informant_contact || "Anónimo estricto"}
                      </td>
                      <td className="p-3.5">
                        <span className="bg-blue-50 text-blue-700 font-bold px-2 py-0.5 rounded capitalize">
                          {t.status}
                        </span>
                      </td>
                      <td className="p-3.5 text-slate-400">
                        {new Date(t.created_at).toLocaleDateString("es-NI")}
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          )}
        </div>
      )}

      {/* TAB 3: AUDIT LOGS */}
      {activeTab === "audit" && (
        <div className="bg-white rounded-2xl shadow-sm border border-slate-200 overflow-x-auto">
          <table className="w-full text-left text-xs text-slate-700">
            <thead className="bg-slate-50 border-b border-slate-200 text-[11px] font-bold text-slate-600 uppercase">
              <tr>
                <th className="p-3.5">Fecha / Hora</th>
                <th className="p-3.5">Usuario</th>
                <th className="p-3.5">Acción</th>
                <th className="p-3.5">Entidad</th>
                <th className="p-3.5">IP</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-100 font-mono text-[11px]">
              {auditLogs.map((l) => (
                <tr key={l.id} className="hover:bg-slate-50">
                  <td className="p-3.5 text-slate-400">
                    {new Date(l.created_at).toLocaleString("es-NI")}
                  </td>
                  <td className="p-3.5 font-sans font-medium text-slate-800">{l.user_email}</td>
                  <td className="p-3.5 font-bold text-[#0D9488]">{l.action}</td>
                  <td className="p-3.5 text-slate-500">{l.entity_name} ({l.entity_id.slice(0, 8)}...)</td>
                  <td className="p-3.5 text-slate-400">{l.ip_address || "127.0.0.1"}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}

      {/* AI ASSISTANCE MODAL (MÓDULO H) */}
      {aiModalReport && (
        <div className="fixed inset-0 z-50 bg-black/50 backdrop-blur-sm flex items-center justify-center p-4">
          <div className="bg-white rounded-2xl max-w-2xl w-full p-6 space-y-5 shadow-2xl max-h-[90vh] overflow-y-auto">
            <div className="flex justify-between items-center border-b pb-3">
              <div className="flex items-center gap-2">
                <Sparkles className="w-5 h-5 text-purple-600" />
                <h3 className="font-bold text-slate-900 text-base">
                  Análisis Asistido por IA: {aiModalReport.first_name} {aiModalReport.last_name}
                </h3>
              </div>
              <button
                onClick={() => setAiModalReport(null)}
                className="text-slate-400 hover:text-slate-600"
              >
                ✕
              </button>
            </div>

            {aiLoading ? (
              <div className="text-center py-10 text-xs text-slate-500">
                Analizando similitudes semánticas y completitud de datos...
              </div>
            ) : (
              <div className="space-y-4 text-xs">
                {/* Completeness & Summary */}
                {aiSummary && (
                  <div className="bg-purple-50 p-4 rounded-xl border border-purple-200 space-y-2">
                    <div className="flex justify-between items-center">
                      <span className="font-bold text-purple-900">Ficha Sintética:</span>
                      <span className="bg-purple-200 text-purple-800 font-bold px-2 py-0.5 rounded">
                        Completitud: {(aiSummary.completeness_score * 100).toFixed(0)}%
                      </span>
                    </div>
                    <p className="text-slate-700 leading-relaxed">{aiSummary.summary_text}</p>
                    {aiSummary.missing_or_weak_fields?.length > 0 && (
                      <div className="pt-2">
                        <strong className="text-purple-900 block mb-1">Campos recomendados para verificar:</strong>
                        <ul className="list-disc pl-4 space-y-0.5 text-slate-600">
                          {aiSummary.missing_or_weak_fields.map((f: string, i: number) => (
                            <li key={i}>{f}</li>
                          ))}
                        </ul>
                      </div>
                    )}
                  </div>
                )}

                {/* Duplicates Check */}
                <div className="space-y-2">
                  <h4 className="font-bold text-slate-900 uppercase tracking-wider text-[11px]">
                    Detección de Posibles Reportes Duplicados:
                  </h4>
                  {aiDuplicates?.potential_duplicates?.length === 0 ? (
                    <div className="p-3 bg-emerald-50 text-emerald-800 border border-emerald-200 rounded-lg">
                      ✓ No se detectaron reportes duplicados existentes para esta persona.
                    </div>
                  ) : (
                    <div className="space-y-2">
                      {aiDuplicates?.potential_duplicates?.map((dup: any, i: number) => (
                        <div key={i} className="p-3 bg-amber-50 border border-amber-200 rounded-lg text-slate-800 space-y-1">
                          <div className="flex justify-between font-bold">
                            <span>{dup.full_name} ({dup.case_number})</span>
                            <span className="text-amber-700">Similitud: {(dup.similarity_score * 100).toFixed(0)}%</span>
                          </div>
                          <ul className="list-disc pl-4 text-slate-600 text-[11px]">
                            {dup.reasons?.map((r: string, idx: number) => (
                              <li key={idx}>{r}</li>
                            ))}
                          </ul>
                        </div>
                      ))}
                    </div>
                  )}
                </div>

                <div className="p-3 bg-slate-50 text-slate-500 rounded-lg text-[10px] italic border">
                  * Salvaguarda Ética: La IA asiste la revisión humana. La decisión de aprobación, rechazo o declaración de estatus es ejecutada exclusivamente por el moderador.
                </div>
              </div>
            )}

            <div className="flex justify-end pt-2">
              <button
                onClick={() => setAiModalReport(null)}
                className="bg-slate-800 text-white text-xs font-semibold px-4 py-2 rounded-lg"
              >
                Cerrar Asistente
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
