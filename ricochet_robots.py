# -*- coding: utf-8 -*-
"""
Created on Thu Dec 25 22:51:16 2014

@author: Phil.Howard
"""

#required modules and functions
import sys, pygame
from initialise_game import Board
from graphics import Graphics

#create game
pygame.init()

#initialise board
board = Board()
board.initialise()

#initialise display of board
images = Graphics(board.gridsize,board.boardsize)
images.draw_initial_board(images.screen,board)

#respond to input
while 1:
    for event in pygame.event.get():
        if event.type==pygame.QUIT: 
            sys.exit()
        elif event.type==pygame.KEYDOWN:
            #update robot location on board
            board.process_keypress(event.key)
            #move_active_robot(event.key)
            
            #animate motion
            images.animate(images.screen,board,event.key)
            
            print 'key pressed'
            #check victory condition
            if board.check_victory():
                images.sidebar.update_info_text('You made it to the flag','Congratulations!')        
            
        #screen.fill(black)
        #pygame.display.flip()
        
        
   
#check victory conditions
