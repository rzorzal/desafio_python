"""create flight_raw table

Revision ID: 9c1cbfdff044
Revises: 3f2faf536fc0
Create Date: 2024-12-03 00:12:56.026016

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '9c1cbfdff044'
down_revision: Union[str, None] = '3f2faf536fc0'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute("""
    CREATE TABLE flight_raw (
        id UUID DEFAULT uuid_generate_v4() PRIMARY KEY,
        FL_DATE TIMESTAMP NOT NULL,
        OP_CARRIER VARCHAR NOT NULL,
        OP_CARRIER_FL_NUM VARCHAR NOT NULL,
        ORIGIN VARCHAR NOT NULL,
        DEST VARCHAR NOT NULL,
        CRS_DEP_TIME INTEGER NOT NULL,
        DEP_TIME REAL NULL,
        DEP_DELAY REAL NULL,
        TAXI_OUT REAL NULL,
        WHEELS_OFF REAL NULL,
        WHEELS_ON REAL NULL,
        TAXI_IN REAL NULL,
        CRS_ARR_TIME INTEGER NOT NULL,
        ARR_TIME REAL NULL,
        ARR_DELAY REAL NULL,
        CANCELLED INTEGER NOT NULL,
        CANCELLATION_CODE VARCHAR NULL,
        DIVERTED INTEGER NOT NULL,
        CRS_ELAPSED_TIME REAL NOT NULL,
        ACTUAL_ELAPSED_TIME REAL NULL,
        AIR_TIME REAL NULL,
        DISTANCE REAL NOT NULL,
        CARRIER_DELAY REAL NULL,
        WEATHER_DELAY REAL NULL,
        NAS_DELAY REAL NULL,
        SECURITY_DELAY REAL NULL,
        LATE_AIRCRAFT_DELAY REAL NULL,
        created_at TIMESTAMP DEFAULT (now())
    );
""")


def downgrade() -> None:
    op.execute("""
        DROP TABLE flight_raw;
    """)
