from dotenv import load_dotenv
load_dotenv()
from kaggle.api.kaggle_api_extended import KaggleApi
from src.common.const import PATH_TO_KAGGLE_DOWNLOADS


class Downloader(object):
    def __init__(self):
        self.api = KaggleApi()
        self.api.authenticate()

    def download_dataset(self, dataset_name):
        self.api.dataset_download_files(dataset_name, path=PATH_TO_KAGGLE_DOWNLOADS)