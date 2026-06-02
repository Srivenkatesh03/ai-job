"use client";

import { useEffect } from "react";
import { useRouter } from "next/navigation";
import { Loader2 } from "lucide-react";

export default function RootPage() {
  const router = useRouter();

  useEffect(() => {
    router.push("/login");
  }, [router]);

  return (
    <div className="min-h-screen flex items-center justify-center bg-[#07090e] select-none text-sky-400">
      <div className="flex flex-col items-center gap-4">
        <Loader2 className="animate-spin text-sky-500" size={36} />
        <p className="text-sm font-semibold tracking-wide text-slate-400 font-sans">
          Routing Secure Connection...
        </p>
      </div>
    </div>
  );
}
