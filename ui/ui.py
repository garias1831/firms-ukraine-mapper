from cmu_graphics import * #Import star bad, but cmu_graphics convention
import ui.assets

def config_app(app):
    app.config = ui.assets.VisualConfig(_bgcolor=(54, 130, 127))

def onAppStart(app):
    config_app(app)

def redrawAll(app):
    draw_background(app)

def draw_background(app):
    drawRect(0, 0, app.width, app.height, fill=rgb(*app.config.bgcolor))

#==============App configuration methods========================================================

def run_ui():
    runApp()
    
    

