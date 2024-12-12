import kagglehub, os

class DownloadDataset():
    def __init__(self, dataset_path):
        self.dataset_path = dataset_path
        pass

    def downloadAll(self):
        # Download all csv file in path constructor.
        path = kagglehub.dataset_download(self.dataset_path)
        new_path = "./csv"

        try:
            os.mkdir(new_path)
            print(f"Directory '{new_path}' created successfully.")
        except FileExistsError:
            print(f"Directory '{new_path}' already exists.")

        print(f"Moving files from {path} to {new_path}")
        os.rename(path, new_path)

        print("Path to dataset files:", new_path)
