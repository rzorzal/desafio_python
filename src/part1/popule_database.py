import csv, os
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker
from src.model.flightMigration import Flight
from progress.bar import Bar
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

class PopuleDatabase():
        
    def configure_data_column(self, value):
        try:
            if not value:
                return 'NaN'
            return value
        except Exception:
            return value

    def load_data(self):
        # insert by bulk_insert_mappings method
        csv_files = os.listdir(f"{os.getcwd()}/src/part1/csv/")
        with Bar(f'Processing csv files...', max=len(csv_files)) as bar:

            for csv_file in csv_files:
                bar.next()
                if '.csv' in csv_file:
                    with open(f"{os.getcwd()}/src/part1/csv/{csv_file}", newline='') as csvfile:
                        reader = csv.DictReader(csvfile)
                        columns_valid = {col.name for col in Flight.__table__.columns}
                        data_filted = [
                            {key: self.configure_data_column(value) for key, value in column_.items() if key in columns_valid}
                            for column_ in reader
                        ]
                    session.bulk_insert_mappings(Flight, data_filted)
                    session.commit()
        print("Data insertion completed successfully!")
