from decouple import config

class GetEnvironment:
    
    def get(self, name):
        try:
            return config(name)
        except Exception:
            pass
