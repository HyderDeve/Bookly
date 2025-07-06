"""added tables again with extra fields

Revision ID: b9e801602a1c
Revises: cf3c9f07e9d8
Create Date: 2025-07-06 22:14:50.633583

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
import sqlmodel


# revision identifiers, used by Alembic.
revision: str = 'b9e801602a1c'
down_revision: Union[str, None] = 'cf3c9f07e9d8'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
