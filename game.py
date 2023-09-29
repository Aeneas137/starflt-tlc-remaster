"""
Starflight - The Lost Colony - Remastered

Requires:
    Python 3.10
    pygame 2.1
        pip install pygame
        https://www.pygame.org/docs/index.html
    pygame_gui 
        pip install pygame_gui -U
        https://pygame-gui.readthedocs.io/en/latest/modules.html
        
"""

import sys, time, random, math, pygame, pygame_gui
from pygame.locals import *
from MyLibrary import *
from ship import Ship

from pygame.locals import (
    K_UP,K_DOWN,K_LEFT,K_RIGHT,K_ESCAPE,K_RETURN,K_SPACE,KEYDOWN,QUIT,
    K_a,K_s,K_d,K_f
)

#
# all globals must be pre-defined
#
running=False
screen=None
SCREENW=1600
SCREENH=1024
backbuffer=None
fontl=None
fonts=None
ship=None

C_GRAY=(200,200,200)

gui=None
guiwin_debug=None
guitxt_debug=None
guibtn_test=None

#
# Initialization (be sure to call get_video_info() first)
#
def init_game():
    global screen, backbuffer, SCREENW, SCREENH
    global fontl, fonts, timer
    global ship

    pygame.init()

    SCREENW,SCREENH = 1280,1024 #2560,1440

    screen = pygame.display.set_mode(size= (SCREENW,SCREENH))
    #pygame.display.toggle_fullscreen()

    title = "Starflight - The Lost Colony (Remastered)"
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


#
# Initialize the GUI
#
def init_gui():
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
    
    
#
#
#
def print_debug_info(target):
    global fonts
    
    debugx=SCREENW-200
    debugy=SCREENH-100
    nl=16

    s = ""
    
    mouse = pygame.mouse.get_pos()
    x,y=mouse
    
    s += "Mouse: " + str(x) + "," + str(y) 
    s += "<br>"
    #print_text(backbuffer, fonts, debugx, debugy, s, C_GRAY)

    guitxt_debug.html_text = s
    guitxt_debug.rebuild()


""" 
-----------------------------------------------
MAIN ENGINE LOOP
-----------------------------------------------
"""
init_game()
init_gui()
game_over = False
last_time = 0
inputdelay = 0
clock = pygame.time.Clock()

#main loop
while True:
    timer.tick(30)
    ticks = pygame.time.get_ticks()
    time_delta = clock.tick(60)/1000.0

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
    if pygame.time.get_ticks() > inputdelay + 100:
        inputdelay = pygame.time.get_ticks()
        
    #let the GUI perform updates
    gui.update(time_delta)
    
    #clear the background
    backbuffer.fill((20,20,20))
    
    #ship.draw(backbuffer)
   
    print_debug_info(backbuffer)
    
    gui.draw_ui(backbuffer)


    #draw the back buffer
    screen.blit(backbuffer, (0,0))

    pygame.display.update()
    
pygame.quit()



