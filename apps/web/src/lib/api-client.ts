"use client";

import type { ConnectionSettings } from "./connection-settings";

export class ApiError extends Error {
  constructor(
    message: string,
    public status: number,
    public body?: unknown
  ) {
    super(message);
    this.name = "ApiError";
  }
}

function authHeaders(s: ConnectionSettings): HeadersInit {
  const key = s.apiKey.trim();
  if (!key) return {};
  if (s.authKind === "bearer") {
    return { Authorization: `Bearer ${key}` };
  }
  return { "X-API-Key": key };
}

export async function apiFetch(
  s: ConnectionSettings,
  path: string,
  init: RequestInit = {}
): Promise<Response> {
  const base = s.baseUrl.replace(/\/$/, "");
  const url = `${base}${path.startsWith("/") ? path : `/${path}`}`;
  const headers = new Headers(init.headers);
  const auth = authHeaders(s);
  for (const [k, v] of Object.entries(auth)) {
    headers.set(k, v);
  }
  if (init.body && !headers.has("Content-Type")) {
    headers.set("Content-Type", "application/json");
  }
  return fetch(url, { ...init, headers });
}

export async function parseJson<T>(res: Response): Promise<T> {
  const text = await res.text();
  if (!text) return {} as T;
  try {
    return JSON.parse(text) as T;
  } catch {
    return text as unknown as T;
  }
}
