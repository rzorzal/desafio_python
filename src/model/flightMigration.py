from datetime import datetime
from sqlalchemy import Column, DateTime, Integer, Text, Float
from sqlalchemy.ext.declarative import declarative_base

# Define class model
Base = declarative_base()

class Flight(Base):
    __tablename__ = "flight"
    id = Column(Integer, primary_key=True)

    FL_DATE = Column(DateTime, default=datetime.now())
    OP_CARRIER = Column(Text, default="NaN")
    OP_CARRIER_FL_NUM = Column(Integer, default=0)
    ORIGIN = Column(Text, default="NaN")
    DEST = Column(Text, default="NaN")
    CRS_DEP_TIME = Column(Integer, default=0)
    DEP_TIME = Column(Float, default=0)
    DEP_DELAY = Column(Float, default=0)
    TAXI_OUT = Column(Float, default=0)
    WHEELS_OFF = Column(Float, default=0)
    WHEELS_ON = Column(Float, default=0)
    TAXI_IN = Column(Float, default=0)
    CRS_ARR_TIME = Column(Integer, default=0)
    ARR_TIME = Column(Float, default=0)
    ARR_DELAY = Column(Float, default=0)
    CANCELLED = Column(Float, default=0)
    CANCELLATION_CODE = Column(Text, default="NaN")
    DIVERTED = Column(Float, default=0)
    CRS_ELAPSED_TIME = Column(Float, default=0)
    ACTUAL_ELAPSED_TIME = Column(Float, default=0)
    AIR_TIME = Column(Float, default=0)
    DISTANCE = Column(Float, default=0)
    CARRIER_DELAY = Column(Float, default=0.0)
    WEATHER_DELAY = Column(Float, default=0)
    NAS_DELAY = Column(Float, default=0)
    SECURITY_DELAY = Column(Float, default=0)
    LATE_AIRCRAFT_DELAY = Column(Float, default=0)
    CREATED_AT = Column(DateTime, default=datetime.now())

