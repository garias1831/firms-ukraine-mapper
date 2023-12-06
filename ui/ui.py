from cmu_graphics import * #Import star bad, but cmu_graphics convention
import ui.assets
import datetime

def onAppStart(app): 
    app.stepsPerSecond = 8 #FIXME -- not rrly sure how fast i want the app to run, or how many shapes we should allow, but dis works
    app.setMaxShapeCount(8000)

def redrawAll(app):
    draw_background(app) #TODO -- clean this up
    app.screen.draw_app_screen()
    app.uilayout.timelapse_btn.draw_timelapse_btn()
    app.uilayout.timelapse_forward_btn.draw_forward_btn()
    app.uilayout.timelapse_back_btn.draw_back_btn()
    app.timeline.draw_timeline()
    app.timeline.draw_slider()
    app.graph.draw_background()

    timelapse_month_yr = datetime.date(year=app.timelapse_date.year, month=app.timelapse_date.month, day=1)
    app.graph.draw_bars(timelapse_month_yr)
    app.graph.draw_trendline()
    app.graph.draw_info_if_hovering(app.bar_showing_info)    
    app.screen.draw_firms() #This is slow when drawing a ton ton, but works for most purposess

def draw_background(app):
    drawRect(0, 0, app.width, app.height, fill=rgb(*app.config.bgcolor))    

def onResize(app):
    update_app_size(app)
    
def update_app_size(app):
    '''Constinuously updates the dimensions of the app in the global config.'''
    app.config.set_appsize(app.width, app.height)
    app.uilayout.fix_element_layouts() #Update the layout values
    app.uilayout.place_ui_elements() #Update the widget instances with the new layout values
    app.timeline.set_size()

def onStep(app):
    if app.timelapse_started:
        if app.timelapse_forward:
            dt = 1
        else:
            dt = -1
        update_screen(app, dt)
        update_timeline_slider(app)

def update_screen(app, dt:int):
    '''Adds new firms onto the appscreen.'''
    app.screen.firms = app.datamanager.get_firms_from_date(app.timelapse_date)
    next_date = app.timelapse_date + dt*datetime.timedelta(days=1) 
    if app.datamanager.is_valid_date(next_date):
        app.timelapse_date = next_date

def update_timeline_slider(app):
    timelapse_progress = app.datamanager.get_timelapse_progress(app.timelapse_date)
    app.timeline.timelapse_progress = timelapse_progress

def onMousePress(app, mouseX, mouseY):
    if app.uilayout.timelapse_btn.click_intercepted(mouseX, mouseY):
        app.uilayout.timelapse_btn.pressed(app)
    if app.uilayout.timelapse_forward_btn.click_intercepted(mouseX, mouseY):
        app.timelapse_forward = True
    if app.uilayout.timelapse_back_btn.click_intercepted(mouseX, mouseY):
        app.timelapse_forward = False

def onMouseMove(app, mouseX, mouseY):
    check_bar_hovering(mouseX, mouseY)

def check_bar_hovering(mouseX, mouseY):
    for idx, bar in enumerate(app.graph.bars):
        if bar.mouse_over_bar(mouseX, mouseY):
            app.bar_showing_info = idx
            return
    app.bar_showing_info = None

def onMouseDrag(app, mouseX, mouseY):
    if app.timeline.mouse_over_slider(mouseX, mouseY):
        progress = app.timeline.get_timelapse_progress_from_x(mouseX)
        app.timelapse_date = app.datamanager.get_closest_date_from_progress(progress)
        app.timeline.timelapse_progress = progress
        
def onKeyPress(app, key): 
    if key == 'n': 
        app.graph.bars_per_month += 1
        counts = app.datamanager.get_firms_per_months(app.graph.bars_per_month) #FIXME -- dis a lil laggy, but is okay
        app.graph.firms_counts = counts
        app.graph.coeffs = app.datamanager.get_trendline_coeffs(counts)
    if key == 'm':
        app.graph.bars_per_month -= 1
        counts = app.datamanager.get_firms_per_months(app.graph.bars_per_month)
        app.graph.firms_counts = counts
        app.graph.coeffs = app.datamanager.get_trendline_coeffs(counts)

#==============App configuration methods========================================================
def load_ui_elements(app):
    '''Creates instances of the UI assets from the assets.py file and stores them as attributes in the app class.'''
    app.config = ui.assets.VisualConfig(app.width, app.height, bgcolor=(33, 33, 33))
    app.uilayout = ui.assets.UILayout(app.config) #Some elements loaded within this class
    app.uilayout.load_ui_elements() #Instantiate button objects
    app.uilayout.fix_element_layouts()
    app.uilayout.place_ui_elements()
    
    #Instantiate non-button objects
    app.screen = ui.assets.AppScreen(app.config, border=(48, 48, 48)) 
    app.timeline = ui.assets.Timeline(app.config, color=(129, 134, 156), slider_color=(250, 243, 243))
    counts = app.datamanager.get_firms_per_months(1) 
    coeffs = app.datamanager.get_trendline_coeffs(counts)
    app.graph = ui.assets.Graph(app.config, counts, coeffs, bgcolor=(46, 53, 83), axiscolor=(250, 243, 243),
                                barcolor=(224, 102, 102), selected_barcolor=(234, 153, 153))

def load_data_attributes(app, datamanager):
    '''Loads data related to the application state.'''
    app.datamanager = datamanager
    app.timelapse_date = datetime.date(year=2022, month=2, day=24) #Feb 24, 2022
    app.timelapse_started = False
    app.timelapse_forward = True #Timelapse can either run forwards or backwards
    app.bar_showing_info = None #The current bar on the graph displaying its info panel when 

def run_ui(datamanager):
    load_data_attributes(app, datamanager)
    load_ui_elements(app)
    runApp()