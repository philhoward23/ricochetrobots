# -*- coding: utf-8 -*-
"""
Created on Thu Dec 25 22:51:16 2014

@author: Phil.Howard
"""

#required modules and functions
import sys, pygame
import numpy as np
from grid_globals import gridsize,boardsize
from grid_tools import getXYOffset,getXYGridOffset,moveRobot,getIJBoard
from initialise_game import Graphics,Board

#create game
pygame.init()

#initialise board
board = Board(gridsize,boardsize)
board.initialise()

#initialise display of board
images = Graphics(gridsize,boardsize)

screen=pygame.display.set_mode(images.screensize)
screen.fill(images.background)


tilesize,wallsize=images.tilesize,images.wallsize

#draw
for i in range(gridsize):
    for j in range(gridsize):
        screen.blit(images.floor,
                    (wallsize+i*(tilesize+wallsize),
                     wallsize+j*(tilesize+wallsize)))



#set walls
for i in range(boardsize):
    for j in range(boardsize):
        if board.boardstate[i,j]==1:
            #horizontal, vertical or gap?
            if i%2==0:
                if j%2==0:
                    #gap
                    screen.blit(images.wall_c,
                    (getXYOffset(i,j,images)))
                else:
                    screen.blit(images.wall_h,
                    (getXYOffset(i,j,images)))
            else:
                screen.blit(images.wall_v,
                (getXYOffset(i,j,images)))

#draw robot(s) and flag
for colour in board.robot_colours:
    screen.blit(images.robot,getXYGridOffset(board.robots[colour].position[0],board.robots[colour].position[1],images))
    robotrect=images.robot.get_rect()

screen.blit(images.flag,getXYGridOffset(board.flagloc[0],board.flagloc[1],images))

#respond to input
while 1:
    for event in pygame.event.get():
        if event.type==pygame.QUIT: 
            sys.exit()
        elif event.type==pygame.KEYDOWN:
            screen.blit(images.floor,
                        getXYGridOffset(board.robots[board.active_robot].position[0],
                                        board.robots[board.active_robot].position[1],
                                        images))
            board.boardstate,irobot,jrobot=moveRobot(board.boardstate,board.robots[board.active_robot].position[0],
                                                     board.robots[board.active_robot].position[1],
                                                        event.key)
            board.robots[board.active_robot].position[0]=irobot
            board.robots[board.active_robot].position[1]=jrobot            
            screen.blit(images.robot,getXYGridOffset(irobot,jrobot,images))
            print 'key pressed'
                    
        #screen.fill(black)
        pygame.display.flip()
        
        
   
#check victory conditions
