"use client";

import Link from "next/link";
import { useState, useEffect } from "react";
import { Search, MapPin, PlusCircle, Shield, FileText, User as UserIcon, LogOut, Menu, X } from "lucide-react";

export default function Navbar() {
  const [session, setSession] = useState<{ full_name: string; role: string } | null>(null);
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false);

  useEffect(() => {
    const raw = localStorage.getItem("encuentrame_session");
    if (raw) {
      try {
        setSession(JSON.parse(raw));
      } catch (e) {}
    }
  }, []);

  const handleLogout = () => {
    localStorage.removeItem("encuentrame_session");
    setSession(null);
    window.location.href = "/";
  };

  return (
    <header className="sticky top-0 z-50 bg-[#0F2A4A] text-white shadow-md border-b border-slate-700">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex items-center justify-between h-16">
          {/* Logo & Slogan */}
          <Link href="/" className="flex items-center space-x-3 group">
            <div className="w-10 h-10 rounded-lg bg-[#0D9488] flex items-center justify-center text-white font-bold text-xl shadow-inner">
              EN
            </div>
            <div>
              <span className="font-extrabold text-lg tracking-tight block group-hover:text-[#14B8A6] transition">
                ENCUÉNTRAME NICARAGUA
              </span>
              <span className="text-xs text-slate-300 block -mt-1 font-light tracking-wide">
                Cada persona importa
              </span>
            </div>
          </Link>

          {/* Desktop Nav */}
          <nav className="hidden md:flex items-center space-x-1 lg:space-x-4">
            <Link
              href="/"
              className="px-3 py-2 rounded-md text-sm font-medium text-slate-200 hover:text-white hover:bg-slate-800 transition"
            >
              Inicio
            </Link>
            <Link
              href="/casos.html"
              className="px-3 py-2 rounded-md text-sm font-medium text-slate-200 hover:text-white hover:bg-slate-800 transition flex items-center gap-1.5"
            >
              <Search className="w-4 h-4 text-[#14B8A6]" />
              Catálogo de Casos
            </Link>
            <Link
              href="/mapa.html"
              className="px-3 py-2 rounded-md text-sm font-medium text-slate-200 hover:text-white hover:bg-slate-800 transition flex items-center gap-1.5"
            >
              <MapPin className="w-4 h-4 text-[#14B8A6]" />
              Mapa Nacional
            </Link>
            <Link
              href="/pistas.html"
              className="px-3 py-2 rounded-md text-sm font-medium text-slate-200 hover:text-white hover:bg-slate-800 transition flex items-center gap-1.5"
            >
              <FileText className="w-4 h-4 text-[#14B8A6]" />
              Aportar Pista
            </Link>
            <Link
              href="/reportar.html"
              className="px-3.5 py-2 rounded-md text-sm font-semibold bg-[#0D9488] text-white hover:bg-[#0f766e] transition flex items-center gap-1.5 shadow-sm"
            >
              <PlusCircle className="w-4 h-4" />
              Reportar Caso
            </Link>

            {/* Admin/Moderator Link */}
            {session && (session.role === "admin" || session.role === "moderator") && (
              <Link
                href="/admin.html"
                className="px-3 py-2 rounded-md text-sm font-medium bg-amber-600/30 text-amber-300 hover:bg-amber-600/50 transition flex items-center gap-1.5 border border-amber-500/40"
              >
                <Shield className="w-4 h-4" />
                Moderación
              </Link>
            )}

            {/* Auth Actions */}
            {session ? (
              <div className="flex items-center space-x-2 pl-2 border-l border-slate-700">
                <span className="text-xs text-slate-300 font-medium hidden lg:inline">
                  {session.full_name.split(" ")[0]}
                </span>
                <button
                  onClick={handleLogout}
                  title="Cerrar Sesión"
                  className="p-2 text-slate-300 hover:text-red-400 hover:bg-slate-800 rounded-md transition"
                >
                  <LogOut className="w-4 h-4" />
                </button>
              </div>
            ) : (
              <Link
                href="/login.html"
                className="px-3 py-2 text-sm font-medium text-slate-300 hover:text-white transition flex items-center gap-1"
              >
                <UserIcon className="w-4 h-4" />
                Ingresar
              </Link>
            )}
          </nav>

          {/* Mobile menu button */}
          <div className="md:hidden flex items-center">
            <button
              onClick={() => setMobileMenuOpen(!mobileMenuOpen)}
              className="p-2 rounded-md text-slate-300 hover:text-white hover:bg-slate-800"
            >
              {mobileMenuOpen ? <X className="w-6 h-6" /> : <Menu className="w-6 h-6" />}
            </button>
          </div>
        </div>
      </div>

      {/* Mobile Menu */}
      {mobileMenuOpen && (
        <div className="md:hidden bg-[#0A192F] border-b border-slate-700 px-4 pt-2 pb-4 space-y-1">
          <Link
            href="/"
            onClick={() => setMobileMenuOpen(false)}
            className="block px-3 py-2 rounded-md text-base font-medium text-slate-200 hover:bg-slate-800"
          >
            Inicio
          </Link>
          <Link
            href="/casos.html"
            onClick={() => setMobileMenuOpen(false)}
            className="block px-3 py-2 rounded-md text-base font-medium text-slate-200 hover:bg-slate-800"
          >
            Catálogo de Casos
          </Link>
          <Link
            href="/mapa.html"
            onClick={() => setMobileMenuOpen(false)}
            className="block px-3 py-2 rounded-md text-base font-medium text-slate-200 hover:bg-slate-800"
          >
            Mapa Nacional
          </Link>
          <Link
            href="/pistas.html"
            onClick={() => setMobileMenuOpen(false)}
            className="block px-3 py-2 rounded-md text-base font-medium text-slate-200 hover:bg-slate-800"
          >
            Aportar Pista Confidencial
          </Link>
          <Link
            href="/reportar.html"
            onClick={() => setMobileMenuOpen(false)}
            className="block px-3 py-2 rounded-md text-base font-semibold bg-[#0D9488] text-white"
          >
            Reportar Desaparición
          </Link>
          {session && (session.role === "admin" || session.role === "moderator") && (
            <Link
              href="/admin.html"
              onClick={() => setMobileMenuOpen(false)}
              className="block px-3 py-2 rounded-md text-base font-medium text-amber-300 bg-amber-950/40"
            >
              Panel de Moderación
            </Link>
          )}
          {session ? (
            <button
              onClick={() => {
                handleLogout();
                setMobileMenuOpen(false);
              }}
              className="w-full text-left px-3 py-2 rounded-md text-base font-medium text-red-300 hover:bg-slate-800"
            >
              Cerrar Sesión ({session.full_name})
            </button>
          ) : (
            <Link
              href="/login.html"
              onClick={() => setMobileMenuOpen(false)}
              className="block px-3 py-2 rounded-md text-base font-medium text-slate-200 hover:bg-slate-800"
            >
              Iniciar Sesión
            </Link>
          )}
        </div>
      )}
    </header>
  );
}
