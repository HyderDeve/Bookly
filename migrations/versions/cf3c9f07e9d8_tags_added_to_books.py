"""tags added to books

Revision ID: cf3c9f07e9d8
Revises: 8f04bb123315
Create Date: 2025-07-02 15:51:12.631959

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
import sqlmodel


# revision identifiers, used by Alembic.
revision: str = 'cf3c9f07e9d8'
down_revision: Union[str, None] = '8f04bb123315'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
