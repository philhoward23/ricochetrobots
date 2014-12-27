# -*- coding: utf-8 -*-
"""
Created on Thu Dec 25 22:48:05 2014

@author: Phil.Howard
"""
import pygame
import numpy as np
from grid_tools import getXYOffset,getXYGridOffset,moveRobot,getIJBoard

#functions to initialise board and graphics for ricochet robots
def load_graphics(graphics):
    #default floor tile
    graphics.floor = pygame.image.load("graphics/floor_small.png")
    
    #vertical, horizontal and fill walls
    graphics.wall_v = pygame.image.load("graphics/wall_v_small.png")
    graphics.wall_h = pygame.image.load("graphics/wall_h_small.png")
    graphics.wall_c = pygame.image.load("graphics/wall_c.png")
    
    #robot
    graphics.robot = pygame.image.load("graphics/robot.png")
    
    #flag
    graphics.flag = pygame.image.load("graphics/flag.png")
    
    #dimensions for drawing
    graphics.tilesize = graphics.floor.get_width()
    graphics.wallsize = graphics.wall_c.get_width()


class Graphics(object):
    def __init__(self, gridsize, boardsize):
        #load images and set dimensions
        load_graphics(self)
        
        self.screensize = width, height = gridsize*self.tilesize+(gridsize+1)*self.wallsize,gridsize*self.tilesize+(gridsize+1)*self.wallsize
        #speed = [2,2]
        self.black=0,0,0
        self.background=200,200,200

        
class Board(object):
    #boardstate is an integer array representing the game board state, where:
    #0=floor/space
    #1=wall
    #2=centre tiles
    #3=robot
    #4=flag
    def __init__(self,gridsize,boardsize):
        self.gridsize = gridsize
        self.boardsize = boardsize
        self.boardstate = np.full((boardsize,boardsize),0,dtype=int)
        #default walls
        self.boardstate[:,0] = [1]*boardsize
        self.boardstate[0,:] = [1]*boardsize
        self.boardstate[:,boardsize-1] = [1]*boardsize
        self.boardstate[boardsize-1,:] = [1]*boardsize
        #centre walls
        self.boardstate[gridsize-2:gridsize+3,gridsize-2:gridsize+3] = np.full((5,5),1,dtype=int)
        self.boardstate[gridsize-1:gridsize+2,gridsize-1:gridsize+2] = np.full((3,3),2,dtype=int)
        
        #create robots map too
        #self.robot_colours=["yellow","red","green","blue","silver"]
        self.robot_colours=["yellow"]
        self.robots={colour:None for colour in self.robot_colours}

        
    def initialise(self):    
        #generate random configuration of walls and update state         
        #sample board: y,x format for np array filling referenced to robot's gridsize*gridsize game board
        vwalls=[(1,5),(1,11),(2,3),(2,9),(3,16),(4,1),(5,6),(5,11),(7,6),(7,12),(8,4),(10,4),(10,15),(11,9),(12,1),(12,13),(13,7),(14,10),(15,2),(16,6),(16,12)]
        hwalls=[(2,3),(2,10),(2,15),(4,2),(4,7),(5,1),(5,11),(5,16),(6,6),(6,13),(8,4),(9,4),(10,9),(10,15),(11,16),(12,2),(12,14),(13,7),(13,11),(14,1),(14,3)]
        
        for wall in vwalls:
            self.boardstate[1+2*(wall[0]-1),2*wall[1]]=1
        for wall in hwalls:
            self.boardstate[2*wall[0],1+2*(wall[1]-1)]=1
        
        
        #initialize target
        flaglocs=[(10,4)]
        #pick a random target from possibles
        self.flagloc=flaglocs[np.random.randint(len(flaglocs))]
        self.boardstate[getIJBoard(*self.flagloc)]=4       
        
        #randomise robot start position(s)
        for colour in self.robot_colours:
            self.robots[colour]=Robot(colour,self)
        self.active_robot="yellow"
        
        #display configuration
        for i in range(self.boardsize):
            print self.boardstate[i]

class Robot(object):
    #robot inhabits a gridsize*gridsize game board
    #that maps into the boardsize*boardsize game boardstate, which inludes walls
    def __init__(self,colour,board):
        self.colour=colour
        self.gridsize=board.gridsize
        while 1:
            irobot,jrobot=1+np.random.randint(self.gridsize),1+np.random.randint(self.gridsize)
            if (irobot not in (self.gridsize//2,(self.gridsize//2)+1) 
                    and jrobot not in (self.gridsize//2,(self.gridsize//2)+1)
                    and board.boardstate[getIJBoard(irobot,jrobot)]==0):
                self.position=[irobot,jrobot]
                board.boardstate[getIJBoard(*self.position)]=3
#                screen.blit(images.robot,getXYGridOffset(irobot,jrobot,images))
#                robotrect=images.robot.get_rect()
                break
        
    def move(self,coords,boardstate):
        return None
                
                