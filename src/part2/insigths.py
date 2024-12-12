from sqlalchemy import create_engine, text
from sqlalchemy.orm import Session, sessionmaker
from src.model.usersInsightsMigration import UsersInsights as UsersInsightsModel
from src.model.usersInsightsMigration import UsersInsightsView
from sqlalchemy import select, insert
from src.utils.getEnvironment import GetEnvironment

import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report

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
            print(f"OP_CARRIER:  {row.OP_CARRIER}, DELAY_AVERAGE: {row.DELAY_AVERAGE}, TOTAL_AIR_TIME: {int(row.TOTAL_AIR_TIME)}")
            session.execute(insert(UsersInsightsModel), [{
                "OP_CARRIER":row.OP_CARRIER,
                "DELAY_AVERAGE":row.DELAY_AVERAGE,
                "TOTAL_AIR_TIME":row.TOTAL_AIR_TIME
            }])
            session.commit()
        print("Result saved in users_insights table...")
            

    def flights_cancellation(self):
        # code... #
        print("Probabilidade de cancelamento do voo:", 0)
