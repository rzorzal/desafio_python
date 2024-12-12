from alembic import op
import uuid

# Revisão Alembic
revision = uuid.uuid4()
down_revision = uuid.uuid4()
branch_labels = None
depends_on = None

def upgrade():
    # Criação da view
    op.execute("""
    CREATE VIEW data_transformation_view AS
    select 
	item."OP_CARRIER",
	sum(item."CARRIER_DELAY") as CARRIER_DELAY, 
	sum(item."WEATHER_DELAY") as WEATHER_DELAY,
	sum(item."NAS_DELAY") as NAS_DELAY,
	sum(item."SECURITY_DELAY") as SECURITY_DELAY,
	sum(item."SECURITY_DELAY") as LATE_AIRCRAFT_DELAY,
	sum(item."AIR_TIME") as AIR_TIME 
	from flight item 
	where item."CARRIER_DELAY" !=  'NaN'
	group by item."OP_CARRIER";
    """)

def downgrade():
    # Remoção da view
    op.execute("DROP VIEW data_transformation_view;")

    
