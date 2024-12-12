"""insights table

Revision ID: 32853ba357f0
Revises: 2c540606d300
Create Date: 2024-12-12 17:30:22.905952

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '32853ba357f0'
down_revision: Union[str, None] = '2c540606d300'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        'users_insights',
        sa.Column('id', sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column('OP_CARRIER', sa.String, nullable=False),
        sa.Column('DELAY_AVERAGE', sa.Float(), default=0),
        sa.Column('TOTAL_AIR_TIME', sa.Integer(), default=0),
        sa.Column('CREATED_AT', sa.DateTime(), server_default=sa.func.now())
    )
    pass


def downgrade() -> None:
    op.drop_table('users_insights')
    pass
