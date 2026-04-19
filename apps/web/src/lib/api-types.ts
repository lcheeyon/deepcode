export interface ScanResponse {
  scan_id: string;
  tenant_id: string;
  status: string;
  current_stage: string;
  percent_complete: number;
  job_config: Record<string, unknown>;
  created_at: string;
  updated_at: string;
  idempotency_key?: string | null;
  repo_commit_sha?: string | null;
  cancellation_requested: boolean;
}

export interface PrepareRepoUploadResponse {
  upload_id: string;
  upload_url: string;
  upload_headers: Record<string, string>;
  storage_uri: string;
  expires_in_seconds: number;
}
