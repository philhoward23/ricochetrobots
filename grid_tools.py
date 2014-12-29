# -*- coding: utf-8 -*-
"""
Created on Thu Dec 11 15:54:26 2014

@author: phil.howard
"""

import pygame
import numpy as np
#from grid_globals import tilesize,wallsize


#function that converts board location (i,j) to screen location (x,y)
def getXYOffset(i,j,graphics):
    x=(j%2)*graphics.wallsize + (j//2)*(graphics.tilesize+graphics.wallsize)
    y=(i%2)*graphics.wallsize + (i//2)*(graphics.tilesize+graphics.wallsize)
    return x,y

#function that converts robot grid location (16*16) to screen location (x,y)
def getXYGridOffset(i,j,graphics):
    x=graphics.wallsize + (j-1)*(graphics.tilesize+graphics.wallsize)
    y=graphics.wallsize + (i-1)*(graphics.tilesize+graphics.wallsize)
    return x,y


#function that converts robot grid location (16*16) to board location (33*33, zero-indexed)
def getIJBoard(i,j):
    x=2*i-1
    y=2*j-1
    return x,y

#function that converts board location (33*33, zero-indexed) to robot grid location (16*16)
def getIJGrid(i,j):
    x=1+i//2
    y=1+j//2
    return x,y


def check_flag_between_grid_locations(flagloc,position,last_position):
    #first check between x locs
    if last_position[0] >= position[0]:
        if (flagloc[0] >= position[0]) and (flagloc[0] <= last_position[0]):
            xflag = True
        else:
            xflag = False
    else:
        if (flagloc[0] >= last_position[0]) and (flagloc[0] <= position[0]):
            xflag = True
        else:
            xflag = False
    #then check y locs
    if last_position[1] >= position[1]:
        if (flagloc[1] >= position[1]) and (flagloc[1] <= last_position[1]):
            yflag = True
        else:
            yflag = False
    else:
        if (flagloc[1] >= last_position[1]) and (flagloc[1] <= position[1]):
            yflag = True
        else:
            yflag = False            
    return xflag and yflag        
            
            
        