from cmu_graphics import * #Import star bad, but cmu_graphics convention
import ui.assets

def config_app(app):
    #app.width = 1920 #TODO -- make this generic fullscreen (if possible)
    #app.height = 1080

    app.config = ui.assets.VisualConfig(app.width, app.height, bgcolor=(33, 33, 33))
    app.screen = ui.assets.AppScreen(app.config, border=(1, 2, 3))
    app.timelapse_btn = ui.assets.TimelapseBtn(app.config)

def onAppStart(app):
    config_app(app)

def redrawAll(app):
    draw_background(app)
    draw_screen(app)
    app.timelapse_btn.draw_timelapse_btn()

#=============#Drawing==========================================================================

def draw_background(app):
    drawRect(0, 0, app.width, app.height, fill=rgb(*app.config.bgcolor))

def draw_screen(app):
    app.screen.draw_app_screen()

def onStep(app):
    update_app_size(app)

    
def update_app_size(app):
    '''Updates the dimensions of the app in the global config.'''
    app.config.appwidth = app.width
    app.config.appheight = app.height

#==============App configuration methods========================================================

def run_ui(): 
    runApp()
    
    

