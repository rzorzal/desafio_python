from src.services.postgres import Postgres
from src.app.models.flight_insight import FlightInsight


class Loader(object):
    def __init__(self):
        pass

    def load_data_into_database(self, df, table_name):
        postgres = Postgres()

        try:
            for _, row in df.iterrows():
                query, values = self._create_query(row, table_name)
                postgres.execute(query, values)
        except Exception as e:
            print(f'Error: {e}')
        finally:
            postgres.close()

    def load_insights_into_database(self, df, table_name):
        postgres = Postgres()

        try:
            for _, row in df.iterrows():
                insight = FlightInsight(row)
                
                query, values = self._create_query(insight, table_name)
                postgres.execute(query, values)
        except Exception as e:
            print(f'Error: {e}')
        finally:
            postgres.close()

    def _create_query(self, row, table_name):
        row_dict = row.to_dict()

        columns = list(row_dict.keys())
        values = list(row_dict.values())

        query = f"INSERT INTO {table_name} ({', '.join(columns)}) VALUES ({', '.join(['%s'] * len(values))});"

        return query, values