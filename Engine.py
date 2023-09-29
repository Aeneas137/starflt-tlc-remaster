"""
"""

import sys, time, random, math, pygame
from pygame.locals import *

PI = 3.1415926535
PI_div_180 = 0.017453292519444



# calculates distance between two points
def distance(point1, point2):
    delta_x = point1.x - point2.x
    delta_y = point1.y - point2.y
    dist = math.sqrt(delta_x*delta_x + delta_y*delta_y)
    return dist


# calculates velocity of an angle
def angular_velocity(angle):
    vel = Point(0,0)
    vel.x = math.cos( math.radians(angle) )
    vel.y = math.sin( math.radians(angle) )
    return vel
    
# calculates angle between two points
def target_angle(x1,y1,x2,y2):
    delta_x = x2 - x1
    delta_y = y2 - y1
    angle_radians = math.atan2(delta_y,delta_x)
    angle_degrees = math.degrees(angle_radians)
    return angle_degrees
    
    
# wraps a degree angle at boundary
def wrap_angle(angle):
    return abs(angle % 360)

# prints text using the supplied font #CHANGE
def print_text(target, font, x, y, text, color=(255,255,255), center=False):
    imgText = font.render(text, True, color)
    if center:
        r = target.get_bounding_rect()
        x-=r.width/2
        y-=r.height/2
    target.blit(imgText, (x,y))



"""
class BaseSprite(pygame.sprite.Sprite):
    
    def __init__(self):
        pygame.sprite.Sprite.__init__(self) 
        self.master_image = None
        self.last_time = 0
        self.direction = 0
        self.velocity = Point(0.0,0.0)
        self.rotation = 0.0 
        self.old_rotation = 0.0 

    #X property
    def _getx(self): return self.rect.x
    def _setx(self,value): self.rect.x = value
    X = property(_getx,_setx)

    #Y property
    def _gety(self): return self.rect.y
    def _sety(self,value): self.rect.y = value
    Y = property(_gety,_sety)

    #position property
    def _getpos(self): return self.rect.topleft
    def _setpos(self,pos): self.rect.topleft = pos  
    position = property(_getpos,_setpos)

    def load(self, filename):
        self.master_image = pygame.image.load(filename).convert_alpha()

    def set_image(self, image):
        self.master_image = image

    def draw(self, surface):
        surface.blit(self.image, (self.X,self.Y))

    def __str__(self):
        return str(self.rect)
"""

# Point class
class Point(object):
    def __init__(self, x, y):
        self._x = x
        self._y = y

    #x property
    def getx(self): return self._x
    def setx(self, x): self._x = x #pass a float
    x = property(getx, setx)

    #y property
    def gety(self): return self._y
    def sety(self, y): self._y = y #pass a float
    y = property(gety, sety)

    #export to tuple
    def toTuple(self): return (self._x,self._y)

    def __str__(self):
        return "{X:" + "{:.0f}".format(self.__x,2) + \
            ",Y:" + "{:.0f}".format(self.__y) + "}"


class Sprite(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self) 
        self.image = pygame.Surface((0,0))
        self.DebugMode = False
        self.state = 0
        self.objectType = 0
        self.alive = True
        self.loaded = False
        self.masterImage = pygame.Surface((0,0))
        self.width = 0
        self.height = 0

        self.rotation = 0.0 
        self.oldRotation = 0.0 

        #movement properties
        self.velocity = (0.0,0.0)
        self.position = (0,0)
        self.speed = 0.0
        self.direction = 0
        self.faceAngle = 0.0
        self.moveAngle = 0.0

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


    def load(self, filename, width=0, height=0, columns=1):
        self.masterImage = pygame.image.load(filename).convert_alpha()
        if self.masterImage == None:
            print("Error loading image: " + filename)
        else:
            self.set_image(self.masterImage, width, height, columns)
            print(str(self))

    def set_image(self, image, width=0, height=0, columns=1):
        self.masterImage = image
        self.image = image
        self.animColumns = columns

        #set animation frame size to whole image if not told otherwise
        if width==0 or height==0:
            self.frameWidth = image.get_width()
            self.frameHeight = image.get_height()
            self.rect = self.image.get_rect()
        else:
            #set animation frame size to passed values
            self.frameWidth = width
            self.frameHeight = height
            rect = self.masterImage.get_rect()
            self.lastFrame = (rect.width//width) * (rect.height//height) - 1
            self.rect = pygame.Rect(0,0,self.frameWidth,self.frameHeight)


    def update(self, currentTime, rate=30):
        #only animate if there are frames
        if self.animColumns > 1:
            #update animation frame number
            if currentTime > self.lastTime + rate:
                self.currentFrame += 1
                if self.currentFrame > self.lastFrame:
                    self.currentFrame = self.firstFrame
                self.lastTime = currentTime
        else:
            self.currentFrame = self.firstFrame

        #build current frame only if it changed
        if self.animColumns > 1:
            frame_x = (self.currentFrame % self.animColumns) * self.frameWidth
            frame_y = (self.currentFrame // self.animColumns) * self.frameHeight
            rect = Rect(frame_x, frame_y, self.frameWidth, self.frameHeight)
            self.image = self.masterImage.subsurface(rect)
            self.oldFrame = self.currentFrame


    def draw(self, surface):
        pos = (self.position[0],self.position[1])
        surface.blit(self.image, pos)

    def __str__(self):
        return "SPRITE:\n" + \
            str(self.currentFrame) + "," + str(self.firstFrame) + \
            "," + str(self.lastFrame) + "," + str(self.frameWidth) + \
            "," + str(self.frameHeight) + "," + str(self.animColumns) + \
            "," + str(self.rect)


"""
bool Sprite::load(const char *filename) {
	this->image = load_bitmap(filename, NULL);
	if (!this->image) 
	{
		std::ostringstream s;
		s << "Error loading sprite file: " << filename;
		g_game->message(s.str().c_str());
		return false;
	}
	this->width = image->w;
	this->height = image->h;
	this->bLoaded = true;
	
	//default frame size equals whole image size unless manually changed
	this->frameWidth = this->width;
	this->frameHeight = this->height;
	
	set_alpha_blender();
    return true;
}

bool Sprite::setImage(BITMAP *source)
{
	//if new source image is null, then abort
	if (!source) return false;
	
	//if old image exists, it must be freed first
	if (this->image && bLoaded) {
		destroy_bitmap(this->image);
		this->image = NULL;
	}
	
	this->image = source;
	this->width = source->w;
	this->height = source->h;
	this->frameWidth = source->w;
	this->frameHeight = source->h;
	this->bLoaded = false;
	
	set_alpha_blender();

	return true;
}


//draw normally with optional alpha channel support
void Sprite::drawframe(BITMAP *dest, bool UseAlpha)  {
    if (!image) return;

	int fx = animStartX + (currFrame % animColumns) * frameWidth;
	int fy = animStartY + (currFrame / animColumns) * frameHeight;

	if (!UseAlpha) {
		//draw normally
		masked_blit(this->image, dest, fx, fy, (int)x, (int)y, frameWidth, frameHeight);
	} 
	else {
		//paste frame onto scratch image using alpha channel
		BITMAP *temp = create_bitmap(frameWidth, frameHeight);
		masked_blit(image, temp, fx, fy, 0, 0, frameWidth, frameHeight);
		draw_trans_sprite(dest, temp, (int)x, (int)y);
		destroy_bitmap(temp);
	}
	
	if (DebugMode) {
		rect(dest, (int)x, (int)y, (int)x + frameWidth, (int)y + frameHeight, BLUE);
	}
}


//draw with scaling
void Sprite::drawframe_scale(BITMAP *dest, int dest_w, int dest_h)  {
    if (!image) return;

    int fx = animStartX + (currFrame % animColumns) * frameWidth;
    int fy = animStartY + (currFrame / animColumns) * frameHeight;
    masked_stretch_blit(image, dest, fx, fy, frameWidth, frameHeight, (int)x, (int)y, dest_w, dest_h);

	if (DebugMode) {
		rect(dest, (int)x, (int)y, (int)x + dest_w, (int)y + dest_h, BLUE);
	}
}


//draw with rotation
void Sprite::drawframe_rotate(BITMAP *dest, int angle)  {
    if (!image) return;

    //create scratch frame if necessary
    if (!frame) {
        frame = create_bitmap(frameWidth, frameHeight);
    }

    //first, draw frame normally but send it to the scratch frame image
    int fx = animStartX + (currFrame % animColumns) * frameWidth;
    int fy = animStartY + (currFrame / animColumns) * frameHeight;
    blit(image, frame, fx, fy, 0, 0, frameWidth, frameHeight);

    //draw rotated image in scratch frame onto dest 
    //adjust for Allegro's 16.16 fixed trig (256 / 360 = 0.7) then divide by 2 radians
    rotate_sprite(dest, frame, (int)x, (int)y, itofix((int)(angle / 0.7f / 2.0f)));

	if (DebugMode) {
		rect(dest, (int)x, (int)y, (int)x + frameWidth, (int)y + frameHeight, BLUE);
	}
}

void Sprite::move()
{
    //update x position
    if (++countX > delayX)  {
        countX = 0;
        x += velX;
    }

    //update y position
    if (++countY > delayY)  {
        countY = 0;
        y += velY;
    }
}

void Sprite::animate() 
{
	animate(0, totalFrames-1);
}

void Sprite::animate(int low, int high) 
{
    //update frame based on animdir
    if (++frameCount > frameDelay)  {
        frameCount = 0;
		currFrame += animDir;

		if (currFrame < low) {
            currFrame = high;
		}
		if (currFrame > high) {
            currFrame = low;
        }
    }
}

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