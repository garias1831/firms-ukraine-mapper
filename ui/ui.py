from cmu_graphics import * #Import star bad, but cmu_graphics convention
import ui.assets

def config_app(app):
    app.config = ui.assets.VisualConfig(_bgcolor=(54, 130, 127))
    app.screen = ui.assets.AppScreen(_border=(1, 2, 3))

def onAppStart(app):
    config_app(app)

def redrawAll(app):
    draw_background(app)
    draw_main_screen(app)

#=============#Drawing==========================================================================

def draw_background(app):
    drawRect(0, 0, app.width, app.height, fill=rgb(*app.config.bgcolor))

def draw_main_screen(app):
    url = r'C:\code\python\firms-ukraine-mapper\ui\images\ukraine.png'
    drawImage(url, 7*app.width/24, app.height/15, width=app.width/2, height=13*app.height/15, #Looks aight, but not totes epic. Also looks bad when resized souper small
              border=rgb(*app.screen.border), borderWidth=3) #TODO - change the URL to not be absolute


    #drawRect(7*app.width/24, app.height/15, app.width/2, 13*app.height/15, 
             #fill='white', border=rgb(*app.screen.border), borderWidth=2) #TODO -- might be nice to implement a better resizing algo like in the myannmar project, where it only resizes to a certain size

#==============App configuration methods========================================================

def run_ui():
    runApp()
    
    

