from src.app.transform.transform import Transform
from src.app.load.loader import Loader
from src.common.const import INSIGHTS_TABLE_NAME
from src.common.thread import Thread
import numpy as np
import time


def main():
    transform = Transform()
    loader = Loader()
    print('Generating insights...')
    df = transform.generate_insights_from_flight_raw_data()
    print('Insights generated!')

    chunk_size = 100000
    chunks = np.array_split(df, len(df) // chunk_size)

    for chunk in chunks:
        start_time = time.time()
        print('Loading insights into database...')
        thread = Thread()
        thread.run_threads(
            df=chunk,
            target=loader.load_insights_into_database,
            kwargs={"table_name": INSIGHTS_TABLE_NAME}
        )

        end = time.time()

        elapsed_time = end - start_time
        minutes = int(elapsed_time // 60)
        seconds = elapsed_time % 60
        print(f"Took {minutes} minutes and {seconds:.2f} seconds to load chunk")
main()