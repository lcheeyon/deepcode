# BDD scenarios — DeepGuard benchmark campaign (10 OSS repos)

Backed by `docs/benchmarks/deepguard-benchmark-manifest.json`.

Purpose: exercise scan creation paths (git + archive-style input), poll scan completion, and validate eventual compliance report retrieval endpoints to support GitHub sharing of evidence.

## Feature: Benchmark scan campaign setup

**Scenario: Verify API connectivity and benchmark corpus loaded**  
Given the operator has configured API base URL and key  
When the campaign test starts  
Then `/v1/healthz` is reachable and the manifest has 10 benchmark entries.

## Feature: Create benchmark scans from manifest

**Scenario: Create all benchmark scans (mix of git and archive ingestion)**  
Given benchmark entries with source mode `git` or `zip_archive`  
When the operator (or automation) submits scan requests for each entry  
Then each request returns `201` with a valid `scan_id`.

## Feature: Track completion and reports

**Scenario: Poll scans to terminal states and capture report references**  
Given created benchmark scan IDs  
When scan statuses are polled  
Then each scan reaches a terminal state and complete scans expose report artifact references.

**Scenario: Resolve report download endpoint**  
Given a completed scan with report artifact id/reference  
When the artifact endpoint is requested  
Then the response is a valid report retrieval path (typically `302` redirect or authenticated stream `200`).

## Feature: Publish benchmark evidence to GitHub

**Scenario: Build reviewer/investor summary bundle**  
Given completed benchmark scan metadata and report links  
When the export script/build step runs  
Then a GitHub-shareable summary (markdown index + report links/files) is produced without secrets.
