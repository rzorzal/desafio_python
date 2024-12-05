from src.services.kaggle import Downloader
from src.common.const import PATH_TO_KAGGLE_DOWNLOADS
from src.common.config import Config
from src.services.postgres import Postgres
import zipfile


class Extractor(object):
    def __init__(self):
        self.config = Config()
        self.downloader = Downloader()
        self.postgres = Postgres()

    def extract_dataset_from_kaggle(self):
        self.downloader.download_dataset(self.config.dataset_name)

    def unzip_downloaded_dataset(self):
        unzipped_file_name = self.config.dataset_name.split('/')[1]
        with zipfile.ZipFile(f'{PATH_TO_KAGGLE_DOWNLOADS}/{unzipped_file_name}.zip', 'r') as zip_ref:
            zip_ref.extractall(f'{PATH_TO_KAGGLE_DOWNLOADS}/data')

    def extract_data_from_postgres_as_df(self, query):
        return self.postgres.query_to_df(query)