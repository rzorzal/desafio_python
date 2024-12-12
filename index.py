# from src.part1.download_dadaset import DownloadDataset
# from src.part1.popule_database import PopuleDatabase
from src.part2.insigths import UsersInsights

class PrincipalClass():

    def run(self):
        # # Download datasets
        # DownloadDataset("yuanyuwendymu/airline-delay-and-cancellation-data-2009-2018").downloadAll()

        # Run Migrations
        # import migrations.main

        # Popule database - data load
        # PopuleDatabase().load_data()

        # Make users insights
        UsersInsights().generateInsigths()

PrincipalClass().run()