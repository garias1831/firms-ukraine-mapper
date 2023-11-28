from config.definitions import ROOT_DIR
import datetime
import pandas as pd
import os

class DataManager:
    '''Manages the firms data to be used throughout the application.'''
    def __init__(self): 
        df = pd.read_csv(os.path.join(ROOT_DIR, r'data\firms', 'firms.csv'))
        self.firms = df.drop(['scan', 'track', 'acq_time', 'satellite', 'instrument', 
                         'confidence', 'version', 'frp', 'daynight'], axis=1)
            
    def str_to_date(self, date_str):
        '''Converts string date (YYYY-MM-DD) representation to datetime object'''
        yr, month, day = date_str.split('-')
        date = datetime.date(year=int(yr), month=int(month), day=int(day))
        return date

    def get_firms_from_date(self, enddate:datetime.date): 
        '''Gets the last 3 days's worth of firms based on the given end date, inclusive. For example, if end= "2022-03-07",
        this method would return a DataFrame containing all firms from 2022-03-04 to 2022-03-07.'''
        startdate = enddate - datetime.timedelta(days=3)

        #pd.Series with all of the firms dates but as datetime.date objects
        datetime_series = self.firms['acq_date'].apply(self.str_to_date)
        slice = self.firms.loc[(startdate <= datetime_series) & 
                        (datetime_series <= enddate)]
        
        return slice
    
    def get_timelapse_progress(self, curr_date:datetime.date):
        series_dates = self.firms['acq_date'].drop_duplicates()
        
        series_dates = series_dates.apply(self.str_to_date)
        dates_until_now = series_dates.loc[series_dates <= curr_date]
    
        progress = len(dates_until_now) / len(series_dates)
        return progress



