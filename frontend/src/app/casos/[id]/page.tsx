import CasoDetailClient from "./CasoDetailClient";
import { OFFICIAL_SEED_REPORTS } from "../../../lib/catalogData";

export async function generateStaticParams() {
  const ids = new Set<string>();
  
  // Agregar IDs y números de caso de todos los reportes semilla
  OFFICIAL_SEED_REPORTS.forEach((report) => {
    ids.add(report.id);
    ids.add(report.case_number);
  });
  
  // Agregar IDs comunes y placeholder
  ids.add("placeholder");
  for (let i = 1; i <= 25; i++) {
    ids.add(`case-${String(i).padStart(2, "0")}`);
    ids.add(`EN-2026-${String(i).padStart(4, "0")}`);
  }

  return Array.from(ids).map((id) => ({ id }));
}

export default function CasoDetailPage() {
  return <CasoDetailClient />;
}
