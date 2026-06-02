"use client";

import React, { useEffect, useState } from "react";
import { useRouter } from "next/navigation";
import { useAuthStore } from "@/stores/authStore";
import { Sidebar } from "@/components/dashboard/Sidebar";
import { Header } from "@/components/dashboard/Header";
import { Loader2 } from "lucide-react";

export default function DashboardLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  const router = useRouter();
  const { isAuthenticated } = useAuthStore();
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    if (!isAuthenticated) {
      router.push("/login");
    } else {
      setLoading(false);
    }
  }, [isAuthenticated, router]);

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-[#07090e] text-sky-400 select-none">
        <div className="flex flex-col items-center gap-4">
          <Loader2 className="animate-spin text-sky-500" size={36} />
          <p className="text-sm font-semibold tracking-wide text-slate-400 font-sans">
            Securing Connection...
          </p>
        </div>
      </div>
    );
  }

  return (
    <div className="flex h-screen bg-[#07090e] overflow-hidden text-slate-100 font-sans select-none">
      {/* Responsive Sidebar */}
      <Sidebar />

      {/* Main Panel */}
      <div className="flex-1 flex flex-col overflow-hidden">
        {/* Top Header */}
        <Header />

        {/* Scrollable Viewport */}
        <main className="flex-1 overflow-y-auto bg-[#090d16] p-6 lg:p-8">
          {children}
        </main>
      </div>
    </div>
  );
}
