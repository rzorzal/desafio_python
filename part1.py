from src.app.extract.extractor import Extractor
from datetime import datetime
from src.common.const import PATH_TO_KAGGLE_DOWNLOADS, RAW_TABLE_NAME
from src.app.sanitize.sanitizer import Sanitizer
from src.app.load.loader import Loader
from src.common.thread import Thread
import time
import os
import pandas as pd


def main():
    start_time = time.time()

    extractor = Extractor()
    sanitizer = Sanitizer()
    thread = Thread()
    loader = Loader()


    print('Downloading dataset...')
    download_start_time = time.time()
    extractor.extract_dataset_from_kaggle()
    print('Download completed!')

    download_finish_time = time.time()

    elapsed_time = download_finish_time - download_start_time
    minutes = int(elapsed_time // 60)
    seconds = elapsed_time % 60

    print(f"Took {minutes} minutes and {seconds:.2f} seconds to downlaod dataset")

    print('Extracting files...')
    extractor.unzip_downloaded_dataset()
    print('Files extracted!')

    files = [f'{PATH_TO_KAGGLE_DOWNLOADS}/data/{item}' for item in os.listdir(f'{PATH_TO_KAGGLE_DOWNLOADS}/data')]

    for file in files:
        for chunk in pd.read_csv(file, chunksize=500000):
            chunk_start_time = time.time()

            chunk = sanitizer.sanitize_raw_data(chunk)

            print(f'Loading chunk into database...')
            thread.run_threads(df=chunk,
                            target=loader.load_data_into_database,
                            kwargs={"table_name": RAW_TABLE_NAME},
                            max_threads=20
                            )
            print(f'Chunk loaded into database!')

            end = time.time()

            elapsed_time = end - chunk_start_time
            minutes = int(elapsed_time // 60)
            seconds = elapsed_time % 60

            print(f"Took {minutes} minutes and {seconds:.2f} seconds to load chunk")

    end_time = time.time()

    total_time = end_time - start_time
    minutes = int(total_time // 60)
    seconds = total_time % 60

    print(f"Took {minutes} minutes and {seconds:.2f} seconds to load dataset")

main()
