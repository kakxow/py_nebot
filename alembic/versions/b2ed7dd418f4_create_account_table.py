"""create account table

Revision ID: b2ed7dd418f4
Revises:
Create Date: 2022-12-21 13:03:24.565916

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "b2ed7dd418f4"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "account",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("name", sa.String(50), nullable=False),
        sa.Column("description", sa.Unicode(200)),
    )


def downgrade() -> None:
    op.drop_table("account")
