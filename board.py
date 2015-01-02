# -*- coding: utf-8 -*-
"""
Created on Thu Jan 01 19:34:06 2015

@author: Phil.Howard
"""

import pygame
import numpy as np
from grid_tools import getXYOffset,getXYGridOffset,getIJBoard,getIJGrid

def rotate_clockwise(coord,gridsize):
    shift_matrix = np.array((gridsize/2 + 0.5, gridsize/2 + 0.5), dtype=float)
    centred_coord = np.array(coord,dtype=float) - shift_matrix
    rotation_matrix = np.array(((0,1),(-1,0)),dtype=float)
    rotated_coord = np.dot(rotation_matrix, centred_coord)
    final_coord = rotated_coord + shift_matrix
    #convert back to integer tuple coordinates
    return tuple(map(int,final_coord))
    
    
#store and initialise board configurations
#game comes with 4 2-sided tiles that can be combined - 2*(3*2)*(2*2)*(1*2)=96 configurations possible
class Board(object):
    def initialise_tile(self,board,tile):
        current_tile = np.full((self.boardsize,self.boardsize),0,dtype=int)
        #default walls
        current_tile[:,0] = [1]*self.boardsize
        current_tile[0,:] = [1]*self.boardsize
        #centre walls
        current_tile[self.boardsize-3:,self.boardsize-3:] = np.full((3,3),1,dtype=int)
        current_tile[self.boardsize-2:,self.boardsize-2:] = np.full((3,3),2,dtype=int)            
        
        self.tiles[board][tile]["tile"] = current_tile
        #self.boards[board][tile] = current_tile
       
    def generate_game_board(self):
        #pick top left, top right, bottom right, bottom left tiles in turn
        board_order = np.random.permutation(4)
        board_variants = np.random.randint(0,2,4)
        
        top_left = self.tiles[board_order[0]][board_variants[0]]
        top_right = self.tiles[board_order[1]][board_variants[1]]            
        bottom_right = self.tiles[board_order[2]][board_variants[2]]            
        bottom_left = self.tiles[board_order[3]][board_variants[3]]  
        
        #assemble game board
        game_board = top_left["tile"]
        top_right_tile = np.rot90(top_right["tile"],3)
        
        #check overlap and join
        game_board[:,self.boardsize-1] = np.max(game_board[:,self.boardsize-1],top_right_tile[:,0])
        game_board = np.hstack(game_board, top_right_tile[:,1:])
        
        #generate bottom half of game board
        bottom_right_tile = np.rot90(bottom_right["tile"],2)
        bottom_left_tile = np.rot90(bottom_left["tile"],1)
        bottom_left_tile[:,self.boardsize-1] = np.max(bottom_left_tile[:,self.boardsize-1],bottom_right_tile[:,0])
        bottom_half = np.hstack(bottom_left_tile, bottom_right_tile[:,1:])
        
        #check overlap and join
        game_board[self.boardsize-1,:] = np.max(game_board[self.boardsize-1,:],bottom_half[0,:])
        game_board = np.vstack(game_board, bottom_half[1:,:])
        
        #determine flag locations
        flags = {"red":[], "yellow":[], "green":[], "blue":[], "rainbow":[]}
        
        for colour in flags.keys():
            if top_left["flags"][colour] is not None:
                flags[colour].append(top_left["flags"][colour])
            if top_right["flags"][colour] is not None:
                flags[colour].append(rotate_clockwise(top_right["flags"][colour],self.gridsize))
            if bottom_right["flags"][colour] is not None:
                flags[colour].append(rotate_clockwise(top_right["flags"][colour],self.gridsize))

        
        return game_board, flags
       
    def __init__(self):
        self.gridsize = 8
        self.boardsize=1+2*self.gridsize
        #self.boards=[ [None, None] for i in range(4) ]
                
        #define all 8 possible tiles                
        self.tiles = [ [ {"vwalls":[(1,2), (2,4), (3,2), (4,7), (7,3)],
                     "hwalls":[(1,5), (2,2), (4,7), (6,1), (7,4)], 
                     "flags":{"red":(2,5), "yellow":(4,7), "green":(3,2), "blue":(7,4), "rainbow":None}
                    },
                    {"vwalls":[(1,5), (2,7), (3,1), (6,7), (7,3)],
                     "hwalls":[(2,2), (2,7), (5,7), (6,1), (7,4)], 
                     "flags":{"red":(7,4), "yellow":(2,7), "green":(3,2), "blue":(6,7), "rainbow":None}
                    } 
                  ],
                  [ {"vwalls":[(1,5), (2,3), (4,1), (5,6), (7,6), (8,4)],
                     "hwalls":[(2,3), (4,2), (4,7), (5,1), (6,6), (8,4)], 
                     "flags":{"red":(2,3), "yellow":(5,7), "green":(4,2), "blue":(7,6), "rainbow":(8,4)}
                    },
                    {"vwalls":[(1,4), (2,6), (4,2), (5,5), (6,3), (6,8)],
                     "hwalls":[(2,7), (3,2), (4,6), (6,3), (6,8), (7,1)], 
                     "flags":{"red":(6,3), "yellow":(4,2), "green":(5,6), "blue":(2,7), "rainbow":(6,8)}
                    } 
                  ],
                  [ {"vwalls":[(1,4), (2,1), (3,7), (5,3), (6,7)],
                     "hwalls":[(2,2), (2,7), (5,3), (5,8), (6,1)], 
                     "flags":{"red":(2,2), "yellow":(6,8), "green":(3,7), "blue":(5,3), "rainbow":None}
                    },
                    {"vwalls":[(1,4), (3,6), (5,3), (6,7), (7,1)],
                     "hwalls":[(3,6), (4,3), (5,1), (6,2), (6,8)], 
                     "flags":{"red":(6,8), "yellow":(7,2), "green":(5,3), "blue":(3,6), "rainbow":None}
                    } 
                  ],
                  [ {"vwalls":[(1,4), (2,6), (3,1), (5,6), (7,3)],
                     "hwalls":[(2,6), (3,2), (4,1), (4,7), (6,3)], 
                     "flags":{"red":(3,2), "yellow":(5,7), "green":(2,6), "blue":(7,3), "rainbow":None}
                    },
                    {"vwalls":[(1,5), (2,2), (4,6), (6,5), (7,2)],
                     "hwalls":[(1,3), (4,7), (5,1), (5,5), (7,2)], 
                     "flags":{"red":(6,5), "yellow":(2,3), "green":(7,2), "blue":(4,7), "rainbow":None}
                    } 
                  ]
                ]
        
        
        for board in range(4):
            for tile in range(2):
                self.initialise_tile(self,board,tile)
                for wall in self.tiles[board][tile]["vwalls"]:
                    self.tiles[board][tile]["tile"][1+2*(wall[0]-1),2*wall[1]] = 1
                for wall in self.tiles[board][tile]["hwalls"]:
                    self.tiles[board][tile]["tile"][2*wall[0],1+2*(wall[1]-1)] = 1


        
