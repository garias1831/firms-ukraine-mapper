import copy
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
        '''Updates the app's width and height values if changed via a call to onResize.'''
        #Set the config's width and height values
        self.appwidth = width
        self.appheight = height
        self.btn_panel_width = 7.5*width/24

    def resize_ui_elements(self, element, *args): #Want to get this called from ui, and to resize all elements based on the factor
        '''Takes in array of scaling coefficients'''
        pass        


class UILayout: #NOTE -- okay to hardcode coords here, but not in the individual app classes
    '''Holds Widget objects as well as their position on the canvas and their sizes. '''
    def __init__(self, config:VisualConfig) -> None:
        self.config = config
        self.layouts = dict() #Dict of layouts and their associated elements
        
    def load_ui_elements(self):
        '''Instantiates objects on the UI. Called once in onAppStart'''
        # self.timelapse_btn = TimelapseBtn(self.config, self.timelapse_layout['x'], self.timelapse_layout['y'],
        #                                         self.timelapse_layout['width'], self.timelapse_layout['height'])
        self.timelapse_btn = TimelapseBtn(self.config)
        self.timelapse_forward_btn = TimelapseForwardBtn(app.config)
        self.timelapse_back_btn = TimelaspeBackBtn(app.config)

    def fix_element_layouts(self):
        '''Loads positioning and sizes for all elements on the UI. Also updated in onResize'''
        appwidth = self.config.appwidth
        appheight = self.config.appheight
        panel_width = self.config.btn_panel_width

        #Define a base layout dictionary. All elements will have an x and y coordinate, as well as a width and a height
        layout = {'x': 0, 'y': 0, 'width':0, 'height': 0}

        timelapse_layout = copy.copy(layout)
        timelapse_layout['x'], timelapse_layout['y']  = 40*panel_width/100, 11*appheight/15
        timelapse_layout['width'], timelapse_layout['height'] = 20*panel_width/100, appheight/8
        self.layouts[self.timelapse_btn] = timelapse_layout

        fwd_layout = copy.copy(layout)
        fwd_layout['width'], fwd_layout['height'] = 33*panel_width/100, appheight/10
        fwd_layout['x'], fwd_layout['y'] = 62*panel_width/100, 11*appheight/15 + (1/10) * appheight/10
        self.layouts[self.timelapse_forward_btn] = fwd_layout

        back_layout = copy.copy(layout)
        back_layout['width'], back_layout['height'] = 33*panel_width/100, appheight/10
        back_layout['x'], back_layout['y'] = 5*panel_width/100, 11*appheight/15 + (1/10) * appheight/10
        self.layouts[self.timelapse_back_btn] = back_layout

        
    def place_ui_elements(self):
        #All widgets, so we chill
        for element in self.layouts:
            layout = self.layouts[element]

            element.x = layout['x']
            element.y = layout['y']
            element.width = layout['width']
            element.height = layout['height']


class Widget:
    '''Base object for visual elements in the application. This class should not be instantiated on its own.
    The class contains information about its position and size, and generally things that everything on the UI should have. Instance
    attribtutes of this object are expected to be ovverwritten by inheriting objects.'''
    def __init__(self) -> None:

        self.x = None
        self.y = None
        self.width = None
        self.height = None

    #We're going to be putting these in dicts
    def __hash__(self) -> int:
        return(hash(str(self)))


class AppScreen:
    '''Defines the map display where FIRMS data will be mapped.
    Attributes:
        firms: pd.Dataframe of all the current firms to be drawn.'''
    def __init__(self, config, border):
        self.config = config
        self.border = border
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

        lat_top = 52.8583 
        lat_btm = 43.776
        long_left = 21.3046
        long_right = 40.8805 

        latitude_vals = self.firms['latitude']
        longitude_vals = self.firms['longitude']
        
        for idx in self.firms.index:
            latitude = latitude_vals.loc[idx]
            longitude = longitude_vals.loc[idx]

            delta_x = (longitude - long_left) / (long_right - long_left) #How far across a given data point is as a percentage of the screen width.
            delta_y = (latitude - lat_btm) / (lat_top - lat_btm)

            screen_left = 8*appwidth/24
            screen_top = 2*appheight/15
            screen_width = 7*appwidth/12
            screen_height = 11*appheight/15

            #Latitude longitude goes up-down (like an x-y canvas), but graphics canvas goes up-down, hence the expression for the y-coord 
            drawRect(screen_left + float(delta_x*screen_width), screen_top + (screen_height - float(delta_y*screen_height)),
                     6, 6, fill='red', align='center')
        

class Button(Widget):
    def __init__(self) -> None:
        pass

    def click_intercepted(self, mouseX, mouseY):
        #Assuming align = left-top here
        if (self.x <= mouseX <= self.x + self.width and
            self.y <= mouseY <= self.y + self.height):
            return True
        return False


class TimelapseBtn(Button):
    '''Toggles whether or not the timelapse is running or paused.'''
    def __init__(self, config):
        self.config = config
       
        self.img_path = os.path.join(ROOT_DIR, r'ui\images', 'playbtn.png')  #TODO - gonna be one of these two

        #self.img_path = r'C:\code\python\firms-ukraine-mapper\ui\images\pausebtn.png'  
    #Here, app is the cmu graphics app
    def pressed(self, app):
        app.timelapse_started = not app.timelapse_started #TODO -- need to change the img
        if app.timelapse_started:
            self.img_path = os.path.join(ROOT_DIR, r'ui\images', 'pausebtn.png')
        else:
            self.img_path = os.path.join(ROOT_DIR, r'ui\images', 'playbtn.png')


    def draw_timelapse_btn(self):
        drawImage(self.img_path, self.x, self.y, width=self.width, height=self.height) 


class TimelapseForwardBtn(Button): #TODO -- a setter method might be nice for these
    def __init__(self, config):
        self.config = config
        self.img_path =  self.img_path = os.path.join(ROOT_DIR, r'ui\images', 'forwardbtn.png')

    def draw_forward_btn(self):
        drawImage(self.img_path, self.x, self.y, width=self.width, height=self.height)


class TimelaspeBackBtn(Button):
    def __init__(self, config):
        self.config = config
        self.img_path = os.path.join(ROOT_DIR, r'ui\images', 'backwardsbtn.png')

    def draw_back_btn(self):
        drawImage(self.img_path, self.x, self.y, width=self.width, height=self.height)


class Timeline: #might be a better name for this?
    def __init__(self, config, color, slider_color) -> None:
        self.config = config
        self.color = color
        self.slider_color = slider_color

        self.slider_min = self.config.appwidth/40 #TODO -- need to place upper and lower bounds on the timeline dates
        self.timelapse_progress = 0 #The day the timelapse is currently on as a percentage of all the dates in the timmelapse

    def set_size(self): 
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


class GraphBar:
    '''Defines an individual bar that will appear in the app graph.'''
    def __init__(self, left, bottom, width, height) -> None:
        self.left = left
        self.bottom = bottom
        self.width = width
        self.height = height

    def mouse_over_bar(self, mouseX, mouseY):  #FIXME -- this method is a little jank
        if ((self.left <= mouseX and mouseX <= self.left + self.width) and
            self.bottom - self.height <= mouseY and mouseY <= self.bottom):
            
            #Dict is ordered, so get the date associated with this bar, and return it
            #date = self.firms_counts.keys()[x] 
            return True
        return False


class Graph:
    '''Bar graph showing the number of FIRMS events over a given time.
    Attributes:
        firms_counts: dict{(datetime.date, datetime.date): int}. Has keys of datetime.date objects representing the given date range
        in which FIRMS data was collected during the timelapse. Values represent the numebr of firms events corresponding to a given range.'''
    def __init__(self, config, firms_counts:dict, coeffs:tuple, bgcolor, axiscolor, barcolor, selected_barcolor,) -> None:
        self.config = config
        self.bg = bgcolor
        self.axis = axiscolor
        self.barcolor = barcolor
        self.selected_barcolor = selected_barcolor

        self.bars = []  #List of graphbar objects
        self._bars_per_month = 1 #FIXME -- this is poorly named, as this is what gets passed to the datamaneger to generate the firms_counts dict
        self.firms_counts = firms_counts #Set from ui.ui
        self.trendline_coeffs = coeffs #Stored as (a, b), where a is the slope and b is the y-intercept

    @property
    def bars_per_month(self): #FIXME Not sure if i need dis
        return self._bars_per_month

    @bars_per_month.setter
    def bars_per_month(self, _bars_per_month:int):
        if 1 <= _bars_per_month and _bars_per_month <= 4:
            self._bars_per_month =  _bars_per_month
       
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

        current_bars = []
        for dx, date in enumerate(self.firms_counts):
            
            #If the timelapse date is the same as the date for this bar, change the color
            start_date = date[0]
            end_date = date[1]
            if start_date <= timelapse_month_yr and timelapse_month_yr <= end_date:
                color = self.selected_barcolor
            else:
                color = self.barcolor

            count = int(self.firms_counts[date]) #cast to int b/c stored as numpy val
            x, y = graph_left + dx*graph_width/total_bars + 0.5*graph_width/100, graph_bottom
            width = graph_width/total_bars - graph_width/100
            height = float(count*graph_height/largest_count) - 0.5*graph_height/100

            #Add the bar to the list of bars
            bar = GraphBar(x, y, width, height)
            current_bars.append(bar)

            drawRect(x, y, width, height, fill=rgb(*color), align='left-bottom')
        self.bars = current_bars

    def draw_trendline(self): 
        appwidth = self.config.appwidth
        appheight = self.config.appheight
        panel_width = self.config.btn_panel_width

        graph_height = 67*appheight/100
        graph_width = 90*panel_width/100
        graph_left = 5*panel_width/100
        graph_bottom = 70*appheight/100

        total_bars = len(self.firms_counts)
        largest_count = max(self.firms_counts.values())
        bar_width = graph_width/total_bars - graph_width/100

        a, b = self.trendline_coeffs

        x0 = graph_left + 0.5*graph_width/100 + bar_width/2
        xf = graph_left + graph_width - 0.5*graph_width/100 - bar_width/2

        first_line_eq = a*1 + b #Get value for x = bar 1
        second_line_eq = a*total_bars + b #Get y val for x = bar 2

        y0 = float(graph_bottom - (first_line_eq)*graph_height/largest_count) 
        yf = float(graph_bottom - (second_line_eq)*graph_height/largest_count) 
    
        if yf < graph_bottom - graph_height:
            yf = graph_bottom - graph_height #Because the trendline has a large slope, we need to cap it off at the top of the graph such that it doesn't go over
            #FIXME -- (turns out, it always is, (ig trendline is just too fat... not sure if this is a bug, or just how the math works out, but eh))
            

        drawLine(x0, y0, xf, yf, fill='green', lineWidth=4, dashes=True)
    


    def draw_info_if_hovering(self, bar_idx:int or None): 
        '''Draws a little text box displaying the date associated with the bar and how many firms events occured on that date.'''
        if bar_idx == None or bar_idx > len(self.firms_counts) or bar_idx < 0: #Need to add this second case if the user tries scaling the bars while hovering over a bar
            return
        
        #Date range associated with the bar
        date_range = list(self.firms_counts.keys())[bar_idx]
        count = self.firms_counts[date_range]

        def date_to_str(date:datetime.date):
            year, month, day = date.year, date.month, date.day
            return f'{year}-{month}-{day}'
        
        startdate = date_to_str(date_range[0])
        enddate = date_to_str(date_range[1])

        text = f'FIRMS events from {startdate} to {enddate}: {count}'
        
        #Draw the label:==========================
        appwidth = self.config.appwidth
        appheight = self.config.appheight
        panel_width =  self.config.btn_panel_width

        graph_left = 5*panel_width/100
        graph_top = 3*appheight/100
        graph_width = 90*panel_width/100

        drawLabel(text, graph_left + graph_width/2, graph_top + 2*appheight/100,
                  size=18, font='montserrat', fill='white') #FIXME Font not working, but whatever ig