/** Map FastAPI / Pydantic 422 `detail` to field keys for inline alerts. */

export function mapValidationDetail(detail: unknown): Record<string, string> {
  const out: Record<string, string> = {};
  if (!Array.isArray(detail)) {
    if (typeof detail === "string") {
      out._form = detail;
    }
    return out;
  }
  for (const item of detail) {
    if (typeof item !== "object" || item === null) continue;
    const loc = (item as { loc?: unknown }).loc;
    const msg = (item as { msg?: unknown }).msg;
    if (typeof msg !== "string") continue;
    const key = Array.isArray(loc)
      ? loc.filter((x) => typeof x === "string" && x !== "body").join(".")
      : "_form";
    out[key || "_form"] = msg;
  }
  return out;
}

/** Map API `loc` segments (e.g. `repo.url`) onto create-scan form field keys. */
export function mapApiValidationToFormFields(detail: unknown): Record<string, string> {
  const raw = mapValidationDetail(detail);
  const out: Record<string, string> = { ...raw };
  if (raw["repo.url"]) out.gitUrl = raw["repo.url"];
  if (raw["repo.ref"]) out.gitRef = raw["repo.ref"];
  if (raw["repo.storage_uri"]) out.storageUri = raw["repo.storage_uri"];
  if (raw["repo.clone_depth"]) out.cloneDepth = raw["repo.clone_depth"];
  if (raw["repo.sub_path"]) out.subPath = raw["repo.sub_path"];
  if (raw.policy_ids) out.policyIdsText = raw.policy_ids;
  return out;
}
