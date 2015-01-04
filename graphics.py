# -*- coding: utf-8 -*-
"""
Created on Sun Dec 28 11:49:54 2014

@author: Phil.Howard
"""
import pygame
from grid_tools import getXYOffset,getXYGridOffset,check_flag_between_grid_locations
from sidebar import Sidebar

#functions to initialise graphics for ricochet robots
def get_n_frames(xold,yold,xnew,ynew,speed):
    #assumes only movement is parallel to an axis ie one of x and y is fixed
    npixels=abs(xnew-xold)+abs(ynew-yold)
    nframes=npixels//speed
    return nframes


class Graphics(object):
    def load_graphics(self):
        #default floor tile
        self.floor = pygame.image.load("graphics/floor_small.png").convert()
        
        #vertical, horizontal and fill walls
        self.wall_v = pygame.image.load("graphics/wall_v_small.png").convert()
        self.wall_h = pygame.image.load("graphics/wall_h_small.png").convert()
        self.wall_c = pygame.image.load("graphics/wall_c.png").convert()
        
        #robots and flags
        self.robots={"yellow":pygame.image.load("graphics/robot_yellow_small.png").convert(),
                         "red":pygame.image.load("graphics/robot_red_small.png").convert(),
                         "green":pygame.image.load("graphics/robot_green_small.png").convert(),
                         "blue":pygame.image.load("graphics/robot_blue_small.png").convert(),
                         "silver":pygame.image.load("graphics/robot_silver_small.png").convert()}
                         
        self.flags={"yellow":pygame.image.load("graphics/flag_yellow_small.png").convert(),
                        "red":pygame.image.load("graphics/flag_red_small.png").convert(),
                        "green":pygame.image.load("graphics/flag_green_small.png").convert(),
                        "blue":pygame.image.load("graphics/flag_blue_small.png").convert(),
                        "rainbow":pygame.image.load("graphics/flag_rainbow_small.png").convert()}
            
        #sidebar
        #title
        self.title = pygame.image.load("graphics/title.png").convert()      
        
        #dimensions for drawing
        self.tilesize = self.floor.get_width()
        self.wallsize = self.wall_c.get_width()
        self.sidebar_width = self.title.get_width()
    
    def __init__(self, gridsize, boardsize):
        #initialise display for converting pixel format of images
        self.screen=pygame.display.set_mode()
        
        #load images and set dimensions
        self.load_graphics()
        
        self.screensize = width, height = gridsize*self.tilesize + (gridsize+1)*self.wallsize + self.sidebar_width,gridsize*self.tilesize+(gridsize+1)*self.wallsize
        self.sidebar_rect = pygame.Rect(width-self.sidebar_width,0,self.sidebar_width,height)
        self.speed = 2 #pixels per frame
        self.black=0,0,0
        self.background=200,200,200
        self.screen=pygame.display.set_mode(self.screensize)
        pygame.display.set_caption("Ricochet Robots")
    
    def redraw_flag(self,board):
        self.screen.blit(self.flags[board.flag_colour],getXYGridOffset(board.flagloc[0],board.flagloc[1],self))
        pygame.display.flip()
    
    def redraw_robots(self,board):    
        for colour in board.robot_colours:
            self.screen.blit(self.robots[colour],getXYGridOffset(board.robots[colour].position[0],board.robots[colour].position[1],self))        
        pygame.display.flip()
        
    
    def draw_initial_board(self,board):
        #clear any previous game state
        self.screen.fill(self.background)  
        
        #sidebar - check if already exists in case of board reset
        if hasattr(self, 'sidebar'):
            self.sidebar.__init__(self,board)
        else:
            self.sidebar=Sidebar(self,board)        
        
        #draw
        for i in range(board.gridsize):
            for j in range(board.gridsize):
                self.screen.blit(self.floor,
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
                            self.screen.blit(self.wall_c,
                                             (getXYOffset(i,j,self)))
                        else:
                            self.screen.blit(self.wall_h,
                                             (getXYOffset(i,j,self)))
                    else:
                        self.screen.blit(self.wall_v,
                                         (getXYOffset(i,j,self)))
                        
        #draw flag
        self.redraw_flag(board)
                
        #draw robot(s) at their turn start positions, which should be same as current in all cases
        self.robot_rects={}
        for colour in board.robot_colours:
            self.screen.blit(self.robots[colour],getXYGridOffset(board.robots[colour].position[0],board.robots[colour].position[1],self))
            self.robot_rects[colour]=self.robots[colour].get_rect()
            self.robot_rects[colour]=self.robot_rects[colour].move(getXYGridOffset(board.robots[colour].position[0],board.robots[colour].position[1],self))
        
        pygame.display.flip()
        
    def animate(self,board,key):                
        #check for reset (pressed r)
        if key in (pygame.K_r,pygame.K_n,pygame.K_f,pygame.K_u):
            self.draw_initial_board(board)
            return
        
        #check for victory state - only allows reset options unless still needs to do the final animation to reach that state
        if board.victory and ((self.robot_rects[board.active_robot].left,self.robot_rects[board.active_robot].top)==getXYGridOffset(board.flagloc[0],board.flagloc[1],self)):
            if key not in (pygame.K_r,pygame.K_n,pygame.K_f,pygame.K_u):
                return        
        
        #find active robot
        robot=board.robots[board.active_robot]
        #image
        robot_image=self.robots[board.active_robot]
        #copy of active rectangle - must update before returning
        robotrect=self.robot_rects[board.active_robot]
        #ensure info pane has correct info
        if key in (pygame.K_1,pygame.K_2,pygame.K_3,pygame.K_4,pygame.K_5,pygame.K_KP1,pygame.K_KP2,pygame.K_KP3,pygame.K_KP4,pygame.K_KP5):
            self.sidebar.update_active_text(board.active_robot) 
            
        #determine number of frames from speed and difference between new robot position and old
        xnew,ynew=getXYGridOffset(robot.position[0],
                                    robot.position[1],
                                    self)
                                    
        xold,yold=getXYGridOffset(robot.last_position[0],
                                    robot.last_position[1],
                                    self)
            
        nframes=get_n_frames(xold,yold,xnew,ynew,self.speed)
                
        #case when no movement - do nothing
        if nframes==0:
            return
        
        #check whether flag needs including in animation
        draw_flag=check_flag_between_grid_locations(board.flagloc,tuple(robot.position),tuple(robot.last_position))
        flagloc=getXYGridOffset(board.flagloc[0],board.flagloc[1],self)
        
        #set lag to slow movement
        frame_delay=0
        
        if key == pygame.K_LEFT:
            #print 'left pressed'
            velocity=(-self.speed,0)
            #animate
            for frame in range(nframes):
                #fill rectangle with background - rectangle skips edge walls
                animation_rect = (xnew,ynew,xold-xnew+self.tilesize,self.tilesize)
                self.screen.fill(self.background,animation_rect)
                #draw floor (and flag when necessary) then robot in new location
                for i in range(1+robot.last_position[1]-robot.position[1]):
                    #print robot.position, robot.last_position, i
                    self.screen.blit(self.floor,
                                (self.wallsize+(robot.position[1]+i-1)*(self.tilesize+self.wallsize),
                                 self.wallsize+(robot.position[0]-1)*(self.tilesize+self.wallsize)))
                if draw_flag:
                    self.screen.blit(self.flags[board.flag_colour],flagloc)
                robotrect=robotrect.move(velocity)
                self.screen.blit(robot_image,robotrect)
                #pygame.display.flip()
                pygame.display.update(animation_rect)
                #slow animation down
                pygame.time.wait(frame_delay)
                       
        elif key == pygame.K_RIGHT:
            velocity=(self.speed,0)
            #animate
            for frame in range(nframes):
                #fill rectangle with background - rectangle skips edge walls
                animation_rect = (xold,ynew,xnew-xold+self.tilesize,self.tilesize)
                self.screen.fill(self.background,animation_rect)
                #draw floor (and flag when necessary) then robot in new location
                for i in range(1+robot.position[1]-robot.last_position[1]):
                    #print robot.position, robot.last_position, i
                    self.screen.blit(self.floor,
                                (self.wallsize+(robot.last_position[1]+i-1)*(self.tilesize+self.wallsize),
                                 self.wallsize+(robot.last_position[0]-1)*(self.tilesize+self.wallsize)))
                if draw_flag:
                    self.screen.blit(self.flags[board.flag_colour],flagloc)
                robotrect=robotrect.move(velocity)
                self.screen.blit(robot_image,robotrect)
                #pygame.display.flip()
                pygame.display.update(animation_rect)
                #slow animation down
                pygame.time.wait(frame_delay)            
        elif key == pygame.K_UP:
            velocity=(0,-self.speed)
            #animate
            for frame in range(nframes):
                #fill rectangle with background - rectangle skips edge walls
                animation_rect = (xnew,ynew,self.tilesize,yold-ynew+self.tilesize)
                self.screen.fill(self.background,animation_rect)
                #draw floor (and flag when necessary) then robot in new location
                for i in range(1+robot.last_position[0]-robot.position[0]):
                    #print robot.position, robot.last_position, i
                    self.screen.blit(self.floor,
                                (self.wallsize+(robot.position[1]-1)*(self.tilesize+self.wallsize),
                                 self.wallsize+(robot.position[0]+i-1)*(self.tilesize+self.wallsize)))
                if draw_flag:
                    self.screen.blit(self.flags[board.flag_colour],flagloc)
                robotrect=robotrect.move(velocity)
                self.screen.blit(robot_image,robotrect)
                #pygame.display.flip()
                pygame.display.update(animation_rect)
                #slow animation down
                pygame.time.wait(frame_delay)            
        elif key == pygame.K_DOWN:
            velocity=(0,self.speed)
            #animate
            for frame in range(nframes):
                #fill rectangle with background - rectangle skips edge walls
                animation_rect = (xnew,yold,self.tilesize,ynew-yold+self.tilesize)
                self.screen.fill(self.background,animation_rect)
                #draw floor (and flag when necessary) then robot in new location
                for i in range(1+robot.position[0]-robot.last_position[0]):
                    #print robot.position, robot.last_position, i
                    self.screen.blit(self.floor,
                                (self.wallsize+(robot.last_position[1]-1)*(self.tilesize+self.wallsize),
                                 self.wallsize+(robot.last_position[0]+i-1)*(self.tilesize+self.wallsize)))
                if draw_flag:
                    self.screen.blit(self.flags[board.flag_colour],flagloc)
                robotrect=robotrect.move(velocity)
                self.screen.blit(robot_image,robotrect)
                #pygame.display.flip()
                pygame.display.update(animation_rect)
                #slow animation down
                pygame.time.wait(frame_delay)              
        else:
            return
        
        #update moves taken and final robot rectangle
        self.sidebar.update_moves_text(board.moves_taken)
        self.robot_rects[board.active_robot]=robotrect
                
        return
            

            
            