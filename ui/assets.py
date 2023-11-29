from cmu_graphics import *
import datetime
import os
from config.definitions import ROOT_DIR
import pandas as pd

class VisualConfig: #TODO -- gernerally, the code for this lowkey sucks, and a lot of it is kinda hardcoded, but for now is good, make it better later tho
    '''Global configuration for app visual state. Includes data such as primary/secondary colors.
    Attributes:
        bgcolor, tuple<int>:
            defines the background color for the UI.
        btn_panel_width, float: 
            Represents the portion of the canvas dedicated to holding the timelapse buttons and
            interactive timeline. 
    '''
    def __init__(self, appwidth, appheight, bgcolor):
        self.appwidth = appwidth
        self.appheight = appheight
        self.bgcolor = bgcolor

        self.btn_panel_width = 7.5*appwidth/24

    def set_appsize(self, width, height):
        '''Sets app size if changed'''
        self.appwidth = width
        self.appheight = height

        self.btn_panel_width = 7.5*width/24        

class AppScreen:
    '''Defines the map display where FIRMS data will be mapped.
    Attributes:
        firms: pd.Dataframe of all the current firms to be drawn.'''
    def __init__(self, config, border):
        self.config = config
        self.border = border
        
        #self.img_path = r'C:\code\python\firms-ukraine-mapper\ui\images\ukraine.png' #FIXME -- make this not absolute (and all the paths tbhs!)
        self.img_path = os.path.join(ROOT_DIR, r'ui\images', 'ukraine.png')
        self.firms = None #FIXME -- would probably be nicer just to pass in data from datamanager in to this, rather than modifying this attribute (which is a lot less readable!)

    def draw_app_screen(self): #TODO -- all thest 'draw thing' methods need some fixing .. specifically, they should probably take in location params form outside, rather then hardcoding them in the class
        appwidth = self.config.appwidth
        appheight = self.config.appheight

        drawRect(7.5*appwidth/24, 0, 7.5*appwidth/12, appheight, fill=rgb(*self.border))
        drawImage(self.img_path, 8*appwidth/24, 2*appheight/15, width=7*appwidth/12, height=11*appheight/15, #Looks aight, but not totes epic. Also looks bad when resized souper small
              border=rgb(*self.border), borderWidth=3)
        
    def draw_firms(self):
        '''Plots firms data'''

        if self.firms is None:
            return

        appwidth = self.config.appwidth
        appheight = self.config.appheight

        #Lattitude and longitude values of Ukraine borders
        # lat_top = 52.4214
        # lat_btm = 44.376
        # long_left = 22.2014
        # long_right = 40.2182

        lat_top = 52.8583 
        lat_btm = 43.776
        long_left = 21.3046
        long_right = 40.8805 

        latitude_vals = self.firms['latitude']
        longitude_vals = self.firms['longitude']
        
        #print(firms.index)
        for idx in self.firms.index:
            #print(idx)
            #print(latitude_vals)
            latitude = latitude_vals.loc[idx]
            longitude = longitude_vals.loc[idx]

            delta_x = (longitude - long_left) / (long_right - long_left) #How far across a given data point is as a percentage of the screen width.
            delta_y = (latitude - lat_btm) / (lat_top - lat_btm)

            screen_left = 8*appwidth/24
            screen_top = 2*appheight/15
            screen_width = 7*appwidth/12
            screen_height = 11*appheight/15

            #print(latitude, longitude)
            #Latitude longitude goes up-down (like an x-y canvas), but graphics canvas goes up-down, hence the expression for the y-coord 
            drawRect(screen_left + float(delta_x*screen_width), screen_top + (screen_height - float(delta_y*screen_height)),
                     6, 6, fill='red', align='center')
        
    def get_min_dimensions(self):
        '''Gets the minimum possible dimensions that the screen can be resized.'''

#TODO-- might create a base btn class with a intercept_click method or somethin (just for dry purposes)

class TimelapseBtn:
    '''Toggles whether or not the timelapse is running or paused.'''
    def __init__(self, config):
        self.config = config
       
        self.img_path = os.path.join(ROOT_DIR, r'ui\images', 'playbtn.png')  #TODO - gonna be one of these two
        #self.img_path = r'C:\code\python\firms-ukraine-mapper\ui\images\pausebtn.png'   
                
    def draw_timelapse_btn(self):
        appwidth = self.config.appwidth
        appheight = self.config.appheight
        panel_width = self.config.btn_panel_width

        x, y = 40*panel_width/100, 11*appheight/15 
        width, height = 20*panel_width/100, appheight/8
    
        drawImage(self.img_path, x, y, width=width, height=height) #TODO -- temp coords


class TimelapseForwardBtn:
    def __init__(self, config):
        self.config = config
        self.img_path =  self.img_path = os.path.join(ROOT_DIR, r'ui\images', 'forwardbtn.png')

    def draw_forward_btn(self):
        appwidth = self.config.appwidth
        appheight = self.config.appheight
        panel_width = self.config.btn_panel_width

        width, height = 33*panel_width/100, appheight/10
        x, y = 62*panel_width/100, 11*appheight/15 + (1/10) * height

        drawImage(self.img_path, x, y, width=width, height=height)


class TimelaspeBackBtn:
    def __init__(self, config):
        self.config = config
        self.img_path = os.path.join(ROOT_DIR, r'ui\images', 'backwardsbtn.png')

    def draw_back_btn(self):
        appwidth = self.config.appwidth
        appheight = self.config.appheight
        panel_width = self.config.btn_panel_width

        
        width, height = 33*panel_width/100, appheight/10
        x, y = 5*panel_width/100, 11*appheight/15 + (1/10) * height

        drawImage(self.img_path, x, y, width=width, height=height)


class Timeline: #might be a better name for this?
    def __init__(self, config, color, slider_color) -> None:
        self.config = config
        self.color = color
        self.slider_color = slider_color

        self.slider_min = self.config.appwidth/40 #TODO -- need to place upper and lower bounds on the timeline dates
        self.timelapse_progress = 0 #The day the timelapse is currently on as a percentage of all the dates in the timmelapse

    def set_size(self): #TODO -- not drawing at the correct spot, prob bc of this method, but whatever
        self.slider_min = self.config.appwidth/40 #Reset with new appwidth val (called from update_app_size in ui.py)

    def draw_timeline(self):
        appwidth = self.config.appwidth
        appheight = self.config.appheight

        drawRect(appwidth/40, 65*appheight/72, 38*appwidth/40, 5*appheight/72, fill=rgb(*self.color))

    def draw_slider(self):
        appwidth = self.config.appwidth
        appheight = self.config.appheight
        
        #Times the timeline width
        drawRect(self.slider_min + (self.timelapse_progress)*(38*appwidth/40 - 0.5*appwidth/40), 63.5*appheight/72 , 
                 0.5*appwidth/40, 8*appheight/72, fill=rgb(*self.slider_color))


class AxisTabHeader: #TODO -- class might be not necceasry
    def __init__(self, config, color):
        self.config = config
        self.img_url =  self.img_path = os.path.join(ROOT_DIR, r'ui\images', 'axisheader.png')
        self.underline = color

    def draw_axis_header(self):
        appwidth = self.config.appwidth
        appheight = self.config.appheight
        panel_width = self.config.btn_panel_width

        text_x, text_y = 7*panel_width/100, 13*appheight/24
        text_width, text_height = 35*panel_width/100, appheight/10
        drawImage(self.img_url, text_x, text_y, width=text_width, height=text_height)

        under_x, under_y = 5*panel_width/100, text_y + text_height 
        drawRect(under_x, under_y, 85*panel_width/100, appheight/100, fill=rgb(*self.underline))


class Graph:
    '''Bar graph showing the number of FIRMS events over a given time.'''
    def __init__(self, config, firms_counts:dict, bgcolor, axiscolor, barcolor, selected_barcolor,) -> None:
        self.config = config
        self.bg = bgcolor
        self.axis = axiscolor
        self.barcolor = barcolor
        self.selected_barcolor = selected_barcolor

        self.bars_per_month = 1 #How many bars will show on the graph, can be scaled by the user (from 1 to maybe like 4?)

        self.firms_counts = firms_counts #Will be set from ui.ui

    def draw_background(self):
        appwidth = self.config.appwidth
        appheight = self.config.appheight
        panel_width = self.config.btn_panel_width

        width, height = 90*panel_width/100, 67*appheight/100
        x, y = 5*panel_width/100, 3*appheight/100
        drawRect(x, y, width, height, fill=rgb(*self.bg))

        underline_x, underline_y = x - 2*panel_width/100, y + height
        underline_width, underline_height = width + 4*panel_width/100, 1*appheight/100
        drawRect(underline_x, underline_y, underline_width , underline_height, fill=rgb(*self.axis))


    def draw_bars(self, timelapse_month_yr:datetime.date): #TODO -- a dict or series might work here
        '''Draws bars on the graph corresponding to the number of firms events per month.'''
        appwidth = self.config.appwidth
        appheight = self.config.appheight
        panel_width = self.config.btn_panel_width

        graph_height = 67*appheight/100
        graph_width = 90*panel_width/100
        graph_left = 5*panel_width/100
        graph_bottom = 70*appheight/100

        total_bars = len(self.firms_counts)
        largest_count = max(self.firms_counts.values()) #Scaling other bars to the max of the largest bar
        for dx, date in enumerate(self.firms_counts):
            
            #If the timelapse date is the same as the date for this bar, change the color
            color = self.selected_barcolor if date == timelapse_month_yr else self.barcolor

            count = int(self.firms_counts[date]) #cast to int b/c stored as numpy val
            x, y = graph_left + dx*graph_width/total_bars + 0.5*graph_width/100, graph_bottom
            width = graph_width/total_bars - graph_width/100
            height = float(count*graph_height/largest_count) - 0.5*graph_height/100

            drawRect(x, y, width, height, fill=rgb(*color), align='left-bottom')