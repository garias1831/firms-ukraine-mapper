import pandas as pd
import datetime

class DataManager:
    '''Manages the firms data to be used throughout the application.'''
    def __init__(self):
        df =  pd.read_csv(r'C:\code\python\firms-ukraine-mapper\data\firms\fire_nrt_J1V-C2_404869_new.csv')
        self.firms = df.drop(['scan', 'track', 'acq_time', 'satellite', 'instrument', 
                         'confidence', 'version', 'frp', 'daynight'], axis=1)
        
    def get_firms_from_date(self, enddate:datetime.date): 
        '''Gets the last week's worth of firms based on the given end date, inclusive. For example, if end= "2022-03-07",
        this method would return a DataFrame containing all firms from 2022-02-28 to 2022-03-07.'''

        def str_to_date(date_str):
            '''Converts string date (YYYY-MM-DD) representation to datetime object'''
            yr, month, day = date_str.split('-')
            date = datetime.date(year=int(yr), month=int(month), day=int(day))
            return date

        startdate = enddate - datetime.timedelta(days=3)

        #pd.Series with all of the firms dates but as datetime.date objects
        datetime_series = self.firms['acq_date'].apply(str_to_date)
        slice = self.firms.loc[(startdate <= datetime_series) & 
                        (datetime_series <= enddate)]
        
        return slice



