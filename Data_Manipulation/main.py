import os
import logging
from typing import Optional

import kaggle
import pandas as pd
from tqdm import tqdm

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class AirportDataAnalyzer:
    def __init__(self):
        self._setup_kaggle_credentials()

    def _setup_kaggle_credentials(self):
        #Configurar credenciais do Kaggle a partir de variáveis de ambiente
        kaggle_username = os.getenv('KAGGLE_USERNAME')
        kaggle_key = os.getenv('KAGGLE_KEY')

        if not kaggle_username or not kaggle_key:
            logger.warning("Credenciais do Kaggle não configuradas")
            return

        os.environ['KAGGLE_USERNAME'] = kaggle_username
        os.environ['KAGGLE_KEY'] = kaggle_key

    def download_dataset(
        self, 
        dataset: str, 
        download_path: Optional[str] = None
    ) -> pd.DataFrame:
        
        #Baixar dataset do Kaggle
        download_path = download_path or './data'
        os.makedirs(download_path, exist_ok=True)

        try:
            kaggle.api.dataset_download_files(
                dataset, 
                path=download_path, 
                unzip=True
            )
            
            # Percorrer diretório
            csv_files = [f for f in os.listdir(download_path) if f.endswith('.csv')]
            
            if not csv_files:
                raise ValueError("Nenhum arquivo CSV encontrado")
            
            file_path = os.path.join(download_path, csv_files[0])
            return pd.read_csv(file_path)
        
        except Exception as e:
            logger.error(f"Erro ao baixar dataset: {e}")
            raise

def main():
    analyzer = AirportDataAnalyzer()
    
    try:
        df = tqdm(analyzer.download_dataset('yuanyuwendymu/airline-delay-and-cancellation-data-2009-2018'))
        logger.info(df.head())
    
    except Exception as e:
        logger.error(f"Erro ao tentar realizar download: {e}")

if __name__ == "__main__":
    main()