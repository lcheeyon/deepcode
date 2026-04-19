"use client";

import { CreateScanForm } from "@/components/create-scan-form";

export default function NewScanPage() {
  return (
    <div>
      <h1 className="mb-6 text-[22px] font-semibold tracking-tight">New scan</h1>
      <CreateScanForm />
    </div>
  );
}
