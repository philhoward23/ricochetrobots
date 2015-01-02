# -*- coding: utf-8 -*-
"""
Created on Thu Dec 25 22:48:05 2014

@author: Phil.Howard
"""
import pygame
import numpy as np
from grid_tools import getIJBoard,getIJGrid
from tiles import Tiles

#functions to initialise board for ricochet robots
        
class Board(object):
    #boardstate is an integer array representing the game board state, where:
    #0=floor/space
    #1=wall
    #2=centre tiles
    #3=robot
    #-1=flag, negative since positive values block robot movement
    def __init__(self):
        #initialise game board tiles and array sizes
        self.tiles = Tiles()
        self.gridsize = 2*self.tiles.gridsize
        self.boardsize = 1 + 2*self.gridsize
        
        #create robots map too
        self.robot_colours=["yellow","red","green","blue","silver"]
        #self.robot_colours=["yellow"]
        self.robots={colour:None for colour in self.robot_colours}

        
    def initialise(self):    
        #generate random configuration of board tiles   
        self.boardstate, self.flaglocs = self.tiles.generate_game_board()      
        
        #initialize target
        #pick a random target from 17 possibles
        self.flag_order = np.random.permutation(len(self.flaglocs))
        self.turn = 0
        self.flagloc=self.flaglocs[self.flag_order[self.turn]]["location"]
        self.boardstate[getIJBoard(*self.flagloc)]=-1     
        self.flag_colour=self.flaglocs[self.flag_order[self.turn]]["colour"]
        
        #randomise robot start position(s)
        for colour in self.robot_colours:
            self.robots[colour]=Robot(colour,self)
        if self.flag_colour=="rainbow":
            self.active_robot="silver"
        else:
            self.active_robot=self.flag_colour
        
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
        #check whether a robot is here first 
        if self.boardstate[getIJBoard(*self.flagloc)]==0:
            self.boardstate[getIJBoard(*self.flagloc)]=-1     
        self.victory=False
        self.moves_taken=0
        
    def new_turn(self):
        self.turn+=1
        if self.turn<17:
            #choose new flag location and colour, leave robots in place
            self.flagloc=self.flaglocs[self.flag_order[self.turn]]["location"]
            self.flag_colour=self.flaglocs[self.flag_order[self.turn]]["colour"]
            
            #reset flag    
            #check whether a robot is here first TODO
            if self.boardstate[getIJBoard(*self.flagloc)]==0:
                self.boardstate[getIJBoard(*self.flagloc)]=-1   
            self.victory=False
            self.moves_taken=0
        else:
            #all flag positions solved for this game - user must (r)eset or start a new (g)ame
            return

    def new_game(self):
        #choose new board configurations and initialise again
        self.initialise()
        
    #move_active_robot    
    def process_keypress(self,key):
        #check for victory state - only allows reset options
        if self.victory:
            if key not in (pygame.K_r,pygame.K_n,pygame.K_g):
                print "In victory state, please reset turn or start a new game"
                return
        
        #check for reset (pressed r)
        if key==pygame.K_r:
            self.reset_turn()
        #check for new turn (pressed n)
        elif key==pygame.K_n:
            self.new_turn()
        #check for new game (pressed g)
        elif key==pygame.K_g:
            self.new_game() 
        #check for movement
        elif key in (pygame.K_LEFT,pygame.K_RIGHT,pygame.K_UP,pygame.K_DOWN):
            self.robots[self.active_robot].move(self,key)
        #check for switch active robot
        elif key in (pygame.K_1,pygame.K_2,pygame.K_3,pygame.K_4,pygame.K_5,pygame.K_KP1,pygame.K_KP2,pygame.K_KP3,pygame.K_KP4,pygame.K_KP5):
            self.active_robot=self.robot_colours[int(pygame.key.name(key))-1]
        else:
            #no action for this key
            print "Input not recognised"
        return
            
    def check_victory(self):
        #need to reach the flag with the same coloured robot
        if (tuple(self.robots[self.active_robot].position)==self.flagloc) and ((self.flag_colour==self.active_robot) or (self.flag_colour=="rainbow")):
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
                