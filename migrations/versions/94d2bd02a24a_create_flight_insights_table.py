"""create flight_insights table

Revision ID: 94d2bd02a24a
Revises: 9c1cbfdff044
Create Date: 2024-12-03 09:21:56.636757

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '94d2bd02a24a'
down_revision: Union[str, None] = '9c1cbfdff044'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute("""
    CREATE TABLE flight_insights (
        id UUID DEFAULT uuid_generate_v4() PRIMARY KEY,
        airline VARCHAR NOT NULL,
        flight_number VARCHAR NOT NULL,
        origin VARCHAR NOT NULL,
        average_delay REAL NOT NULL,
        total_air_time REAL NOT NULL,
        amount_of_times_flew INTEGER NOT NULL,
        cancellation_chance REAL NOT NULL,
        created_at TIMESTAMP DEFAULT (now())
    );
""")


def downgrade() -> None:
    op.execute("""
        DROP TABLE flight_insights;
    """)
