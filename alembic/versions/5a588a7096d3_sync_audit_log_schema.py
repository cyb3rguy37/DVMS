"""sync audit log schema

Revision ID: 5a588a7096d3
Revises: f135c89e4aab
"""

from alembic import op
import sqlalchemy as sa


revision = "5a588a7096d3"
down_revision = "f135c89e4aab"
branch_labels = None
depends_on = None


def upgrade():
    # SQLite requires recreating the table for this type of schema change.

    op.create_table(
        "audit_logs_new",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column(
            "actor_id",
            sa.Integer(),
            sa.ForeignKey("users.id"),
            nullable=False,
        ),
        sa.Column(
            "visit_id",
            sa.Integer(),
            sa.ForeignKey("visits.id"),
            nullable=True,
        ),
        sa.Column(
            "event_type",
            sa.String(length=18),
            nullable=False,
        ),
        sa.Column("event_data", sa.Text(), nullable=True),
        sa.Column(
            "previous_hash",
            sa.String(length=64),
            nullable=False,
        ),
        sa.Column(
            "current_hash",
            sa.String(length=64),
            nullable=False,
            unique=True,
        ),
        sa.Column("timestamp", sa.DateTime(), nullable=True),
    )

    # Preserve existing audit records.
    # Existing visitor_id values cannot safely be converted to visit_id,
    # because one visitor may have multiple visits.
    op.execute(
        """
        INSERT INTO audit_logs_new (
            id,
            actor_id,
            event_type,
            event_data,
            previous_hash,
            current_hash,
            timestamp
        )
        SELECT
            id,
            actor_id,
            event_type,
            event_data,
            previous_hash,
            current_hash,
            timestamp
        FROM audit_logs
        """
    )

    op.drop_table("audit_logs")

    op.rename_table(
        "audit_logs_new",
        "audit_logs"
    )


def downgrade():
    op.create_table(
        "audit_logs_old",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column(
            "actor_id",
            sa.Integer(),
            sa.ForeignKey("users.id"),
            nullable=False,
        ),
        sa.Column(
            "visitor_id",
            sa.Integer(),
            sa.ForeignKey("visitors.id"),
            nullable=True,
        ),
        sa.Column(
            "event_type",
            sa.String(length=18),
            nullable=False,
        ),
        sa.Column("event_data", sa.Text(), nullable=True),
        sa.Column(
            "previous_hash",
            sa.String(length=64),
            nullable=False,
        ),
        sa.Column(
            "current_hash",
            sa.String(length=64),
            nullable=False,
            unique=True,
        ),
        sa.Column("timestamp", sa.DateTime(), nullable=True),
    )

    op.execute(
        """
        INSERT INTO audit_logs_old (
            id,
            actor_id,
            event_type,
            event_data,
            previous_hash,
            current_hash,
            timestamp
        )
        SELECT
            id,
            actor_id,
            event_type,
            event_data,
            previous_hash,
            current_hash,
            timestamp
        FROM audit_logs
        """
    )

    op.drop_table("audit_logs")

    op.rename_table(
        "audit_logs_old",
        "audit_logs"
    )
