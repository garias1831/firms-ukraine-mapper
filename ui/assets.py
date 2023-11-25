from cmu_graphics import *
import pandas as pd

class VisualConfig:
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
    '''Defines the map display where FIRMS data will be mapped.'''
    def __init__(self, config, border):
        self.config = config
        self.border = border
        
        self.img_path = r'C:\code\python\firms-ukraine-mapper\ui\images\ukraine.png' #TODO -- make this not absolute (and all the paths tbhs!)

    def draw_app_screen(self): #TODO -- all thest 'draw thing' methods need some fixing .. specifically, they should probably take in location params form outside, rather then hardcoding them in the class
        appwidth = self.config.appwidth
        appheight = self.config.appheight

        drawRect(7.5*appwidth/24, 0, 7.5*appwidth/12, appheight, fill=rgb(*self.border))
        drawImage(self.img_path, 8*appwidth/24, 2*appheight/15, width=7*appwidth/12, height=11*appheight/15, #Looks aight, but not totes epic. Also looks bad when resized souper small
              border=rgb(*self.border), borderWidth=3)
        
    def draw_firms(self, firms:pd.DataFrame):
        '''Plots firms data'''
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

        #print(firms)

        latitude_vals = firms['latitude']
        longitude_vals = firms['longitude']
        
        print(firms.index)
        for idx in firms.index:
            print(idx)
            print(latitude_vals)
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
        #self.timelapse_running = False #TODO -- not sure if timelapse should start running or paused -- will change img to fit .. also sidenote, not sure if should create new dir for buttons images and stuff?
        self.img_path = r'C:\code\python\firms-ukraine-mapper\ui\images\playbtn.png' #TODO - gonna be one of these two
        #self.img_path = r'C:\code\python\firms-ukraine-mapper\ui\images\pausebtn.png'   
                
    def draw_timelapse_btn(self):
        appwidth = self.config.appwidth
        appheight = self.config.appheight
        panel_width = self.config.btn_panel_width

        x, y = 40*panel_width/100, 5*appheight/15 
        width, height = 20*panel_width/100, appheight/8
    
        drawImage(self.img_path, x, y, width=width, height=height) #TODO -- temp coords


class TimelapseForwardBtn:
    def __init__(self, config):
        self.config = config
        self.img_path = r'C:\code\python\firms-ukraine-mapper\ui\images\forwardbtn.png'

    def draw_forward_btn(self):
        appwidth = self.config.appwidth
        appheight = self.config.appheight
        panel_width = self.config.btn_panel_width

        width, height = 33*panel_width/100, appheight/10
        x, y = 62*panel_width/100, 5*appheight/15 + (1/10) * height

        drawImage(self.img_path, x, y, width=width, height=height)


class TimelaspeBackBtn:
    def __init__(self, config):
        self.config = config
        self.img_path = r'C:\code\python\firms-ukraine-mapper\ui\images\backwardsbtn.png'

    def draw_back_btn(self):
        appwidth = self.config.appwidth
        appheight = self.config.appheight
        panel_width = self.config.btn_panel_width

        
        width, height = 33*panel_width/100, appheight/10
        x, y = 5*panel_width/100, 5*appheight/15 + (1/10) * height

        drawImage(self.img_path, x, y, width=width, height=height)


class Timeline: #might be a better name for this?
    pass


class AxisTabHeader:
    def __init__(self, config, color):
        self.config = config
        self.img_url = r'C:\code\python\firms-ukraine-mapper\ui\images\axisheader.png'
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