"""
Starflight: The Lost Colony (Remastered)

ENGINE-LEVEL CODE

Main loop that calls gameplay methods

Requires Python 3.10
See Engine.py for dependent libraries

*** THIS IS STILL IN EARLY DEV: IT WILL BE CLEANED UP! ***
        
"""

import sys, time, random, math, pygame, pygame_gui
from pygame.locals import *
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

        self.running=False
        self.screen=None
        self.backbuffer=None
        self.fontl=None
        self.fonts=None
        self.fontt=None

        self.GALAXY_LIMIT_X = 256 #tiles
        self.GALAXY_LIMIT_Y = 256
        self.TS_WINDOW_W = 0 #these must be set during engine_init
        self.TS_WINDOW_H = 0
        self.ts:TileScroller.TileScroller = None 
        self.guiwin_galaxy:pygame_gui.elements.UIWindow=None 
        self.guitxt_space:pygame_gui.elements.UITextBox=None 
        self.guilbl_space:pygame_gui.elements.UILabel=None
        self.scrollspeedx=0.0
        self.scrollspeedy=0.0

        self.gui=None
        self.guiwin_debug:pygame_gui.elements.UIWindow=None
        self.guitxt_debug:pygame_gui.elements.UITextBox=None
        self.guibtn_test:pygame_gui.elements.UIButton=None
        self.guibtn_testsprite1:pygame_gui.elements.UIButton=None
        self.guibtn_teststarmap:pygame_gui.elements.UIButton=None
        self.guibtn_testsprite3:pygame_gui.elements.UIButton=None
        
        self.guiwin_sprite1:pygame_gui.elements.UIWindow = None
        self.guiimg_sprite1:pygame_gui.elements.UIImage = None
        self.guilbl_sprite1:pygame_gui.elements.UILabel = None
        self.guiwin_starmap:pygame_gui.elements.UIWindow=None
        self.guiimg_starmap:pygame_gui.elements.UIImage=None 
        self.guilbl_starmap:pygame_gui.elements.UILabel=None 
        self.guiwin_sprite3:pygame_gui.elements.UIWindow=None
        self.guiimg_sprite3:pygame_gui.elements.UIImage=None 
        self.guilbl_sprite3:pygame_gui.elements.UILabel=None 

        #planet rendering
        self.noise = None 
        self.pixels = None
        self.perlinSurface:pygame.Surface=None
        self.perlinTexSize = 256
        self.sphere:TexturedSphere.TexturedSphere = None 
        self.sphereImg:pygame.Surface = None 



globals:Globals = Globals()



def engine_init():
    """
    Game engine initialization
    in a future update each module will have its own engine calls for init, update, draw
    """
    pygame.init()

    globals.SCREENW,globals.SCREENH = 1920,1080
    #globals.SCREENW,globals.SCREENH = 2560,1440

    #create the screen object used to render the backbuffer
    globals.screen = pygame.display.set_mode(size= (globals.SCREENW, globals.SCREENH))
    #pygame.display.toggle_fullscreen()

    #set scroller size based on screen size
    globals.TS_WINDOW_W = round( globals.SCREENW / 128 ) * 128
    globals.TS_WINDOW_H = round( globals.SCREENH / 128 ) * 128


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
    globals.fonts = pygame.font.SysFont("arial", size=18, bold=False)
    globals.fontt = pygame.font.SysFont("arial", size=12, bold=False)

    pygame.mouse.set_visible(True)

    #start the framerate timer running
    pygame.time.set_timer(Engine.TIMER_EVENT_FRAMERATE, 1000)

    #initialize keyboard input
    pygame.key.set_repeat(10,100)



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
    globals.guibtn_test = pygame_gui.elements.UIButton(
        relative_rect=pygame.Rect((0, h-100), (120, 40)), 
        text="MessageBox", 
        container=globals.guiwin_debug, manager=globals.gui
    )
    globals.guibtn_testsprite1 = pygame_gui.elements.UIButton(
        relative_rect=pygame.Rect((120,h-100),(140,40)),
        text="Star Sprite",
        container=globals.guiwin_debug, manager=globals.gui 
    )
    globals.guibtn_teststarmap = pygame_gui.elements.UIButton(
        relative_rect=pygame.Rect((260,h-100),(140,40)),
        text="Starmap",
        container=globals.guiwin_debug, manager=globals.gui
    )
    globals.guibtn_testsprite3 = pygame_gui.elements.UIButton(
        relative_rect=pygame.Rect((400,h-100),(140,40)),
        text="Ship Transforms",
        container=globals.guiwin_debug, manager=globals.gui
    )


    #build the star test window
    w,h = 260,210
    x,y = 0,0
    globals.guiwin_sprite1 = pygame_gui.elements.UIWindow(
        rect=pygame.Rect((x,y),(w+10,h+10)),
        window_display_title="STAR ANIMATION",
        element_id="guiwin_sprite1",
        manager=globals.gui
    )
    globals.guiwin_sprite1.hide()
    globals.guiimg_sprite1 = pygame_gui.elements.UIImage(
        relative_rect=pygame.Rect((0,0),(w,h)),
        image_surface=pygame.Surface((w,h)),
        container=globals.guiwin_sprite1, manager=globals.gui
    )
    globals.guilbl_sprite1 = pygame_gui.elements.UILabel(
        relative_rect=pygame.Rect((0,130),(-1,-1)),
        object_id="guilbl_sprite1",
        text="star animation",
        container=globals.guiwin_sprite1, manager=globals.gui
    )


    #build the starmap window
    w,h = 600,600
    x,y = 0,190
    globals.guiwin_starmap = pygame_gui.elements.UIWindow(
        rect=pygame.Rect((x,y),(w+15,h+15)),
        window_display_title="STARMAP",
        element_id="guiwin_starmap",
        manager=globals.gui
    )
    globals.guiimg_starmap = pygame_gui.elements.UIImage(
        relative_rect=pygame.Rect((0,0),(w,h)),
        image_surface=pygame.Surface((w,h)),
        container=globals.guiwin_starmap, manager=globals.gui
    )
    globals.guilbl_starmap = pygame_gui.elements.UILabel(
        relative_rect=pygame.Rect((0,h-70),(-1,-1)),
        object_id="guilbl_starmap",
        text="starmap",
        container=globals.guiwin_starmap, manager=globals.gui
    )


    #build the ship test window
    w,h = 300,300
    x,y = 0,510
    globals.guiwin_sprite3 = pygame_gui.elements.UIWindow(
        rect=pygame.Rect((x,y),(w+10,h+10)),
        window_display_title="SHIP TRANSFORMS",
        element_id="guiwin_sprite3",
        manager=globals.gui
    )
    #globals.guiwin_sprite3.disable()
    globals.guiwin_sprite3.hide()
    globals.guiimg_sprite3 = pygame_gui.elements.UIImage(
        relative_rect=pygame.Rect((0,0),(w,h)),
        image_surface=pygame.Surface((w,h)),
        container=globals.guiwin_sprite3, manager=globals.gui
    )
    globals.guilbl_sprite3 = pygame_gui.elements.UILabel(
        relative_rect=pygame.Rect((0,370),(-1,-1)),
        object_id="guilbl_sprite3",
        text="ship transforms",
        container=globals.guiwin_sprite3, manager=globals.gui
    )


    #build the galaxy data test window 
    w,h = 510,250
    x,y = 600, globals.SCREENH - h
    globals.guiwin_galaxy = pygame_gui.elements.UIWindow(
        rect=pygame.Rect((x,y),(w,h)),
        window_display_title="GALAXY DATA",
        element_id="guiwin_galaxy",
        manager=globals.gui
    )
    globals.guitxt_space = pygame_gui.elements.UITextBox( 
        relative_rect=pygame.Rect((0,0),(w-29,h-100)),
        html_text="", 
        container=globals.guiwin_galaxy, manager=globals.gui
    )    
    globals.guilbl_space = pygame_gui.elements.UILabel(
        relative_rect=pygame.Rect((0,h-80),(-1,-1)),
        object_id="guilbl_space",
        text="space travel label",
        container=globals.guiwin_galaxy, manager=globals.gui
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
    pass

    
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
star_sp.alive = False

srship = Engine.Sprite()
srship.load_image("Player_Ship_Military.png")
srship.init_animation()
srship.position = (0,0) #relative inside guiwindow
srship.DebugMode = True
srship.DebugColor = (60,60,60)
scale = 0.4
sdir = 1.0
angle = 1
srship.alive = False



"""
test the textured sphere
"""
"""
image_file = "molten_256.png"
globals.sphere = TexturedSphere.TexturedSphere()
if not globals.sphere.LoadTexture(image_file): 
    print("Error loading " + image_file)
    sys.exit()
 #planet rotation 
planetRotationSpeed = 1.0
planetRotation = 0.0
planetRadius = 64
planetTicks = 0
planetLastTicks = 0
planetDelay = 100
#the +6 is due to edges in the sphere map
globals.sphereImg = pygame.Surface((planetRadius*2+6,planetRadius*2+6)).convert_alpha()
#globals.sphereImg.set_alpha(0xff)
#globals.sphereImg.set_colorkey('#ff00ff')
#globals.sphereImg.fill('#ff00ff')
"""


"""
load the galaxy data
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
    if star.x < 0 or star.x > globals.GALAXY_LIMIT_X:
        print("Star #"+str(star.id) +" is out of bounds")
        sys.exit()
    if star.y < 0 or star.y > globals.GALAXY_LIMIT_Y:
        print("Star "+str(star.id) +" is out of bounds")
        sys.exit()
    text += str(star) + "<br>"

globals.guitxt_space.html_text += text
globals.guitxt_space.rebuild()

"""
create the tile scroller
"""
globals.ts = TileScroller.TileScroller(tilewidth=128,tileheight=128,mapwidth=256,mapheight=256)

#set scroll buffer 1 tile larger than output window
sb_width = globals.TS_WINDOW_W + globals.ts.tilewidth
sb_height = globals.TS_WINDOW_H + globals.ts.tileheight
globals.ts.createScrollBuffer(width=sb_width,height=sb_height)
globals.ts.loadTilemapSourceImage(filename="is_tiles.png", columns=5)

#populate tilemap with star tiles
for star in galaxy.stars:
    spec_index = SpectralIndex(star.spectralClass)
    globals.ts.setTile(star.x, star.y, spec_index)

#starting scroll position at home system
globals.ts.setScrollPositionByTile(122,100)


"""
populate the starmap with stars
"""
w,h = 600,600
scalex = w / globals.ts.mapwidth
scaley = h / globals.ts.mapheight
starmap_image = pygame.Surface(size=(w,h)).convert_alpha()
for star in galaxy.stars:
    x = star.x * scalex
    y = star.y * scaley
    color = star.get_color()
    pygame.draw.circle(starmap_image,color,(x,y),radius=2.0)
globals.guiimg_starmap.set_image(starmap_image)

"""
PERLIN TEXTURE TEST
"""

#create perlin noise data for a texture
"""
noise = NoiseUtils.NoiseUtils(globals.perlinTexSize)
noise.makeTexture(texture = noise.planetTexture)

#transfer perlin data into a Surface
perlinSurface = pygame.Surface((globals.perlinTexSize,globals.perlinTexSize)).convert()
perlinSurface.fill((255,255,255))
for y in range(globals.perlinTexSize):
    for x in range(globals.perlinTexSize):
        c = noise.img[x, y]
        perlinSurface.set_at((x,y), (c,c,c,255))

#pygame.image.save(perlinSurface, "planet.png")
"""


""" 
-----------------------------------------------
ENGINE MAIN LOOP
-----------------------------------------------
"""
while True:
    Engine.ms = globals.clock.tick_busy_loop(0)
    Engine.deltaTime = Engine.ms / 60
    Engine.frames += 1

    """
    ENGINE INPUT/GUI HANDLER START
    """
    for event in pygame.event.get():
        if event.type == pygame.QUIT: sys.exit()

        #used to calculate framerate
        elif event.type == Engine.TIMER_EVENT_FRAMERATE:
            Engine.frameRate = Engine.frames 
            Engine.frames = 0

        #handle key input events
        elif event.type == KEYDOWN:
            if event.key == K_ESCAPE: sys.exit()
            elif event.key==K_LEFT: 
                globals.scrollspeedx += -1.0
            elif event.key==K_RIGHT: 
                globals.scrollspeedx += 1.0
            elif event.key==K_UP:
                globals.scrollspeedy += -1.0
            elif event.key==K_DOWN:
                globals.scrollspeedy += 1.0
            elif event.key==K_SPACE:
                globals.ts.setScrollPositionByTile(122,100)
                globals.scrollspeedx = 0.0
                globals.scrollspeedy = 0.0

        elif event.type == pygame.KEYUP:
            match event.key:
                case pygame.K_LEFT:
                    globals.scrollspeedx = 0.0
                case pygame.K_RIGHT:
                    globals.scrollspeedx = 0.0
                case pygame.K_UP:
                    globals.scrollspeedy = 0.0
                case pygame.K_DOWN:
                    globals.scrollspeedy = 0.0

        #handle gui button events
        if event.type == pygame_gui.UI_BUTTON_PRESSED:

            button:pygame_gui.elements.UIButton = event.ui_element 
            #globals.guilbl_starmap.set_text(button.text)

            if button.text == "MessageBox":
                msgbox = pygame_gui.windows.ui_message_window.UIMessageWindow(
                    rect=pygame.Rect((500,500),(200,160)),
                    html_message="This is a message box test",
                    manager=globals.gui,
                    window_title="Message Test"
                )
            elif button.text == "Star Sprite":
                star_sp.alive = not star_sp.alive 
                if globals.guiwin_sprite1.visible:
                    globals.guiwin_sprite1.hide()
                else:
                    globals.guiwin_sprite1.show()
            elif button.text == "Starmap":
                if globals.guiwin_starmap.visible:
                    globals.guiwin_starmap.hide()
                else:
                    globals.guiwin_starmap.show()
            elif button.text == "Ship Transforms":
                srship.alive = not srship.alive
                if globals.guiwin_sprite3.visible:
                    globals.guiwin_sprite3.hide()
                else:
                    globals.guiwin_sprite3.show()

        #gui event processing
        globals.gui.process_events(event)

    #give gui some energy
    globals.gui.update(Engine.deltaTime)


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
    globals.backbuffer.fill((0,0,0))

    #reset debug text buffer
    clear_debug_text(globals.backbuffer)

    mx,my = pygame.mouse.get_pos()
    add_debug_text("Mouse: " + str(mx) + "," + str(my))


    """
    RUN SOME TESTS
    """


    #star sprite test
    if star_sp.alive:
        star_sp.update(300)
        globals.guiimg_sprite1.set_image(star_sp.image)
        globals.guilbl_sprite1.set_text( str(star_sp) )


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
    draw the tile scroller
    """
    sx = globals.scrollspeedx 
    if not globals.ts.scroll(sx,0):
        globals.scrollspeedx = 0

    sy = globals.scrollspeedy 
    if not globals.ts.scroll(0,sy):
        globals.scrollspeedy = 0

    #this can be optimized by only updating the buffer when the tile boundary is reached
    globals.ts.updateScrollBuffer()

    globals.ts.drawScrollWindow(dest_surface=globals.backbuffer,x=0,y=0,width=globals.TS_WINDOW_W,height=globals.TS_WINDOW_H)

    #draw Perlin generated texture
    #globals.backbuffer.blit(perlinSurface, (470,500))

    #draw the starmap
    #globals.guiimg_starmap.set_image(starmap_image)
    #globals.backbuffer.blit(starmap_image,(0,0))

    """
    planet rotation test
    """
    """
    t = "RAD " + str(planetRadius) + ", ROT " + str(planetRotation)
    globals.guilbl_starmap.set_text(t)

    if globals.guiwin_starmap.visible:
        if Engine.get_ticks() > planetLastTicks + planetDelay:
            planetLastTicks = Engine.get_ticks()

            planetRotation += 2.0 # planetRotationSpeed
            planetRotation = Engine.WrapValue(planetRotation, 0.0, 256.0)

            cx = cy = globals.sphereImg.get_width()/2
            globals.sphere.Draw( globals.sphereImg, 0, 0, planetRotation, planetRadius, cx,cy )
            globals.guiimg_starmap.set_image(globals.sphereImg)
    """


    game_update(globals.backbuffer, Engine.deltaTime)
   
    #draw the gui
    globals.gui.draw_ui(globals.backbuffer)


    #print debug info at mouse cursor 
    mx,my = pygame.mouse.get_pos()
    tsx,tsy = 0,0
    if mx > tsx and mx < tsx+globals.TS_WINDOW_W and my > tsy and my < tsy+globals.TS_WINDOW_H:
        relx,rely = mx - tsx, my - tsy
        sx,sy = globals.ts.scrollx + relx, globals.ts.scrolly + rely 
        tile = globals.ts.getTilebyCoords(sx,sy)
        tx,ty = int(sx / globals.ts.tilewidth), int(sy / globals.ts.tileheight)
        t = str(tx) + "," + str(ty)
        t += ",TILE " + str(tile)

        for star in galaxy.stars:
            if star.x == tx and star.y == ty:
                t += ",STAR " + star.name
                break 

        Engine.PrintText(globals.backbuffer, globals.fonts, (mx,my+40), t, '#ffffff')



    #print tile scroller debug info
    x,y = globals.SCREENW-300,globals.SCREENH-20
    t = str(globals.ts)
    Engine.PrintText(globals.backbuffer, globals.fonts, (x,y), t, '#cc8800')


    #print the framerate
    x,y = globals.SCREENW-100,globals.SCREENH-20
    fps = str(int(Engine.frameRate))
    t = "FPS " + fps + " ({:.2f}".format(Engine.deltaTime) + ")"
    Engine.PrintText(globals.backbuffer, globals.fonts, (x,y), t, '#cc8800')


    #draw the back buffer
    globals.screen.blit(globals.backbuffer, (0,0))

    pygame.display.update()

    """
    ENGINE RENDERING END
    """

    
pygame.quit()

