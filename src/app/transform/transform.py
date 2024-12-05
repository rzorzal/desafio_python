from src.app.extract.extractor import Extractor
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
import xgboost as xgb
import math
import pandas as pd


class Transform(object):
    def __init__(self):
        self.extractor = Extractor()
        self.le_carrier = LabelEncoder()
        self.le_origin = LabelEncoder()
        self.le_flight_num = LabelEncoder()
        self.batch_size = 500000

    def generate_insights_from_flight_raw_data(self):
        total_rows = self._get_total_rows()
        num_batches = math.ceil(total_rows / self.batch_size)

        all_batches = []

        for batch_num in range(num_batches):   
            query = self._create_flight_delay_query(batch_num)

            df = self.extractor.extract_data_from_postgres_as_df(query)

            self._pre_process_data(df)
            df_with_probabilities = self._train_model(df)

            self._decode_columns(df_with_probabilities)
            all_batches.append(df_with_probabilities)

        final_df = pd.concat(all_batches, ignore_index=True)

        return final_df

    
    def _get_total_rows(self):
        query = """SELECT
                        COUNT(*) AS num_rows
                    FROM (
                        SELECT DISTINCT
                            op_carrier,
                            op_carrier_fl_num,
                            origin
                        FROM
                            flight_raw
                    ) AS distinct_combinations;
        """
        total_rows = self.extractor.extract_data_from_postgres_as_df(query).iloc[0, 0]
        return total_rows

    def _create_flight_delay_query(self, batch_num):
        offset = batch_num * self.batch_size
        query = f"""
            SELECT 
                op_carrier,
                op_carrier_fl_num,
                origin,
                count(*) as flight_count,
                SUM(CASE WHEN cancelled = 1 THEN 1 ELSE 0 END) AS cancelled_count,  -- Count the number of cancelled flights
                SUM(carrier_delay) AS total_carrier_delay,  -- Sum of all carrier delays
                SUM(weather_delay) AS total_weather_delay,  -- Sum of all weather delays
                SUM(nas_delay) AS total_nas_delay,  -- Sum of all NAS delays
                SUM(security_delay) AS total_security_delay,  -- Sum of all security delays
                ROUND(AVG(carrier_delay + weather_delay + nas_delay + security_delay + late_aircraft_delay)::numeric, 2) AS avg_delay, -- Sum of all late aircraft delays
                SUM(air_time) AS total_air_time  -- Sum of all air time
            FROM 
                flight_raw
            GROUP BY 
                op_carrier, 
                op_carrier_fl_num, 
                origin
            ORDER BY 
                op_carrier,
                op_carrier_fl_num,
                origin
            LIMIT {self.batch_size} OFFSET {offset};
        """


        return query

    def _pre_process_data(self, df):
            df['op_carrier'] = self.le_carrier.fit_transform(df['op_carrier'])
            df['origin'] = self.le_origin.fit_transform(df['origin'])
            df['op_carrier_fl_num'] = self.le_flight_num.fit_transform(df['op_carrier_fl_num'])
        
    def _train_model(self, df):
        print('Training model...')
        if df.empty:
            print("No data available to train the model.")
            return df
        
        X = df.drop(columns=['cancelled_count', 'avg_delay', 'total_air_time'])
        y = (df['cancelled_count'] > 0).astype(int)

        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

        model = xgb.XGBClassifier(random_state=42, scale_pos_weight=1, use_label_encoder=False, eval_metric='logloss')

        model.fit(X_train, y_train)

        y_proba = model.predict_proba(X_test)

        cancellation_probabilities = y_proba[:, 1]

        y_pred = (cancellation_probabilities > 0.5).astype(int)

        print("Model trained! Accuracy:", accuracy_score(y_test, y_pred))

        cancellation_probabilities_percentage = cancellation_probabilities * 100

        df['cancellation_chance'] = 0
        df.loc[X_test.index, 'cancellation_chance'] = cancellation_probabilities_percentage

        return df
    
    def _decode_columns(self, df):
            df['op_carrier'] = self.le_carrier.inverse_transform(df['op_carrier'])
            df['origin'] = self.le_origin.inverse_transform(df['origin'])
            df['op_carrier_fl_num'] = self.le_flight_num.inverse_transform(df['op_carrier_fl_num'])