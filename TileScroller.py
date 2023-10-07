"""
Starflight: The Lost Colony (Remastered)

ENGINE CODE

See Engine.py for dependencies.

"""

import sys, time, random, math, pygame
from pygame.locals import *
from array import *

MAX = 250

class TileScroller(object):
    tiledata = None
    scrollbuffer = None
    sourcetiles = None
    columns = 0
    rows = 0
    scrollx = 0.0
    scrolly = 0.0
    mapwidth = 0
    mapheight = 0
    windowwidth = 0
    windowheight = 0
    tilewidth = 0
    tileheight = 0


    def __init__(self, tilewidth, tileheight, mapwidth, mapheight):
        """ TileScroller constructor """
        self.tiledata = [[0 for y in range(MAX)] for x in range(MAX)]
        self.sourcetiles = None 
        self.scrollbuffer = None 
        self.rows = 0
        self.columns = 0
        self.scrollx = 0
        self.scrolly = 0
        self.mapwidth = mapwidth
        self.mapheight = mapheight
        self.tilewidth = tilewidth 
        self.tileheight = tileheight


    def setScrollPosition(self, x, y):
        self.scrollx = x
        self.scrolly = y
    

    def setMapSize(self, w, h):
        """ mapwidth/mapheight """
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
        """ """
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
        Fills the scroll buffer image with source tile images based on current scroll position.
        Note: This is memory efficient since only the viewport is filled.
        """
        #prevent a crash
        if self.scrollbuffer==None: return False 
        if self.sourcetiles==None: return False
        if self.tilewidth==0 or self.tileheight==0: return False 

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
                #sourcetileimage = self.sourcetiles.subsurface(rect)
                
                self.scrollbuffer.blit(self.sourcetiles, 
                                       (x*self.tilewidth, y*self.tilewidth), 
                                       (left,top,self.tilewidth,self.tileheight))

                #blit(tiles, scrollbuffer, left, top, x*tilewidth, y*tileheight, tilewidth, tileheight);


    def drawScrollWindow(self, dest_surface, x, y, width, height):
        """
        Draws the portion of the scroll buffer based on the current partial tile scroll position
        """ 

        #prevent a crash
        if (self.tilewidth==0 or self.tileheight==0): return False
        
        #calculate the partial sub-tile lines to draw using modulus
        partialx = int(self.scrollx % self.tilewidth)
        partialy = int(self.scrolly % self.tileheight)
        
        #draw the scroll buffer to the destination bitmap
        if self.scrollbuffer==None:
            print("drawScrollWindow: scrollbuffer is invalid")
            return False 

        dest_surface.blit(self.scrollbuffer, (x,y), (partialx,partialy,width,height))
        return True 
        


