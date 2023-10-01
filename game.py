"""
Starflight: The Lost Colony (Remastered)

Requires Python 3.10
See Engine.py for dependent libraries
        
"""

import sys, time, random, math, pygame, pygame_gui
from pygame.locals import (
    K_UP,K_DOWN,K_LEFT,K_RIGHT,K_ESCAPE,K_RETURN,K_SPACE,KEYDOWN,QUIT,
    K_a,K_s,K_d,K_f
)
from Engine import *

"""
all globals must be pre-defined
"""
running=False
screen=None
SCREENW=1600
SCREENH=1024
backbuffer=None
fontl=None
fonts=None

C_GRAY=(200,200,200)

gui=None
guiwin_debug=None
guitxt_debug=None
guibtn_test=None


def game_init():
    """
    Game engine initialization
    in a future update each module will have its own engine calls for init, update, draw
    """
    global screen, backbuffer, SCREENW, SCREENH
    global fontl, fonts, timer
    global ship

    pygame.init()

    SCREENW,SCREENH = 1280,1024 #2560,1440

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
    global gui
    global guiwin_debug
    global guiwin_ship
    global guiimg_ship
    global guitxt_debug
    global guibtn_test
    
    gui = pygame_gui.UIManager((SCREENW,SCREENH))

    #build the debug window
    w,h = 500,300
    x = SCREENW-w
    y = SCREENH-h
    guiwin_debug = pygame_gui.elements.ui_window.UIWindow(
        rect=pygame.Rect((x,y),(w,h)),
        window_display_title="DEBUG OUTPUT",
        element_id="guiwin_debug",
        manager=gui
    )
    guitxt_debug = pygame_gui.elements.ui_text_box.UITextBox(
        relative_rect=pygame.Rect((0,0),(w-10,200)),
        html_text="",
        container=guiwin_debug,
        manager=gui
    )
    guibtn_test = pygame_gui.elements.UIButton(
        relative_rect=pygame.Rect((125, 200), (120, 40)), 
        text='Test Message', 
        container=guiwin_debug,
        manager=gui
    )
    
    
def print_debug_info(target):
    """ 
    display helpful information during development 
    """
    global fonts
    
    debugx=SCREENW-200
    debugy=SCREENH-100
    nl=16

    s = ""
    
    mouse = pygame.mouse.get_pos()
    x,y=mouse
    
    s += "Mouse: " + str(x) + "," + str(y) 
    s += "<br>"
    print_text(backbuffer, fonts, (debugx,debugy), s, C_GRAY)

    guitxt_debug.html_text = s
    guitxt_debug.rebuild()


def game_update(surf, time_delta):
    """
    Main engine gameplay timed updates
    in a future update each module will have its own engine calls for init, update, draw
    """
    global fontl,fonts
    global playership
    #do nothing yet

    
def rot_center(image, rect, angle):
    """
    rotate an image from its center
    """
    rot_image = pygame.transform.rotate(image, angle)
    rot_rect = rot_image.get_rect(center=rect.center)
    return rot_image,rot_rect
    

""" 
-----------------------------------------------
ENGINE MAIN LOOP
-----------------------------------------------
"""
game_init()
game_gui_init()
game_over = False
last_time = 0
inputdelay = 0
clock = pygame.time.Clock()

star = Sprite()
star.load_image("is_tiles.png")
star.init_animation(128,128,5)
star.firstFrame = 1
star.lastFrame = 8
star.position = (10,10)
star.DebugMode = True
star.DebugColor = (60,60,255)

planet = Sprite()
planet.load_image("ip_tiles.png")
planet.init_animation(256,256,9)
planet.firstFrame = 1
planet.lastFrame = 8
planet.position = (10,170)
planet.DebugMode = True
planet.DebugColor = (255,200,100)

srship = Sprite()
srship.load_image("Player_Ship_Military.png")
srship.init_animation()
srship.position = (10,470)
srship.DebugMode = True
srship.DebugColor = (60,60,60)
scale = 1.0
sdir = 1.0
angle = 1


#main loop
while True:
    timer.tick(30)
    ticks = pygame.time.get_ticks()
    timeDelta = clock.tick(60)/1000.0

    for event in pygame.event.get():
        if event.type == QUIT: sys.exit()
        elif event.type == KEYDOWN:
            if event.key == K_ESCAPE: sys.exit()

        #send events to GUI
        gui.process_events(event)
        
        #handle all gui buttons
        if event.type == pygame_gui.UI_BUTTON_PRESSED:
        
            #debug labels toggle
            if event.ui_element == guibtn_test:
                msgbox = pygame_gui.windows.ui_message_window.UIMessageWindow(
                    rect=pygame.Rect((500,500),(200,160)),
                    html_message="This is a message test",
                    manager=gui,
                    window_title="Message Test"
                )

    #handle input events
    pressed_keys = pygame.key.get_pressed()
    if ticks > inputdelay + 100:
        inputdelay = ticks
        
    #let the GUI perform updates
    gui.update(timeDelta)
    
    #clear the background
    backbuffer.fill((60,60,60))


    #run some tests

    planet.update(250)
    planet.draw(backbuffer)
    (x,y) = planet.position
    y += planet.frameHeight
    print_text(backbuffer, fonts, (x,y), str(planet))


    star.update(500)
    star.draw(backbuffer)
    (x,y) = star.position
    y += star.frameHeight
    print_text(backbuffer, fonts, (x,y), str(star))


    angle = wrap_angle(angle+1)
    scale += 0.025 * sdir
    if scale > 1.0 or scale < 0.01: sdir *= -1
    srship.draw_scale_rotate(backbuffer, scale, angle, True)

    
    
    game_update(backbuffer, timeDelta)
   
    print_debug_info(backbuffer)
    
    gui.draw_ui(backbuffer)

    #draw the back buffer
    screen.blit(backbuffer, (0,0))

    pygame.display.update()
    
pygame.quit()

