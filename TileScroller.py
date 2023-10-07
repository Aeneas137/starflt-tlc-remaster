"""
Starflight: The Lost Colony (Remastered)

ENGINE-LEVEL CODE

TileScroller class

See Engine.py for dependencies.

"""

import sys, time, random, math, pygame
from pygame.locals import *
from array import *

MAX = 500

class TileScroller(object):
    """
    tiledata = None
    scrollbuffer = None
    sourcetiles = None
    columns = 0
    rows = 0
    scrollx = 0.0
    scrolly = 0.0
    oldscrollx = 0.0
    oldscrolly = 0.0
    mapwidth = 0
    mapheight = 0
    windowwidth = 0
    windowheight = 0
    tilewidth = 0
    tileheight = 0
    """

    def __init__(self, tilewidth, tileheight, mapwidth, mapheight):
        """ 
        TileScroller constructor.\n
        tilewidth/tileheight = dimensions of an individual tile (e.g. 64x64).\n
        mapwidth/mapheight = dimensions of the entire map in TILES (not pixels).
        """
        self.tiledata = [[0 for y in range(MAX)] for x in range(MAX)]
        self.sourcetiles = None 
        self.scrollbuffer = None 
        self.rows = 0
        self.columns = 0
        self.scrollx = 0
        self.scrolly = 0
        self.oldscrollx = -1
        self.oldscrolly = -1
        self.mapwidth = mapwidth
        self.mapheight = mapheight
        self.tilewidth = tilewidth 
        self.tileheight = tileheight
        self.windowwidth = 0
        self.windowheight = 0

    def getMapSizeInPixels(self):
        w = self.mapwidth * self.tilewidth
        h = self.mapheight * self.tileheight 
        return (int(w),int(h))
    
    def getViewportSizeInPixels(self):
        return self.scrollbuffer.get_rect()

    def scrollUp(self, y = -1):
        return self.scroll(0,y)

    def scrollDown(self, y = 1):
        return self.scroll(0,y)
    
    def scrollLeft(self, x = -1):
        return self.scroll(x,0)

    def scrollRight(self, x = 1):
        return self.scroll(x,0)

    def scroll(self, x, y):
        """
        Scroll the tile scroller in any direction.\n
        Goal of this logic is to notify caller of a boundary hit by returning False so caller
        can adjust the scrolling.\n
        To-do: auto-wrapping
        """
        w,h = self.getMapSizeInPixels()
        r = self.getViewportSizeInPixels()
        ret = True 

        x = int(x)
        y = int(y)

        if x < 0:
            if self.scrollx > 0+x:
                self.oldscrollx = self.scrollx 
                self.scrollx += x
            else:
                #scroller hit west boundary
                ret = False 

        if x > 0:
            if self.scrollx < w - r.width:
                self.oldscrollx = self.scrollx 
                self.scrollx += x
            else:
                #scroller hit east boundary
                ret = False

        if y < 0:
            if self.scrolly > 0+y:
                self.oldscrolly = self.scrolly 
                self.scrolly += y 
            else:
                #scroller hit north boundary
                ret = False

        if y > 0:
            if self.scrolly < h - r.height:
                self.oldscrolly = self.scrolly 
                self.scrolly += y 
            else:
                #scroller hit south boundary
                ret = False
        
        return ret


    def setScrollPosition(self, x, y):
        self.oldscrollx = self.scrollx
        self.oldscrolly = self.scrolly 
        self.scrollx = int(x)
        self.scrolly = int(y)
    

    def setMapSize(self, w, h):
        """ 
        Set the map width/height in tile dimensions (not pixels).
        """
        if w >= 0 and w <= self.MAX: self.mapwidth = w
        if h >= 0 and h <= self.MAX: self.mapheight = h
    

    def setTile(self, col, row, value):
        """ """
        self.tiledata[col][row] = value
    

    def getTile(self, col, row):
        """ """
        return self.tiledata[col][row]
    

    def getTilebyCoords(self, x, y):
        """ """
        return self.tiledata[x / self.tilewidth][y / self.tileheight]
    

    def loadTilemapSourceImage(self, filename, columns):
        """ """
        self.sourcetiles = None 
        self.sourcetiles = pygame.image.load(filename)
        self.columns = columns 
        if (self.sourcetiles==None):
            print("Error loading tilemap source image: " + filename)
            return False 
        else:
            return True 

    def setTilemapSourceImage(self, image, columns):
        if image==None: return False
        self.sourcetiles = None
        self.sourcetiles = image
        self.columns = columns 
        return True 


    def createScrollBuffer(self, width, height):
        """ 
        Creates the tile scroll buffer in pixel dimensions.\n
        width/height = dimensions of your viewport (in pixels).\n
        A perimeter of one tile is added for smooth scrolling.
        """
        self.windowwidth = width
        self.windowheight = height
        bufferw = width + self.tilewidth * 2
        bufferh = height + self.tileheight * 2
        self.scrollbuffer = pygame.Surface((bufferw, bufferh))
        if self.scrollbuffer==None:
            return False
        else:
            return True


    def resetTiles(self, value=0):
        """ """
        for col in self.tiledata:
            for row in col:
                row = value


    def updateScrollBuffer(self):
        """
        Fills the scroll buffer image with tile images based on current scroll position.\n
        This is memory efficient since only the viewport is filled,  but this should only be
        called when the scroll position moves past one of the edges (viewport + tile w/h).
        At minimum, for efficiency, only rebuild the scroll buffer when the scroll position changes.
        """
        #prevent a crash
        if self.scrollbuffer==None: return False 
        if self.sourcetiles==None: return False
        if self.tilewidth==0 or self.tileheight==0: return False 

        #efficiency: only update buffer if the scroll position changed
        if self.scrollx == self.oldscrollx and self.scrolly == self.oldscrolly:
            return False 

        #calculate starting tile position
        tilex = int(self.scrollx / self.tilewidth)
        tiley = int(self.scrolly / self.tileheight)

        #calculate the number of columns and rows
        cols = int(self.windowwidth / self.tilewidth)
        rows = int(self.windowheight / self.tileheight)

        for y in range(0, rows):
            for x in range(0, cols):
                tx = tilex + x
                if (tx < 0): tx = 0
                ty = tiley + y
                if (ty < 0): ty = 0
                tilenum = self.getTile(tx,ty)

                left = (tilenum % self.columns) * self.tilewidth
                top = (tilenum // self.columns) * self.tileheight
                rect = Rect(left, top, self.tilewidth, self.tileheight)
                
                self.scrollbuffer.blit(self.sourcetiles, 
                                       (x*self.tilewidth, y*self.tilewidth), 
                                       (left,top,self.tilewidth,self.tileheight))



    def drawScrollWindow(self, dest_surface, x, y, width, height):
        """
        Draw a viewport of the scroll buffer based on the current scroll position.
        """ 
        #prevent a crash
        if (self.tilewidth==0 or self.tileheight==0): return False
        
        #calculate the partial sub-tile lines to draw using modulus for smooth scrolling
        partialx = int(self.scrollx % self.tilewidth)
        partialy = int(self.scrolly % self.tileheight)
        
        #draw the scroll buffer to the destination bitmap
        if self.scrollbuffer==None:
            print("drawScrollWindow: scrollbuffer is invalid")
            return False 

        dest_surface.blit(self.scrollbuffer, (x,y), (partialx,partialy,width,height))
        return True 
        


    def __str__(self):
        s=""
        s+= str(self.scrollx) + "/" + str(self.scrolly) + " "
        s+= "tile:" + str(self.tilewidth) + "/" + str(self.tileheight) + " "
        s+= "win:"+str(self.windowwidth) + "/" + str(self.windowheight) + " "
        s+= "map:" + str(self.mapwidth) + "/" + str(self.mapheight) + " "
        s+= "sb:" + str(self.scrollbuffer.get_width()) + "/" + str(self.scrollbuffer.get_height()) + " "
        
        return s 
