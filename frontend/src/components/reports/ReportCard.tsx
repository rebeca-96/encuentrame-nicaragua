import Link from "next/link";
import { MapPin, Calendar, AlertCircle, FileText, ChevronRight, CheckCircle2 } from "lucide-react";
import { ReportPublicItem } from "../../types";
import { getCasePhotoUrl } from "../../lib/catalogData";

export default function ReportCard({ report }: { report: ReportPublicItem }) {
  const formattedDate = new Date(report.disappearance_date).toLocaleDateString("es-NI", {
    year: "numeric",
    month: "long",
    day: "numeric",
  });

  const photoSrc = report.primary_photo_url && !report.primary_photo_url.includes("avatar-placeholder")
    ? (report.primary_photo_url.startsWith("http") || report.primary_photo_url.startsWith("/") || report.primary_photo_url.startsWith("data:")
        ? report.primary_photo_url
        : `${process.env.NEXT_PUBLIC_API_URL ? process.env.NEXT_PUBLIC_API_URL.replace("/api/v1", "") : ""}${report.primary_photo_url}`)
    : getCasePhotoUrl(report.case_number, report.primary_photo_url);

  const isClosed = 
    report.status === "closed" || 
    report.status === "closed_found" || 
    report.status === "closed_resolved" || 
    report.status === "resolved";

  return (
    <div className={`bg-white rounded-xl shadow-sm border overflow-hidden hover:shadow-md transition flex flex-col group ${
      isClosed ? "border-emerald-300 bg-slate-50/50" : "border-slate-200"
    }`}>
      {/* Top Banner / Photo */}
      <Link href={`/casos/${report.id}`} className="block relative h-56 bg-slate-100 overflow-hidden cursor-pointer">
        <img
          src={photoSrc}
          alt={`Fotografía autorizada de ${report.first_name} ${report.last_name}`}
          className={`w-full h-full object-cover group-hover:scale-105 transition duration-300 ${
            isClosed ? "grayscale-[20%] opacity-90" : ""
          }`}
          onError={(e) => {
            (e.target as HTMLImageElement).src = "/images/avatar-placeholder.svg";
          }}
        />

        {/* Status & Minor Badges */}
        <div className="absolute top-3 left-3 flex flex-col gap-1.5 items-start">
          {/* Status Badge */}
          {isClosed ? (
            <span className="bg-emerald-600 text-white text-[11px] font-bold px-2.5 py-0.5 rounded-full shadow-md flex items-center gap-1">
              <CheckCircle2 className="w-3.5 h-3.5" />
              LOCALIZADO / CASO RESUELTO
            </span>
          ) : (
            <span className="bg-[#0D9488] text-white text-[11px] font-bold px-2.5 py-0.5 rounded-full shadow-md flex items-center gap-1.5">
              <span className="w-2 h-2 rounded-full bg-emerald-300 animate-pulse" />
              BÚSQUEDA ACTIVA
            </span>
          )}

          {/* Age / Minor Badge */}
          {report.is_minor ? (
            <span className="bg-red-600 text-white text-[11px] font-bold px-2.5 py-0.5 rounded-full shadow-sm flex items-center gap-1">
              <AlertCircle className="w-3 h-3" />
              MENOR DE EDAD ({report.age_at_disappearance} AÑOS)
            </span>
          ) : (
            <span className="bg-[#0F2A4A] text-white text-[11px] font-medium px-2.5 py-0.5 rounded-full shadow-sm">
              {report.age_at_disappearance} años
            </span>
          )}
        </div>

        <div className="absolute bottom-2 right-2 bg-slate-900/80 backdrop-blur-sm text-white text-[11px] font-mono px-2 py-0.5 rounded">
          {report.case_number}
        </div>
      </Link>

      {/* Card Content */}
      <div className="p-5 flex-1 flex flex-col justify-between">
        <div>
          <div className="flex items-center justify-between gap-2">
            <Link href={`/casos/${report.id}`} className="font-bold text-lg text-slate-900 group-hover:text-[#0D9488] transition">
              {report.first_name} {report.last_name}
            </Link>
          </div>

          <div className="mt-2 space-y-1.5 text-xs text-slate-600">
            <div className="flex items-center gap-1.5 font-medium text-slate-700">
              <MapPin className="w-3.5 h-3.5 text-[#0D9488] shrink-0" />
              <span>{report.municipality}, {report.department}</span>
            </div>
            <div className="flex items-center gap-1.5">
              <Calendar className="w-3.5 h-3.5 text-slate-400 shrink-0" />
              <span>{isClosed ? "Fecha del hecho" : "No localizado desde"}: {formattedDate}</span>
            </div>
          </div>

          <p className="mt-3 text-xs text-slate-600 line-clamp-2 leading-relaxed">
            {report.physical_description}
          </p>

          {(report as any).resolution_notes && (
            <div className="mt-2 text-[11px] text-emerald-800 bg-emerald-50 p-2 rounded border border-emerald-200">
              <strong>Estado:</strong> {(report as any).resolution_notes}
            </div>
          )}
        </div>

        {/* Actions */}
        <div className="mt-5 pt-3 border-t border-slate-100 flex items-center justify-between gap-2">
          <Link
            href={`/casos/${report.id}`}
            className="text-xs font-semibold text-[#0F2A4A] hover:text-[#0D9488] transition flex items-center gap-1"
          >
            Ver ficha completa
            <ChevronRight className="w-3.5 h-3.5" />
          </Link>

          {isClosed ? (
            <span className="text-xs font-semibold text-emerald-700 bg-emerald-50 border border-emerald-200 px-3 py-1.5 rounded-md flex items-center gap-1">
              <CheckCircle2 className="w-3.5 h-3.5 text-emerald-600" />
              Caso Concluido
            </span>
          ) : (
            <Link
              href={`/casos/${report.id}#pistas`}
              className="text-xs font-semibold bg-emerald-50 text-emerald-700 hover:bg-emerald-100 border border-emerald-200 px-3 py-1.5 rounded-md transition flex items-center gap-1"
            >
              <FileText className="w-3.5 h-3.5" />
              Aportar Pista
            </Link>
          )}
        </div>
      </div>
    </div>
  );
}
