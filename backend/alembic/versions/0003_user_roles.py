"""Add explicit operator and demo roles to user accounts."""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = "0003_user_roles"
down_revision: str | None = "0002_command_expiration"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    columns = {column["name"] for column in sa.inspect(op.get_bind()).get_columns("users")}
    if "role" not in columns:
        op.add_column(
            "users",
            sa.Column("role", sa.String(length=20), nullable=False, server_default="operator"),
        )


def downgrade() -> None:
    columns = {column["name"] for column in sa.inspect(op.get_bind()).get_columns("users")}
    if "role" in columns:
        op.drop_column("users", "role")
