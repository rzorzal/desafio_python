from datetime import datetime
from sqlalchemy import Column, DateTime, Integer, Text, Float
from sqlalchemy.ext.declarative import declarative_base

# Define class model
Base = declarative_base()

class UsersInsights(Base):
    __tablename__ = "users_insights"
    id = Column(Integer, primary_key=True)
    OP_CARRIER = Column(Text, default="NaN", nullable=True)
    DELAY_AVERAGE = Column(Float, default=0, nullable=True)
    TOTAL_AIR_TIME = Column(Integer, default=0, nullable=True)
    CREATED_AT = Column(DateTime, default=datetime.now())

class UsersInsightsView():
    __tablename__ = 'data_transformation_view'
    __table_args__ = {'info': dict(is_view=True)}