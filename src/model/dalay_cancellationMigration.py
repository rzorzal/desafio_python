from datetime import datetime
from sqlalchemy import Column, DateTime, Integer, Float, Text, create_engine
from sqlalchemy.ext.declarative import declarative_base

# # Define database connection
# engine = create_engine(
#     "postgresql+psycopg2://postgres:postgres@localhost/airline?client_encoding=utf8"
# )

# Define class model
Base = declarative_base()

class DalayCancellation(Base):
    __tablename__ = "dalay_cancellation"
    id = Column(Integer, primary_key=True)

    FL_DATE = Column(Text, default="NaN")
    OP_CARRIER = Column(Text, default="NaN")
    OP_CARRIER_FL_NUM = Column(Text, default="NaN")
    ORIGIN = Column(Text, default="NaN")
    DEST = Column(Text, default="NaN")
    CRS_DEP_TIME = Column(Text, default="NaN")
    DEP_TIME = Column(Text, default="NaN")
    DEP_DELAY = Column(Text, default="NaN")
    TAXI_OUT = Column(Text, default="NaN")
    WHEELS_OFF = Column(Text, default="NaN")
    WHEELS_ON = Column(Text, default="NaN")
    TAXI_IN = Column(Text, default="NaN")
    CRS_ARR_TIME = Column(Text, default="NaN")
    ARR_TIME = Column(Text, default="NaN")
    ARR_DELAY = Column(Text, default="NaN")
    CANCELLED = Column(Text, default="NaN")
    CANCELLATION_CODE = Column(Text, default="NaN")
    DIVERTED = Column(Text, default="NaN")
    CRS_ELAPSED_TIME = Column(Text, default="NaN")
    ACTUAL_ELAPSED_TIME = Column(Text, default="NaN")
    AIR_TIME = Column(Text, default="NaN")
    DISTANCE = Column(Text, default="NaN")
    CARRIER_DELAY = Column(Text, default="NaN")
    WEATHER_DELAY = Column(Text, default="NaN")
    NAS_DELAY = Column(Text, default="NaN")
    SECURITY_DELAY = Column(Text, default="NaN")
    LATE_AIRCRAFT_DELAY = Column(Text, default="NaN")
    createdAt = Column(DateTime, default=datetime.now())

# Create tables in database
# Base.metadata.create_all(bind=engine)
