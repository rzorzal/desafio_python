from src.part1.download_dadaset import DownloadDataset
from src.part1.popule_database import PopuleDatabase
from src.part2.insigths import UsersInsights
from src.utils.getEnvironment import GetEnvironment
import subprocess

DATASET_BASE = GetEnvironment().get("DATASET_BASE")

class PrincipalClass():

    def run(self):
        # Download datasets
        DownloadDataset(DATASET_BASE).downloadAll()

        # Run Migrations
        cmd = "cd migrations && alembic upgrade head && cd .."
        subprocess.check_output(cmd, shell=True, text=True)

        # Popule database - data load
        PopuleDatabase().load_data()

        # Make users insights
        UsersInsights().generateInsigths()

        # UsersInsights().flights_cancellation()
        

PrincipalClass().run()