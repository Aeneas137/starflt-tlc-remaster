"""
Software textured sphere renderer, quick ported from C++ code. 
IT WORKS, but it's slow and not optimized and needs attention.

Sphere is drawn with pixels, no geometry needed.

Adapted from Allegro code posted by Plucky on allegro.cc 05/22/2002:
https://www.allegro.cc/forums/thread/186206/186206#target

Original code packed 5,6,5 into an 8-bit short int:
"TEX_SIZE must be <= 256 due to coord_transform_table holding shorts.
In this code, it needs to be a power of 2, but a couple of minor tweaks, 
and this constraint can go away."

This should be removed from the Python code and better optimized!
TEX_SIZE should be passable but code must be cleaned up first.
"""

import sys, pygame, array, math 
from pygame.locals import *
from array import *

"""
RGB to Int conversions:
rgb = [255,255,255]
color = rgbtoint32(rgb)
rgb_c = int32torgb(color)
"""
def rgbtoint32(rgb):
    color = 0
    for c in rgb[::-1]:
        color = (color<<8) + c
    return color
def int32torgb(color):
    rgb = []
    for i in range(3):
        rgb.append(color&0xff)
        color = color >> 8
    return rgb


class TexturedSphere:

    def __init__(self):
        self.TEX_SIZE:int = 256
        self.MAP_SIZE:int = 256
        self.ASPECT_RATIO:float = 1.04
        self.coord_transform_table:array = None 
        self.screen2sphere_table:array = None 
        self.tex_table:array = None 
        self.texture:pygame.Surface = None 

        # initialize lookup tables
        alpha:int; beta:int   # spherical coordinates
        i:int; j:int 
        x:float; y:float; z:float # cartesian coordinates 
        
        size = self.TEX_SIZE * (self.TEX_SIZE + 1)
        self.coord_transform_table = [0 for a in range(size)]
        
        self.screen2sphere_table = [0 for a in range(self.TEX_SIZE)]
        
        # compute the lookup table to convert the coordinate system
        for j in range(self.TEX_SIZE+1):
            for i in range(self.TEX_SIZE): 

                # convert spherical coord to cartesian coord
                x,y,z = self.Spherical2Cartesian(i, j)

                # Convert cartesian to spherical. notice that x,z,y is passed, not x,y,z
                alpha,beta = self.Cartesian2Sphere(x, z, y)

                # copy 2D coordinates into 1D array
                # note: Python conversion does not use a malloc buffer but an array
                self.coord_transform_table[ i + j * self.TEX_SIZE ] = alpha + beta * self.TEX_SIZE

        # compute the lookup table used to map texture onto sphere
        for i in range(self.TEX_SIZE):
            value = (int)(math.acos( (float)(i - self.TEX_SIZE / 2 + 1) * 2 / self.TEX_SIZE) * self.TEX_SIZE / math.pi)
            value %= self.TEX_SIZE 
            self.screen2sphere_table[i] = value 


    def LoadTexture(self, filename:str)->bool:
        self.texture = None 
        self.texture = pygame.image.load(filename)
        if self.texture==None: return False

        #generate the sphere texture map
        x:int; y:int
        destj:int; desti:int = 0
        self.tex_table = [0 for a in range( self.TEX_SIZE * (self.TEX_SIZE + 1) ) ]

        """
        fills tex_table bottom-to-top, right-to-left, so texture appears correct on sphere
        i / j point to pixel on source texture: T2B, L2R
        i is source column starting at 0
        j is source row starting at 0
        desti / destj point to dest pixel on sphere: B2T, R2L
        desti starts row at 255
        destj starts col at 255
        """
        for i in range(self.TEX_SIZE-1):

            destj:int = self.TEX_SIZE
            desti:int = (self.TEX_SIZE - 1) - i

            for j in range(self.TEX_SIZE-1):

                #get source pixel
                x = (int)( i * self.texture.get_width() / self.TEX_SIZE )
                y = (int)( j * self.texture.get_height() / self.TEX_SIZE )
                r,g,b,a = self.texture.get_at((x, y)) 
                
                #pack RGB into an integer
                p = rgbtoint32([r,g,b])

                #map pixel from 2D coords into 1D array
                self.tex_table[destj * self.TEX_SIZE + desti] = p
                destj -= 1

        return True 


    def Spherical2Cartesian(self, alpha:int, beta:int):
        # Convert to radians 
        alpha1:float = (float)(alpha) * 2 * math.pi / self.MAP_SIZE
        beta1:float  = (float)(beta - self.MAP_SIZE / 2) * math.pi / self.MAP_SIZE
        
        # Convert to Cartesian 
        x:float = math.cos(alpha1) * math.cos(beta1)
        y:float = math.sin(beta1)
        z:float = math.sin(alpha1) * math.cos(beta1)

        return [x, y, z]


    def Cartesian2Sphere(self, x:float, y:float, z:float):
        beta1:float; alpha1:float; w:float
        
        # convert to Spherical Coordinates 
        beta1 = math.asin(y)
        if math.fabs(math.cos(beta1)) > 0.0: 
            w = x / math.cos(beta1)
            if (w > 1): w = 1
            if (w < -1): w = -1  
            alpha1 = math.acos(w)

            # Check for wrapping around top/bottom of sphere
            if (z / math.cos(beta1) < 0):  
                alpha1 = 2 * math.pi - alpha1
        else:
            alpha1 = 0
        
        # Convert to texture coordinates 
        alpha = (int)(alpha1 / (math.pi * 2) * self.MAP_SIZE);
        beta  = (int)(beta1 / math.pi * self.MAP_SIZE + self.MAP_SIZE/2);
        
        # 'Clip' the texture coordinates 
        if (alpha < 0): alpha = 0
        if (alpha >= self.MAP_SIZE): alpha = self.MAP_SIZE-1
        if (beta < 0): beta = 0
        if (beta >= self.MAP_SIZE): beta = self.MAP_SIZE-1
    
        return [alpha, beta]
            

    #phi, theta, psi must be 0-255 due to lookup table
    def Draw(self, dest:pygame.Surface, phi:int, theta:int, psi:int, radius:int, centerx:int, centery:int):
        x:int; y:int 
        xr:int              # Half Width of Sphere (pixels) in current scanline 
        beta1:int; alpha1:int   # initial spherical coordinates 
        xinc:int; xscaled:int  # auxiliary variables 

        # spherical coordinates of the 2nd and 3rd rotated system 
        # (the 2 coordinates are stored in a single integer)       
        alpha_beta2:int; alpha_beta3:int 
        

        # For all Scanlines 
        # previously: for (y = -radius+1; y<radius; y++)
        y_index_end = radius * 2 - 1
        for y_index in range(y_index_end):
            y = y_index - radius + 1
        
            # compute the width of the sphere in this scanline 
            xr = (int)( math.sqrt( (float)(radius * radius - y * y) ) * self.ASPECT_RATIO )
            if (xr==0): xr = 1
            
            # compute the first spherical coordinate beta 
            table_index = (int)((y + radius) * self.TEX_SIZE / (2 * radius))
            beta1 = self.screen2sphere_table[table_index] * self.TEX_SIZE

            # this is a remnant of C++ integer-packed optimization: is it necessary in Python?

            xinc = 16776960 / (2 * xr)
            xscaled = 0
        
            # For all pixels in this scanline ... 
            # previously: for(x = -xr; x < xr; x++) 
            x_index_end = xr * 2 - 1
            for x_index in range(x_index_end):
                x = x_index - xr
            
                # compute the second spherical coordinate alpha 

                # another remnant of the C++ integer packing: alternative?

                table_index = (int)(xscaled / 65536)

                alpha1 = self.screen2sphere_table[ table_index ] / 2
                xscaled += xinc
                alpha1 = alpha1 + phi

                # rotate texture in the first coordinate system (alpha,beta)
                # switch to the next coordinate system and rotate there
                alpha_beta2 = self.coord_transform_table[ (int)(beta1 + alpha1) ] + theta
                
                # the same procedure again ... 
                alpha_beta3 = self.coord_transform_table[alpha_beta2] + psi

                #pull RGB out of packed integer            
                r,g,b = int32torgb( self.tex_table[ (int)(alpha_beta3) ] )

                # draw the Pixel 
                posxy = ((int)(centerx + x),(int)(centery + y))
                dest.set_at( posxy, (r,g,b) )
       
    


def print_text(target, font, position, text, color=(255,255,255)):
    x,y = position[0], position[1]
    imgText = font.render(text, True, color)
    target.blit(imgText, (x,y))


def WrapValue(value:float, min:float=0.0, max:float=360.0):
    """
    WrapValue(): Given a min-max range, this takes the value and wraps it as necessary to keep it within the range [min, max).
    """
    if min >= max: return max

    if value < min:
        value = max + math.fmod((value-min), (max-min))
    elif value >= max:
        value = math.fmod((value-min), (max-min))

    return value


if __name__ == "__main__":
    pygame.init()
    SX=1200
    SY=1000
    screen = pygame.display.set_mode(size=(SX,SY))
    backbuffer = pygame.Surface((1200,1000))
    clock = pygame.time.Clock()
    fontt = pygame.font.SysFont("None", size=30, bold=False)

    image_file = "earth.png"
    sphere = TexturedSphere()
    if not sphere.LoadTexture(image_file): 
        print("Error loading " + image_file)
        sys.exit()


    #planet rotation 
    cx = int(SX/2)
    cy = int(SY/2)
    planetRotationSpeed = 2.0
    planetRotation = 0.0
    planetRadius = 128

    C_WHITE = (255,255,255)
    running:bool = True 
    while running:
        pressed_keys = pygame.key.get_pressed()
        for event in pygame.event.get():
            if event.type == QUIT: sys.exit()
            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE: running = False 
                elif event.key==K_LEFT: planetRotationSpeed -= 1.0
                elif event.key==K_RIGHT: planetRotationSpeed += 1.0


        backbuffer.fill((0,0,0))


        planetRotation += planetRotationSpeed
        planetRotation = WrapValue(planetRotation, 0.0, 256.0)

        sphere.Draw( backbuffer, 0, 0, planetRotation, planetRadius, cx, cy )

        print_text(backbuffer, fontt, (cx-100,cy+planetRadius+70), "PLANET RADIUS: " + str(planetRadius))
        print_text(backbuffer, fontt, (cx-100,cy+planetRadius+90), "PLANET ROTATION: " + str(planetRotation))

        screen.blit(backbuffer, (0,0))
        pygame.display.update()
        clock.tick(60)

    pygame.quit()
