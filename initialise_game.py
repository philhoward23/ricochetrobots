# -*- coding: utf-8 -*-
"""
Created on Thu Dec 25 22:48:05 2014

@author: Phil.Howard
"""
import pygame
import numpy as np
from grid_tools import getXYOffset,getXYGridOffset,getIJBoard,getIJGrid

#functions to initialise board for ricochet robots
        
class Board(object):
    #boardstate is an integer array representing the game board state, where:
    #0=floor/space
    #1=wall
    #2=centre tiles
    #3=robot
    #-1=flag, negative since positive values block robot movement
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
        self.robot_colours=["yellow","red","green","blue","silver"]
        #self.robot_colours=["yellow"]
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
        self.boardstate[getIJBoard(*self.flagloc)]=-1     
        self.flag_colour="yellow"
        
        #randomise robot start position(s)
        for colour in self.robot_colours:
            self.robots[colour]=Robot(colour,self)
        self.active_robot="yellow"
        
        self.victory=False
        self.moves_taken=0
        
        #display configuration
        for i in range(self.boardsize):
            print self.boardstate[i]
    
    
    def reset_turn(self):
        for colour in self.robot_colours:
            #erase current location
            self.boardstate[getIJBoard(*tuple(self.robots[colour].position))]=0
            #reset to turn start
            self.robots[colour].position=self.robots[colour].turn_start_position
            self.robots[colour].last_position=self.robots[colour].turn_start_position
            self.boardstate[getIJBoard(*tuple(self.robots[colour].position))]=3
            
        #reset flag    
        self.boardstate[getIJBoard(*self.flagloc)]=-1     
        self.victory=False
        self.moves_taken=0

    #move_active_robot    
    def process_keypress(self,key):
        #check for victory state - only allows reset options
        if self.victory:
            if key not in (pygame.K_r,pygame.K_n):
                print "In victory state, please reset turn or start a new game"
                return
        
        #check for reset (pressed r)
        if key==pygame.K_r:
            self.reset_turn()
        elif key in (pygame.K_LEFT,pygame.K_RIGHT,pygame.K_UP,pygame.K_DOWN):
            self.robots[self.active_robot].move(self,key)
        elif key in (pygame.K_1,pygame.K_2,pygame.K_3,pygame.K_4,pygame.K_5):
            self.active_robot=self.robot_colours[int(pygame.key.name(key))-1]
        else:
            #no action for this key
            print "Input not recognised"
        return
            
    def check_victory(self):
        #need to reach the flag with the same coloured robot
        if (tuple(self.robots[self.active_robot].position)==self.flagloc) and (self.flag_colour==self.active_robot):
            self.victory=True
            return True
        else:
            self.victory=False
            return False
            
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
                self.last_position=self.position
                self.turn_start_position=self.position
                board.boardstate[getIJBoard(*self.position)]=3
#                screen.blit(images.robot,getXYGridOffset(irobot,jrobot,images))
#                robotrect=images.robot.get_rect()
                break
        
    def move(self,board,key):
        #map robot coords to boardstate coords
        boardi,boardj=getIJBoard(*self.position)
        #initialise new coords at current coords
        inew,jnew=self.position
        if key == pygame.K_LEFT:
            #find first non-collision square to left
            boardjnew=1+np.max(np.where(board.boardstate[boardi,0:boardj]>0))
            #shift to right one if a robot collision to account for space between tiles
            if board.boardstate[boardi,boardjnew-1]==3:
                boardjnew=boardjnew+1
            board.boardstate[boardi,boardj]=0
            board.boardstate[boardi,boardjnew]=3
            inew,jnew=getIJGrid(boardi,boardjnew)
        elif key == pygame.K_RIGHT:
            #find first non-collision square to right
            boardjnew=boardj+np.min(np.where(board.boardstate[boardi,boardj+1:]>0))
            #shift to left one if a robot collision to account for space between tiles
            if board.boardstate[boardi,boardjnew+1]==3:
                boardjnew=boardjnew-1
            board.boardstate[boardi,boardj]=0
            board.boardstate[boardi,boardjnew]=3
            inew,jnew=getIJGrid(boardi,boardjnew)
        elif key == pygame.K_UP:
            #find first non-collision square above
            boardinew=1+np.max(np.where(board.boardstate[0:boardi,boardj]>0))
            #shift down one if a robot collision to account for space between tiles
            if board.boardstate[boardinew-1,boardj]==3:
                boardinew=boardinew+1            
            board.boardstate[boardi,boardj]=0
            board.boardstate[boardinew,boardj]=3
            inew,jnew=getIJGrid(boardinew,boardj)
        elif key == pygame.K_DOWN:
            #find first non-collision square below
            boardinew=boardi+np.min(np.where(board.boardstate[boardi+1:,boardj]>0))
            #shift up one if a robot collision to account for space between tiles
            if board.boardstate[boardinew+1,boardj]==3:
                boardinew=boardinew-1            
            board.boardstate[boardi,boardj]=0
            board.boardstate[boardinew,boardj]=3
            inew,jnew=getIJGrid(boardinew,boardj)
        else:
            pass
        
        #was this a valid move?
        if (self.position!=[inew,jnew]):
            board.moves_taken+=1
            #check flag location is updated if robot has moved off        
            if (tuple(self.position)==board.flagloc):
                board.boardstate[boardi,boardj]=-1
                
        #update robot position variables including if no move was made so animated correctly
        self.last_position=self.position            
        self.position=[inew,jnew]        
        #return(boardstate,inew,jnew)                
                