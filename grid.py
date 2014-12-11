# -*- coding: utf-8 -*-
"""
Created on Thu Dec 11 10:56:55 2014

@author: phil.howard
"""



import sys, pygame
import numpy as np


pygame.init()


from grid_globals import gridsize,boardsize,tilesize,wallsize

#globals
#gridsize=16
#boardsize=1+2*gridsize
#
#tilesize=40
#wallsize=10


from grid_tools import getXYOffset,getXYGridOffset,moveRobot,getIJBoard

size = width, height = gridsize*tilesize+(gridsize+1)*wallsize,gridsize*tilesize+(gridsize+1)*wallsize
speed = [2,2]
black=0,0,0
background=200,200,200

screen=pygame.display.set_mode(size)
screen.fill(background)

ball=pygame.image.load("ball.gif")
ballrect=ball.get_rect()

floor=pygame.image.load("floor.png")
#vertical, horizontal and fill walls
wall_v=pygame.image.load("wall_v.png")
wall_h=pygame.image.load("wall_h.png")
wall_c=pygame.image.load("wall_c.png")

#robot
robot=pygame.image.load("robot.png")

#flag
flag=pygame.image.load("flag.png")


#initialise board
#0=floor/space
#1=wall
#2=centre tiles
#3=robot
#4=flag
boardstate=np.full((boardsize,boardsize),0,dtype=int)
#default walls
boardstate[:,0]=[1]*boardsize
boardstate[0,:]=[1]*boardsize
boardstate[:,boardsize-1]=[1]*boardsize
boardstate[boardsize-1,:]=[1]*boardsize
#centre walls
boardstate[gridsize-2:gridsize+3,gridsize-2:gridsize+3]=np.full((5,5),1,dtype=int)
boardstate[gridsize-1:gridsize+2,gridsize-1:gridsize+2]=np.full((3,3),2,dtype=int)

#sample board y,x format for np array filling and bad decisions...
vwalls=[(1,5),(1,11),(2,3),(2,9),(3,16),(4,1),(5,6),(5,11),(7,6),(7,12),(8,4),(10,4),(10,15),(11,9),(12,1),(12,13),(13,7),(14,10),(15,2),(16,6),(16,12)]
hwalls=[(2,3),(2,10),(2,15),(4,2),(4,7),(5,1),(5,11),(5,16),(6,6),(6,13),(8,4),(9,4),(10,9),(10,15),(11,16),(12,2),(12,14),(13,7),(13,11),(14,1),(14,3)]

for wall in vwalls:
    boardstate[1+2*(wall[0]-1),2*wall[1]]=1
for wall in hwalls:
    boardstate[2*wall[0],1+2*(wall[1]-1)]=1

for i in range(boardsize):
    print boardstate[i]


#draw
for i in range(gridsize):
    for j in range(gridsize):
        screen.blit(floor,
                    (wallsize+i*(tilesize+wallsize),
                     wallsize+j*(tilesize+wallsize)))



#set walls
for i in range(boardsize):
    for j in range(boardsize):
        if boardstate[i,j]==1:
            #horizontal, vertical or gap?
            if i%2==0:
                if j%2==0:
                    #gap
                    screen.blit(wall_c,
                    (getXYOffset(i,j)))
                else:
                    screen.blit(wall_h,
                    (getXYOffset(i,j)))
            else:
                screen.blit(wall_v,
                (getXYOffset(i,j)))

#initialize robot
while 1:
    irobot,jrobot=1+np.random.randint(gridsize),1+np.random.randint(gridsize)
    if irobot not in (8,9) and jrobot not in (8,9):
        boardstate[getIJBoard(irobot,jrobot)]=3
        screen.blit(robot,getXYGridOffset(irobot,jrobot))
        robotrect=robot.get_rect()
        break

#initialize target
flaglocs=[(10,4)]
flagloc=flaglocs[np.random.randint(len(flaglocs))]
screen.blit(flag,getXYGridOffset(*flagloc))


while 1:
    for event in pygame.event.get():
        if event.type==pygame.QUIT: 
            sys.exit()
        elif event.type==pygame.KEYDOWN:
            screen.blit(floor,getXYGridOffset(irobot,jrobot))
            boardstate,irobot,jrobot=moveRobot(boardstate,irobot,jrobot,event.key)
            screen.blit(robot,getXYGridOffset(irobot,jrobot))
            print 'key pressed'
            
        ballrect=ballrect.move(speed)
        if ballrect.left < 0 or ballrect.right > width:
            speed[0]=-speed[0]
        if ballrect.top<0 or ballrect.bottom>height:
            speed[1]=-speed[1]
        
        #screen.fill(black)
        screen.blit(ball,ballrect)
        pygame.display.flip()
        
        
    