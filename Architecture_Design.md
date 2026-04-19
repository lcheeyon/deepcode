# DeepGuard Compliance Engine — Detailed Architecture Design

**Document Status:** Implementation specification (draft) — sections 24+ are normative for build v0  
**Version:** 0.2  
**Date:** April 2026  
**Classification:** Internal — Engineering

---

## Table of Contents

1. [Document Scope & Conventions](#1-document-scope--conventions)
2. [System Context & Boundaries (C4 Level 1–2)](#2-system-context--boundaries)
3. [Agentic Reasoning Architecture](#3-agentic-reasoning-architecture)
4. [LangGraph Orchestration Design](#4-langgraph-orchestration-design)
5. [Inter-Agent Communication Protocol](#5-inter-agent-communication-protocol)
6. [LangChain Component Usage](#6-langchain-component-usage)
7. [LangSmith — Tracing & Evaluation](#7-langsmith--tracing--evaluation)
8. [LangFuse — Observability & Cost Governance](#8-langfuse--observability--cost-governance)
9. [Caching Architecture](#9-caching-architecture)
10. [Memory & Context Compaction Strategy](#10-memory--context-compaction-strategy)
11. [Ingestion & Multi-Language Parsing Architecture](#11-ingestion--multi-language-parsing-architecture)
12. [Vector Store & RAG Design](#12-vector-store--rag-design)
13. [LLM Selection, Routing & Fallback](#13-llm-selection-routing--fallback)
14. [State Management & Data Flow](#14-state-management--data-flow)
15. [IaC & Cloud Config Scanning Architecture](#15-iac--cloud-config-scanning-architecture)
16. [Compliance Mapping Engine](#16-compliance-mapping-engine)
17. [Remediation & Patch Generation](#17-remediation--patch-generation)
18. [Report Assembly Pipeline](#18-report-assembly-pipeline)
19. [Error Handling, Resilience & Circuit Breakers](#19-error-handling-resilience--circuit-breakers)
20. [Security & Secrets Architecture](#20-security--secrets-architecture)
21. [Performance, Scalability & Cost Model](#21-performance-scalability--cost-model)
22. [Deployment Topologies](#22-deployment-topologies)
23. [Open Design Questions](#23-open-design-questions)
24. [Feature Flags and runtime_config Schema](#24-feature-flags-and-runtime_config-schema)
25. [Repository Layout & Ownership Boundaries](#25-repository-layout--ownership-boundaries)
26. [Implementation Stack & Version Pins](#26-implementation-stack--version-pins)
27. [Configuration Surface (Environment Variables)](#27-configuration-surface-environment-variables)
28. [Control Plane HTTP API (FastAPI)](#28-control-plane-http-api-fastapi)
29. [Relational Schema — Tenancy, Jobs, Findings](#29-relational-schema--tenancy-jobs-findings)
30. [Async Job Execution & Queue Contract](#30-async-job-execution--queue-contract)
31. [LangGraph Runtime Contract](#31-langgraph-runtime-contract)
32. [Object Storage Layout & Lifecycle](#32-object-storage-layout--lifecycle)
33. [Testing, CI Gates, & Golden Datasets](#33-testing-ci-gates--golden-datasets)
34. [Local Development Topology](#34-local-development-topology)
35. [Operational Hooks (SLOs, Backpressure, Runbooks)](#35-operational-hooks-slos-backpressure-runbooks)

---

## 1. Document Scope & Conventions

### 1.1 Purpose

This document defines the internal technical architecture of the DeepGuard Compliance Engine. It covers the agentic reasoning model, orchestration topology, inter-agent protocols, observability stack, caching and memory strategies, and the multi-language code ingestion pipeline. It is intended for the engineering team to guide implementation, for technical due diligence, and as the authoritative reference for architectural decisions.

### 1.2 What This Document Is NOT

- A product specification (see Business Proposal v5.0)
- An API reference (see separate API Design doc)
- An operations runbook (see separate Ops doc)

### 1.3 Conventions

| Symbol | Meaning |
|---|---|
| `AgentNode` | A LangGraph node wrapping an LLM-powered agent |
| `ToolNode` | A LangGraph node executing a deterministic tool call |
| `StateKey` | A typed field in the shared `ScanState` TypedDict |
| `→` | Directed data or control flow |
| `⇌` | Bidirectional message exchange |
| `[BLOCKING]` | Node that blocks the graph until resolved |
| `[ASYNC]` | Node that runs in a background thread/task |

### 1.4 Agent Name Registry

| Code Name (Greek) | Chinese Name | Role |
|---|---|---|
| Hermes | 太白金星 | Ingestion Gateway |
| Tiresias | 伏羲 | Policy Parser |
| Argus | 千里眼 | Code Indexer |
| Laocoon | 钟馗 | IaC Analyzer |
| Cassandra | 比干 | Cloud Config Agent |
| Athena | 观音菩萨 | Compliance Mapper |
| Circe | 神农氏 | Remediation Advisor |
| Penelope | 织女 | Report Assembler |
| Calypso | 东海龙王 | Secrets Manager |
| Aeolus | 风伯 | Queue / Event Bus |
| Eumaeus | 门神 | Auth & AuthZ |
| **Odysseus Engine** | **姜子牙** | LangGraph Orchestrator |

---

## 2. System Context & Boundaries

### 2.1 C4 Level 1 — System Context

```
┌─────────────────────────────────────────────────────────────────────┐
│  ENTERPRISE SECURITY BOUNDARY (Customer VPC)                        │
│                                                                     │
│  ┌──────────────┐    scan request    ┌─────────────────────────┐   │
│  │  Developer / │ ────────────────▶  │                         │   │
│  │  CI Pipeline │                    │   DeepGuard             │   │
│  │  (GitHub     │ ◀──────────────── │   Compliance Engine     │   │
│  │   Actions /  │    PDF Report      │                         │   │
│  │   GitLab CI) │                    │   (Odysseus Engine +    │   │
│  └──────────────┘                    │    Agent Crew)          │   │
│                                      └────────────┬────────────┘   │
│  ┌──────────────┐                                 │               │
│  │  Cloud APIs  │ ◀───────────────────────────────┘               │
│  │  (read-only) │   CloudConnector.get_resources()                 │
│  │  AWS/Ali/TCE │                                                  │
│  │  /HW/GCP     │                                                  │
│  └──────────────┘                                                  │
│                                                                     │
│  ┌──────────────┐                                                   │
│  │  LLM         │  ← stays inside VPC for on-prem deployments      │
│  │  Endpoint    │    or calls SaaS API over private link            │
│  │  (Bedrock /  │                                                   │
│  │  Qwen3 /     │                                                   │
│  │  DeepSeek /  │                                                   │
│  │  Ollama)     │                                                   │
│  └──────────────┘                                                   │
└─────────────────────────────────────────────────────────────────────┘
```

### 2.2 C4 Level 2 — Container Diagram

| Container | Technology | Responsibility |
|---|---|---|
| **API Gateway** | FastAPI + Uvicorn | Accepts scan jobs, returns job status and report URLs |
| **Odysseus Engine** | LangGraph 0.2+ | Graph orchestrator — drives agent DAG execution |
| **Agent Workers** | Python + LangChain | Hermes…Penelope — each a stateless async worker |
| **Vector Store** | PostgreSQL + pgvector | Code chunk embeddings, policy chunk embeddings |
| **Object Store** | S3 / OSS / OBS | Raw repo archives, generated reports |
| **Job Queue** | Redis Streams / Kafka | Async job dispatch and inter-agent events (Aeolus) |
| **Secrets Store** | AWS SM / KV / Vault | Cloud credentials, LLM API keys (Calypso) |
| **Metadata DB** | PostgreSQL | Scan history, finding records, policy versions |
| **Observability** | LangSmith + LangFuse | Traces, evals, cost accounting |
| **Cache Layer** | Redis | LLM response cache, semantic cache, repo fingerprint cache |

### 2.3 Key Design Constraints

- **No code egress:** Source code must never leave the customer's VPC boundary, not even as LLM prompt fragments sent to a remote API unless the customer explicitly opts in to a SaaS LLM tier.
- **Read-only cloud access:** Cloud connector credentials are scoped to read-only IAM policies. No mutation of customer infrastructure.
- **Deterministic report generation:** Given the same inputs and policy version, two scans of the same repo must produce structurally identical reports (LLM non-determinism is bounded via `temperature=0` and response caching).
- **Scan completion SLA:** P95 full-stack scan (code + IaC + cloud) must complete in under 10 minutes for repos up to 500k LOC.

---

## 3. Agentic Reasoning Architecture

### 3.1 Reasoning Paradigm: Structured ReAct

Each agent follows a **Structured ReAct** loop rather than open-ended ReAct:

```
┌─────────────────────────────────────────────────────────┐
│  STRUCTURED ReAct LOOP (per AgentNode)                  │
│                                                         │
│  1. OBSERVE  — receive typed inputs from ScanState     │
│  2. THINK    — CoT reasoning over structured context   │
│  3. PLAN     — emit a typed ToolCallPlan (Pydantic)    │
│  4. ACT      — ToolNode executes deterministic tools   │
│  5. VERIFY   — agent checks tool output for coherence  │
│  6. EMIT     — write typed output back to ScanState    │
│                                                         │
│  Max iterations per agent: configurable (default 5)    │
│  Loop guard: iteration_count + confidence_score check  │
└─────────────────────────────────────────────────────────┘
```

The key departure from vanilla ReAct:
- **Input schema is typed** (Pydantic models, not raw strings). The agent cannot "hallucinate" a different input format.
- **Tool call is a structured object** (`ToolCallPlan`), validated before execution — prevents prompt injection via malicious file content.
- **Output schema is typed** — the agent's LLM call uses structured output / function calling mode, ensuring every finding has required fields (`control_id`, `severity`, `evidence_refs`, `reasoning_chain`).

### 3.2 Self-Critique & Confidence Scoring

After VERIFY, the agent produces a `confidence_score: float [0.0–1.0]`.

```python
class AgentOutput(BaseModel):
    findings: list[Finding]
    confidence_score: float       # 0.0 = uncertain, 1.0 = certain
    reasoning_summary: str
    loop_count: int
    should_escalate: bool         # trigger human review flag
```

Rules:
- `confidence_score < 0.6` → re-enter the ReAct loop (up to `max_iterations`)
- `confidence_score < 0.4` after max iterations → mark finding as `status=UNCERTAIN`, set `should_escalate=True`
- `confidence_score >= 0.85` on first pass → short-circuit remaining iterations

### 3.3 Critique Agent Pattern (Athena)

The Compliance Mapper (Athena) implements a **Generator → Critic** pattern:

```
[Generator Pass]  Athena maps each control requirement → PASS/FAIL/PARTIAL/NA
        ↓
[Critic Pass]     Athena re-reads its own output as a "second reviewer",
                  checks for logical contradictions, missing evidence,
                  and over-claiming (marking FAIL where evidence is absent)
        ↓
[Reconcile]       Merge generator and critic outputs; disagreements → UNCERTAIN
```

This two-pass approach significantly reduces false positives — the single largest complaint about rule-based scanners.

### 3.4 Cross-Layer Correlation Reasoning

Athena's most powerful capability is correlating findings across layers:

```
Finding type: "Infrastructure promise vs. code reality gap"

Example:
  - IaC (Laocoon):   S3 bucket has server-side encryption = AES-256  [PASS]
  - Code (Argus):    boto3 calls use presigned URLs with no expiry    [FAIL]
  - Cloud (Cassandra): S3 bucket policy allows s3:GetObject from *    [FAIL]

Cross-layer finding:
  Even though encryption is configured at-rest, the access control gap
  (overly permissive bucket policy + non-expiring presigned URLs) renders
  the encryption control partially ineffective. Composite severity: HIGH.
  Maps to: ISO 27001 A.10.1.1, SOC2 CC6.1, MAS TRM 9.1.3
```

The cross-layer reasoning prompt template is the core IP of the engine.

### 3.5 Reasoning Trace Schema

Every reasoning step is persisted as a `ReasoningTrace` object:

```python
class ReasoningTrace(BaseModel):
    agent_id: str                  # "athena", "laocoon", etc.
    scan_id: UUID
    step_number: int
    step_type: Literal["observe","think","plan","act","verify","emit"]
    input_tokens: int
    output_tokens: int
    tool_calls: list[ToolCall]
    llm_model: str
    latency_ms: int
    confidence_before: float | None
    confidence_after: float | None
    raw_llm_output: str            # stored encrypted, for audit
```

All traces feed LangSmith and LangFuse simultaneously via a dual-sink handler.

---

## 4. LangGraph Orchestration Design

### 4.1 Graph Topology

The Odysseus Engine is a **conditional directed acyclic graph** with two parallel fan-out branches and a mandatory convergence gate before the compliance mapping phase.

```
[START]
   │
   ▼
[hermes_node]          # IngestionAgent — fetch & stage repo
   │
   ▼
[tiresias_node]        # PolicyParserAgent — parse compliance docs
   │
   ▼
[argus_node]           # CodeIndexerAgent — AST + pgvector index
   │
   ├──────────────────────────────────────────────┐
   ▼                                              ▼
[laocoon_node]                             [cassandra_node]
(IaC Analyzer)                           (Cloud Config Agent)
   │                                              │
   └──────────────┬───────────────────────────────┘
                  ▼
         [convergence_gate]    # waits for both branches, validates outputs
                  │
                  ▼
         [athena_node]         # ComplianceMappingAgent — core reasoning
                  │
                  ▼
         [circe_node]          # RemediationAdvisorAgent
                  │
                  ▼
         [penelope_node]       # ReportAssemblerAgent → PDF
                  │
                  ▼
              [END]
```

### 4.2 ScanState — The Shared State TypedDict

```python
from typing import TypedDict, Annotated
from langgraph.graph.message import add_messages

class ScanState(TypedDict):
    # ── Job metadata ──────────────────────────────────────────────
    scan_id:              str
    job_config:           ScanJobConfig
    created_at:           datetime

    # ── Hermes outputs ────────────────────────────────────────────
    repo_local_path:      str | None
    repo_metadata:        RepoMetadata | None
    cloud_snapshots:      dict[str, CloudSnapshot]   # cloud_id → snapshot

    # ── Tiresias outputs ──────────────────────────────────────────
    policy_controls:      list[PolicyControl]        # parsed control requirements
    policy_version:       str | None

    # ── Argus outputs ─────────────────────────────────────────────
    code_index_id:        str | None                 # pgvector collection ID
    dependency_graph:     DependencyGraph | None
    language_breakdown:   dict[str, int]             # lang → line count

    # ── Laocoon outputs ───────────────────────────────────────────
    iac_findings:         list[IaCFinding]

    # ── Cassandra outputs ─────────────────────────────────────────
    cloud_findings:       list[CloudFinding]

    # ── Athena outputs ────────────────────────────────────────────
    compliance_findings:  list[ComplianceFinding]
    cross_layer_findings: list[CrossLayerFinding]
    compliance_summary:   ComplianceSummary | None

    # ── Circe outputs ─────────────────────────────────────────────
    remediations:         list[Remediation]

    # ── Control flow ──────────────────────────────────────────────
    error_log:            list[AgentError]
    should_abort:         bool
    agent_traces:         Annotated[list[ReasoningTrace], add_messages]
```

### 4.3 Node Implementation Pattern

```python
from langgraph.graph import StateGraph
from langchain_core.runnables import RunnableConfig

def hermes_node(state: ScanState, config: RunnableConfig) -> ScanState:
    """Ingestion node — clone repo, stage to object store, call cloud connectors."""
    agent = HermesAgent(config=config)
    result = agent.run(
        repo_url=state["job_config"].repo_url,
        cloud_profiles=state["job_config"].cloud_profiles,
    )
    return {
        "repo_local_path":  result.local_path,
        "repo_metadata":    result.metadata,
        "cloud_snapshots":  result.cloud_snapshots,
    }
```

All nodes return a **partial state dict** — LangGraph merges it into the full `ScanState` via reducer functions, avoiding the need to pass the entire state on every update.

### 4.4 Conditional Edges & Routing Logic

```python
def route_after_ingestion(state: ScanState) -> str:
    if state.get("should_abort"):
        return "error_handler"
    if not state["repo_local_path"] and not state["cloud_snapshots"]:
        return "error_handler"
    return "tiresias_node"

graph.add_conditional_edges("hermes_node", route_after_ingestion, {
    "tiresias_node": "tiresias_node",
    "error_handler": "error_handler",
})
```

### 4.5 Parallel Execution (Fan-out / Fan-in)

LangGraph's `Send` API dispatches Laocoon and Cassandra simultaneously:

```python
from langgraph.constants import Send

def fan_out_after_indexing(state: ScanState) -> list[Send]:
    sends = []
    if state["job_config"].scan_iac:
        sends.append(Send("laocoon_node", state))
    if state["job_config"].scan_cloud and state["cloud_snapshots"]:
        sends.append(Send("cassandra_node", state))
    return sends

graph.add_conditional_edges("argus_node", fan_out_after_indexing)
```

The `convergence_gate` node uses a **reducer** on `iac_findings` and `cloud_findings` that blocks until both lists are populated (or their respective agents mark themselves as skipped).

### 4.6 Graph Checkpointing & Resume

```python
from langgraph.checkpoint.postgres import PostgresSaver

checkpointer = PostgresSaver.from_conn_string(os.environ["CHECKPOINT_DB_URL"])

app = graph.compile(checkpointer=checkpointer)

# Resume a crashed scan from last checkpoint:
app.invoke(
    None,                          # None = resume, not restart
    config={"configurable": {"thread_id": scan_id}},
)
```

Checkpoints are written after every node completes. On worker restart, the scan resumes from the last successful node — critical for long-running scans on large repos.

### 4.7 Human-in-the-Loop Interrupts

```python
graph.compile(
    checkpointer=checkpointer,
    interrupt_before=["athena_node"],   # pause for human review if flagged
)
```

When `should_escalate=True` is set by any upstream agent, the graph pauses before Athena. A webhook notifies the security reviewer. The reviewer can inject annotations into `ScanState` before resuming.

---

## 5. Inter-Agent Communication Protocol

### 5.1 Communication Model

Agents do **not** call each other directly. All communication flows through:

1. **ScanState** (synchronous, within a single graph run) — structured state fields
2. **Aeolus Event Bus** (asynchronous, for long-running sub-tasks) — Redis Streams / Kafka topics
3. **Shared Artifact Store** (for large payloads) — S3/OSS presigned URLs embedded in ScanState

This avoids tight coupling and enables the parallel branches to operate truly independently.

### 5.2 Message Schema

All inter-agent messages, whether in state or on the event bus, conform to `AgentMessage`:

```python
class AgentMessage(BaseModel):
    msg_id:       UUID = Field(default_factory=uuid4)
    scan_id:      UUID
    sender:       AgentName           # enum: hermes, tiresias, argus, ...
    recipient:    AgentName | Literal["broadcast"]
    msg_type:     MessageType         # enum: TASK, RESULT, ERROR, HEARTBEAT
    payload:      dict                # typed per msg_type
    timestamp:    datetime
    schema_ver:   str = "1.0"
    trace_id:     str | None          # LangSmith/LangFuse trace correlation
```

### 5.3 Large Payload Protocol (Artifact Store Pattern)

Code index payloads, cloud snapshots, and generated PDFs are never embedded directly in messages. Instead, agents exchange **artifact references**:

```python
class ArtifactRef(BaseModel):
    artifact_id:  UUID
    store:        Literal["s3", "oss", "obs", "local"]
    bucket:       str
    key:          str
    checksum:     str          # SHA-256 of raw bytes
    size_bytes:   int
    expires_at:   datetime     # presigned URL expiry
    encrypted:    bool = True
```

Pattern: Producer uploads → writes `ArtifactRef` into `ScanState` → Consumer downloads on demand.

### 5.4 Agent Contract: Input/Output Types

Each agent publishes a typed contract. Breaking changes to these types require a version bump and migration.

| Agent | Input State Keys | Output State Keys |
|---|---|---|
| Hermes | `job_config` | `repo_local_path`, `repo_metadata`, `cloud_snapshots` |
| Tiresias | `job_config.policy_ids`, `repo_metadata` | `policy_controls`, `policy_version` |
| Argus | `repo_local_path`, `repo_metadata` | `code_index_id`, `dependency_graph`, `language_breakdown` |
| Laocoon | `repo_local_path`, `policy_controls` | `iac_findings` |
| Cassandra | `cloud_snapshots`, `policy_controls` | `cloud_findings` |
| Athena | `code_index_id`, `iac_findings`, `cloud_findings`, `policy_controls` | `compliance_findings`, `cross_layer_findings`, `compliance_summary` |
| Circe | `compliance_findings`, `cross_layer_findings`, `code_index_id` | `remediations` |
| Penelope | all findings + remediations + `job_config` | `report_artifact_ref` |

---

## 6. LangChain Component Usage

### 6.1 Design Philosophy — LCEL Over Legacy Chains

All agent logic uses **LangChain Expression Language (LCEL)** `Runnable` composition rather than legacy `Chain` classes. LCEL provides:
- Native async support
- Streaming out of the box
- First-class LangSmith tracing
- Composable parallel execution via `RunnableParallel`

### 6.2 Core Runnable Patterns

**Pattern A: Structured Output Agent**
```python
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough

compliance_chain = (
    RunnablePassthrough.assign(
        context=lambda x: retriever.invoke(x["query"])
    )
    | ChatPromptTemplate.from_messages([
        ("system", ATHENA_SYSTEM_PROMPT),
        ("human", "{query}\n\nContext:\n{context}"),
    ])
    | llm.with_structured_output(ComplianceFindingList)
)
```

**Pattern B: Tool-Calling Agent**
```python
from langchain.agents import create_tool_calling_agent, AgentExecutor

laocoon_agent = create_tool_calling_agent(
    llm=llm,
    tools=[parse_terraform_tool, parse_ros_tool, parse_cfn_tool],
    prompt=LAOCOON_PROMPT,
)
laocoon_executor = AgentExecutor(
    agent=laocoon_agent,
    tools=[...],
    max_iterations=5,
    return_intermediate_steps=True,   # for LangSmith trace
)
```

**Pattern C: Parallel RAG Retrieval**
```python
from langchain_core.runnables import RunnableParallel

parallel_retrieval = RunnableParallel(
    code_context=code_retriever,
    policy_context=policy_retriever,
    iac_context=iac_retriever,
)
```

### 6.3 Prompt Template Management

All prompts are versioned in LangSmith Hub and loaded at runtime:

```python
from langchain import hub

ATHENA_PROMPT   = hub.pull("deepguard/athena-compliance-v2")
LAOCOON_PROMPT  = hub.pull("deepguard/laocoon-iac-v1")
CIRCE_PROMPT    = hub.pull("deepguard/circe-remediation-v1")
```

Benefits: prompt changes deploy without code releases; A/B testing via LangSmith evaluations; rollback in seconds.

### 6.4 Output Parsers & Structured Outputs

All agent outputs use Pydantic v2 `BaseModel` with `.with_structured_output()` (function calling / JSON mode). Fallback: `PydanticOutputParser` with retry logic:

```python
from langchain.output_parsers import RetryWithErrorOutputParser

robust_parser = RetryWithErrorOutputParser.from_llm(
    parser=PydanticOutputParser(pydantic_object=FindingList),
    llm=llm,
    max_retries=2,
)
```

### 6.5 Tool Definitions

Tools are thin wrappers around deterministic functions. LLMs cannot execute arbitrary code — every tool is pre-registered:

```python
from langchain_core.tools import tool

@tool
def read_terraform_file(file_path: str) -> dict:
    """Parse a Terraform HCL file and return its resource map."""
    # path is validated against repo sandbox before execution
    return parse_hcl2(safe_read(file_path, sandbox=repo_sandbox))
```

Security: `safe_read()` enforces the repo sandbox — no path traversal outside the cloned repo directory.

---

## 7. LangSmith — Tracing & Evaluation

### 7.1 Tracing Strategy

Every LangGraph run is automatically traced by LangSmith when `LANGCHAIN_TRACING_V2=true`. The trace hierarchy:

```
Scan Run (trace root)
 ├── hermes_node (span)
 │    └── cloud_connector.get_resources (span)
 ├── tiresias_node (span)
 │    └── policy_parser_chain (span)
 ├── argus_node (span)
 │    ├── ast_parse_files (span, batch)
 │    └── pgvector_upsert (span, batch)
 ├── laocoon_node (span)
 │    ├── tool: read_terraform_file (span ×N)
 │    └── iac_findings_chain (span)
 ├── cassandra_node (span)
 ├── athena_node (span)
 │    ├── parallel_retrieval (span)
 │    ├── generator_pass (span)
 │    └── critic_pass (span)
 ├── circe_node (span)
 └── penelope_node (span)
```

### 7.2 Custom Metadata Tags

```python
from langsmith import traceable

@traceable(
    name="athena_generator_pass",
    tags=["athena", "compliance", "generator"],
    metadata={"scan_id": scan_id, "policy": policy_version}
)
def generator_pass(state): ...
```

### 7.3 Evaluation Datasets & Regression Testing

LangSmith stores curated evaluation datasets:

| Dataset | Purpose | Size |
|---|---|---|
| `iac-findings-gold` | Known Terraform misconfigs with expected findings | 200+ examples |
| `cloud-findings-gold` | Known cloud misconfigs per framework | 150+ examples |
| `cross-layer-gold` | Known cross-layer correlation cases | 50+ examples |
| `false-positive-registry` | Cases that must NOT trigger a finding | 300+ examples |
| `remediation-quality` | Human-rated remediation suggestions | 100+ examples |

CI pipeline runs evaluations on every prompt change:

```bash
langsmith eval run \
  --dataset iac-findings-gold \
  --evaluator exact_match \
  --evaluator semantic_similarity \
  --prompt deepguard/laocoon-iac-v{NEW}
```

---

## 8. LangFuse — Observability & Cost Governance

### 8.1 Why LangFuse Alongside LangSmith

| Capability | LangSmith | LangFuse |
|---|---|---|
| Trace collection | ✅ Native | ✅ via SDK |
| Prompt versioning | ✅ Hub | ✅ via UI |
| Evaluation framework | ✅ Strong | ✅ Good |
| Cost tracking per tenant | ❌ | ✅ |
| Self-hosted (air-gapped) | ❌ SaaS only | ✅ Docker |
| Per-scan cost breakdown | ❌ | ✅ |
| Budget alerts | ❌ | ✅ |
| GDPR / data-sovereign logging | ❌ | ✅ self-host |

LangFuse is the **mandatory** observability layer for enterprise (on-prem) deployments where data sovereignty prohibits sending traces to external SaaS.

### 8.2 Dual-Sink Trace Handler

```python
from langfuse.callback import CallbackHandler as LangFuseHandler
from langchain.callbacks import LangChainTracer

def build_callbacks(scan_id: str, tenant_id: str) -> list:
    callbacks = []
    if settings.langfuse_enabled:
        callbacks.append(LangFuseHandler(
            session_id=scan_id,
            user_id=tenant_id,
            tags=["deepguard", settings.environment],
        ))
    if settings.langsmith_enabled:
        callbacks.append(LangChainTracer(project_name="deepguard-prod"))
    return callbacks
```

### 8.3 Per-Tenant Cost Model

LangFuse's `generation` spans capture token usage per LLM call. A daily aggregation job builds the per-tenant cost ledger:

```sql
SELECT
    tenant_id,
    DATE(created_at)           AS scan_date,
    SUM(prompt_tokens)         AS total_prompt_tokens,
    SUM(completion_tokens)     AS total_completion_tokens,
    SUM(total_cost_usd)        AS total_cost_usd
FROM langfuse.observations
WHERE type = 'GENERATION'
GROUP BY 1, 2;
```

This feeds the billing engine for metered SaaS pricing.

### 8.4 Alerting

| Alert | Condition | Action |
|---|---|---|
| Cost spike | Single scan > $X threshold | Abort scan, notify ops |
| Latency degradation | P95 > 2× baseline | Page on-call |
| High retry rate | Agent retry rate > 20% | Alert engineering |
| Low confidence | >30% findings UNCERTAIN | Flag scan for human review |

---

## 9. Caching Architecture

### 9.1 Cache Taxonomy

```
┌─────────────────────────────────────────────────────────────────┐
│                    CACHE LAYERS                                 │
│                                                                 │
│  L1: Repo Fingerprint Cache       (Redis, TTL 24h)             │
│      key: sha256(repo_url + commit_sha + policy_version)       │
│      value: complete ScanResult (if unchanged, skip rescan)    │
│                                                                 │
│  L2: LLM Semantic Cache           (Redis + pgvector, TTL 1h)  │
│      key: embedding_similarity(prompt) > 0.97 threshold        │
│      value: previous LLM response for near-identical prompt    │
│                                                                 │
│  L3: Tool Output Cache            (Redis, TTL 30min)           │
│      key: sha256(tool_name + serialized_args)                  │
│      value: tool return value (for deterministic tools)        │
│                                                                 │
│  L4: Embedding Cache              (pgvector, TTL 7d)           │
│      key: sha256(text_chunk + model_id)                        │
│      value: embedding vector                                   │
│                                                                 │
│  L5: Policy Parse Cache           (Redis, TTL until version    │
│      key: policy_id + policy_version                changes)   │
│      value: parsed PolicyControl[]                             │
└─────────────────────────────────────────────────────────────────┘
```

### 9.2 Semantic Cache Implementation

```python
from langchain.cache import RedisSemanticCache
from langchain_openai import OpenAIEmbeddings
import langchain

langchain.llm_cache = RedisSemanticCache(
    redis_url=settings.redis_url,
    embedding=embeddings_model,
    score_threshold=0.97,   # cosine similarity — tuned for compliance prompts
)
```

For compliance use cases, semantic similarity threshold must be **high** (0.97+). At 0.90, similar-but-different control requirements share cached responses, producing incorrect findings.

### 9.3 Incremental Rescan (Delta Cache)

For repos with frequent CI scans, re-scanning unchanged files wastes compute:

```python
class DeltaScanStrategy:
    """Only re-analyze files changed since last scan."""

    def compute_delta(self, prev_scan: ScanResult, current_commit: str) -> DeltaScope:
        changed_files = git_diff(prev_scan.commit_sha, current_commit)
        return DeltaScope(
            files_to_rescan=changed_files,
            findings_to_carry_forward=self._find_unaffected(prev_scan, changed_files),
        )
```

Expected impact: 60–80% token cost reduction for active repos on daily scans.

### 9.4 Cache Invalidation Rules

| Cache | Invalidated By |
|---|---|
| Repo Fingerprint | New commit SHA or new policy version |
| Semantic Cache | Prompt template version change |
| Tool Output | Tool implementation version change |
| Embedding Cache | Embedding model version change |
| Policy Parse Cache | Policy document update |

---

## 10. Memory & Context Compaction Strategy

### 10.1 The Token Budget Problem

Large repos can generate scanning contexts that exceed LLM context windows:

| Scenario | Estimated tokens |
|---|---|
| Full code index summary | 20,000 – 200,000 tokens |
| All control requirements (ISO 27001 full) | ~15,000 tokens |
| IaC findings from large Terraform repo | 5,000 – 30,000 tokens |
| Cloud snapshot (1000+ resources) | 10,000 – 80,000 tokens |

Strategy: **Never pass raw data to the LLM. Always compress to a retrieval-augmented summary.**

### 10.2 Hierarchical Summarization

```
Raw code files (millions of tokens)
         ↓  [Argus — AST analysis]
Per-file summaries (hundreds of tokens each)
         ↓  [pgvector index]
RAG retrieval: top-K chunks per control requirement (< 4,000 tokens)
         ↓  [Athena — per-control reasoning]
Per-control finding (< 200 tokens)
         ↓  [Penelope — report assembly]
Final report (structured, bounded length)
```

### 10.3 Sliding Window Trace Compaction

For agents that loop (e.g., Athena processing 300 controls), the ReAct trace grows unboundedly. Compaction strategy:

```python
class TraceCompactor:
    """Compress completed reasoning steps into a summary token budget."""

    MAX_ACTIVE_TOKENS = 6_000   # keep last N tokens of trace in context
    COMPACTION_SUMMARY_TOKENS = 800   # summary of compacted steps

    def compact(self, trace: list[ReasoningStep]) -> list[ReasoningStep]:
        if token_count(trace) <= self.MAX_ACTIVE_TOKENS:
            return trace
        old_steps = trace[:-10]          # compact everything except last 10 steps
        summary   = self.llm_summarize(old_steps, max_tokens=self.COMPACTION_SUMMARY_TOKENS)
        return [SummaryStep(content=summary)] + trace[-10:]
```

### 10.4 Working Memory vs. External Memory

| Type | Storage | Use Case |
|---|---|---|
| **In-context (working)** | LLM context window | Current control being analyzed; last 10 reasoning steps |
| **Short-term (scan-scoped)** | Redis (TTL = scan duration) | Intermediate findings awaiting correlation |
| **Long-term (vector)** | pgvector | Repo code embeddings; policy chunk embeddings |
| **Episodic (audit log)** | PostgreSQL | Full reasoning traces for every scan (retained 7 years) |
| **Semantic (entity)** | PostgreSQL | Known resource types, historical finding patterns per tenant |

### 10.5 Context Window Allocation Strategy (per LLM call)

```
Total context budget: 128k tokens (Claude 3.5 Sonnet / GPT-4o)

Allocation:
  ├── System prompt + agent persona:     ~800  tokens  (fixed)
  ├── Policy control requirement:       ~400  tokens  (per control)
  ├── Retrieved code context (RAG):    ~3,000 tokens  (top-5 chunks)
  ├── Retrieved IaC context:           ~2,000 tokens  (top-3 chunks)
  ├── Cloud snapshot (filtered):       ~1,500 tokens  (relevant resources)
  ├── Cross-agent findings so far:     ~1,000 tokens  (compressed)
  ├── Compacted trace summary:           ~800 tokens  (prior steps)
  └── Output schema + instructions:     ~500 tokens  (fixed)
                                      ──────────────
  Total per control:                  ~10,000 tokens

  Max controls before context pressure: ~12 per call
  Strategy: batch controls by semantic similarity cluster
```

---

## 11. Ingestion & Multi-Language Parsing Architecture

### 11.1 Ingestion Sources

| Source Type | Transport | Agent | Notes |
|---|---|---|---|
| Git repo (GitHub/GitLab/Gitee/Bitbucket) | HTTPS clone / SSH | Hermes | Shallow clone for speed; full clone for blame analysis |
| ZIP / tarball upload | Multipart HTTP | Hermes | Max 2GB compressed |
| S3 / OSS / OBS bucket (code stored in object store) | Cloud SDK | Hermes | Requires read-only bucket policy |
| CI pipeline injection | REST API | Hermes | GitHub Actions / GitLab CI artifact push |
| IaC-only scan (no code) | File upload | Hermes | Terraform plan JSON, CloudFormation template |
| Cloud-only scan (no code, no IaC) | Cloud credentials | Hermes | Live API enumeration via Cassandra |

### 11.2 Source Language Support Matrix

| Language | AST Parser | Dependency Analysis | Semantic Chunking | Status |
|---|---|---|---|---|
| Python | `tree-sitter-python` | `pipdeptree`, `ast.parse` | Function + class boundaries | ✅ GA |
| TypeScript / JavaScript | `tree-sitter-typescript` | `package.json` graph | Module + function | ✅ GA |
| Go | `tree-sitter-go` | `go mod graph` | Package + function | ✅ GA |
| Java | `tree-sitter-java` | `pom.xml` / Gradle | Class + method | ✅ GA |
| Kotlin | `tree-sitter-kotlin` | `build.gradle.kts` | Class + function | ✅ GA |
| Rust | `tree-sitter-rust` | `Cargo.lock` | Crate + function | 🔧 Beta |
| C / C++ | `tree-sitter-c`, `tree-sitter-cpp` | `CMakeLists.txt` | Function + struct | 🔧 Beta |
| C# / .NET | `tree-sitter-c_sharp` | `*.csproj` NuGet | Class + method | 🔧 Beta |
| Ruby | `tree-sitter-ruby` | `Gemfile.lock` | Class + method | 📋 Planned |
| PHP | `tree-sitter-php` | `composer.json` | Class + function | 📋 Planned |
| Swift / Obj-C | `tree-sitter-swift` | SPM | Class + function | 📋 Planned |
| Terraform HCL | `python-hcl2` | provider graph | Resource block | ✅ GA |
| CloudFormation YAML | `cfn-flip` | resource dependency | Resource + property | ✅ GA |
| Alibaba Cloud ROS | Custom YAML parser | resource graph | Resource block | ✅ GA |
| Huawei Cloud Template | Custom YAML parser | resource graph | Resource block | ✅ GA |
| Kubernetes YAML | `kubernetes-validate` | label selectors | Manifest per resource | ✅ GA |
| Bicep | `bicep decompile` → ARM | ARM parser | Resource block | 🔧 Beta |
| Pulumi (Python/TS) | Language-native AST | resource graph | Resource declaration | 📋 Planned |
| Helm Charts | YAML + Go templating | chart dependency | Template per resource | 🔧 Beta |

### 11.3 Parsing Pipeline Architecture

```
Raw source file
      │
      ▼
[Language Detector]       # linguist-style heuristics + file extension
      │
      ▼
[Syntax Parser]           # tree-sitter grammar per language
      │                   # produces: CST (concrete syntax tree)
      ▼
[AST Transformer]         # strips whitespace/comments → normalized AST
      │
      ├──► [Symbol Extractor]     → function/class/variable name index
      │
      ├──► [Dependency Mapper]    → import/require/use graph
      │
      ├──► [Security Pattern Scanner]  → semgrep rules per language
      │                                  (OWASP Top 10, CWE patterns)
      │
      └──► [Semantic Chunker]     → chunks for pgvector embedding
```

### 11.4 Semantic Chunking Strategy

Chunking is **AST-boundary-aware** — chunks never split mid-function or mid-class:

```python
class ASTAwareChunker:
    """Chunk code at semantic boundaries, not arbitrary token counts."""

    CHUNK_TARGETS = {
        "python":     ["function_definition", "class_definition"],
        "typescript": ["function_declaration", "class_declaration", "arrow_function"],
        "go":         ["function_declaration", "method_declaration"],
        "java":       ["method_declaration", "class_declaration"],
        "terraform":  ["resource", "module", "data"],
    }

    MAX_CHUNK_TOKENS  = 600    # stay well within embedding model limits
    OVERLAP_TOKENS    = 80     # preserve context at chunk boundaries
    MIN_CHUNK_TOKENS  = 50     # skip trivially small functions
```

For files where the entire function exceeds `MAX_CHUNK_TOKENS`, a **sliding window with semantic overlap** is applied, and the chunk metadata records which function it belongs to.

### 11.5 Dependency Graph Construction

```python
class DependencyGraph(BaseModel):
    nodes: list[CodeNode]      # each file/module/class is a node
    edges: list[DependencyEdge]
    entry_points: list[str]    # main(), handler(), app startup
    external_deps: list[ExternalDep]   # third-party packages + version
    vulnerable_deps: list[VulnerableDep]  # cross-ref with OSV/NVD
```

The dependency graph feeds Athena's cross-layer reasoning — for example, a vulnerable transitive dependency in `package-lock.json` can be correlated with the code path that actually invokes it, producing a more accurate severity score than a blanket "vulnerable dependency" finding.

### 11.6 Large Repo Handling

| Repo Size | Strategy |
|---|---|
| < 50k LOC | Full parse + full index |
| 50k – 500k LOC | Full parse; selective deep-index (top-risk files by language + path heuristics) |
| 500k – 2M LOC | Shallow parse; security-relevant files only (auth, crypto, network, config); monorepo sub-path scoping |
| > 2M LOC | Mandatory scoping — customer must specify sub-paths; full monorepo scan available as async batch job |

---

## 12. Vector Store & RAG Design

### 12.1 Collections Schema

```sql
-- Code chunks collection
CREATE TABLE code_chunks (
    id          UUID PRIMARY KEY,
    scan_id     UUID NOT NULL,
    tenant_id   UUID NOT NULL,
    file_path   TEXT,
    language    TEXT,
    node_type   TEXT,            -- function, class, resource, etc.
    content     TEXT,
    embedding   vector(1536),    -- OpenAI text-embedding-3-small or equivalent
    token_count INT,
    metadata    JSONB,           -- function name, class name, line range, etc.
    created_at  TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX ON code_chunks USING ivfflat (embedding vector_cosine_ops)
    WITH (lists = 100);

-- Policy chunks collection (shared across tenants, per policy version)
CREATE TABLE policy_chunks (
    id              UUID PRIMARY KEY,
    policy_id       TEXT,
    policy_version  TEXT,
    control_id      TEXT,        -- e.g. "ISO27001-A.10.1.1"
    control_text    TEXT,
    embedding       vector(1536),
    framework       TEXT,        -- ISO27001, SOC2, MAS-TRM, GB-T-22239
    scope_tags      TEXT[]       -- ["encryption", "access_control", "audit_logging"]
);
```

### 12.2 Retrieval Strategy per Agent

| Agent | Collection | Query Type | Top-K | Re-rank? |
|---|---|---|---|---|
| Tiresias | `policy_chunks` | Semantic | 20 | No — full policy needed |
| Argus | `code_chunks` | Hybrid (BM25 + vector) | 10 per file | No |
| Athena | `code_chunks` | Semantic per control | 5 | Yes — MMR for diversity |
| Laocoon | `code_chunks` (IaC only) | Keyword + semantic | 5 | No |
| Circe | `code_chunks` | Semantic (by finding) | 3 | No |

### 12.3 Hybrid Search (BM25 + Vector)

For code retrieval, pure semantic search misses exact identifier matches (function names, variable names, API endpoint paths). Hybrid search combines:

```python
from langchain.retrievers import EnsembleRetriever

hybrid_retriever = EnsembleRetriever(
    retrievers=[bm25_retriever, vector_retriever],
    weights=[0.3, 0.7],   # vector-weighted; BM25 for exact symbol names
)
```

### 12.4 Embedding Model Selection

| Deployment | Embedding Model | Dimensions | Notes |
|---|---|---|---|
| AWS / Azure | `text-embedding-3-small` (OpenAI) | 1536 | Cost-effective, strong code understanding |
| Alibaba Cloud | `text-embedding-v3` (Tongyi) | 1536 | Data-sovereign within AliCloud |
| Huawei Cloud / air-gap | `bge-m3` (BAAI, Ollama) | 1024 | Fully local, excellent multilingual |
| All tiers | `cohere-embed-v3` (fallback) | 1024 | Good code retrieval |

---

## 13. LLM Selection, Routing & Fallback

### 13.1 Task-to-Model Matrix

| Task | Preferred Model | Reason | Fallback |
|---|---|---|---|
| Policy parsing (Tiresias) | GPT-4o / Claude 3.5 Sonnet | Long context, high accuracy | Qwen3-72B |
| Code indexing summary (Argus) | GPT-4o-mini / Haiku | Fast, cheap — many files | DeepSeek-V2 |
| IaC analysis (Laocoon) | Claude 3.5 Sonnet | Strong structured output | GPT-4o |
| Cloud config (Cassandra) | GPT-4o / Claude 3.5 Sonnet | Deep tool use | Qwen3-Coder |
| Compliance mapping (Athena) | Claude 3 Opus / GPT-4o | Highest reasoning quality | Claude 3.5 Sonnet |
| Remediation (Circe) | Claude 3.5 Sonnet / GPT-4o | Code generation quality | Qwen3-Coder |
| Report assembly (Penelope) | GPT-4o-mini / Haiku | Fast, cheap — formatting task | Qwen3-7B |
| Chinese language output | Qwen3-72B / DeepSeek-R1 | Native Chinese reasoning | GPT-4o |
| Air-gapped / Xinchuang | DeepSeek-R1 (Ollama) | Fully local | Qwen3-Coder (Ollama) |

### 13.2 LLM Router Architecture

```python
class LLMRouter:
    """Route LLM calls based on task type, deployment tier, and cost budget."""

    def get_llm(self, task: TaskType, context: ScanContext) -> BaseChatModel:
        if context.deployment == "xinchuang" or context.air_gapped:
            return self._local_llm(task)
        if context.tenant_config.preferred_provider == "alibaba":
            return self._alibaba_llm(task)
        if context.budget_remaining < LOW_BUDGET_THRESHOLD:
            return self._economy_llm(task)
        return self._primary_llm(task)
```

### 13.3 Fallback Chain

```python
from langchain_core.runnables import with_fallbacks

primary_llm   = ChatAnthropic(model="claude-opus-4-7")
fallback_llm  = ChatOpenAI(model="gpt-4o")
economy_llm   = ChatOpenAI(model="gpt-4o-mini")

robust_llm = primary_llm.with_fallbacks(
    [fallback_llm, economy_llm],
    exceptions_to_handle=(RateLimitError, APITimeoutError),
)
```

---

## 14. State Management & Data Flow

### 14.1 State Lifecycle

```
CREATED → INGESTING → INDEXING → ANALYZING → MAPPING → REMEDIATING → REPORTING → COMPLETE
                                                                               ↗
                                            ↘ ERROR (at any stage) → FAILED
```

### 14.2 State Persistence Strategy

| State Stage | Storage | Retention |
|---|---|---|
| In-flight (active graph run) | LangGraph Postgres checkpointer | Until scan completes |
| Completed scan state | PostgreSQL `scan_results` table | 7 years (audit requirement) |
| Raw artifact (code archive) | S3/OSS/OBS | Configurable (default: deleted after 24h) |
| Findings | PostgreSQL `findings` table | 7 years |
| Reports (PDF) | S3/OSS/OBS, encrypted | 7 years |
| Reasoning traces | PostgreSQL + LangFuse | 1 year (configurable) |
| Embeddings | pgvector | TTL per collection (code: 30d, policy: indefinite) |

---

## 15. IaC & Cloud Config Scanning Architecture

### 15.1 IaC Parser Registry

```python
IaC_PARSERS = {
    "terraform":       TerraformParser(backend="python-hcl2"),
    "cloudformation":  CloudFormationParser(backend="cfn-flip"),
    "alibaba-ros":     AliyunROSParser(backend="custom"),
    "huawei-template": HuaweiROSParser(backend="custom"),
    "kubernetes":      KubernetesParser(backend="kubernetes-validate"),
    "helm":            HelmParser(backend="helm-template + kubernetes"),
    "bicep":           BicepParser(backend="bicep-decompile + arm-ttk"),
    "pulumi-python":   PulumiPythonParser(backend="ast + pulumi-sdk-introspection"),
    "cdk-typescript":  CDKTypeScriptParser(backend="ts-morph + cdk-nag"),
}
```

### 15.2 Cloud Connector Interface

```python
class CloudConnector(ABC):
    """Unified read-only interface to cloud provider APIs."""

    @abstractmethod
    def get_iam_policies(self) -> list[IAMPolicy]: ...

    @abstractmethod
    def get_network_topology(self) -> NetworkTopology: ...

    @abstractmethod
    def get_storage_configs(self) -> list[StorageResource]: ...

    @abstractmethod
    def get_compute_configs(self) -> list[ComputeResource]: ...

    @abstractmethod
    def get_encryption_status(self) -> list[EncryptionStatus]: ...

    @abstractmethod
    def get_audit_log_status(self) -> AuditLogStatus: ...

class AlibabaClouConnector(CloudConnector): ...
class TencentCloudConnector(CloudConnector): ...
class HuaweiCloudConnector(CloudConnector): ...
class AWSConnector(CloudConnector): ...
```

---

## 16. Compliance Mapping Engine

### 16.1 Framework Registry

```python
COMPLIANCE_FRAMEWORKS = {
    "ISO-27001-2022":     ISO27001Framework(),
    "SOC2-Type2":         SOC2Framework(),
    "MAS-TRM-2021":       MASTRMFramework(),
    "MAS-FSAP":           MASFSAPFramework(),
    "GB-T-22239-2019":    DengBao20Framework(),    # 等保 2.0
    "MLPS-2-Level3":      DengBaoLevel3Framework(),
    "CSL-2017":           CybersecurityLawFramework(),
    "DSL-2021":           DataSecurityLawFramework(),
    "PIPL-2021":          PIPLFramework(),
    "GenAI-Mgmt-2023":    GenAIMgmtFramework(),   # 生成式AI管理办法
    "GDPR":               GDPRFramework(),
    "HIPAA":              HIPAAFramework(),
    "PCI-DSS-4.0":        PCIDSSFramework(),
    "NIST-CSF-2.0":       NISTCSFFramework(),
    "CIS-Benchmarks":     CISBenchmarksFramework(),
}
```

### 16.2 Control Requirement Schema

```python
class PolicyControl(BaseModel):
    control_id:       str              # e.g. "DengBao-8.1.4"
    framework:        str
    title:            str
    description:      str
    scope_tags:       list[str]        # ["encryption", "audit", "network"]
    layer_relevance:  list[ScanLayer]  # [CODE, IAC, CLOUD]
    severity_weight:  float            # how heavily this control weighs in scoring
    test_procedures:  list[str]        # what to look for — feeds Athena's prompt
    evidence_types:   list[EvidenceType]
    chinese_title:    str | None       # for 等保 and Chinese regulatory frameworks
```

---

## 17. Remediation & Patch Generation

### 17.1 Remediation Types

| Type | Output Format | Agent Tool |
|---|---|---|
| Code patch | Unified diff (`git diff` format) | `generate_code_patch` |
| IaC fix | HCL / YAML diff | `generate_iac_patch` |
| Cloud CLI command | Shell commands (provider-specific) | `generate_cli_remediation` |
| Policy recommendation | Natural language + reference links | LLM direct output |
| Architecture guidance | Markdown section | LLM direct output |

### 17.2 Patch Safety Rules

Circe operates under strict guardrails:
- Patches are **diff-only** — never applied automatically
- All patches include a `test_suggestion` field (how to verify the fix)
- Patches for security-critical changes include a `risk_of_fix` field
- Multi-file patches include an ordering dependency graph
- No patch may introduce new `import` statements (reduces supply chain risk)

---

## 18. Report Assembly Pipeline

### 18.1 Report Structure

```
1. Executive Summary (auto-generated, LLM-polished)
2. Scan Metadata (repo, policy, timestamp, scan duration)
3. Compliance Score Dashboard (per-framework radar chart)
4. Critical Findings (CVSS >= 7.0) — with evidence + remediation
5. High Findings (CVSS 5.0–6.9)
6. Medium / Low Findings (summary table)
7. Cross-Layer Correlation Analysis (prose + diagram)
8. Dependency Risk Summary (vulnerable transitive deps)
9. Per-Framework Control Mapping Table
10. Remediation Roadmap (prioritized, with effort estimates)
11. Appendix A: Methodology
12. Appendix B: Evidence References (file:line citations)
13. Appendix C: Scan Configuration
```

### 18.2 Structured Output → PDF Pipeline

```
ComplianceFindings (Pydantic) → Penelope (Jinja2 templates) → Markdown
    → generate_pdf.py (ReportLab) → Encrypted PDF → Object Store
```

ReportLab is used for PDF generation with full CJK font support (STHeiti / Songti for Chinese reports). Diagrams are generated via matplotlib (system architecture) and mermaid-cli (pipeline flowcharts) and embedded as vector/rasterized images.

---

## 19. Error Handling, Resilience & Circuit Breakers

### 19.1 Error Taxonomy

| Error Class | Examples | Strategy |
|---|---|---|
| `TransientLLMError` | Rate limit, timeout | Exponential backoff, retry up to 3× |
| `StructuredOutputError` | LLM returned invalid JSON | Retry with error feedback in prompt (up to 2×) |
| `ToolExecutionError` | File not found, parse error | Log + mark file as `SKIPPED`, continue |
| `AgentFatalError` | Agent crashed after all retries | Mark scan stage as `FAILED`, notify |
| `ContextLengthError` | Prompt exceeds model limit | Trigger context compaction, retry |
| `CloudConnectorError` | API rate limit, auth failure | Partial scan with degraded cloud coverage |
| `ScanAbortError` | User-triggered abort or budget exceeded | Graceful shutdown, save partial state |

### 19.2 Circuit Breaker per LLM Provider

```python
from circuitbreaker import circuit

@circuit(failure_threshold=5, recovery_timeout=60, expected_exception=OpenAIError)
def call_openai(prompt: str) -> str: ...
```

When a provider's circuit opens, the LLM router automatically switches to the fallback provider.

---

## 20. Security & Secrets Architecture

### 20.1 Secrets Flow (Calypso)

All credentials (cloud API keys, LLM API keys, DB passwords) are managed by Calypso:

```
Agent needs cloud credentials
    → Requests short-lived token from Calypso
    → Calypso fetches from secrets store (AWS SM / Alibaba KMS / Vault)
    → Returns token with 15-minute TTL
    → Token used for cloud connector call
    → Token discarded (never written to state or logs)
```

### 20.2 Prompt Injection Defence

Code content reaches LLM prompts via RAG retrieval — it must be treated as untrusted input:

| Defence | Implementation |
|---|---|
| Content sanitisation | Strip null bytes, control characters before embedding |
| Prompt boundary markers | XML-style delimiters: `<code_evidence>...</code_evidence>` |
| Structured output enforcement | LLM returns Pydantic schema — free-form text injection is discarded |
| Tool call allowlist | Only pre-registered tools can be invoked — LLM cannot call arbitrary functions |
| Sandbox file access | `safe_read()` enforces chroot-style boundary around repo directory |

### 20.3 Data Classification in ScanState

```python
class DataClassification(Enum):
    PUBLIC        = "public"
    INTERNAL      = "internal"
    CONFIDENTIAL  = "confidential"   # default for all scan data
    SECRET        = "secret"         # credential values, raw source code
```

Fields classified as `SECRET` in `ScanState` are encrypted at rest in the checkpointer and never appear in LangSmith / LangFuse traces (redacted with `[REDACTED]`).

---

## 21. Performance, Scalability & Cost Model

### 21.1 Latency Budget (P95 targets)

| Stage | P95 Target | Primary Bottleneck |
|---|---|---|
| Hermes (ingestion) | 45s | Git clone + cloud enumeration |
| Tiresias (policy parse) | 15s | LLM call (cached after first parse) |
| Argus (indexing) | 2–8 min | tree-sitter parse + embedding batch |
| Laocoon + Cassandra (parallel) | 1–3 min | LLM calls per IaC resource |
| Athena (compliance mapping) | 2–5 min | Per-control LLM calls (batched) |
| Circe (remediation) | 1–2 min | Code patch generation |
| Penelope (report) | 30s | PDF rendering |
| **Total P95** | **< 10 min** | |

### 21.2 LLM Cost Estimate per Scan

| Tier | LOC | Estimated LLM Cost (USD) |
|---|---|---|
| Small repo | < 10k LOC | $0.08 – $0.20 |
| Medium repo | 10k – 100k LOC | $0.30 – $1.20 |
| Large repo | 100k – 500k LOC | $1.50 – $6.00 |
| With delta cache (active repo) | Any | 60–80% reduction |

### 21.3 Horizontal Scaling Architecture

```
API Gateway (stateless, N replicas)
    │
    ▼
Job Queue (Redis Streams / Kafka)
    │
    ▼
Odysseus Engine Workers (stateless, auto-scaled)
    │
    ├── Parallel branches: Laocoon + Cassandra run on separate workers
    │
    ▼
Shared State (PostgreSQL checkpointer + pgvector + Redis cache)
```

Workers are stateless — any worker can resume any scan from the PostgreSQL checkpointer.

---

## 22. Deployment Topologies

### 22.1 Topology Comparison

| Topology | Where | LLM | Data Residency | Target Segment |
|---|---|---|---|---|
| **SaaS** | DeepGuard-hosted cloud | OpenAI / Anthropic API | Customer accepts SaaS TOS | SME, startups |
| **Private Cloud** | Customer VPC (AWS/Ali/TCE/HW) | Bedrock / Qwen3 / Hunyuan | Full VPC isolation | Enterprise, regulated |
| **Air-gapped / Xinchuang** | On-prem bare metal / private DC | DeepSeek-R1 / Qwen3 (Ollama) | Never leaves premises | Gov, defence, 信创 |

### 22.2 Xinchuang-Specific Constraints

- All containers from certified domestic registries (e.g., Huawei SWR, Alibaba ACR)
- LLM: DeepSeek-R1 or Qwen3 served locally via Ollama or vLLM
- Embedding model: `bge-m3` (BAAI) served locally
- Encryption: SM4 (国密) for all data at rest; SM2/SM3 for TLS and signing
- No external SaaS dependencies (LangSmith replaced by self-hosted LangFuse)
- Vector DB: pgvector on domestic-hardware Postgres (Gauss-compatible schema)

---

## 23. Open Design Questions

The table below records questions that motivated deeper design. **MVP defaults that unblock implementation are locked in §23.1**; revisit any row when production metrics or regulation demand it.

| # | Question | Owner | Priority | Notes |
|---|---|---|---|---|
| 1 | Should Athena process all controls in a single LangGraph node, or should each control become its own sub-graph node (enabling per-control checkpointing and parallel execution)? | Arch | HIGH | Per-control parallelism could reduce Athena latency 5-10× but increases graph complexity significantly |
| 2 | What is the right semantic cache similarity threshold for compliance prompts? 0.97 is a first guess — needs empirical tuning against the gold dataset. | ML Eng | HIGH | Risk: too low → wrong cached answers; too high → near-zero cache hit rate |
| 3 | How should cross-tenant model fine-tuning work? Can we use anonymized finding patterns to fine-tune Athena without leaking customer code patterns? | ML Eng | MED | Federated fine-tuning or DP-SGD may be necessary |
| 4 | LangGraph `Send` API for fan-out: what happens if Cassandra finishes in 30s but Laocoon takes 8 min? Does the convergence gate incur memory pressure? | Eng | HIGH | Need to benchmark with large IaC repos |
| 5 | For the critic pass in Athena — should the critic use the same model as the generator, or a different (possibly cheaper) model? | ML Eng | MED | Using the same model may not produce independent critique |
| 6 | Dependency graph for monorepos: how do we bound the graph size for repos with 1000+ packages? Should we use a `max_depth` traversal limit? | Eng | MED | |
| 7 | How should the incremental delta scan handle policy version changes? If the policy changes between two scans, all affected findings from the prior scan should be re-evaluated. | Arch | HIGH | Invalidation scope could be large |
| 8 | LangFuse self-hosted for Xinchuang: what is the required hardware spec for a LangFuse instance that can handle 100 concurrent scan traces? | DevOps | LOW | |
| 9 | Should ReasoningTrace (full raw LLM output) be stored in LangFuse or in the customer's own PostgreSQL, and who holds the encryption key? | Security | HIGH | Critical for regulated industries |
| 10 | For Circe's patch generation: should we run the generated patch through a validation step (e.g., `terraform validate`, `tflint`, unit test execution) before including it in the report? | Eng | MED | Would significantly improve patch quality but adds latency |

### 23.1 MVP engineering decisions (default resolutions)

These defaults unblock implementation; revisit after first production traffic.

| # | Decision | MVP choice | Rationale |
|---|----------|------------|-----------|
| 1 | Athena graph shape | **Single `athena_node`** that processes controls in **batches** (see §31.3). Optional per-control `Send` subgraph is **Phase 2** behind feature flag `ATHENA_PER_CONTROL_SEND`. | Keeps checkpointing and debugging simple; batching preserves context efficiency from §10.5. |
| 2 | Semantic cache threshold | **0.97** default; tenant flag `semantic_cache_enabled` and override `semantic_cache_threshold` (range 0.95–0.99). | Start conservative; tune with `false-positive-registry` dataset (§7.3). |
| 3 | Cross-tenant fine-tuning | **Out of scope** for v0; collect opt-in telemetry schema only. | Legal + data minimisation; no training pipeline in MVP. |
| 4 | Fan-out memory | **Convergence gate** waits on **completion markers** + **artifact refs** for large branch payloads; never require both full IaC and full cloud snapshots in RAM on the gate node. | Avoids OOM when one branch is huge. |
| 5 | Critic model | **Same base model** as generator, **different system prompt**, `temperature=0`, separate trace span `athena_critic_pass`. Phase 2: optional second provider for independence. | Balance cost vs. critique diversity; measurable in LangSmith A/B. |
| 6 | Dependency graph caps | `max_depth=6`, `max_nodes=50_000`; on truncation set `dependency_graph.status=TRUNCATED` and surface warning in report §18.1. | Predictable memory/CPU for monorepos. |
| 7 | Delta + policy change | **Repo fingerprint** (§9.1) includes `policy_version`. On policy bump: invalidate L1 fingerprint hit; **re-run Athena (+ Circe + Penelope)** for all controls; Argus/Laocoon/Cassandra may be skipped if `repo_commit_sha` unchanged **and** `job_config.scan_layers` unchanged (feature flag `DELTA_SKIP_ANALYSIS`). | Correctness over savings until delta proven. |
| 8 | LangFuse self-hosted sizing | **v0 guidance:** 4 vCPU / 16 GiB RAM / 100 GiB SSD for ≤20 concurrent scans; scale horizontally for UI + ingest. Re-benchmark at 100 concurrent (original question). | Placeholder for infra ticket. |
| 9 | Reasoning trace storage | **Raw LLM output** → **tenant PostgreSQL** only (`reasoning_traces` table, app-level AES-256 or pgcrypto). LangFuse/LangSmith receive **redacted** generations (`raw_llm_output` stripped; max 4 KiB excerpt). | Meets regulated audit without shipping secrets to SaaS. |
| 10 | Circe validation | **Best-effort sandbox**: run `terraform fmt -check`, `terraform validate`, `tflint` when Terraform present; attach exit code + stdout/stderr to remediation record. **No** auto network in sandbox. Flag `remediation.validation_status`. | Quality uplift with bounded latency; failures do not fail scan. |

---

## 24. Feature flags and runtime_config schema

Section §23.1 is authoritative for product behaviour defaults. **Per-tenant overrides** live in `tenants.runtime_config` (JSONB). Keys are **snake_case** booleans, numbers, or enums.

### 24.1 Normative keys (v0)

```json
{
  "semantic_cache_enabled": true,
  "semantic_cache_threshold": 0.97,
  "athena_per_control_send": false,
  "delta_skip_analysis": false,
  "graph_interrupt_before_athena": false,
  "circe_terraform_validation": true,
  "max_concurrent_scans": 3,
  "retention_repo_archive_hours": 24
}
```

### 24.2 Merge semantics

At worker startup: `effective_config = deep_merge(DEFAULT_RUNTIME_CONFIG, tenants.runtime_config, scan_job_overrides?)`. **Scan-level** overrides are allowed only for `budget.*` and `notifications.*` (§28.4), not for safety flags like `semantic_cache_threshold` unless role `admin`.

---

## 25. Repository layout & ownership boundaries

### 25.1 Proposed monorepo tree

```
deepguard/
├── apps/
│   ├── api/                    # FastAPI: auth, job CRUD, signed URL issuance
│   └── worker/                 # LangGraph runner + tool executors (same image, different CMD)
├── packages/
│   ├── core/                   # Pydantic models: ScanState, Finding, PolicyControl, errors
│   ├── graph/                  # Odysseus StateGraph build, compile, checkpoint config
│   ├── agents/                 # Hermes…Penelope node factories (thin wrappers)
│   ├── tools/                  # @tool implementations; all filesystem access via RepoSandbox
│   ├── retrieval/              # pgvector + BM25 retriever wiring
│   ├── connectors/             # CloudConnector implementations + normalisers → ResourceSnapshot
│   ├── parsers/                # tree-sitter wrappers, IaC parser registry (§15.1)
│   ├── policies/               # Framework registry loaders; PDF/YAML ingestion adapters
│   └── reporting/              # Jinja templates, PDF pipeline (§18.2)
├── infra/
│   ├── terraform/              # modules per §22 / business docs
│   └── helm/                   # api, worker, migrations Job, langfuse (optional)
├── eval/
│   ├── datasets/               # JSONL gold sets (paths only; no secrets)
│   └── harness/                # LangSmith / offline eval runners
├── docker/
│   └── compose.dev.yml         # §34
└── docs/
    └── Architecture_Design.md
```

### 25.2 Dependency rules (import matrix)

| Package | May import | Must not import |
|---------|------------|-----------------|
| `core` | stdlib, pydantic | `langgraph`, cloud SDKs |
| `tools` | `core`, parser libs | `agents` (avoid cycles) |
| `agents` | `core`, `tools`, `retrieval`, `langchain*` | `apps.api` |
| `graph` | `agents`, `langgraph` | HTTP frameworks |
| `apps.*` | all packages | — |

Circular imports between `agents` and `graph` are forbidden: `graph` wires nodes; `agents` expose callables only.

---

## 26. Implementation stack & version pins

### 26.1 Language & packaging

- **Python:** 3.12.x (minimum 3.12; 3.13 acceptable once CI matrix passes).
- **Packaging:** `uv` or `pip-tools` for lockfiles; single workspace `pyproject.toml` with `[tool.uv.sources]` optional.
- **Containers:** distroless or `python:3.12-slim` non-root user `deepguard` (uid 10001).

### 26.2 Core libraries (minimum versions for API stability)

| Area | Library | Minimum version | Notes |
|------|---------|-----------------|-------|
| Graph | `langgraph` | ≥ 0.2.28 | Checkpointing + `Send` API |
| Chains | `langchain-core` | ≥ 0.3.15 | `Runnable`, messages, tools |
| HTTP | `fastapi` | ≥ 0.115 | `lifespan` context |
| ASGI | `uvicorn[standard]` | ≥ 0.30 | Workers = 1 per pod for in-memory graph unless graph externalised |
| DB | `sqlalchemy` | ≥ 2.0.36 | Async engine + `text()` migrations |
| Migrations | `alembic` | ≥ 1.13 | Required from day one |
| Validation | `pydantic` | ≥ 2.7 | `BaseModel`, JSON schema export |
| Postgres | `asyncpg` | ≥ 0.29 | Vector types via raw SQL or `pgvector` extension |
| Redis | `redis` (async) | ≥ 5.0 | Streams consumer groups |
| HTTP client | `httpx` | ≥ 0.27 | Cloud APIs, webhook delivery |
| Observability | `opentelemetry-sdk` | ≥ 1.25 | Exporter per deployment |
| PDF | `reportlab` | ≥ 4.2 | CJK fonts bundled in image layer |

Pin exact versions in `requirements.lock` per release branch.

### 26.3 LLM provider packages (install only what deployment uses)

| Provider | Extra name | Package |
|----------|------------|---------|
| OpenAI | `llm-openai` | `langchain-openai` |
| Anthropic | `llm-anthropic` | `langchain-anthropic` |
| AWS Bedrock | `llm-bedrock` | `langchain-aws` |
| Ollama / local | `llm-local` | `langchain-ollama` or OpenAI-compatible base URL |

Router (§13.2) selects implementation at runtime from `LLM_ROUTING_CONFIG` JSON.

---

## 27. Configuration surface (environment variables)

### 27.1 Global service config (API + worker)

| Variable | Required | Example | Purpose |
|----------|----------|---------|---------|
| `ENV` | yes | `prod` / `staging` / `dev` | Feature gating |
| `LOG_LEVEL` | no | `INFO` | Structured JSON logs |
| `DATABASE_URL` | yes | `postgresql+asyncpg://user:pass@host:5432/deepguard` | Metadata + traces + optional LangGraph checkpoints |
| `CHECKPOINT_DB_URL` | no | same as `DATABASE_URL` | Override when using dedicated checkpointer DB |
| `REDIS_URL` | yes | `redis://redis:6379/0` | Streams, cache, heartbeats |
| `OBJECT_STORE_URL` | yes | `s3://bucket` or `oss://` via compatible endpoint | Artifacts |
| `OBJECT_STORE_REGION` | yes | `ap-southeast-1` | SDK region |
| `OBJECT_STORE_SSE` | no | `aws:kms` | Encryption at rest |
| `LANGGRAPH_CHECKPOINT` | yes | `postgres` | `postgres` \| `memory` (tests only) |
| `LANGCHAIN_TRACING_V2` | no | `false` | LangSmith |
| `LANGSMITH_API_KEY` | no | — | Omit in air-gap |
| `LANGFUSE_HOST` | no | `https://langfuse.internal` | Self-hosted |
| `LANGFUSE_PUBLIC_KEY` / `LANGFUSE_SECRET_KEY` | no | — | SDK |
| `JWT_ISSUER` / `JWT_AUDIENCE` | yes (SaaS) | OIDC | API auth |
| `WEBHOOK_SIGNING_SECRET` | no | HMAC key | Outbound webhook signatures |
| `MAX_CONCURRENT_SCANS_PER_TENANT` | no | `3` | Backpressure (§35) |

### 27.2 Worker-only

| Variable | Required | Example | Purpose |
|----------|----------|---------|---------|
| `WORKER_CONCURRENCY` | no | `2` | Async scans per pod |
| `GRAPH_INTERRUPT_BEFORE_ATHENA` | no | `false` | Human gate (§4.7) |
| `REPO_CLONE_DEPTH` | no | `50` | Hermes shallow clone |
| `REPO_MAX_BYTES` | no | `2147483648` | 2 GiB soft cap before abort |
| `TOOL_SANDBOX_ROOT` | yes | `/var/deepguard/work` | Writable root for clones |

### 27.3 Secrets (never plain env in production)

Use **Calypso** pattern (§20.1): at runtime resolve `CALYPSO_BACKEND=aws_sm|vault|alibaba_kms` and inject **short-lived** credentials into process env **before** graph starts. Keys such as `OPENAI_API_KEY` must never be persisted in `ScanState`.

---

## 28. Control plane HTTP API (FastAPI)

### 28.1 API versioning

- Base path: **`/v1`**
- Breaking changes require `/v2`; deprecate with `Sunset` header (RFC 8594).

### 28.2 Authentication & tenancy

- **Enterprise:** Bearer JWT (OIDC) with claim `tenant_id` (UUID) and roles `scanner`, `admin`, `auditor`.
- **Machine:** optional mTLS for worker → internal API (certificate bound to `tenant_id`).
- Every row in DB is scoped by `tenant_id`; API middleware rejects cross-tenant paths.

### 28.3 Core resources

| Method | Path | Body / query | Response | Idempotency |
|--------|------|----------------|----------|---------------|
| `POST` | `/v1/scans` | `CreateScanRequest` JSON | `201` + `Scan` | `Idempotency-Key` header optional; if duplicate within 24h return same `scan_id` |
| `GET` | `/v1/scans/{scan_id}` | — | `Scan` + phase + percents | — |
| `GET` | `/v1/scans/{scan_id}/findings` | `?severity=&framework=&cursor=` | paginated `Finding` list | — |
| `GET` | `/v1/scans/{scan_id}/artifacts/{artifact_id}` | — | `302` to presigned GET or streaming proxy | Short TTL URLs |
| `POST` | `/v1/scans/{scan_id}/cancel` | optional reason | `202` | — |
| `POST` | `/v1/scans/{scan_id}/resume` | annotations for HITL | `202` | Requires `interrupt_before` cleared |
| `GET` | `/v1/policies` | — | list installed frameworks + versions | — |
| `POST` | `/v1/policies:upload` | multipart PDF/YAML | `policy_id` + `policy_version` | Admin role |

### 28.4 `CreateScanRequest` (normative JSON)

```json
{
  "repo": {
    "url": "https://github.com/acme/service",
    "ref": "main",
    "commit_sha": "optional-if-known"
  },
  "policy_ids": ["ISO-27001-2022", "GB-T-22239-2019"],
  "scan_layers": {
    "code": true,
    "iac": true,
    "cloud": true
  },
  "cloud_profiles": [
    {
      "profile_id": "aws-prod-readonly",
      "provider": "aws",
      "connector_credential_ref": "calypso://secret/aws-prod-ro",
      "regions": ["ap-southeast-1"]
    }
  ],
  "notifications": {
    "webhook_url": "https://customer.internal/hooks/deepguard",
    "on": ["completed", "failed"]
  },
  "budget": {
    "max_llm_usd": 12.5,
    "max_wall_seconds": 3600
  }
}
```

Validation rules: at least one of `repo` or `cloud_profiles` when `scan_layers.cloud`; `repo` required if `scan_layers.code` or `scan_layers.iac`.

### 28.5 `Scan` status model (API + DB)

```
PENDING → QUEUED → INGESTING → INDEXING → ANALYZING → MAPPING → REMEDIATING → REPORTING → COMPLETE
                      ↘ FAILED (terminal)   ↘ CANCELLED
                      ↘ AWAITING_REVIEW (HITL, §4.7)
```

Expose `current_stage`, `stage_started_at`, `percent_complete` (best-effort), `error_code` (stable machine string), `error_message` (sanitised).

### 28.6 Webhook delivery

- **Payload:** `{ "event": "scan.completed", "scan_id": "...", "tenant_id": "...", "report_artifact_id": "..." }`
- **Signature:** `X-DeepGuard-Signature: sha256=<hex>` over raw body with `WEBHOOK_SIGNING_SECRET`.
- **Retries:** exponential backoff 1m → 5m → 30m (max 24h); dead-letter row in `webhook_deliveries`.

---

## 29. Relational schema — tenancy, jobs, findings

Alembic owns migrations. Extension: `CREATE EXTENSION IF NOT EXISTS vector;`

### 29.1 Core tables (DDL sketch)

```sql
CREATE TABLE tenants (
    id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name            TEXT NOT NULL,
    runtime_config  JSONB NOT NULL DEFAULT '{}',
    created_at      TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE TABLE scans (
    id                      UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    tenant_id               UUID NOT NULL REFERENCES tenants(id),
    status                  TEXT NOT NULL,
    current_stage           TEXT NOT NULL,
    job_config              JSONB NOT NULL,
    repo_commit_sha         TEXT,
    policy_versions         JSONB NOT NULL DEFAULT '{}',
    percent_complete        SMALLINT NOT NULL DEFAULT 0,
    error_code              TEXT,
    error_message           TEXT,
    idempotency_key         TEXT,
    cancellation_requested  BOOLEAN NOT NULL DEFAULT false,
    created_at              TIMESTAMPTZ NOT NULL DEFAULT now(),
    updated_at              TIMESTAMPTZ NOT NULL DEFAULT now(),
    completed_at            TIMESTAMPTZ,
    UNIQUE (tenant_id, idempotency_key)
);

CREATE TABLE findings (
    id                  UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    tenant_id           UUID NOT NULL REFERENCES tenants(id),
    scan_id             UUID NOT NULL REFERENCES scans(id) ON DELETE CASCADE,
    framework           TEXT NOT NULL,
    control_id          TEXT NOT NULL,
    status              TEXT NOT NULL,
    severity            TEXT NOT NULL,
    title               TEXT NOT NULL,
    evidence_refs       JSONB NOT NULL,
    reasoning_summary   TEXT,
    confidence_score    DOUBLE PRECISION NOT NULL,
    policy_version      TEXT NOT NULL,
    created_at          TIMESTAMPTZ NOT NULL DEFAULT now()
);
CREATE INDEX findings_scan_idx ON findings (scan_id);
CREATE INDEX findings_control_idx ON findings (tenant_id, framework, control_id);

CREATE TABLE reasoning_traces (
    id                  UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    tenant_id           UUID NOT NULL REFERENCES tenants(id),
    scan_id             UUID NOT NULL REFERENCES scans(id) ON DELETE CASCADE,
    agent_id            TEXT NOT NULL,
    step_number         INT NOT NULL,
    step_type           TEXT NOT NULL,
    llm_model           TEXT,
    input_tokens        INT,
    output_tokens       INT,
    latency_ms          INT,
    raw_llm_payload     BYTEA,
    redacted_excerpt    TEXT,
    created_at          TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE TABLE artifacts (
    id                  UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    tenant_id           UUID NOT NULL REFERENCES tenants(id),
    scan_id             UUID NOT NULL REFERENCES scans(id) ON DELETE CASCADE,
    kind                TEXT NOT NULL,
    storage_uri         TEXT NOT NULL,
    checksum_sha256     TEXT NOT NULL,
    size_bytes          BIGINT NOT NULL,
    encryption          TEXT NOT NULL DEFAULT 'sse-kms',
    created_at          TIMESTAMPTZ NOT NULL DEFAULT now(),
    expires_at          TIMESTAMPTZ
);
```

### 29.2 LangGraph checkpointer

Prefer **official** `PostgresSaver` / async variant from `langgraph-checkpoint-postgres` when available; schema managed by the library plus Alembic glue migration. Store **no** `SECRET`-classified fields in checkpoint rows (§20.3); replace with `ArtifactRef` pointers.

### 29.3 pgvector collections

Reuse §12.1 `code_chunks` / `policy_chunks`; ensure **`tenant_id`** on `code_chunks`; `policy_chunks` may be shared catalog with `policy_version` scoping.

### 29.4 Webhook deliveries (DLQ)

```sql
CREATE TABLE webhook_deliveries (
    id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    tenant_id       UUID NOT NULL REFERENCES tenants(id),
    scan_id         UUID NOT NULL REFERENCES scans(id) ON DELETE CASCADE,
    event           TEXT NOT NULL,
    target_url      TEXT NOT NULL,
    payload         JSONB NOT NULL,
    attempt         INT NOT NULL DEFAULT 0,
    last_error      TEXT,
    next_attempt_at TIMESTAMPTZ,
    delivered_at    TIMESTAMPTZ,
    created_at      TIMESTAMPTZ NOT NULL DEFAULT now()
);
CREATE INDEX webhook_deliveries_due_idx ON webhook_deliveries (next_attempt_at) WHERE delivered_at IS NULL;
```

---

## 30. Async job execution & queue contract

### 30.1 Queue technology

- **Default:** Redis Streams key `stream:scans` with consumer group `workers`.
- **Enterprise option:** Kafka topic `deepguard.scans.v1` (same payload schema).

### 30.2 Message payload (`ScanJobMessage`)

```json
{
  "schema_ver": "1.0",
  "scan_id": "uuid",
  "tenant_id": "uuid",
  "enqueued_at": "2026-04-18T12:00:00Z",
  "priority": 0
}
```

Worker **must** verify `scans.status == QUEUED` before claim; use `XCLAIM` stale pending after visibility timeout (e.g. 15m).

### 30.3 Heartbeat & stall detection

- Key: `scan:{scan_id}:heartbeat` → TTL 120s; renewed every **30s** during graph execution.
- Watchdog process (sidecar or cron) marks `FAILED` with `error_code=WORKER_LOST` if heartbeat missing while status not terminal.

### 30.4 Cancellation

- API sets `cancellation_requested=true` on `scans` row and publishes optional control message on `stream:scans:control`.
- Worker checks cooperative cancel points between LangGraph nodes; on cancel, transition to `CANCELLED` and retain partial artifacts for audit.

---

## 31. LangGraph runtime contract

### 31.1 Compilation

- Build graph once at worker startup: `app = build_odysseus_graph().compile(checkpointer=checkpointer)`.
- **Thread ID:** `config["configurable"]["thread_id"] = str(scan_id)` — stable across retries.

### 31.2 Invocation modes

| Mode | When | Call pattern |
|------|------|--------------|
| Fresh run | New scan | `app.invoke(initial_state, config)` |
| Resume | Crash / HITL | `app.invoke(None, config)` per §4.6 |
| Stream (optional) | Progress UI | `app.astream_events` → translate to `Scan` progress fields |

### 31.3 Athena batching (MVP)

- Partition `policy_controls` into batches of **8–12** controls by clustering `scope_tags` + embedding similarity (cheap offline clustering at Tiresias output).
- Each batch: one generator LLM call + one critic LLM call; append findings to `ScanState` via reducer.
- Checkpoint **after each batch** to bound re-run cost on failure.

### 31.4 Error propagation

- Node catches `ToolExecutionError` → append `AgentError` to `error_log`, set partial outputs, **do not** raise unless `severity=fatal`.
- Fatal errors set `should_abort=True`; conditional edge routes to `error_handler` node which persists `FAILED` and writes `error_code`.

---

## 32. Object storage layout & lifecycle

### 32.1 Key layout

```
s3://{tenant_bucket}/tenants/{tenant_id}/scans/{scan_id}/
  repo.tar.zst
  cloud_snapshots/{profile_id}.json.zst
  reports/report.pdf
  embeddings/code_chunks.parquet
```

(`embeddings/` spill file optional for rebuild.)

### 32.2 Lifecycle

- Default: delete `repo.tar.zst` **24h** after `COMPLETE` (configurable).
- Reports: retain **7 years** (audit); transition to Glacier-class storage if supported.

---

## 33. Testing, CI gates, & golden datasets

### 33.1 Test pyramid

| Layer | Scope | Tools |
|-------|-------|-------|
| Unit | Pydantic models, parsers, `safe_read`, reducers | `pytest` |
| Contract | Each `CloudConnector` against recorded **VCR** fixtures (sanitised) | `pytest-recording` |
| Graph | Full graph with `MemorySaver` + **FakeListChatModel** | `langchain_core` test utils |
| Eval | Prompt/regression on gold datasets (§7.3) | LangSmith `pytest` plugin or CLI |

### 33.2 CI mandatory gates on `main`

- `ruff check`, `mypy` (strict on `packages/core`, `packages/graph`), `pytest -q` with coverage ≥ 80% on `tools/` parsers.
- **No merge** if `false-positive-registry` eval regression > 2% absolute.

### 33.3 Synthetic repo fixtures

Maintain `eval/fixtures/repos/` minimal apps covering: SQLi, weak crypto, IAM `*`, public S3, K8s privileged pod — used for smoke + golden expectations.

---

## 34. Local development topology

`docker compose -f docker/compose.dev.yml up`:

| Service | Image / build | Ports | Notes |
|---------|---------------|-------|-------|
| `postgres` | `pgvector/pgvector:pg16` | 5432 | init.sql enables extension |
| `redis` | `redis:7` | 6379 | |
| `minio` | `minio/minio` | 9000 | S3 compatible |
| `api` | build `apps/api` | 8000 | hot reload |
| `worker` | build `apps/worker` | — | `LLM_MODE=fake` uses deterministic FakeLLM |
| `ollama` | optional | 11434 | Local Qwen smoke |

Developer flow: `uv run alembic upgrade head`; seed tenant; `POST /v1/scans` against fixture repo URL or `file://` volume mount (Hermes dev adapter).

---

## 35. Operational hooks (SLOs, backpressure, runbooks)

### 35.1 SLOs (initial)

- API availability **99.5%** monthly.
- P95 scan duration **< 10 min** for reference repo ≤ 500k LOC (§21.1).
- Webhook success **99%** within 24h excluding customer endpoint failures.

### 35.2 Backpressure

- Enforce `MAX_CONCURRENT_SCANS_PER_TENANT` at enqueue; HTTP `429` with `Retry-After` when exceeded.
- Global queue depth alert when **> 500** pending for **15m** (scale workers).

### 35.3 Runbook triggers (PagerDuty / Opsgenie)

| Alert | Condition | First action |
|-------|-----------|---------------|
| LLM provider circuit open | §19.2 | Confirm router fallback; page if all circuits open |
| Checkpoint DB lag | replication lag > 30s | Pause new scans; fail-safe read-only |
| Disk pressure on worker | `/var/deepguard/work` > 85% | Drain node; evict oldest staged repos |

---

*Document status: v0.2 adds implementation contracts (§24–§35). §23.1 is the engineering default until superseded by ADR.*

*Next steps: (1) Scaffold monorepo per §25. (2) Land Alembic migrations for §29. (3) Implement `/v1/scans` + worker consumer per §28–§30. Owner: Engineering Lead.*
