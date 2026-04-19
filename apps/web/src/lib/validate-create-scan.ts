/**
 * Client-side validation aligned with deepguard_core CreateScanRequest / RepoSpec.
 */

export type RepoSource = "git" | "archive";

export interface CloudProfileForm {
  profile_id: string;
  provider: string;
  connector_credential_ref: string;
  regionsText: string;
}

export interface CreateScanFormState {
  repoSource: RepoSource;
  gitUrl: string;
  gitRef: string;
  cloneDepth: string;
  subPath: string;
  storageUri: string;
  checksumSha256: string;
  policyIdsText: string;
  layerCode: boolean;
  layerIac: boolean;
  layerCloud: boolean;
  cloudProfiles: CloudProfileForm[];
  webhookUrl: string;
  webhookEvents: { completed: boolean; failed: boolean };
  budgetMaxUsd: string;
  budgetWallSec: string;
  idempotencyKey: string;
}

export const defaultCreateScanForm = (): CreateScanFormState => ({
  repoSource: "git",
  gitUrl: "https://github.com/octocat/Hello-World",
  gitRef: "main",
  cloneDepth: "",
  subPath: "",
  storageUri: "",
  checksumSha256: "",
  policyIdsText: "ISO-27001-2022",
  layerCode: true,
  layerIac: false,
  layerCloud: false,
  cloudProfiles: [],
  webhookUrl: "",
  webhookEvents: { completed: true, failed: false },
  budgetMaxUsd: "",
  budgetWallSec: "",
  idempotencyKey: "",
});

export type FieldErrors = Record<string, string>;

function parsePolicyIds(text: string): string[] {
  return text
    .split(/[,;\n]+/)
    .map((s) => s.trim())
    .filter(Boolean);
}

function parseRegions(text: string): string[] {
  return text
    .split(/[,;\s]+/)
    .map((s) => s.trim())
    .filter(Boolean);
}

export function validateCreateScanForm(f: CreateScanFormState): {
  ok: boolean;
  errors: FieldErrors;
  payload?: Record<string, unknown>;
} {
  const errors: FieldErrors = {};
  const policy_ids = parsePolicyIds(f.policyIdsText);
  if (policy_ids.length < 1) {
    errors.policyIdsText = "Enter at least one policy id.";
  }

  if (!f.layerCode && !f.layerIac && !f.layerCloud) {
    errors.scan_layers = "Select at least one scan layer.";
  }

  const scan_layers = {
    code: f.layerCode,
    iac: f.layerIac,
    cloud: f.layerCloud,
  };

  let repo: Record<string, unknown> | null = null;
  const cloud_profiles = f.cloudProfiles
    .filter(
      (c) =>
        c.profile_id.trim() &&
        c.provider.trim() &&
        c.connector_credential_ref.trim() &&
        c.regionsText.trim()
    )
    .map((c) => ({
      profile_id: c.profile_id.trim(),
      provider: c.provider.trim(),
      connector_credential_ref: c.connector_credential_ref.trim(),
      regions: parseRegions(c.regionsText),
    }));

  for (let i = 0; i < f.cloudProfiles.length; i++) {
    const c = f.cloudProfiles[i];
    if (!c.profile_id.trim() && !c.provider && !c.connector_credential_ref && !c.regionsText)
      continue;
    const r = parseRegions(c.regionsText);
    if (!c.profile_id.trim()) errors[`cloud_${i}_profile_id`] = "Required.";
    if (!c.provider.trim()) errors[`cloud_${i}_provider`] = "Required.";
    if (!c.connector_credential_ref.trim())
      errors[`cloud_${i}_connector`] = "Required.";
    if (r.length < 1) errors[`cloud_${i}_regions`] = "At least one region.";
  }

  if (f.repoSource === "git") {
    const url = f.gitUrl.trim();
    if (!url) errors.gitUrl = "Repo URL is required for Git source.";
    if (f.storageUri.trim()) {
      errors.storageUri = "Clear storage URI when using Git source.";
    }
    if (url) {
      try {
        // eslint-disable-next-line no-new -- validate URL
        new URL(url);
      } catch {
        errors.gitUrl = "Enter a valid HTTP(S) URL.";
      }
    }
    const ref = f.gitRef.trim();
    if (!ref) errors.gitRef = "Ref is required.";
    if (f.subPath.trim()) {
      const sp = f.subPath.trim().replace(/\\/g, "/");
      if (sp.startsWith("/")) errors.subPath = "Sub-path must be relative.";
      if (sp.split("/").includes("..")) errors.subPath = "Sub-path must not contain '..'.";
    }
    let clone_depth: number | undefined;
    if (f.cloneDepth.trim()) {
      const n = Number(f.cloneDepth);
      if (!Number.isFinite(n) || n < 1 || n > 10_000) {
        errors.cloneDepth = "Clone depth must be between 1 and 10000.";
      } else {
        clone_depth = n;
      }
    }
    if (Object.keys(errors).length === 0 && url && ref) {
      repo = {
        source: "git",
        url,
        ref,
        ...(clone_depth !== undefined ? { clone_depth } : {}),
        ...(f.subPath.trim() ? { sub_path: f.subPath.trim() } : {}),
        ...(f.checksumSha256.trim()
          ? { checksum_sha256: f.checksumSha256.trim() }
          : {}),
      };
    }
  } else {
    const su = f.storageUri.trim();
    if (!su.startsWith("s3://")) {
      errors.storageUri = "Archive requires storage_uri starting with s3://.";
    }
    if (f.gitUrl.trim()) {
      errors.gitUrl = "Clear repo URL when using Archive source.";
    }
    if (Object.keys(errors).length === 0 && su.startsWith("s3://")) {
      repo = {
        source: "archive",
        storage_uri: su,
        ...(f.checksumSha256.trim()
          ? { checksum_sha256: f.checksumSha256.trim() }
          : {}),
      };
    }
  }

  const repoOk = repo !== null;
  const profilesOk = cloud_profiles.length > 0;

  if (f.layerCloud && !repoOk && !profilesOk) {
    errors.scan_layers =
      "Cloud layer requires a repo and/or at least one cloud profile (see Architecture §28.4).";
  }
  if ((f.layerCode || f.layerIac) && !repoOk) {
    errors.repo =
      "Code or IaC layer requires a valid Git or archive repo configuration.";
  }

  let notifications: Record<string, unknown> | undefined;
  if (f.webhookUrl.trim()) {
    const on: string[] = [];
    if (f.webhookEvents.completed) on.push("completed");
    if (f.webhookEvents.failed) on.push("failed");
    if (on.length < 1) {
      errors.webhookUrl = "Pick at least one webhook event.";
    } else {
      try {
        // eslint-disable-next-line no-new
        new URL(f.webhookUrl.trim());
        notifications = { webhook_url: f.webhookUrl.trim(), on };
      } catch {
        errors.webhookUrl = "Enter a valid webhook URL.";
      }
    }
  }

  let budget: Record<string, unknown> | undefined;
  if (f.budgetMaxUsd.trim() || f.budgetWallSec.trim()) {
    const max_llm_usd = f.budgetMaxUsd.trim()
      ? Number(f.budgetMaxUsd)
      : undefined;
    const max_wall_seconds = f.budgetWallSec.trim()
      ? Number(f.budgetWallSec)
      : undefined;
    if (max_llm_usd !== undefined) {
      if (!Number.isFinite(max_llm_usd) || max_llm_usd <= 0) {
        errors.budgetMaxUsd = "Must be a positive number.";
      }
    }
    if (max_wall_seconds !== undefined) {
      if (!Number.isFinite(max_wall_seconds) || max_wall_seconds <= 0) {
        errors.budgetWallSec = "Must be a positive integer.";
      }
    }
    if (!errors.budgetMaxUsd && !errors.budgetWallSec) {
      budget = {};
      if (max_llm_usd !== undefined) budget.max_llm_usd = max_llm_usd;
      if (max_wall_seconds !== undefined) budget.max_wall_seconds = max_wall_seconds;
      if (Object.keys(budget).length === 0) budget = undefined;
    }
  }

  const ok = Object.keys(errors).length === 0;
  if (!ok || !policy_ids.length) {
    return { ok: false, errors };
  }

  const payload: Record<string, unknown> = {
    policy_ids,
    scan_layers,
    cloud_profiles,
    ...(repo ? { repo } : {}),
    ...(notifications ? { notifications } : {}),
    ...(budget ? { budget } : {}),
  };

  return { ok: true, errors: {}, payload };
}
