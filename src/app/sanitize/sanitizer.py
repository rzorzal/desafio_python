class Sanitizer(object):
    def __init__(self):
        pass

    def sanitize_raw_data(self, df):
        df = df.fillna({
            col: 0.0 if df[col].dtype == 'float64' else 
                0 if df[col].dtype == 'int64' else 
                'N/A'
            for col in df.columns
        })
        
        if 'Unnamed: 27' in df.columns:
            df = df.drop(columns=['Unnamed: 27'])
        
        return df