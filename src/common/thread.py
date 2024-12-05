import threading
import numpy as np


class Thread:
    def __init__(self):
        pass

    def run_threads(self, df, target, kwargs={}, max_threads=10):
        if not df.empty:
            threads = min(len(df), max_threads)
            chunks = self._chunkify(df, threads)

            procs = []
            for chunk in chunks:
                t = threading.Thread(
                    target=target, args=(chunk,), kwargs={**kwargs}
                )
                t.start()
                procs.append(t)

            for proc in procs:
                proc.join()

    def _chunkify(self, df, threads):
        return np.array_split(df, threads)

