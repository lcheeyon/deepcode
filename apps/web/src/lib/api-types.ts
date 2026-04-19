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
  report_artifact_id?: string | null;
}

export interface FindingListItem {
  finding_id: string;
  framework: string;
  control_id: string;
  status: string;
  severity: string;
  title: string;
  evidence_refs: Record<string, unknown>[];
  reasoning_summary?: string | null;
  confidence_score: number;
  policy_version: string;
  created_at: string;
}

export interface FindingsPage {
  items: FindingListItem[];
  next_cursor?: string | null;
}

export interface ArtifactSummary {
  artifact_id: string;
  kind: string;
  checksum_sha256: string;
  size_bytes: number;
  storage_uri: string;
  created_at: string;
}

export interface ArtifactsListResponse {
  artifacts: ArtifactSummary[];
}

export interface PolicyUploadResponse {
  upload_id: string;
  policy_version: string;
  controls_extracted: number;
  warnings: { detail: string }[];
  source_filename: string;
}

export interface PolicyUploadListItem {
  upload_id: string;
  policy_version: string;
  source_filename: string;
  controls_extracted: number;
  warnings: { detail: string }[];
  created_at: string;
}

export interface PolicyUploadListResponse {
  uploads: PolicyUploadListItem[];
}

export interface PrepareRepoUploadResponse {
  upload_id: string;
  upload_url: string;
  upload_headers: Record<string, string>;
  storage_uri: string;
  expires_in_seconds: number;
}

export interface ScanWorkflowChecklistItem {
  node: string;
  state: string;
}

export interface ScanWorkflowEventItem {
  id: string;
  event_seq: number;
  event_type: string;
  node?: string | null;
  correlation_id?: string | null;
  graph_version?: string | null;
  created_at: string;
  payload: Record<string, unknown>;
}

export interface TraceLinkItem {
  vendor: string;
  url?: string | null;
  reason?: string | null;
  root_run_id?: string | null;
  trace_id?: string | null;
  project_id?: string | null;
  workspace_id?: string | null;
}

export interface ScanWorkflowResponse {
  scan_id: string;
  tenant_id: string;
  status: string;
  current_stage: string;
  percent_complete: number;
  correlation_id?: string | null;
  graph_version?: string | null;
  planned_nodes: string[];
  checklist: ScanWorkflowChecklistItem[];
  handoffs: { from_agent: string; to_agent: string; message_type: string; summary?: string | null; at: string }[];
  events: ScanWorkflowEventItem[];
  trace_links: TraceLinkItem[];
  summary_counts: Record<string, unknown>;
}
