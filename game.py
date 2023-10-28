"""
Starflight: The Lost Colony (Remastered)

ENGINE-LEVEL CODE

Main loop that calls gameplay methods

Requires Python 3.10
See Engine.py for dependent libraries

*** THIS IS STILL IN EARLY DEV: IT WILL BE CLEANED UP! ***
        
"""

import sys, time, random, math, pygame, pygame_gui
from pygame.locals import (
    K_UP,K_DOWN,K_LEFT,K_RIGHT,K_ESCAPE,K_RETURN,K_SPACE,KEYDOWN,QUIT,
    K_a,K_s,K_d,K_f
)
from pygame import gfxdraw 
import Engine
import TileScroller
import TexturedSphere
from enum import Enum
import NoiseUtils 
from PIL import Image 
import Galaxy 
from Galaxy import *

"""
all globals must be pre-defined
"""
C_GRAY=(200,200,200)

class Globals():
    def __init__(self):
        self.SCREENW:int=0
        self.SCREENH:int=0

        self.noise = None 
        self.pixels = None
        self.imageSize = 256

        self.running=False
        self.screen=None
        self.backbuffer=None
        self.fontl=None
        self.fonts=None
        self.fontt=None

        self.GALAXY_LIMIT_X = 256 #tiles
        self.GALAXY_LIMIT_Y = 256
        self.ts:TileScroller.TileScroller = None 
        self.guiwin_space:pygame_gui.elements.UIWindow=None 
        self.guitxt_space:pygame_gui.elements.UITextBox=None 
        self.guilbl_space:pygame_gui.elements.UILabel=None
        self.scrolldirx=1
        self.scrolldiry=1
        self.scrollspeedx=0.0
        self.scrollspeedy=0.0

        self.gui=None
        self.guiwin_debug:pygame_gui.elements.UIWindow=None
        self.guitxt_debug=None
        self.guibtn_test=None
        self.guibtn_testsprite1=None
        self.guibtn_testsprite2=None
        self.guibtn_testsprite3=None
        self.guiwin_sprite1:pygame_gui.elements.UIWindow=None
        self.guiimg_sprite1=None
        self.guilbl_sprite1=None
        self.guiwin_sprite2:pygame_gui.elements.UIWindow=None
        self.guiimg_sprite2=None 
        self.guilbl_sprite2=None 
        self.guiwin_sprite3:pygame_gui.elements.UIWindow=None
        self.guiimg_sprite3=None 
        self.guilbl_sprite3=None 

        self.perlinSurface=None

globals:Globals = Globals()



def engine_init():
    """
    Game engine initialization
    in a future update each module will have its own engine calls for init, update, draw
    """
    pygame.init()

    globals.SCREENW = 1600 #2560
    globals.SCREENH = 1024 #1440

    #create the screen object used to render the backbuffer
    globals.screen = pygame.display.set_mode(size= (globals.SCREENW, globals.SCREENH))
    #pygame.display.toggle_fullscreen()

    title = "Starflight: The Lost Colony (Remastered)"
    pygame.display.set_caption(title + " (" + str(globals.SCREENW) + "x" + str(globals.SCREENH)+ ")")
    print("\n" + title)
    
    w,h = globals.screen.get_width(), globals.screen.get_height()
    print("Screen: " + str(w) + "/" + str(h))

    print("Display modes:")
    modes=pygame.display.list_modes(depth=0, flags=0, display=0)
    t=""
    for m in modes:
        if m[1] > 700:
            t += str(m[0]) + "/" + str(m[1]) + ", "
    print(t)

    #create the backbuffer used for all rendering
    globals.backbuffer = pygame.Surface((globals.SCREENW,globals.SCREENH))
    
    #this avoids slow font scaling (add more if needed)
    globals.fontl = pygame.font.SysFont("arial", size=24, bold=True)
    globals.fonts = pygame.font.SysFont("arial", size=16, bold=False)
    globals.fontt = pygame.font.SysFont("arial", size=12, bold=False)

    pygame.mouse.set_visible(True)

    globals.timer = pygame.time.Clock()


def gameplay_init():
    """
    Gameplay initialization 
    """
    a=0
  
    
def gameplay_gui_init():
    """
    Initialize the GUI - generic for now
    A gui sub-class will be needed that works nicely with the engine with update/draw methods and a common theme
    """
    globals.gui = pygame_gui.UIManager((globals.SCREENW,globals.SCREENH))

    #build the gui debug window
    w,h = 580,200
    x,y = 0, globals.SCREENH-h
    globals.guiwin_debug = pygame_gui.elements.UIWindow( 
        rect=pygame.Rect((x,y),(w,h)),
        window_display_title="DEBUG OUTPUT",
        element_id="guiwin_debug",
        manager=globals.gui
    )
    globals.guitxt_debug = pygame_gui.elements.UITextBox( 
        relative_rect=pygame.Rect((0,0),(w-10,h-100)),
        html_text="",
        container=globals.guiwin_debug, manager=globals.gui
    )
    guibtn_test = pygame_gui.elements.UIButton(
        relative_rect=pygame.Rect((0, h-100), (120, 40)), 
        text="MessageBox", 
        container=globals.guiwin_debug, manager=globals.gui
    )
    guibtn_testsprite1 = pygame_gui.elements.UIButton(
        relative_rect=pygame.Rect((120,h-100),(140,40)),
        text="Star Sprite",
        container=globals.guiwin_debug, manager=globals.gui 
    )
    guibtn_testsprite2 = pygame_gui.elements.UIButton(
        relative_rect=pygame.Rect((260,h-100),(140,40)),
        text="Planet Sprite",
        container=globals.guiwin_debug, manager=globals.gui
    )
    guibtn_testsprite3 = pygame_gui.elements.UIButton(
        relative_rect=pygame.Rect((400,h-100),(140,40)),
        text="Ship Transforms",
        container=globals.guiwin_debug, manager=globals.gui
    )

    #build the sprite1 test window
    w,h = 260,210
    x,y = 0,0
    globals.guiwin_sprite1 = pygame_gui.elements.UIWindow(
        rect=pygame.Rect((x,y),(w,h)),
        window_display_title="STAR ANIMATION",
        element_id="guiwin_sprite1",
        manager=globals.gui
    )
    globals.guiwin_sprite1.disable()
    #guiwin_sprite1.hide()
    globals.guiimg_sprite1 = pygame_gui.elements.UIImage(
        relative_rect=pygame.Rect((0,0),(w-10,h-10)),
        image_surface=pygame.Surface((w-10,h-10)),
        container=globals.guiwin_sprite1, manager=globals.gui
    )
    globals.guilbl_sprite1 = pygame_gui.elements.UILabel(
        relative_rect=pygame.Rect((0,130),(-1,-1)),
        object_id="guilbl_sprite1",
        text="star animation",
        container=globals.guiwin_sprite1, manager=globals.gui
    )

    #build the sprite2 test window
    w,h = 300,340
    x,y = 0,190
    globals.guiwin_sprite2 = pygame_gui.elements.UIWindow(
        rect=pygame.Rect((x,y),(w,h)),
        window_display_title="PLANET ANIMATION",
        element_id="guiwin_sprite2",
        manager=globals.gui
    )
    globals.guiwin_sprite2.disable()
    globals.guiimg_sprite2 = pygame_gui.elements.UIImage(
        relative_rect=pygame.Rect((0,0),(w-10,h-10)),
        image_surface=pygame.Surface((w-10,h-10)),
        container=globals.guiwin_sprite2, manager=globals.gui
    )
    globals.guilbl_sprite2 = pygame_gui.elements.UILabel(
        relative_rect=pygame.Rect((0,260),(-1,-1)),
        object_id="guilbl_sprite2",
        text="planet animation",
        container=globals.guiwin_sprite2, manager=globals.gui
    )

    #build the sprite3 test window
    w,h = 300,300
    x,y = 0,510
    globals.guiwin_sprite3 = pygame_gui.elements.UIWindow(
        rect=pygame.Rect((x,y),(w,h)),
        window_display_title="SHIP TRANSFORMS",
        element_id="guiwin_sprite3",
        manager=globals.gui
    )
    globals.guiwin_sprite3.disable()
    globals.guiimg_sprite3 = pygame_gui.elements.UIImage(
        relative_rect=pygame.Rect((0,0),(w-10,h-10)),
        image_surface=pygame.Surface((w-10,h-10)),
        container=globals.guiwin_sprite3, manager=globals.gui
    )
    globals.guilbl_sprite3 = pygame_gui.elements.UILabel(
        relative_rect=pygame.Rect((0,370),(-1,-1)),
        object_id="guilbl_sprite3",
        text="ship transforms",
        container=globals.guiwin_sprite3, manager=globals.gui
    )


    #build the space travel test window 
    w,h = 510,800
    x,y = 280,0
    globals.guiwin_space = pygame_gui.elements.UIWindow(
        rect=pygame.Rect((x,y),(w,h)),
        window_display_title="SPACE TRAVEL",
        element_id="guiwin_space",
        manager=globals.gui
    )
    globals.guitxt_space = pygame_gui.elements.UITextBox( 
        relative_rect=pygame.Rect((0,0),(w-29,h-100)),
        html_text="", 
        container=globals.guiwin_space, manager=globals.gui
    )    
    globals.guilbl_space = pygame_gui.elements.UILabel(
        relative_rect=pygame.Rect((0,h-80),(-1,-1)),
        object_id="guilbl_space",
        text="space travel label",
        container=globals.guiwin_space, manager=globals.gui
    )


def add_debug_text(text):
    globals.guitxt_debug.html_text += text + "<br>"
    globals.guitxt_debug.rebuild()

def clear_debug_text(target):
    """ 
    display helpful information during development 
    """
    globals.guitxt_debug.html_text = ""
    globals.guitxt_debug.rebuild()



def game_update(surf, time_delta):
    """
    Main engine gameplay timed updates
    in a future update each module will have its own engine calls for init, update, draw
    """
    #do nothing yet
    a=0

    

""" 
ENGINE INIT 
"""
engine_init()
gameplay_init()
gameplay_gui_init()
globals.game_over = False
globals.last_time = 0
globals.inputdelay = 0
globals.clock = pygame.time.Clock()

""" 
ENGINE INIT END
"""


""" 
GAMEPLAY INIT
"""

star_sp = Engine.Sprite()
star_sp.load_image("is_tiles.png")
star_sp.init_animation(128,128,5)
star_sp.firstFrame = 1
star_sp.lastFrame = 8
star_sp.position = (0,0) #relative inside guiwindow
star_sp.DebugMode = True
star_sp.DebugColor = (60,60,255)

planet_sp = Engine.Sprite()
planet_sp.load_image("ip_tiles.png")
planet_sp.init_animation(256,256,9)
planet_sp.firstFrame = 1
planet_sp.lastFrame = 8
planet_sp.position = (0,0) #relative inside guiwindow
planet_sp.DebugMode = True
planet_sp.DebugColor = (255,200,100)

srship = Engine.Sprite()
srship.load_image("Player_Ship_Military.png")
srship.init_animation()
srship.position = (0,0) #relative inside guiwindow
srship.DebugMode = True
srship.DebugColor = (60,60,60)
scale = 0.4
sdir = 1.0
angle = 1



"""
test the textured sphere
"""
image_file = "molten.png"
sphere = TexturedSphere.TexturedSphere()
if not sphere.LoadTexture(image_file): 
    print("Error loading " + image_file)
    sys.exit()

 #planet rotation 
planetRotationSpeed = 1.0
planetRotation = 0.0
planetRadius = 64


"""
load the galaxy
"""
galaxy = Galaxy()
res = galaxy.Load("galaxy.xml")
if res==False:
    print("Error loading galaxy data")
    sys.exit()

text = "Galaxy data loaded: " + \
        "Stars: " + str(galaxy.GetTotalStars()) + ", " + \
        "Planets: " + str(galaxy.GetTotalPlanets()) + "<br>"

for star in galaxy.stars:
    text += str(star) + "<br>"

globals.guitxt_space.html_text += text
globals.guitxt_space.rebuild()

"""
create the tile scroller
"""

globals.ts = TileScroller.TileScroller(128,128,256,256)
globals.ts.createScrollBuffer(900,900)
globals.ts.loadTilemapSourceImage("is_tiles.png", 5)

for star in galaxy.stars:
    if star.x < 0 or star.x > globals.GALAXY_LIMIT_X:
        print("Star "+str(star.id) +" is out of bounds")
    if star.y < 0 or star.y > globals.GALAXY_LIMIT_Y:
        print("Star "+str(star.id) +" is out of bounds")

    spec_index = SpectralIndex(star.spectralClass)

    globals.ts.setTile(star.x, star.y, spec_index)

globals.ts.setTile(1, 1, 1)


"""
PERLIN TEXTURE TEST
"""
"""
#create perlin noise data for a texture
noise = NoiseUtils.NoiseUtils(imageSize)
noise.makeTexture(texture = noise.planetTexture)

#transfer perlin data into a Surface
perlinSurface = pygame.Surface((imageSize,imageSize)).convert()
perlinSurface.fill((255,255,255))
for y in range(imageSize):
    for x in range(imageSize):
        c = noise.img[x, y]
        perlinSurface.set_at((x,y), (c,c,c,255))

#pygame.image.save(perlinSurface, "planet.png")
"""


""" 
GAMEPLAY INIT END
"""


""" 
-----------------------------------------------
ENGINE MAIN LOOP
-----------------------------------------------
"""
while True:
    #timer.tick(30)
    #ticks = pygame.time.get_ticks()
 
    #timeDelta = clock.tick(60)/1000.0

    """
    ENGINE INPUT/GUI HANDLER START
    """
    for event in pygame.event.get():
        if event.type == QUIT: sys.exit()
        elif event.type == KEYDOWN:
            if event.key == K_ESCAPE: sys.exit()

            elif event.key==K_LEFT: 
                globals.scrolldirx += -1
                globals.scrollspeedx = 2.0

            elif event.key==K_RIGHT: 
                globals.scrolldirx += 1
                globals.scrollspeedx = 2.0

            elif event.key==K_UP:
                globals.scrolldiry += -1
                globals.scrollspeedy = 2.0

            elif event.key==K_DOWN:
                globals.scrolldiry += 1
                globals.scrollspeedy = 2.0


        #send events to GUI
        globals.gui.process_events(event)
        
        #handle all gui buttons
        if event.type == pygame_gui.UI_BUTTON_PRESSED:
        
            #handle event to show messagebox
            if event.ui_element == globals.guibtn_test:
                msgbox = pygame_gui.windows.ui_message_window.UIMessageWindow(
                    rect=pygame.Rect((500,500),(200,160)),
                    html_message="This is a message box test",
                    manager=globals.gui,
                    window_title="Message Test"
                )

            elif event.ui_element == globals.guibtn_testsprite1:
                star_sp.alive = not star_sp.alive 
                if globals.guiwin_sprite1.visible:
                    globals.guiwin_sprite1.hide()
                else:
                    globals.guiwin_sprite1.show()

            elif event.ui_element == globals.guibtn_testsprite2:
                planet_sp.alive = not planet_sp.alive
                if globals.guiwin_sprite2.visible:
                    globals.guiwin_sprite2.hide()
                else:
                    globals.guiwin_sprite2.show()

            elif event.ui_element == globals.guibtn_testsprite3:
                srship.alive = not srship.alive
                if globals.guiwin_sprite3.visible:
                    globals.guiwin_sprite3.hide()
                else:
                    globals.guiwin_sprite3.show()


    #let the GUI perform updates
    globals.gui.update(0)

    #handle input events
    pressed_keys = pygame.key.get_pressed()
    #if ticks > inputdelay + 100:
    #    inputdelay = ticks


    """
    ENGINE INPUT/GUI HANDLER END
    """


    """
    ENGINE RENDERING START
    """
    #clear the background
    globals.backbuffer.fill((60,60,60))

    #reset debug text buffer
    clear_debug_text(globals.backbuffer)

    x,y = pygame.mouse.get_pos()
    add_debug_text("Mouse: " + str(x) + "," + str(y))


    #run some tests

    #star sprite test
    if star_sp.alive:
        star_sp.update(300)
        globals.guiimg_sprite1.set_image(star_sp.image)
        globals.guilbl_sprite1.set_text( str(star_sp) )

    #planet sprite test
    if planet_sp.alive:
        planet_sp.update(400)
        globals.guiimg_sprite2.set_image(planet_sp.image)
        globals.guilbl_sprite2.set_text( str(planet_sp) )


    #ship transforms test
    if srship.alive:
        angle = Engine.wrap_angle(angle+1)
        scale += 0.001 * sdir
        if scale > 0.6 or scale < 0.10: sdir *= -1
        srship.update(100)

        srship.scale_rotate(scale, angle, True)

        globals.guiimg_sprite3.set_image(srship.rotated_image)
        globals.guilbl_sprite3.set_text( str(srship) )

    """
    test the tile scroller
    """
    sx = globals.scrollspeedx * globals.scrolldirx 
    if not globals.ts.scroll(sx,0):
        globals.scrolldirx = 0

    sy = globals.scrollspeedy * globals.scrolldiry 
    if not globals.ts.scroll(0,sy):
        globals.scrolldiry = 0

    globals.ts.updateScrollBuffer()
    globals.ts.drawScrollWindow(globals.backbuffer, 790, 10, 800, 800)
    posx,posy = globals.ts.scrollx, globals.ts.scrolly
    globals.guilbl_space.set_text(str(globals.ts))



    #draw Perlin generated texture
    #backbuffer.blit(perlinSurface, (470,500))


    #test the textured sphere
    cx = 500; cy = 200
    planetRotation += planetRotationSpeed
    planetRotation = Engine.WrapValue(planetRotation, 0.0, 256.0)

    #sphere.Draw( backbuffer, 0, 0, planetRotation, planetRadius, cx, cy )

    #Engine.PrintText(backbuffer, fontt, (cx-50,cy+planetRadius+10), "PLANET RADIUS: " + str(planetRadius))
    #Engine.PrintText(backbuffer, fontt, (cx-50,cy+planetRadius+30), "PLANET ROTATION: " + str(planetRotation))



    game_update(globals.backbuffer, 0)
   
    globals.gui.draw_ui(globals.backbuffer)

    #draw the back buffer
    globals.screen.blit(globals.backbuffer, (0,0))

    pygame.display.update()

    """
    ENGINE RENDERING END
    """

    
pygame.quit()

