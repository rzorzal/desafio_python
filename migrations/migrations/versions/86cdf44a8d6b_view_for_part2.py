"""view for part2

Revision ID: 86cdf44a8d6b
Revises: 
Create Date: 2024-12-12 01:00:30.168144

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '86cdf44a8d6b'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Create view
    op.execute("""
    CREATE VIEW data_transformation_view AS
    
    select 
	item."OP_CARRIER",
	sum(item."CARRIER_DELAY") as "TOTAL_CARRIER_DELAY", 
	sum(item."WEATHER_DELAY") as "TOTAL_WEATHER_DELAY",
	sum(item."NAS_DELAY") as "TOTAL_NAS_DELAY",
	sum(item."SECURITY_DELAY") as "TOTAL_SECURITY_DELAY",
	sum(item."LATE_AIRCRAFT_DELAY") as "TOTAL_LATE_AIRCRAFT_DELAY",
	sum(item."AIR_TIME") as "TOTAL_AIR_TIME",
    ROUND(AVG(item."CARRIER_DELAY" + item."WEATHER_DELAY" + item."NAS_DELAY" + item."SECURITY_DELAY" + item."LATE_AIRCRAFT_DELAY")::numeric, 2) AS "DELAY_AVERAGE"
	from flight item 
	where item."CARRIER_DELAY" !=  'NaN'
	group by item."OP_CARRIER";

    """)

def downgrade() -> None:
    # Remove view
    op.execute("DROP VIEW data_transformation_view;")
