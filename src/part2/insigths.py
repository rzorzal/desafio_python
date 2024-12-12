from sqlalchemy import create_engine, text
from sqlalchemy.orm import Session, sessionmaker
# from src.model.flightMigration import Flight
from src.model.dalay_cancellationMigration import DalayCancellation
from src.model.usersInsightsMigration import UsersInsightsView
from sqlalchemy import select
from src.utils.getEnvironment import GetEnvironment

DATABASE_USER       = GetEnvironment().get("DATABASE_USER")
DATABASE_PASSWORD   = GetEnvironment().get("DATABASE_PASSWORD")
DATABASE_HOST       = GetEnvironment().get("DATABASE_HOST")
DATABASE_NAME       = GetEnvironment().get("DATABASE_NAME")

# Define database connection
engine = create_engine(
    f"postgresql+psycopg2://{DATABASE_USER}:{DATABASE_PASSWORD}@{DATABASE_HOST}/{DATABASE_NAME}?client_encoding=utf8"
)

Session = sessionmaker(bind=engine)
session = Session()

class UsersInsights():
        
    def generateInsigths(self):

        sql = text("select * from data_transformation_view")
        stmt = session.execute(sql).all()
        for row in stmt:
            delay_average = int(row.CARRIER_DELAY + row.WEATHER_DELAY + row.NAS_DELAY + row.SECURITY_DELAY + row.LATE_AIRCRAFT_DELAY) / 5
            print(f"Airline name:  {row.OP_CARRIER}, Delay average: {delay_average}, Total time flight: {int(row.AIR_TIME)}")
