"""Scan run timeline + external trace refs (US-DG-12-015 / US-DG-14-015–018)."""

from __future__ import annotations

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

revision = "0003_scan_workflow_observability"
down_revision = "0002_policy_uploads"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "scan_run_events",
        sa.Column(
            "id",
            postgresql.UUID(as_uuid=True),
            primary_key=True,
            server_default=sa.text("gen_random_uuid()"),
        ),
        sa.Column(
            "tenant_id",
            postgresql.UUID(as_uuid=True),
            sa.ForeignKey("tenants.id"),
            nullable=False,
        ),
        sa.Column(
            "scan_id",
            postgresql.UUID(as_uuid=True),
            sa.ForeignKey("scans.id", ondelete="CASCADE"),
            nullable=False,
        ),
        sa.Column(
            "event_seq",
            sa.BigInteger(),
            sa.Identity(always=True),
            nullable=False,
        ),
        sa.Column("event_type", sa.Text(), nullable=False),
        sa.Column("node", sa.Text(), nullable=True),
        sa.Column("correlation_id", sa.Text(), nullable=True),
        sa.Column("graph_version", sa.Text(), nullable=True),
        sa.Column(
            "payload",
            postgresql.JSONB(astext_type=sa.Text()),
            nullable=False,
            server_default="{}",
        ),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            nullable=False,
            server_default=sa.text("now()"),
        ),
    )
    op.create_index(
        "scan_run_events_scan_event_seq_idx", "scan_run_events", ["scan_id", "event_seq"]
    )
    op.create_index(
        "scan_run_events_tenant_scan_idx", "scan_run_events", ["tenant_id", "scan_id"]
    )

    op.create_table(
        "scan_external_trace_refs",
        sa.Column(
            "id",
            postgresql.UUID(as_uuid=True),
            primary_key=True,
            server_default=sa.text("gen_random_uuid()"),
        ),
        sa.Column(
            "tenant_id",
            postgresql.UUID(as_uuid=True),
            sa.ForeignKey("tenants.id"),
            nullable=False,
        ),
        sa.Column(
            "scan_id",
            postgresql.UUID(as_uuid=True),
            sa.ForeignKey("scans.id", ondelete="CASCADE"),
            nullable=False,
        ),
        sa.Column("vendor", sa.Text(), nullable=False),
        sa.Column("root_run_id", sa.Text(), nullable=True),
        sa.Column("trace_id", sa.Text(), nullable=True),
        sa.Column("project_id", sa.Text(), nullable=True),
        sa.Column("workspace_id", sa.Text(), nullable=True),
        sa.Column(
            "trace_metadata",
            postgresql.JSONB(astext_type=sa.Text()),
            nullable=False,
            server_default="{}",
        ),
        sa.Column(
            "updated_at",
            sa.DateTime(timezone=True),
            nullable=False,
            server_default=sa.text("now()"),
        ),
        sa.UniqueConstraint("tenant_id", "scan_id", "vendor", name="uq_scan_external_trace_vendor"),
    )
    op.create_index(
        "scan_external_trace_refs_scan_idx", "scan_external_trace_refs", ["scan_id"]
    )


def downgrade() -> None:
    op.drop_index("scan_external_trace_refs_scan_idx", table_name="scan_external_trace_refs")
    op.drop_table("scan_external_trace_refs")
    op.drop_index("scan_run_events_tenant_scan_idx", table_name="scan_run_events")
    op.drop_index("scan_run_events_scan_seq_idx", table_name="scan_run_events")
    op.drop_table("scan_run_events")
