# DeepGuard local targets (see IMPLEMENTATION_PLAN.md)

.PHONY: e2e-local e2e-full pre-commit ci-quality audit docs docs-serve

# Requires a git checkout (pre-commit uses git for hook metadata and remote revs).
pre-commit:
	python3 -m pre_commit run --all-files

# Full gate without relying on git (mirrors pre-commit hooks + deptry + pytest --cov).
ci-quality:
	bash scripts/ci_quality.sh

# Dependency hygiene (may fail on transitive CVEs until pins/upgrades are triaged). Run in CI separately if desired.
audit:
	python3 -m deptry .
	python3 -m pip_audit

# Prerequisites: compose up, alembic upgrade head, seed_dev_tenant.py, API on :8000 with DB+Redis.
e2e-local:
	@echo "Running L12 HTTP e2e (override pytest addopts so integration tests run)."
	DEEPGUARD_E2E_LOCAL=1 \
	DEEPGUARD_API_BASE=$${DEEPGUARD_API_BASE:-http://127.0.0.1:8000} \
	DEEPGUARD_DEV_API_KEY=$${DEEPGUARD_DEV_API_KEY:-dev} \
	python3 -m pytest tests/e2e -m integration \
	  --override-ini="addopts=-q --strict-markers" -v

# One-shot: compose + migrate + seed + uvicorn + worker + pytest poll for COMPLETE (requires dev deps).
e2e-full:
	bash scripts/e2e_full_scan.sh

# Static docs ([Material for MkDocs](https://squidfunk.github.io/mkdocs-material/)); requires `pip3 install -e ".[docs]"`.
docs:
	python3 -m mkdocs build --strict

docs-serve:
	python3 -m mkdocs serve
