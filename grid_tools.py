# -*- coding: utf-8 -*-
"""
Created on Thu Dec 11 15:54:26 2014

@author: phil.howard
"""

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
            
               
def rot90_coord(coord,n_rots=1,gridsize=8):
    #rotate around grid centre by 90 degrees anti-clockwise, n_rots times
    shift_matrix = np.array((gridsize/2 + 0.5, gridsize/2 + 0.5), dtype=float)
    centred_coord = np.array(coord,dtype=float) - shift_matrix
    if n_rots==1:        
        rotation_matrix = np.array(((0,-1),(1,0)),dtype=float)
    elif n_rots==2:        
        rotation_matrix = np.array(((-1,0),(0,-1)),dtype=float)
    elif n_rots==3:        
        rotation_matrix = np.array(((0,1),(-1,0)),dtype=float)
    else:
        raise ValueError('number of rotations must be 1,2 or 3')
        return 1
    rotated_coord = np.dot(rotation_matrix, centred_coord)
    final_coord = rotated_coord + shift_matrix
    #convert back to integer tuple coordinates
    return tuple(map(int,final_coord))
    
def offset_coord(coord,i_offset,j_offset):
    return coord[0]+i_offset, coord[1]+j_offset
        