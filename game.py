"""
Starflight: The Lost Colony (Remastered)

ENGINE-LEVEL CODE

Main loop that calls gameplay methods

Requires Python 3.10
See Engine.py for dependent libraries
        
"""

import sys, time, random, math, pygame, pygame_gui
from pygame.locals import (
    K_UP,K_DOWN,K_LEFT,K_RIGHT,K_ESCAPE,K_RETURN,K_SPACE,KEYDOWN,QUIT,
    K_a,K_s,K_d,K_f
)
import Engine
import TileScroller


"""
all globals must be pre-defined
"""
C_GRAY=(200,200,200)

running=False
screen=None
backbuffer=None
fontl=None
fonts=None

gui=None
guiwin_debug=None
guitxt_debug=None
guibtn_test=None
guibtn_testsprite1=None
guibtn_testsprite2=None
guibtn_testsprite3=None
guiwin_sprite1=None
guiimg_sprite1=None
guilbl_sprite1=None
guiwin_sprite2=None
guiimg_sprite2=None 
guilbl_sprite2=None 
guiwin_sprite3=None
guiimg_sprite3=None 
guilbl_sprite3=None 

scrolldirx=1
scrolldiry=1
scrollspeedx=2.0
scrollspeedy=3.0


def game_init():
    """
    Game engine initialization
    in a future update each module will have its own engine calls for init, update, draw
    """
    global screen, backbuffer, SCREENW, SCREENH
    global fontl, fonts, timer
    global ship

    pygame.init()

    SCREENW,SCREENH = 1600,1024 #2560,1440

    #create the screen object used to render the backbuffer
    screen = pygame.display.set_mode(size= (SCREENW,SCREENH))
    #pygame.display.toggle_fullscreen()

    title = "Starflight: The Lost Colony (Remastered)"
    pygame.display.set_caption(title + " (" + str(SCREENW) + "x" + str(SCREENH)+ ")")
    print("\n" + title)
    
    w,h = screen.get_width(), screen.get_height()
    print("Screen: " + str(w) + "/" + str(h))

    print("Display modes:")
    modes=pygame.display.list_modes(depth=0, flags=0, display=0)
    t=""
    for m in modes:
        if m[1] > 700:
            t += str(m[0]) + "/" + str(m[1]) + ", "
    print(t)

    #create the backbuffer used for all rendering
    backbuffer = pygame.Surface((SCREENW,SCREENH))
    
    #this avoids slow font scaling (add more if needed)
    fontl = pygame.font.SysFont('arial', size=24, bold=True)
    fonts = pygame.font.SysFont('arial', size=16, bold=False)

    pygame.mouse.set_visible(True)

    timer = pygame.time.Clock()

    #load game assets


    
def game_gui_init():
    """
    Initialize the GUI - generic for now
    A gui sub-class will be needed that works nicely with the engine with update/draw methods and a common theme
    """
    global gui, guiwin_debug, guitxt_debug, guibtn_test
    global guiwin_sprite1, guiimg_sprite1, guilbl_sprite1, guibtn_testsprite1
    global guiwin_sprite2, guiimg_sprite2, guilbl_sprite2, guibtn_testsprite2
    global guiwin_sprite3, guiimg_sprite3, guilbl_sprite3, guibtn_testsprite3

    gui = pygame_gui.UIManager((SCREENW,SCREENH))

    #build the gui debug window
    w,h = 600,300
    x,y = SCREENW-w,SCREENH-h
    guiwin_debug = pygame_gui.elements.UIWindow( 
        rect=pygame.Rect((x,y),(w,h)),
        window_display_title="DEBUG OUTPUT",
        element_id="guiwin_debug",
        manager=gui
    )
    guitxt_debug = pygame_gui.elements.UITextBox( 
        relative_rect=pygame.Rect((0,0),(w-10,200)),
        html_text="",
        container=guiwin_debug, manager=gui
    )
    guibtn_test = pygame_gui.elements.UIButton(
        relative_rect=pygame.Rect((0, 200), (120, 40)), 
        text="MessageBox", 
        container=guiwin_debug, manager=gui
    )
    guibtn_testsprite1 = pygame_gui.elements.UIButton(
        relative_rect=pygame.Rect((120,200),(140,40)),
        text="Star Sprite",
        container=guiwin_debug, manager=gui 
    )
    guibtn_testsprite2 = pygame_gui.elements.UIButton(
        relative_rect=pygame.Rect((260,200),(140,40)),
        text="Planet Sprite",
        container=guiwin_debug, manager=gui
    )
    guibtn_testsprite3 = pygame_gui.elements.UIButton(
        relative_rect=pygame.Rect((400,200),(140,40)),
        text="Ship Transforms",
        container=guiwin_debug, manager=gui
    )

    #build the sprite1 test window
    w,h = 260,210
    x,y = 0,0
    guiwin_sprite1 = pygame_gui.elements.UIWindow(
        rect=pygame.Rect((x,y),(w,h)),
        window_display_title="STAR ANIMATION",
        element_id="guiwin_sprite1",
        manager=gui
    )
    guiwin_sprite1.disable()
    #guiwin_sprite1.hide()
    guiimg_sprite1 = pygame_gui.elements.UIImage(
        relative_rect=pygame.Rect((0,0),(w-10,h-10)),
        image_surface=pygame.Surface((w-10,h-10)),
        container=guiwin_sprite1, manager=gui
    )
    guilbl_sprite1 = pygame_gui.elements.UILabel(
        relative_rect=pygame.Rect((0,130),(-1,-1)),
        object_id="guilbl_sprite1",
        text="star animation",
        container=guiwin_sprite1, manager=gui
    )

    #build the sprite2 test window
    w,h = 340,340
    x,y = 0,200
    guiwin_sprite2 = pygame_gui.elements.UIWindow(
        rect=pygame.Rect((x,y),(w,h)),
        window_display_title="PLANET ANIMATION",
        element_id="guiwin_sprite2",
        manager=gui
    )
    guiwin_sprite2.disable()
    guiimg_sprite2 = pygame_gui.elements.UIImage(
        relative_rect=pygame.Rect((0,0),(w-10,h-10)),
        image_surface=pygame.Surface((w-10,h-10)),
        container=guiwin_sprite2, manager=gui
    )
    guilbl_sprite2 = pygame_gui.elements.UILabel(
        relative_rect=pygame.Rect((0,260),(-1,-1)),
        object_id="guilbl_sprite2",
        text="planet animation",
        container=guiwin_sprite2, manager=gui
    )

    #build the sprite3 test window
    w,h = 450,450
    x,y = 0,530
    guiwin_sprite3 = pygame_gui.elements.UIWindow(
        rect=pygame.Rect((x,y),(w,h)),
        window_display_title="SHIP TRANSFORMS",
        element_id="guiwin_sprite3",
        manager=gui
    )
    guiwin_sprite3.disable()
    guiimg_sprite3 = pygame_gui.elements.UIImage(
        relative_rect=pygame.Rect((0,0),(w-10,h-10)),
        image_surface=pygame.Surface((w-10,h-10)),
        container=guiwin_sprite3, manager=gui
    )
    guilbl_sprite3 = pygame_gui.elements.UILabel(
        relative_rect=pygame.Rect((0,370),(-1,-1)),
        object_id="guilbl_sprite3",
        text="ship transforms",
        container=guiwin_sprite3, manager=gui
    )
    
    
def add_debug_text(text):
    guitxt_debug.html_text += text + "<br>"
    guitxt_debug.rebuild()

def clear_debug_text(target):
    """ 
    display helpful information during development 
    """
    guitxt_debug.html_text = ""
    guitxt_debug.rebuild()



def game_update(surf, time_delta):
    """
    Main engine gameplay timed updates
    in a future update each module will have its own engine calls for init, update, draw
    """
    global fontl,fonts
    global playership
    #do nothing yet

    

""" 
ENGINE INIT 
"""
game_init()
game_gui_init()
game_over = False
last_time = 0
inputdelay = 0
clock = pygame.time.Clock()

""" 
ENGINE INIT END
"""

""" 
GAMEPLAY INIT
"""

star = Engine.Sprite()
star.load_image("is_tiles.png")
star.init_animation(128,128,5)
star.firstFrame = 1
star.lastFrame = 8
star.position = (0,0) #relative inside guiwindow
star.DebugMode = True
star.DebugColor = (60,60,255)

planet = Engine.Sprite()
planet.load_image("ip_tiles.png")
planet.init_animation(256,256,9)
planet.firstFrame = 1
planet.lastFrame = 8
planet.position = (0,0) #relative inside guiwindow
planet.DebugMode = True
planet.DebugColor = (255,200,100)

srship = Engine.Sprite()
srship.load_image("Player_Ship_Military.png")
srship.init_animation()
srship.position = (0,0) #relative inside guiwindow
srship.DebugMode = True
srship.DebugColor = (60,60,60)
scale = 1.0
sdir = 1.0
angle = 1


#create the tile scroller
ts = TileScroller.TileScroller(128,128,40,40)
ts.createScrollBuffer(900,900)
ts.loadTilemapSourceImage("is_tiles.png", 5)

print("")
s = ""
t=0
for y in range(20):
    t = (t+1) % 10
    for x in range(20):
        ts.setTile(x,y,t)
        s += str( ts.getTile(x,y) )+","
    print(s)
    s=""

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

        #send events to GUI
        gui.process_events(event)
        
        #handle all gui buttons
        if event.type == pygame_gui.UI_BUTTON_PRESSED:
        
            #handle event to show messagebox
            if event.ui_element == guibtn_test:
                msgbox = pygame_gui.windows.ui_message_window.UIMessageWindow(
                    rect=pygame.Rect((500,500),(200,160)),
                    html_message="This is a message box test",
                    manager=gui,
                    window_title="Message Test"
                )

            elif event.ui_element == guibtn_testsprite1:
                star.alive = not star.alive 
                if guiwin_sprite1.visible:
                    guiwin_sprite1.hide()
                else:
                    guiwin_sprite1.show()

            elif event.ui_element == guibtn_testsprite2:
                planet.alive = not planet.alive
                if guiwin_sprite2.visible:
                    guiwin_sprite2.hide()
                else:
                    guiwin_sprite2.show()

            elif event.ui_element == guibtn_testsprite3:
                srship.alive = not srship.alive
                if guiwin_sprite3.visible:
                    guiwin_sprite3.hide()
                else:
                    guiwin_sprite3.show()


    #let the GUI perform updates
    gui.update(0)

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
    backbuffer.fill((60,60,60))

    #reset debug text buffer
    clear_debug_text(backbuffer)

    x,y = pygame.mouse.get_pos()
    add_debug_text("Mouse: " + str(x) + "," + str(y))


    #run some tests

    #star sprite test
    if star.alive:
        star.update(300)
        guiimg_sprite1.set_image(star.image)
        guilbl_sprite1.set_text( str(star) )

    #planet sprite test
    if planet.alive:
        planet.update(400)
        guiimg_sprite2.set_image(planet.image)
        guilbl_sprite2.set_text( str(planet) )


    #ship transforms test
    if srship.alive:
        angle = Engine.wrap_angle(angle+1)
        scale += 0.025 * sdir
        if scale > 1.0 or scale < 0.01: sdir *= -1
        srship.update(100)

        srship.scale_rotate(scale, angle, True)

        guiimg_sprite3.set_image(srship.rotated_image)
        guilbl_sprite3.set_text( str(srship) )



    #test the tile scroller
    sx = scrollspeedx * scrolldirx
    if not ts.scroll(sx,0):
        scrolldirx *= -1

    sy = scrollspeedy * scrolldiry 
    if not ts.scroll(0,sy):
        scrolldiry *= -1

    ts.updateScrollBuffer()
    ts.drawScrollWindow(backbuffer, 600, 20, 800, 800)
    pos = (ts.scrollx,ts.scrolly)
    add_debug_text("ts: " + str(ts) )



    game_update(backbuffer, 0)
   
    gui.draw_ui(backbuffer)

    #draw the back buffer
    screen.blit(backbuffer, (0,0))

    pygame.display.update()

    """
    ENGINE RENDERING END
    """

    
pygame.quit()

