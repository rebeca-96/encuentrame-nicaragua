import Link from "next/link";
import { Phone, ShieldAlert, Heart, FileCheck } from "lucide-react";

export default function Footer() {
  return (
    <footer className="bg-[#0A192F] text-slate-300 mt-auto border-t border-slate-800 text-sm">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
        <div className="grid grid-cols-1 md:grid-cols-4 gap-8">
          {/* Column 1: Misión */}
          <div className="space-y-3">
            <div className="flex items-center space-x-2">
              <span className="w-8 h-8 rounded bg-[#0D9488] text-white flex items-center justify-center font-bold text-sm">
                EN
              </span>
              <span className="font-bold text-white tracking-tight">
                ENCUÉNTRAME NICARAGUA
              </span>
            </div>
            <p className="text-xs text-slate-400 leading-relaxed">
              Plataforma cívica e inteligente para la centralización, difusión verificada
              y reunificación familiar de personas no localizadas en el territorio nacional.
            </p>
            <div className="flex items-center gap-1.5 text-xs text-emerald-400 pt-1">
              <Heart className="w-3.5 h-3.5" />
              <span>Cada persona importa.</span>
            </div>
          </div>

          {/* Column 2: Canales de Emergencia Oficiales */}
          <div className="space-y-3">
            <h4 className="font-semibold text-white text-xs uppercase tracking-wider flex items-center gap-1.5">
              <Phone className="w-3.5 h-3.5 text-[#14B8A6]" />
              Líneas Oficiales de Auxilio
            </h4>
            <ul className="space-y-2 text-xs">
              <li className="flex justify-between py-1 border-b border-slate-800">
                <span className="text-slate-400">Policía Nacional:</span>
                <span className="font-bold text-white">118</span>
              </li>
              <li className="flex justify-between py-1 border-b border-slate-800">
                <span className="text-slate-400">Ministerio de la Familia:</span>
                <span className="font-bold text-white">133</span>
              </li>
              <li className="flex justify-between py-1 border-b border-slate-800">
                <span className="text-slate-400">Bomberos Unidos de Nicaragua:</span>
                <span className="font-bold text-white">115 / 911</span>
              </li>
              <li className="flex justify-between py-1">
                <span className="text-slate-400">Cruz Blanca Nicaragüense:</span>
                <span className="font-bold text-white">128</span>
              </li>
            </ul>
          </div>

          {/* Column 3: Enlaces y Navegación */}
          <div className="space-y-3">
            <h4 className="font-semibold text-white text-xs uppercase tracking-wider">
              Navegación Cívica
            </h4>
            <ul className="space-y-1.5 text-xs text-slate-400">
              <li>
                <Link href="/casos.html" className="hover:text-white transition">
                  Catálogo de Casos Activos
                </Link>
              </li>
              <li>
                <Link href="/mapa.html" className="hover:text-white transition">
                  Mapa Geográfico Departamental
                </Link>
              </li>
              <li>
                <Link href="/reportar.html" className="hover:text-white transition">
                  Registrar Reporte de Búsqueda
                </Link>
              </li>
              <li>
                <Link href="/pistas.html" className="hover:text-white transition">
                  Aportar Información Confidencial
                </Link>
              </li>
            </ul>
          </div>

          {/* Column 4: Marco Ético y Legal */}
          <div className="space-y-3">
            <h4 className="font-semibold text-white text-xs uppercase tracking-wider flex items-center gap-1.5">
              <ShieldAlert className="w-3.5 h-3.5 text-amber-400" />
              Marco Legal y Privacidad
            </h4>
            <p className="text-xs text-slate-400 leading-relaxed">
              Cumplimiento con la <strong>Ley N.° 787 de Protección de Datos Personales</strong> y el Código de la Niñez y la Adolescencia de Nicaragua.
            </p>
            <div className="bg-slate-800/80 p-2.5 rounded border border-slate-700/60 text-[11px] text-slate-300">
              Esta plataforma es una herramienta ciudadana y no reemplaza la formalización de denuncias ante las autoridades policiales o judiciales.
            </div>
          </div>
        </div>

        {/* Bottom bar */}
        <div className="pt-8 mt-8 border-t border-slate-800 text-center text-xs text-slate-400">
          <p>© {new Date().getFullYear()} ENCUÉNTRAME NICARAGUA. Proyecto de Innovación Social y Tecnológica.</p>
        </div>
      </div>
    </footer>
  );
}
