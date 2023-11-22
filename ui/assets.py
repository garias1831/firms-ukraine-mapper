from cmu_graphics import *

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

        self.btn_panel_width = 7*appwidth/24

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

    def draw_app_screen(self):
        appwidth = self.config.appwidth
        appheight = self.config.appheight

        drawRect(7.5*appwidth/24, 0, 7.5*appwidth/12, appheight, fill=rgb(*self.border))
        drawImage(self.img_path, 8*appwidth/24, 2*appheight/15, width=7*appwidth/12, height=11*appheight/15, #Looks aight, but not totes epic. Also looks bad when resized souper small
              border=rgb(*self.border), borderWidth=3)
        
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