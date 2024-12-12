"""princial table

Revision ID: 2c540606d300
Revises: 86cdf44a8d6b
Create Date: 2024-12-12 16:36:01.995833

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = '2c540606d300'
down_revision: Union[str, None] = '86cdf44a8d6b'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        'flight',
        sa.Column('id', sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column('FL_DATE', sa.DateTime, nullable=False, server_default=sa.func.now()),
        sa.Column('OP_CARRIER', sa.String()),
        sa.Column('OP_CARRIER_FL_NUM', sa.Integer(), default=0),
        sa.Column('ORIGIN', sa.String(), default="NaN"),
        sa.Column('DEST', sa.String(), default="NaN"),
        sa.Column('CRS_DEP_TIME', sa.Integer(), default=0),
        sa.Column('DEP_TIME', sa.Float(), default=0),
        sa.Column('DEP_DELAY', sa.Float(), default=0),
        sa.Column('TAXI_OUT', sa.Float(), default=0),
        sa.Column('WHEELS_OFF', sa.Float(), default=0),
        sa.Column('WHEELS_ON', sa.Float(), default=0),
        sa.Column('CRS_ARR_TIME', sa.Integer(), default=0),
        sa.Column('TAXI_IN', sa.Float(), default=0),
        sa.Column('ARR_DELAY', sa.Float(), default=0),
        sa.Column('CANCELLED', sa.Float(), default=0),
        sa.Column('CANCELLATION_CODE', sa.String(), default="NaN"),
        sa.Column('DIVERTED', sa.Float(), default=0),
        sa.Column('CRS_ELAPSED_TIME', sa.Float(), default=0),
        sa.Column('ACTUAL_ELAPSED_TIME', sa.Float(), default=0),
        sa.Column('AIR_TIME', sa.Float(), default=0),
        sa.Column('DISTANCE', sa.Float(), default=0),
        sa.Column('CARRIER_DELAY', sa.Float(), default=0),
        sa.Column('WEATHER_DELAY', sa.Float(), default=0),
        sa.Column('NAS_DELAY', sa.Float(), default=0),
        sa.Column('SECURITY_DELAY', sa.Float(), default=0),
        sa.Column('LATE_AIRCRAFT_DELAY', sa.Float(), default=0),
        sa.Column('CREATED_AT', sa.DateTime, nullable=False, server_default=sa.func.now()),
    )
    pass


def downgrade() -> None:
    op.drop_table('flight')
    pass
