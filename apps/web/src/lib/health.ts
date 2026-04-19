/** Health check without API key (US-DG-14-002). */

export async function fetchHealthz(
  baseUrl: string
): Promise<{ ok: boolean; status: number; ms: number }> {
  const base = baseUrl.replace(/\/$/, "");
  const t0 = performance.now();
  const res = await fetch(`${base}/v1/healthz`, { method: "GET" });
  const ms = Math.round(performance.now() - t0);
  return { ok: res.ok, status: res.status, ms };
}
