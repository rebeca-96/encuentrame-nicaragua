"use client";

import { useState } from "react";
import Link from "next/link";
import { Lock, Mail, User, Shield, AlertCircle, ArrowRight, UserPlus, CheckCircle2 } from "lucide-react";
import { loginUser, registerUser } from "../../lib/api";

export default function LoginPage() {
  const [isRegisterMode, setIsRegisterMode] = useState(false);
  
  // Login fields
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  
  // Register fields
  const [fullName, setFullName] = useState("");
  const [confirmPassword, setConfirmPassword] = useState("");
  const [phoneNumber, setPhoneNumber] = useState("");

  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [successMessage, setSuccessMessage] = useState<string | null>(null);

  const handleLogin = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setError(null);

    try {
      const data = await loginUser(email, password);
      localStorage.setItem(
        "encuentrame_session",
        JSON.stringify({
          access_token: data.access_token,
          user_id: data.user_id,
          role: data.role,
          full_name: data.full_name,
        })
      );

      if (data.role === "admin" || data.role === "moderator") {
        window.location.href = "/admin";
      } else {
        window.location.href = "/reportar";
      }
    } catch (err: any) {
      setError(err.message || "Error al iniciar sesión");
    } finally {
      setLoading(false);
    }
  };

  const handleRegister = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setError(null);
    setSuccessMessage(null);

    if (password !== confirmPassword) {
      setError("Las contraseñas no coinciden.");
      setLoading(false);
      return;
    }

    try {
      await registerUser({
        email: email.trim(),
        password: password,
        confirm_password: confirmPassword,
        full_name: fullName.trim(),
        phone_number: phoneNumber.trim() || undefined,
        role: "reporter"
      });

      setSuccessMessage("¡Cuenta creada exitosamente! Ya puede iniciar sesión.");
      setIsRegisterMode(false);
      setPassword("");
      setConfirmPassword("");
    } catch (err: any) {
      setError(err.message || "Error al registrar la cuenta");
    } finally {
      setLoading(false);
    }
  };

  // Quick Demo Fill
  const fillCredentials = (userEmail: string, pass: string) => {
    setIsRegisterMode(false);
    setEmail(userEmail);
    setPassword(pass);
  };

  return (
    <div className="max-w-md mx-auto px-4 py-12 space-y-6">
      <div className="text-center space-y-2">
        <div className="w-12 h-12 bg-[#0F2A4A] text-white rounded-xl flex items-center justify-center font-bold text-lg mx-auto shadow-md">
          EN
        </div>
        <h1 className="text-2xl font-extrabold text-slate-900">
          {isRegisterMode ? "Crear Cuenta de Reportante" : "Iniciar Sesión"}
        </h1>
        <p className="text-xs text-slate-500">
          {isRegisterMode
            ? "Regístrese para gestionar reportes con respaldo y seguimiento seguro"
            : "Acceso protegido para reportantes y equipo de moderación"}
        </p>
      </div>

      {/* Mode Switch Tabs */}
      <div className="flex bg-slate-200 p-1 rounded-xl text-xs font-semibold">
        <button
          type="button"
          onClick={() => { setIsRegisterMode(false); setError(null); }}
          className={`w-1/2 py-2 rounded-lg transition ${!isRegisterMode ? "bg-white text-slate-900 shadow-sm" : "text-slate-600 hover:text-slate-900"}`}
        >
          Iniciar Sesión
        </button>
        <button
          type="button"
          onClick={() => { setIsRegisterMode(true); setError(null); }}
          className={`w-1/2 py-2 rounded-lg transition ${isRegisterMode ? "bg-white text-slate-900 shadow-sm" : "text-slate-600 hover:text-slate-900"}`}
        >
          Registrarse
        </button>
      </div>

      <div className="bg-white p-6 sm:p-8 rounded-2xl shadow-sm border border-slate-200 space-y-6">
        {error && (
          <div className="bg-red-50 border border-red-200 rounded-xl p-3 text-xs text-red-700 flex items-center gap-2">
            <AlertCircle className="w-4 h-4 shrink-0" />
            <span>{error}</span>
          </div>
        )}

        {successMessage && (
          <div className="bg-emerald-50 border border-emerald-200 rounded-xl p-3 text-xs text-emerald-700 flex items-center gap-2">
            <CheckCircle2 className="w-4 h-4 shrink-0" />
            <span>{successMessage}</span>
          </div>
        )}

        {!isRegisterMode ? (
          /* LOGIN FORM */
          <form onSubmit={handleLogin} className="space-y-4">
            <div>
              <label htmlFor="login-email" className="block text-xs font-semibold text-slate-700 mb-1">
                Correo Electrónico:
              </label>
              <div className="flex items-center gap-2 px-3 py-2 bg-slate-50 rounded-lg border border-slate-200">
                <Mail className="w-4 h-4 text-slate-400 shrink-0" />
                <input
                  id="login-email"
                  type="email"
                  required
                  value={email}
                  onChange={(e) => setEmail(e.target.value)}
                  placeholder="usuario@encuentrame.ni"
                  className="w-full bg-transparent text-xs text-slate-900 focus:outline-none"
                />
              </div>
            </div>

            <div>
              <label htmlFor="login-password" className="block text-xs font-semibold text-slate-700 mb-1">
                Contraseña:
              </label>
              <div className="flex items-center gap-2 px-3 py-2 bg-slate-50 rounded-lg border border-slate-200">
                <Lock className="w-4 h-4 text-slate-400 shrink-0" />
                <input
                  id="login-password"
                  type="password"
                  required
                  value={password}
                  onChange={(e) => setPassword(e.target.value)}
                  placeholder="••••••••••••"
                  className="w-full bg-transparent text-xs text-slate-900 focus:outline-none"
                />
              </div>
            </div>

            <button
              type="submit"
              disabled={loading}
              className="w-full bg-[#0D9488] hover:bg-[#0f766e] disabled:opacity-50 text-white font-semibold text-xs py-2.5 rounded-lg transition flex items-center justify-center gap-1.5 shadow"
            >
              {loading ? "Verificando..." : "Ingresar a la Plataforma"}
              <ArrowRight className="w-3.5 h-3.5" />
            </button>
          </form>
        ) : (
          /* REGISTER FORM */
          <form onSubmit={handleRegister} className="space-y-3.5">
            <div>
              <label htmlFor="reg-fullname" className="block text-xs font-semibold text-slate-700 mb-1">
                Nombre y Apellidos Completos: *
              </label>
              <div className="flex items-center gap-2 px-3 py-2 bg-slate-50 rounded-lg border border-slate-200">
                <User className="w-4 h-4 text-slate-400 shrink-0" />
                <input
                  id="reg-fullname"
                  type="text"
                  required
                  value={fullName}
                  onChange={(e) => setFullName(e.target.value)}
                  placeholder="Ej. María Teresa Castillo"
                  className="w-full bg-transparent text-xs text-slate-900 focus:outline-none"
                />
              </div>
            </div>

            <div>
              <label htmlFor="reg-email" className="block text-xs font-semibold text-slate-700 mb-1">
                Correo Electrónico: *
              </label>
              <div className="flex items-center gap-2 px-3 py-2 bg-slate-50 rounded-lg border border-slate-200">
                <Mail className="w-4 h-4 text-slate-400 shrink-0" />
                <input
                  id="reg-email"
                  type="email"
                  required
                  value={email}
                  onChange={(e) => setEmail(e.target.value)}
                  placeholder="maria@ejemplo.ni"
                  className="w-full bg-transparent text-xs text-slate-900 focus:outline-none"
                />
              </div>
            </div>

            <div>
              <label htmlFor="reg-phone" className="block text-xs font-semibold text-slate-700 mb-1">
                Teléfono de Contacto (Opcional):
              </label>
              <input
                id="reg-phone"
                type="text"
                value={phoneNumber}
                onChange={(e) => setPhoneNumber(e.target.value)}
                placeholder="Ej. 8888-0000"
                className="w-full p-2 bg-slate-50 border border-slate-200 rounded-lg text-xs"
              />
            </div>

            <div>
              <label htmlFor="reg-password" className="block text-xs font-semibold text-slate-700 mb-1">
                Contraseña Robusta: *
              </label>
              <div className="flex items-center gap-2 px-3 py-2 bg-slate-50 rounded-lg border border-slate-200">
                <Lock className="w-4 h-4 text-slate-400 shrink-0" />
                <input
                  id="reg-password"
                  type="password"
                  required
                  value={password}
                  onChange={(e) => setPassword(e.target.value)}
                  placeholder="Mín. 8 caracteres (Mayús, núm y símbolo)"
                  className="w-full bg-transparent text-xs text-slate-900 focus:outline-none"
                />
              </div>
              {/* Real-time complexity hints */}
              <div className="grid grid-cols-2 gap-1 mt-1.5 text-[10px] text-slate-500">
                <span className={password.length >= 8 ? "text-emerald-600 font-semibold" : ""}>
                  • Mínimo 8 caracteres
                </span>
                <span className={/[A-Z]/.test(password) ? "text-emerald-600 font-semibold" : ""}>
                  • Al menos una mayúscula
                </span>
                <span className={/[0-9]/.test(password) ? "text-emerald-600 font-semibold" : ""}>
                  • Al menos un número
                </span>
                <span className={/[@$!%*?&#_.:,;-]/.test(password) ? "text-emerald-600 font-semibold" : ""}>
                  • Al menos un símbolo (@$!%*?&#_.:,;-)
                </span>
              </div>
            </div>

            <div>
              <label htmlFor="reg-confirm-password" className="block text-xs font-semibold text-slate-700 mb-1">
                Confirmar Contraseña: *
              </label>
              <div className="flex items-center gap-2 px-3 py-2 bg-slate-50 rounded-lg border border-slate-200">
                <Lock className="w-4 h-4 text-slate-400 shrink-0" />
                <input
                  id="reg-confirm-password"
                  type="password"
                  required
                  value={confirmPassword}
                  onChange={(e) => setConfirmPassword(e.target.value)}
                  placeholder="Repita la contraseña"
                  className="w-full bg-transparent text-xs text-slate-900 focus:outline-none"
                />
              </div>
            </div>

            <button
              type="submit"
              disabled={loading}
              className="w-full bg-[#0F2A4A] hover:bg-slate-800 disabled:opacity-50 text-white font-semibold text-xs py-2.5 rounded-lg transition flex items-center justify-center gap-1.5 shadow"
            >
              <UserPlus className="w-3.5 h-3.5" />
              {loading ? "Creando cuenta..." : "Registrar Cuenta"}
            </button>
          </form>
        )}

        {/* Demo Fast Fill Buttons for Testing */}
        <div className="pt-4 border-t border-slate-100 space-y-2">
          <span className="text-[11px] font-bold text-slate-600 block uppercase tracking-wider text-center">
            Accesos de Demostración Rápida:
          </span>
          <div className="grid grid-cols-2 gap-2 text-[11px]">
            <button
              type="button"
              onClick={() => fillCredentials("moderador@encuentrame.ni", "ModPass2026!")}
              className="p-2 rounded-lg bg-amber-50 hover:bg-amber-100 text-amber-800 border border-amber-200 font-semibold transition"
            >
              🛡️ Moderador
            </button>
            <button
              type="button"
              onClick={() => fillCredentials("admin@encuentrame.ni", "AdminPass2026!")}
              className="p-2 rounded-lg bg-blue-50 hover:bg-blue-100 text-[#0F2A4A] border border-blue-200 font-semibold transition"
            >
              👑 Administrador
            </button>
            <button
              type="button"
              onClick={() => fillCredentials("reportante@encuentrame.ni", "ReportPass2026!")}
              className="p-2 rounded-lg bg-teal-50 hover:bg-teal-100 text-teal-800 border border-teal-200 font-semibold transition col-span-2"
            >
              📝 Reportante Familiar
            </button>
          </div>
        </div>
      </div>
    </div>
  );
}
