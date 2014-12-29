# -*- coding: utf-8 -*-
"""
Created on Thu Dec 25 22:51:16 2014

@author: Phil.Howard
"""

#required modules and functions
import sys, pygame
import numpy as np
from grid_globals import gridsize,boardsize
from grid_tools import getXYOffset,getXYGridOffset,getIJBoard,getIJGrid
from initialise_game import Board
from graphics import Graphics

#create game
pygame.init()

#initialise board
board = Board(gridsize,boardsize)
board.initialise()

#initialise display of board
images = Graphics(gridsize,boardsize)

screen=pygame.display.set_mode(images.screensize)
screen.fill(images.background)

images.draw_initial_board(screen,board)


#respond to input
while 1:
    for event in pygame.event.get():
        if event.type==pygame.QUIT: 
            sys.exit()
        elif event.type==pygame.KEYDOWN:
            #replace robot with floor, or flag if on flag at present
            if tuple(board.robots[board.active_robot].position)==board.flagloc:
                screen.blit(images.flag,
                            getXYGridOffset(board.robots[board.active_robot].position[0],
                                            board.robots[board.active_robot].position[1],
                                            images))
            else:
                screen.blit(images.floor,
                            getXYGridOffset(board.robots[board.active_robot].position[0],
                                            board.robots[board.active_robot].position[1],
                                            images))
            #update robot location on board
            board.move_active_robot(event.key)
            
            #animate motion
            images.animate(screen,board,event.key)
            #screen.blit(images.robot,
            #            getXYGridOffset(board.robots[board.active_robot].position[0],
            #                            board.robots[board.active_robot].position[1],
            #                            images))
            print 'key pressed'
                    
        #screen.fill(black)
        pygame.display.flip()
        
        
   
#check victory conditions
