# -*- coding: utf-8 -*-
"""
Created on Thu Dec 11 15:54:26 2014

@author: phil.howard
"""

import pygame
import numpy as np
from grid_globals import tilesize,wallsize


#function that converts board location (i,j) to screen location (x,y)
def getXYOffset(i,j):
    x=(j%2)*wallsize + (j//2)*(tilesize+wallsize)
    y=(i%2)*wallsize + (i//2)*(tilesize+wallsize)
    return x,y

#function that converts robot grid location (16*16) to screen location (x,y)
def getXYGridOffset(i,j):
    x=wallsize + (j-1)*(tilesize+wallsize)
    y=wallsize + (i-1)*(tilesize+wallsize)
    return x,y


#function that converts robot grid location (16*16) to board location (33*33, zero-indexed)
def getIJBoard(i,j):
    x=2*i-1
    y=2*j-1
    return x,y


def moveRobot(boardstate,i,j,key):
    boardi,boardj=getIJBoard(i,j)
    inew,jnew=i,j
    if key == pygame.K_LEFT:
        print i,j
        print boardi,boardj
        inew=i
        #find first non-collision square to left
        boardjnew=1+np.max(np.where(boardstate[boardi][0:boardj]>0))
        boardstate[boardi,boardj]=0
        boardstate[boardi,boardjnew]=3
        jnew=1+boardjnew//2
        print inew,jnew
    elif key == pygame.K_RIGHT:
        pass
    elif key == pygame.K_UP:
        pass
    elif key == pygame.K_DOWN:
        pass
    else:
        pass
    return(boardstate,inew,jnew)
