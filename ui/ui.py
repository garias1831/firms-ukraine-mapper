from cmu_graphics import * #Import star bad, but cmu_graphics convention
import ui.assets
import pandas as pd
import datetime

def onAppStart(app): #TODO -- make UI 'fullscreen', so it doesnt mess with resizing attributes
    app.stepsPerSecond = 50 #FIXME -- not rrly sure how fast i want the app to run, or how many shapes we should allow, but dis works
    app.setMaxShapeCount(10000)


def redrawAll(app):
    draw_background(app) #TODO -- clean this up
    draw_screen(app)
    app.timelapse_btn.draw_timelapse_btn()
    app.timelapse_forward_btn.draw_forward_btn()
    app.timelapse_back_btn.draw_back_btn()
    app.axis_btn_header.draw_axis_header()
    app.timeline.draw_timeline()
    app.timeline.draw_slider()

    #TODO -- test ... all data from feb 24 2023 - march 2 2023
    
    app.screen.draw_firms() #THis is slow when drawing a ton ton, but works for most purposess
#=============#Drawing==========================================================================

def draw_background(app):
    drawRect(0, 0, app.width, app.height, fill=rgb(*app.config.bgcolor))

def draw_screen(app):
    app.screen.draw_app_screen()

def onStep(app):
    update_app_size(app)
    if app.timelapse_started:
        update_screen(app)
        update_timeline_slider(app)
        

def update_app_size(app):
    '''Constinuously updates the dimensions of the app in the global config.'''
    app.config.set_appsize(app.width, app.height)
    app.timeline.set_size()

def update_screen(app):
    '''Adds new firms onto the appscreen.'''
    app.screen.firms = app.datamanager.get_firms_from_date(app.timelapse_date)
    app.timelapse_date += datetime.timedelta(days=1) #TODO -- need to put upper / lower bounds on this ,so that the timeline doesn't run forever

def update_timeline_slider(app):
    timelapse_progress = app.datamanager.get_timelapse_progress(app.timelapse_date)
    app.timeline.timelapse_progress = timelapse_progress

def onKeyPress(app, key): #TODO -- using keys for testing purposes. .. in reality, buttons should control the logic flow
    if key == 'p': #Testing purposes
        print('Timeline start!')
        app.timelapse_started = not app.timelapse_started

#==============App configuration methods========================================================

def load_ui_elements(app):
    '''Creates instances of the UI assets from the assets.py file and stores them as attributes in the app class.'''
    app.config = ui.assets.VisualConfig(app.width, app.height, bgcolor=(33, 33, 33))
    app.screen = ui.assets.AppScreen(app.config, border=(48, 48, 48))
    app.timelapse_btn = ui.assets.TimelapseBtn(app.config)
    app.timelapse_forward_btn = ui.assets.TimelapseForwardBtn(app.config)
    app.timelapse_back_btn = ui.assets.TimelaspeBackBtn(app.config)
    app.axis_btn_header = ui.assets.AxisTabHeader(app.config, color=(250, 243, 243))
    app.timeline = ui.assets.Timeline(app.config, color=(129, 134, 156), slider_color=(250, 243, 243))

def load_data_attributes(app, datamanager):
    '''Loads data related to the application state.'''
    app.datamanager = datamanager
    app.timelapse_date = datetime.date(year=2022, month=2, day=24) #Feb 24, 2022
    
    app.timelapse_started = False

def run_ui(datamanager): 
    app.width = 1536 #FIXME Need this for timeline scaling purposes
    app.height = 793
    load_ui_elements(app)
    load_data_attributes(app, datamanager)
    runApp()
    
    

