from cmu_graphics import *

class VisualConfig:
    '''Global configuration for app visual state. Includes data such as primary/secondary colors.
    Attributes:
        bgcolor: tuple<int>. defines the background color for the UI.
    '''
    def __init__(self, appwidth, appheight, bgcolor):
        self.appwidth = appwidth
        self.appheight = appheight
        self.bgcolor = bgcolor


class AppScreen:
    '''Defines the map display where FIRMS data will be mapped.'''
    def __init__(self, config, border):
        self.config = config
        self.border = border
        
        self.img_path = r'C:\code\python\firms-ukraine-mapper\ui\images\ukraine.png' #TODO -- make this not absolute

    def draw_app_screen(self):
        appwidth = self.config.appwidth
        appheight = self.config.appheight


        drawImage(self.img_path, 7*appwidth/24, appheight/15, width=7*appwidth/12, height=13*appheight/15, #Looks aight, but not totes epic. Also looks bad when resized souper small
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
        drawImage(self.img_path, 100, 100) #TODO -- temp coords


class TimelapseForwardBtn:
    def __init__(self, config):
        self.config = config
        self.img_path = r'C:\code\python\firms-ukraine-mapper\ui\images\forwardsbtn.png'


class TimelaspeBackBtn:
    def __init__(self, config):
        self.config = config
        self.img_path = r'C:\code\python\firms-ukraine-mapper\ui\images\backwardsbtn.png'


class Timeline: #might be a better name for this?
    pass
