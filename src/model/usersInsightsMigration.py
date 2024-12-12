from datetime import datetime
from sqlalchemy import Column, DateTime, Integer, Text
from sqlalchemy.ext.declarative import declarative_base

# Define class model
Base = declarative_base()

class UsersInsights(Base):
    __tablename__ = "users_insights"
    id = Column(Integer, primary_key=True)
    CARRIER_DELAY = Column(Text, default="NaN", nullable=True)
    WEATHER_DELAY = Column(Text, default="NaN", nullable=True)
    NAS_DELAY = Column(Text, default="NaN", nullable=True)
    SECURITY_DELAY = Column(Text, default="NaN", nullable=True)
    LATE_AIRCRAFT_DELAY = Column(Text, default="NaN", nullable=True)
    AIR_TIME = Column(Text, default="NaN", nullable=True)
    CREATED_AT = Column(DateTime, default=datetime.now())

class UsersInsightsView():
    __tablename__ = 'data_transformation_view'
    __table_args__ = {'info': dict(is_view=True)}