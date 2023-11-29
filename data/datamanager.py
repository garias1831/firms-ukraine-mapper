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
        
        def str_to_date(date_str):
            '''Converts string date (YYYY-MM-DD) representation to datetime objects'''
            yr, month, day = date_str.split('-')
            date = datetime.date(year=int(yr), month=int(month), day=int(day))
            return date

        #Convert all strings in the dataframe to datetime.date objects
        self.firms['acq_date'] = self.firms['acq_date'].apply(str_to_date)
            

    def get_firms_from_date(self, enddate:datetime.date): #TODO -- should make this able to get the last x days worth of data (ez fix)
        '''Gets the last 3 days's worth of firms based on the given end date, inclusive. For example, if end= "2022-03-07",
        this method would return a DataFrame containing all firms from 2022-03-04 to 2022-03-07.'''
        startdate = enddate - datetime.timedelta(days=3)

        #pd.Series with all of the firms dates but as datetime.date objects
        datetime_series = self.firms['acq_date']
        slice = self.firms.loc[(startdate <= datetime_series) & 
                        (datetime_series <= enddate)]
        
        return slice
    
    def get_timelapse_progress(self, curr_date:datetime.date):
        series_dates = self.firms['acq_date'].drop_duplicates()
        
        dates_until_now = series_dates.loc[series_dates <= curr_date]
    
        progress = len(dates_until_now) / len(series_dates)
        return progress
    
    def get_firms_per_months(self, months_per:int): #FIXME -- figure out how the graph is gonna work , and implement the months_per para
        '''Gets the number of firms events that occur over months_per months. If there aren't enough months left to total the data, just
        take whatever is left. 
            Params:
                months_per: int. Tells the function to sum up firms data for each months_per set of months. Ex) total number of
                firms events for each month, every 2 months, every 3 months, etc.
        '''

        dates = self.firms['acq_date'].drop_duplicates()
        months =  sorted({datetime.date(year=d.year, month=d.month, day=1) for d in dates}) #Convert to set to remove dupes, then sort to preserve order

        count_per_months = dict()

        for curr_date in months: 
            month, year = curr_date.month, curr_date.year #Current month and year
            #dt = datetime.timedelta(days=30*x) #Months should be around here, and we only rly care about dates

            #We only care about month and year in this case
            if month == 12:
                next_month = datetime.date(year=year+1, month=1, day=1) #First of the next month
            else:
                next_month = datetime.date(year=year, month=month+1, day=1)
            
            firms_month_count = self.firms['acq_date'].loc[(curr_date <= self.firms['acq_date']) & 
                                                           (self.firms['acq_date'] < next_month)].count()

            if curr_date not in count_per_months:
                count_per_months[curr_date] = firms_month_count
            else:
                count_per_months[curr_date] += firms_month_count
        
        return count_per_months



