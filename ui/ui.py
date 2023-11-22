from cmu_graphics import * #Import star bad, but cmu_graphics convention
import ui.assets

def config_app(app):
    app.config = ui.assets.VisualConfig(app.width, app.height, bgcolor=(33, 33, 33))
    app.screen = ui.assets.AppScreen(app.config, border=(48, 48, 48))

    app.timelapse_btn = ui.assets.TimelapseBtn(app.config)
    app.timelapse_forward_btn = ui.assets.TimelapseForwardBtn(app.config)
    app.timelapse_back_btn = ui.assets.TimelaspeBackBtn(app.config)

    app.axis_btn_header = ui.assets.AxisTabHeader(app.config, color=(250, 243, 243))

def onAppStart(app):
    config_app(app)

def redrawAll(app):
    draw_background(app)
    draw_screen(app)
    app.timelapse_btn.draw_timelapse_btn()
    app.timelapse_forward_btn.draw_forward_btn()
    app.timelapse_back_btn.draw_back_btn()
    app.axis_btn_header.draw_axis_header()

#=============#Drawing==========================================================================

def draw_background(app):
    drawRect(0, 0, app.width, app.height, fill=rgb(*app.config.bgcolor))

def draw_screen(app):
    app.screen.draw_app_screen()

def onStep(app):
    update_app_size(app)


def update_app_size(app):
    '''Constinuously updates the dimensions of the app in the global config.'''
    app.config.set_appsize(app.width, app.height)
    

#==============App configuration methods========================================================

def run_ui(): 
    runApp()
    
    

