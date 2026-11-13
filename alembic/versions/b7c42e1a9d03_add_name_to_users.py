"""add name to users

Revision ID: b7c42e1a9d03
Revises: 6b06907d4a39
Create Date: 2026-11-13

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "b7c42e1a9d03"
down_revision: Union[str, Sequence[str], None] = "6b06907d4a39"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column("users", sa.Column("name", sa.String(length=255), nullable=True))


def downgrade() -> None:
    op.drop_column("users", "name")
