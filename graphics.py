# -*- coding: utf-8 -*-
"""
Created on Sun Dec 28 11:49:54 2014

@author: Phil.Howard
"""
import pygame
from grid_tools import getXYOffset,getXYGridOffset,getIJBoard,getIJGrid,check_flag_between_grid_locations

#functions to initialise graphics for ricochet robots
def load_graphics(graphics):
    #default floor tile
    graphics.floor = pygame.image.load("graphics/floor_small.png")
    
    #vertical, horizontal and fill walls
    graphics.wall_v = pygame.image.load("graphics/wall_v_small.png")
    graphics.wall_h = pygame.image.load("graphics/wall_h_small.png")
    graphics.wall_c = pygame.image.load("graphics/wall_c.png")
    
    #robot
    graphics.robot = pygame.image.load("graphics/robot_yellow_small.png")
    
    #flag
    graphics.flag = pygame.image.load("graphics/flag_yellow_small.png")
    
    #dimensions for drawing
    graphics.tilesize = graphics.floor.get_width()
    graphics.wallsize = graphics.wall_c.get_width()

def get_n_frames(xold,yold,xnew,ynew,speed):
    #assumes only movement is parallel to an axis ie one of x and y is fixed
    npixels=abs(xnew-xold)+abs(ynew-yold)
    nframes=npixels//speed
    return nframes


class Graphics(object):
    def __init__(self, gridsize, boardsize):
        #load images and set dimensions
        load_graphics(self)
        
        self.screensize = width, height = gridsize*self.tilesize+(gridsize+1)*self.wallsize,gridsize*self.tilesize+(gridsize+1)*self.wallsize
        self.speed = 2 #pixels per frame
        self.black=0,0,0
        self.background=200,200,200
        
    def draw_initial_board(self,screen,board):
        #draw
        for i in range(board.gridsize):
            for j in range(board.gridsize):
                screen.blit(self.floor,
                            (self.wallsize+i*(self.tilesize+self.wallsize),
                             self.wallsize+j*(self.tilesize+self.wallsize)))
        
        #set walls
        for i in range(board.boardsize):
            for j in range(board.boardsize):
                if board.boardstate[i,j]==1:
                    #horizontal, vertical or gap?
                    if i%2==0:
                        if j%2==0:
                            #gap
                            screen.blit(self.wall_c,
                            (getXYOffset(i,j,self)))
                        else:
                            screen.blit(self.wall_h,
                            (getXYOffset(i,j,self)))
                    else:
                        screen.blit(self.wall_v,
                        (getXYOffset(i,j,self)))
        
        #draw robot(s)
        for colour in board.robot_colours:
            screen.blit(self.robot,getXYGridOffset(board.robots[colour].position[0],board.robots[colour].position[1],self))
            self.robotrect=self.robot.get_rect()
            self.robotrect=self.robotrect.move(getXYGridOffset(board.robots[colour].position[0],board.robots[colour].position[1],self))
        
        #draw flag
        screen.blit(self.flag,getXYGridOffset(board.flagloc[0],board.flagloc[1],self))
        
    def animate(self,screen,board,key):
        #find active robot
        robot=board.robots[board.active_robot]
        
#        screen.blit(self.robot,
#                    getXYGridOffset(robot.position[0],
#                                    robot.position[1],
#                                    self))
        
        #determine number of frames from speed and difference between new robot position and old
        xnew,ynew=getXYGridOffset(robot.position[0],
                                    robot.position[1],
                                    self)
                                    
        xold,yold=getXYGridOffset(robot.last_position[0],
                                    robot.last_position[1],
                                    self)
            
        nframes=get_n_frames(xold,yold,xnew,ynew,self.speed)
                
        #case when no movement - just draw robot again and return
        if nframes==0:
            screen.blit(self.robot,
            getXYGridOffset(robot.position[0],
                            robot.position[1],
                            self))
            return
        
        #check whether flag needs including in animation
        draw_flag=check_flag_between_grid_locations(board.flagloc,tuple(robot.position),tuple(robot.last_position))
        flagloc=getXYGridOffset(board.flagloc[0],board.flagloc[1],self)
        
        if key == pygame.K_LEFT:
            print 'left pressed'
            velocity=(-self.speed,0)
            #animate
            for frame in range(nframes):
                #fill rectangle with background - rectangle skips edge walls
                animation_rect = (xnew,ynew,xold-xnew+self.tilesize,self.tilesize)
                screen.fill(self.background,animation_rect)
                #draw floor (and flag when necessary) then robot in new location
                for i in range(1+robot.last_position[1]-robot.position[1]):
                    #print robot.position, robot.last_position, i
                    screen.blit(self.floor,
                                (self.wallsize+(robot.position[1]+i-1)*(self.tilesize+self.wallsize),
                                 self.wallsize+(robot.position[0]-1)*(self.tilesize+self.wallsize)))
                if draw_flag:
                    screen.blit(self.flag,flagloc)
                self.robotrect=self.robotrect.move(velocity)
                screen.blit(self.robot,self.robotrect)
                pygame.display.flip()
                #pygame.time.wait(100)
                       
        elif key == pygame.K_RIGHT:
            velocity=(self.speed,0)
        elif key == pygame.K_UP:
            velocity=(0,-self.speed)
        elif key == pygame.K_DOWN:
            velocity=(0,self.speed)
        else:
            pass
        

            

            
            