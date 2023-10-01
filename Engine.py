"""
Starflight: The Lost Colony (Remastered)

Requires Python 3.10
Dependencies:
    pygame 2.1
        pip install pygame
        https://www.pygame.org/docs/index.html
    pygame_gui 
        pip install pygame_gui -U
        https://pygame-gui.readthedocs.io/en/latest/modules.html
    perlin-noise
        pip install perlin-noise

    use pip list to see your installed libraries

"""

import sys, time, random, math, pygame
from pygame.locals import *

PI = 3.1415926535
PI_div_180 = 0.017453292519444



def distance(point1, point2):
    """ calculates distance between two points """
    delta_x = point1.x - point2.x
    delta_y = point1.y - point2.y
    dist = math.sqrt(delta_x*delta_x + delta_y*delta_y)
    return dist


def angular_velocity(angle):
    """ 
    calculates velocity required to move in a specific direction
    """
    vel = Point(0,0)
    vel.x = math.cos( math.radians(angle) )
    vel.y = math.sin( math.radians(angle) )
    return vel
    
def target_angle(x1,y1,x2,y2):
    """
    calculates angle to a target position (usually to rotate a sprite in that direction)
    """
    delta_x = x2 - x1
    delta_y = y2 - y1
    angle_radians = math.atan2(delta_y,delta_x)
    angle_degrees = math.degrees(angle_radians)
    return angle_degrees
    
    
def wrap_angle(angle):
    """ wraps a degree angle at boundary """
    return abs(angle % 360)

def print_text(target, font, position, text, color=(255,255,255), center=False):
    """ prints text with optional centering """
    x,y = position[0], position[1]
    imgText = font.render(text, True, color)
    if center:
        r = target.get_bounding_rect()
        x-=r.width/2
        y-=r.height/2
    target.blit(imgText, (x,y))


class Point(object):
    """ 
    2D tuple helper
    """
    def __init__(self, x, y):
        self._x = x
        self._y = y

    #x property
    def _getx(self): return self._x
    def _setx(self, x): self._x = x #pass a float
    x = property(_getx, _setx)

    #y property
    def _gety(self): return self._y
    def _sety(self, y): self._y = y #pass a float
    y = property(_gety, _sety)

    #export to tuple
    def toTuple(self): return (self._x,self._y)

    def __str__(self):
        return "{x:" + "{:.0f}".format(self.__x,2) + ",y:" + "{:.0f}".format(self.__y) + "}"


class Sprite(pygame.sprite.Sprite):
    """
    Sprite class encapsulates image transforms and animation
    """
    def __init__(self):
        pygame.sprite.Sprite.__init__(self) 
        self.masterImage = pygame.Surface((0,0))
        self.image = pygame.Surface((0,0))
        self.DebugMode = False
        self.DebugColor = (80,80,255)
        self.state = 0
        self.objectType = 0
        self.alive = True
        self.loaded = False
        self.width = 0
        self.height = 0

        #movement properties
        self.velocity = (0.0,0.0)
        self.position = (0,0)
        self.speed = 0.0
        self.direction = 0
        self.faceAngle = 0.0
        self.moveAngle = 0.0

        #transform properties
        self.temp_scale_img = pygame.Surface((0,0))
        self.temp_rot_image = pygame.Surface((0,0))

        #animation properties
        self.animColumns = 1
        self.animStartX = 0
        self.animStartY = 0
        self.currentFrame = 0
        self.totalFrames = 1
        self.firstFrame = 0
        self.lastFrame = 0
        self.frameCount = 0
        self.frameDelay = 0
        self.frameWidth = 1
        self.frameHeight = 1
        self.oldFrame = -1
        self.animDir = 1
        self.lastTime = 0

        #counters/triggers
        self.delayX = 0
        self.delayY = 0
        self.countX = 0
        self.countY = 0
        self.counter1 = 0
        self.counter2 = 0
        self.counter3 = 0
        self.threshold1 = 0
        self.threshold2 = 0
        self.threshold3 = 0

    #x property
    def _getx(self): return self.position[0]
    def _setx(self, x): self.position[0] = x 
    x = property(_getx, _setx)

    #y property
    def _gety(self): return self.position[1]
    def _sety(self, y): self.position[1] = y 
    y = property(_gety, _sety)
        

    def load_image(self, filename):
        """
        Load the source image from a file
        Note: init_animation MUST be called after this
        """
        self.masterImage = pygame.image.load(filename).convert_alpha()
        self.image = self.masterImage
        self.rect = self.masterImage.get_rect()
        self.loaded = True
        if self.masterImage == None:
            print("Error loading image: " + filename)
            self.loaded = False

    def set_image(self, image):
        """
        Set or replace the source image with an existing image. 
        If the new image is null then no change is made.
        Note: init_animation MUST be called if the new image is a different size
        """
        if image is not None:
            self.masterImage = image
            self.image = image
            self.loaded = True

    def init_animation(self, framewidth=0, frameheight=0, columns=1):
        """
        Initialize animation properties
        If not called then animation defaults to a static image
        """
        self.animColumns = columns
        #set animation frame size to whole image if not told otherwise
        if framewidth==0 or frameheight==0 or columns==1:
            self.frameWidth = self.masterImage.get_width()
            self.frameHeight = self.masterImage.get_height()
            self.rect = self.masterImage.get_rect()
            self.image = self.masterImage
        else:
            #set animation frame size to passed values
            self.frameWidth = framewidth
            self.frameHeight = frameheight
            rect = self.masterImage.get_rect()
            self.lastFrame = (rect.width//self.frameWidth) * (rect.height//self.frameHeight) - 1
            self.rect = pygame.Rect(0,0,self.frameWidth,self.frameHeight)


    def nextFrame(self):
        self.currentFrame += 1
        if self.currentFrame > self.lastFrame:
            self.currentFrame = self.firstFrame

    def prevFrame(self):
        self.currentFrame -= 1
        if self.currentFrame < 0 or self.currentFrame < self.firstFrame:
            self.currentFrame = self.lastFrame

    def update(self, anim_delay_in_ms=100):
        """
        update the animation and transforms after changing properties
        animation timing is based on pygame.time.Clock() (milliseconds, not framerate)
        """
        #only animate if there are frames, otherwise default to full image
        if self.animColumns > 1:
            #update animation frame number
            clock = pygame.time.get_ticks()
            if clock > self.lastTime + anim_delay_in_ms:
                self.nextFrame()
                self.lastTime = clock

            #build current frame based on properties
            frame_x = (self.currentFrame % self.animColumns) * self.frameWidth
            frame_y = (self.currentFrame // self.animColumns) * self.frameHeight
            rect = Rect(frame_x, frame_y, self.frameWidth, self.frameHeight)
            self.image = self.masterImage.subsurface(rect)
            #self.oldFrame = self.currentFrame
        else:
            self.currentFrame = self.firstFrame



    def draw(self, dest_surface):
        """
        Draw the sprite image with current transforms and animation frame
        Note: update MUST be called at least once before this
        """
        dest_surface.blit(self.image, self.position)

        if self.DebugMode == True:
            rect = (self.x, self.y, self.rect.width, self.rect.height)
            pygame.draw.rect(dest_surface, self.DebugColor, rect, 1)


    def draw_rotate(self, dest_surface, deg_angle):
        """
        Draw the sprite with rotation based on an angle in degrees
        Note: Rectangle is centered so it works best if image is square
        """
        self.temp_rot_image = pygame.transform.rotate(self.image, deg_angle)
        c_rect = self.temp_rot_image.get_rect(center=self.rect.center)

        r = self.image.get_rect()
        x = self.x + c_rect.x
        y = self.y + c_rect.y

        dest_surface.blit(self.temp_rot_image, (x,y))

        if self.DebugMode == True:
            rect = (self.x, self.y, self.rect.width, self.rect.height)
            pygame.draw.rect(dest_surface, self.DebugColor, rect, 1)


    def draw_scale(self, dest_surface, percent_scale, use_smoothscale=False):
        """
        Draw the sprite with scaling based on float percentage 
        Note: scaled position remains at the top-left
        """
        sw = self.frameWidth * percent_scale 
        sh = self.frameHeight * percent_scale 

        if use_smoothscale:
            self.temp_scale_img = pygame.transform.smoothscale(self.image, (sw,sh))            
        else:
            self.temp_scale_img = pygame.transform.scale(self.image, (sw,sh))
        
        dest_surface.blit(self.temp_scale_img, self.position)

        if self.DebugMode == True:
            rw = self.rect.width * percent_scale
            rh = self.rect.height * percent_scale
            rect = (self.x, self.y, rw, rh)
            pygame.draw.rect(dest_surface, self.DebugColor, rect, 1)


    def draw_scale_rotate(self, dest_surface, percent_scale, deg_angle, use_smoothscale=False):
        """
        Draw the sprite with scaling and rotation by combining the transforms
        """
        self.temp_scale_img = None
        self.temp_rot_image = None
        sw = self.frameWidth * percent_scale 
        sh = self.frameHeight * percent_scale 

        if use_smoothscale:
            self.temp_scale_img = pygame.transform.smoothscale(self.image, (sw,sh))
        else:
            self.temp_scale_img = pygame.transform.scale(self.image, (sw,sh))

        self.temp_rot_image = pygame.transform.rotate(self.temp_scale_img, deg_angle)
        c_rect = self.temp_rot_image.get_rect(center=self.temp_scale_img.get_rect().center)
        x = self.x + c_rect.x
        y = self.y + c_rect.y
        dest_surface.blit(self.temp_rot_image, (x,y))



    def __str__(self):
        return "frame:" + str(self.currentFrame) + " (" + str(self.firstFrame) + "-" + str(self.lastFrame) + ")," + \
            "size:(" + str(self.frameWidth) + "," + str(self.frameHeight) + "),cols:" + str(self.animColumns) 




"""
int Sprite::inside(int x,int y,int left,int top,int right,int bottom)
{
    if (x > left && x < right && y > top && y < bottom)
        return 1;
    else
        return 0;
}

int Sprite::pointInside(int px,int py)
{
	return inside(px, py, (int)x, (int)y, (int)x+width, (int)y+height);
}

/*
 * Bounding rectangle collision detection 
 */
bool Sprite::collided(Sprite *other)
{
	if (other == NULL) return false;

    int wa = (int)x + width;
    int ha = (int)y + height;
    int wb = (int)other->x + other->width;
    int hb = (int)other->y + other->height;

    if (inside((int)x, (int)y, (int)other->x, (int)other->y, wb, hb))	return true;
    if (inside((int)x, ha, (int)other->x, (int)other->y, wb, hb))		return true;
    if (inside(wa, (int)y, (int)other->x, (int)other->y, wb, hb))		return true;
    if (inside(wa, ha, (int)other->x, (int)other->y, wb, hb))			return true;
        
    return false;
}

/*
 * Distance based collision detection
 */
bool Sprite::collidedD(Sprite *other)
{
	if (other == NULL) return false;

	//calculate radius 1
	double radius1 = this->getFrameWidth() * 0.4;

	//point = center of sprite 1
	double x1 = this->getX() + this->getFrameWidth()/2;
	double y1 = this->getY() + this->getFrameHeight()/2;

	//calculate radius 2
	double radius2 = other->getFrameWidth() * 0.4;

	//point = center of sprite 2
	double x2 = other->getX() + other->getFrameWidth()/2;
	double y2 = other->getY() + other->getFrameHeight()/2;

	//calculate distance
    double deltaX = (x2-x1);
    double deltaY = (y2-y1);
    double dist = sqrt(deltaX*deltaX + deltaY*deltaY);

	//return distance comparison
	return (dist < radius1 + radius2);


}

double Sprite::calcAngleMoveX(int angle) {
   //calculate X movement value based on direction angle
    return (double) cos(angle * PI_div_180);
}

//calculate Y movement value based on direction angle
double Sprite::calcAngleMoveY(int angle) {
    return (double) sin(angle * PI_div_180);
}
"""
