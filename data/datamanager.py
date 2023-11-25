import pandas as pd

class DataManager:
    def __init__(self):
        df =  pd.read_csv(r'C:\code\python\firms-ukraine-mapper\data\firms\fire_nrt_J1V-C2_404869_new.csv')
        self.firms = df.drop(['scan', 'track', 'acq_time', 'satellite', 'instrument', 
                         'confidence', 'version', 'frp', 'daynight'], axis=1)

