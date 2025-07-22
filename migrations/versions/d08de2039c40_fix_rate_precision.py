"""fix_rate_precision

Revision ID: d08de2039c40
Revises: a4177eb1b6dc
Create Date: 2025-07-22 10:57:38.127197

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'd08de2039c40'
down_revision: Union[str, Sequence[str], None] = 'a4177eb1b6dc'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.alter_column('ExchangeRates', 'rate',
                    type_=sa.Numeric(12, 6),
                    existing_type=sa.Numeric(9, 6))


def downgrade() -> None:
    """Downgrade schema."""
    op.alter_column('ExchangeRates', 'rate',
                    type_=sa.Numeric(9, 6),
                    existing_type=sa.Numeric(12, 6))
