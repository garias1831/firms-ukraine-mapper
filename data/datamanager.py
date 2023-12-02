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

        for x in range(0, len(months), months_per):
            
            if x == 0: #We don't have data for all of feb 2022, so make sure it shows as the date of invasion day 1
                curr_date = datetime.date(year=2022, month=2, day=24)            
            else:
                curr_date = months[x]

            month, year = curr_date.month, curr_date.year #Current month and year
            
            if month + months_per > 12:
                month = (month + months_per) - 12
                next_month = datetime.date(year=year+1, month=month, day=1) #First of the next month
            else:
                month += months_per
                next_month = datetime.date(year=year, month=month, day=1)
            
            firms_month_count = self.firms['acq_date'].loc[(curr_date <= self.firms['acq_date']) & 
                                                           (self.firms['acq_date'] < next_month)].count() 

            end = len(months) - 1
            if end - months_per < x: #Make sure we don't overshoot with the step
                last_date = dates.iloc[-1] #Get the very last day with firms data (as we might only have partial FIRMS for a month)
                next_month = datetime.date(year=last_date.year, month=last_date.month, day=last_date.day)
                month_range = (curr_date, next_month)
            else:
                month_range = (curr_date, next_month - datetime.timedelta(days=1)) #Subtract one to make it more clear that we're only scraping the month

            if curr_date not in count_per_months:
                count_per_months[month_range] = firms_month_count
            else:
                count_per_months[month_range] += firms_month_count

        return count_per_months
    
    def get_trendline_coeffs(self, count_per_months:dict):
        '''Gets the coefficients a and b for the equation y = ax + b, which will be plotted in the graph. Uses
        least squares approximation. See README for formula citation. To be used with the dict returned by get_firms_per_months.'''

        counts = count_per_months

        x_vals = range(1, len(counts) + 1) #We have one bar for each entry in count per months      
        y_vals = [counts[k] for k in counts]

        n = len(counts) #Number of (x, y) pairs we have, in this case equal to the number of bars
        sum_x = sum(x_vals)
        sum_y = sum(y_vals)
        sum_x_squares = sum([x**2 for x in x_vals])
        sum_x_y = sum([x_vals[i] * y_vals[i] for i in range(len(counts))])

        b = ((n * sum_x_y) - (sum_x * sum_y)) / ((n * sum_x_squares) - (sum_x)**2) #y-intercept (might wanna abs this, because its negative)

        a = (sum_y - b * sum_x) / n #Slope of the best-fit line
        
        return float(a), float(b)



