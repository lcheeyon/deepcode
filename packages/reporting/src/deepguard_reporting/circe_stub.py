"""Circe remediation — diff-only, never auto-apply (Phase L11)."""

from __future__ import annotations

from uuid import UUID, uuid4

from deepguard_core.models.remediation import Remediation


def build_remediation_diff_only(
    *,
    scan_id: UUID,
    finding_id: UUID | None,
    title: str,
) -> Remediation:
    """Return a remediation with unified-diff style preview only (no filesystem writes)."""

    return Remediation(
        id=uuid4(),
        scan_id=scan_id,
        finding_id=finding_id,
        title=title,
        diff_preview=(
            "--- a/main.tf\n+++ b/main.tf\n@@ -1,3 +1,3 @@\n"
            "-  insecure = true\n+  insecure = false\n"
        ),
        terraform_validate_exit_code=None,
    )
