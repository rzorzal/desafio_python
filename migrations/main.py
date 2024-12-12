from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from src.utils.getEnvironment import GetEnvironment

DATABASE_USER       = GetEnvironment().get("DATABASE_USER")
DATABASE_PASSWORD   = GetEnvironment().get("DATABASE_PASSWORD")
DATABASE_HOST       = GetEnvironment().get("DATABASE_HOST")
DATABASE_NAME       = GetEnvironment().get("DATABASE_NAME")

# Define database connection
engine = create_engine(
    f"postgresql+psycopg2://{DATABASE_USER}:{DATABASE_PASSWORD}@{DATABASE_HOST}/{DATABASE_NAME}?client_encoding=utf8"
)
        
# Define class model
Base = declarative_base()

# usersInsightsMigration
from src.model.usersInsightsMigration import *
Base.metadata.create_all(bind=engine)

# flightMigration
from src.model.flightMigration import *
Base.metadata.create_all(bind=engine)
# other

