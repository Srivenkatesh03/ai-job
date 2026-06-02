"use client";

import React, { useState, useEffect } from "react";
import { useRouter } from "next/navigation";
import Link from "next/link";
import { useAuthStore } from "@/stores/authStore";
import { authService } from "@/services/auth.service";
import { UserPlus, Mail, Lock, User as UserIcon, ShieldAlert, Loader2, CheckCircle2 } from "lucide-react";

export default function RegisterPage() {
  const router = useRouter();
  const { isAuthenticated } = useAuthStore();

  const [fullName, setFullName] = useState("");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [loading, setLoading] = useState(false);
  const [errorMsg, setErrorMsg] = useState<string | null>(null);
  const [success, setSuccess] = useState(false);

  // Redirect if already authenticated
  useEffect(() => {
    if (isAuthenticated) {
      router.push("/dashboard");
    }
  }, [isAuthenticated, router]);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setErrorMsg(null);
    setLoading(true);

    try {
      const response = await authService.register({
        email,
        password,
        full_name: fullName,
      });

      if (response.success) {
        setSuccess(true);
        // Automatically redirect to login page after a brief delay
        setTimeout(() => {
          router.push("/login");
        }, 2000);
      } else {
        setErrorMsg(
          response.error?.message || "Registration failed. Please check your inputs."
        );
      }
    } catch (err: any) {
      setErrorMsg("An unexpected connection error occurred.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="relative min-h-screen flex items-center justify-center bg-[#07090e] overflow-hidden select-none px-4">
      {/* Decorative background glows */}
      <div className="absolute top-[-10%] right-[-10%] w-[50vw] h-[50vw] rounded-full bg-[radial-gradient(circle_at_center,rgba(99,102,241,0.08)_0,transparent_60%)] filter blur-3xl" />
      <div className="absolute bottom-[-10%] left-[-10%] w-[50vw] h-[50vw] rounded-full bg-[radial-gradient(circle_at_center,rgba(56,189,248,0.08)_0,transparent_60%)] filter blur-3xl" />

      {/* Register Card */}
      <div className="relative w-full max-w-md bg-[#0d121f]/60 backdrop-blur-xl border border-slate-800/80 rounded-2xl shadow-[0_8px_32px_0_rgba(0,0,0,0.37)] p-8 transition-all duration-300 hover:border-slate-700/80">
        <div className="flex flex-col items-center mb-8">
          <div className="p-3 bg-indigo-500/10 border border-indigo-500/20 rounded-xl mb-4 text-indigo-400">
            <UserPlus size={28} />
          </div>
          <h1 className="text-2xl font-bold tracking-tight text-white font-sans">
            Create Account
          </h1>
          <p className="text-sm text-slate-400 mt-1 font-sans">
            Get started with automated job applications
          </p>
        </div>

        {errorMsg && (
          <div className="flex items-start gap-3 p-3.5 bg-red-500/10 border border-red-500/20 rounded-xl mb-6 text-red-400 text-sm animate-shake">
            <ShieldAlert className="shrink-0 mt-0.5" size={16} />
            <div>
              <span className="font-semibold">Registration Failed:</span>
              <p className="mt-0.5 opacity-90">{errorMsg}</p>
            </div>
          </div>
        )}

        {success && (
          <div className="flex items-start gap-3 p-3.5 bg-emerald-500/10 border border-emerald-500/20 rounded-xl mb-6 text-emerald-400 text-sm">
            <CheckCircle2 className="shrink-0 mt-0.5 text-emerald-400" size={16} />
            <div>
              <span className="font-semibold">Success!</span>
              <p className="mt-0.5 opacity-90">Account created. Redirecting to login...</p>
            </div>
          </div>
        )}

        <form onSubmit={handleSubmit} className="space-y-5">
          {/* Full Name Input */}
          <div className="space-y-1.5">
            <label className="text-xs font-semibold text-slate-300 tracking-wide uppercase">
              Full Name
            </label>
            <div className="relative flex items-center">
              <UserIcon className="absolute left-3.5 text-slate-500" size={18} />
              <input
                type="text"
                required
                placeholder="John Doe"
                value={fullName}
                onChange={(e) => setFullName(e.target.value)}
                className="w-full pl-11 pr-4 py-3 bg-[#080b13]/80 border border-slate-800 rounded-xl text-slate-200 placeholder-slate-600 focus:outline-none focus:border-indigo-500/60 focus:ring-1 focus:ring-indigo-500/30 transition-all font-sans text-sm"
              />
            </div>
          </div>

          {/* Email Input */}
          <div className="space-y-1.5">
            <label className="text-xs font-semibold text-slate-300 tracking-wide uppercase">
              Email Address
            </label>
            <div className="relative flex items-center">
              <Mail className="absolute left-3.5 text-slate-500" size={18} />
              <input
                type="email"
                required
                placeholder="you@example.com"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                className="w-full pl-11 pr-4 py-3 bg-[#080b13]/80 border border-slate-800 rounded-xl text-slate-200 placeholder-slate-600 focus:outline-none focus:border-indigo-500/60 focus:ring-1 focus:ring-indigo-500/30 transition-all font-sans text-sm"
              />
            </div>
          </div>

          {/* Password Input */}
          <div className="space-y-1.5">
            <label className="text-xs font-semibold text-slate-300 tracking-wide uppercase">
              Password
            </label>
            <div className="relative flex items-center">
              <Lock className="absolute left-3.5 text-slate-500" size={18} />
              <input
                type="password"
                required
                placeholder="••••••••"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                className="w-full pl-11 pr-4 py-3 bg-[#080b13]/80 border border-slate-800 rounded-xl text-slate-200 placeholder-slate-600 focus:outline-none focus:border-indigo-500/60 focus:ring-1 focus:ring-indigo-500/30 transition-all font-sans text-sm"
              />
            </div>
          </div>

          <button
            type="submit"
            disabled={loading || success}
            className="relative w-full flex items-center justify-center gap-2 py-3 bg-gradient-to-r from-indigo-500 to-sky-600 hover:from-indigo-400 hover:to-sky-500 text-white font-medium rounded-xl transition-all shadow-[0_4px_14px_0_rgba(99,102,241,0.3)] hover:shadow-[0_6px_20px_0_rgba(99,102,241,0.4)] disabled:opacity-50 disabled:cursor-not-allowed select-none active:scale-[0.98]"
          >
            {loading ? (
              <Loader2 className="animate-spin" size={18} />
            ) : (
              <>
                Create Account
                <UserPlus size={16} />
              </>
            )}
          </button>
        </form>

        <div className="mt-8 text-center border-t border-slate-800/80 pt-6">
          <p className="text-sm text-slate-400">
            Already have an account?{" "}
            <Link href="/login" className="text-indigo-400 hover:text-indigo-300 font-semibold transition-colors">
              Sign In
            </Link>
          </p>
        </div>
      </div>
    </div>
  );
}
