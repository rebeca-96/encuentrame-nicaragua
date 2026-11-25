"use client";

import { useState } from "react";
import Link from "next/link";
import { Search, ShieldCheck, Lock, CheckCircle2, AlertCircle, Clock, ArrowRight } from "lucide-react";
import { trackTipStatus } from "../../lib/api";

export default function PistasPage() {
  const [tipCode, setTipCode] = useState("");
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState<{ tip_code: string; status: string; created_at: string; message: string } | null>(null);
  const [error, setError] = useState<string | null>(null);

  const handleTrackSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!tipCode.trim()) return;

    setLoading(true);
    setError(null);
    setResult(null);

    try {
      const data = await trackTipStatus(tipCode.trim());
      setResult(data);
    } catch (err: any) {
      setError(err.message || "No se encontró ninguna pista con este código.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-12 space-y-10">
      {/* Header */}
      <div className="text-center space-y-3">
        <div className="inline-flex items-center gap-2 bg-[#0D9488]/10 text-[#0D9488] px-3.5 py-1.5 rounded-full text-xs font-semibold">
          <ShieldCheck className="w-4 h-4" />
          <span>Canal Ciudadano Protegido</span>
        </div>
        <h1 className="text-3xl font-extrabold text-slate-900">
          Seguimiento Anónimo de Pistas
        </h1>
        <p className="text-sm text-slate-600 max-w-xl mx-auto">
          Si aportó información sobre alguna persona no localizada, ingrese su código de rastreo para consultar el estado del trámite sin revelar su identidad.
        </p>
      </div>

      {/* Track Form Card */}
      <div className="bg-white p-6 sm:p-8 rounded-2xl shadow-sm border border-slate-200 max-w-2xl mx-auto space-y-6">
        <form onSubmit={handleTrackSubmit} className="space-y-4">
          <div>
            <label className="block text-xs font-bold text-slate-700 uppercase tracking-wider mb-1.5">
              Código de la Pista (Ej. PISTA-8A12-9F01):
            </label>
            <div className="flex gap-2">
              <input
                type="text"
                required
                value={tipCode}
                onChange={(e) => setTipCode(e.target.value.toUpperCase())}
                placeholder="PISTA-XXXX-XXXX"
                className="w-full p-3 font-mono text-base uppercase rounded-xl border border-slate-300 focus:ring-2 focus:ring-[#0D9488] focus:outline-none"
              />
              <button
                type="submit"
                disabled={loading || !tipCode.trim()}
                className="bg-[#0D9488] hover:bg-[#0f766e] disabled:opacity-50 text-white font-semibold text-xs px-6 py-3 rounded-xl transition flex items-center gap-2 shrink-0 shadow-sm"
              >
                <Search className="w-4 h-4" />
                {loading ? "Consultando..." : "Consultar"}
              </button>
            </div>
          </div>
        </form>

        {/* Error */}
        {error && (
          <div className="bg-red-50 border border-red-200 rounded-xl p-4 text-xs text-red-700 flex items-center gap-2">
            <AlertCircle className="w-4 h-4 shrink-0" />
            <span>{error}</span>
          </div>
        )}

        {/* Result */}
        {result && (
          <div className="bg-slate-50 border border-slate-200 rounded-xl p-5 space-y-3">
            <div className="flex items-center justify-between border-b pb-2">
              <span className="font-mono text-xs font-bold text-slate-700">
                Código: {result.tip_code}
              </span>
              <span className="bg-blue-100 text-[#0F2A4A] text-[11px] font-bold px-2 py-0.5 rounded capitalize">
                Estado: {result.status}
              </span>
            </div>

            <div className="text-xs text-slate-700 space-y-1.5 pt-1">
              <p className="font-medium text-slate-900">{result.message}</p>
              <div className="text-[11px] text-slate-400 flex items-center gap-1 pt-1">
                <Clock className="w-3.5 h-3.5" />
                <span>Fecha de recepción: {new Date(result.created_at).toLocaleString("es-NI")}</span>
              </div>
            </div>
          </div>
        )}

        <div className="pt-2 text-[11px] text-slate-400 flex items-center justify-center gap-1.5 border-t border-slate-100">
          <Lock className="w-3.5 h-3.5 text-emerald-500" />
          <span>La consulta es anónima y no genera registro de su dirección IP ni identidad.</span>
        </div>
      </div>

      {/* Alternative Action */}
      <div className="bg-slate-100 p-6 rounded-2xl border border-slate-200 text-center max-w-2xl mx-auto space-y-2">
        <h3 className="font-bold text-sm text-slate-800">
          ¿Desea aportar información nueva sobre una persona?
        </h3>
        <p className="text-xs text-slate-600">
          Explore los casos activos en el catálogo nacional para asociar su pista directamente al caso correspondiente.
        </p>
        <div className="pt-2">
          <Link
            href="/casos.html"
            className="inline-flex items-center gap-1.5 text-xs font-bold text-[#0D9488] hover:text-[#0f766e]"
          >
            Ir al catálogo de casos
            <ArrowRight className="w-3.5 h-3.5" />
          </Link>
        </div>
      </div>
    </div>
  );
}
