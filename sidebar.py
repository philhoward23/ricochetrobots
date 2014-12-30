# -*- coding: utf-8 -*-
"""
Created on Mon Dec 29 15:53:55 2014

@author: Phil.Howard
"""
import pygame
import pygame.freetype
#import textwrap

class Sidebar(object):
    def update_moves_text(self,moves):
        #clear
        self.screen.blit(self.moves_box, self.moves_box_rect)
        #update
        self.moves_text, new_text_rect = self.font.render('%d moves taken this turn' % moves, fgcolor=(0, 0, 0), bgcolor=None)
        self.moves_text_rect.height = new_text_rect.height
        self.moves_text_rect.width = new_text_rect.width
        self.screen.blit(self.moves_text, self.moves_text_rect)
        pygame.display.update(self.moves_box_rect)
        
    def update_active_text(self,active_colour):
        #clear
        self.screen.blit(self.active_box, self.active_box_rect)
        #update
        self.active_text, new_text_rect = self.font.render('The %s robot is active' % active_colour, fgcolor=(0, 0, 0), bgcolor=None)
        self.active_text_rect.height = new_text_rect.height
        self.active_text_rect.width = new_text_rect.width
        self.screen.blit(self.active_text, self.active_text_rect)
        pygame.display.update(self.active_box_rect)

    def update_info_text(self,line1,line2=None):
        #clear
        self.screen.blit(self.info_box, self.info_box_rect)
        #update
        self.info_text, new_text_rect = self.font.render(line1, fgcolor=(0, 0, 0), bgcolor=None)
        self.info_text_rect.height = new_text_rect.height
        self.info_text_rect.width = new_text_rect.width
        self.screen.blit(self.info_text, self.info_text_rect)          
        pygame.display.update(self.info_box_rect)
        #line2
        self.info_text_line2, new_text_rect = self.font.render(line2, fgcolor=(0, 0, 0), bgcolor=None)
        self.info_text_line2_rect.height = new_text_rect.height
        self.info_text_line2_rect.width = new_text_rect.width
        self.screen.blit(self.info_text_line2, self.info_text_line2_rect)          
        pygame.display.update(self.info_text_line2_rect)
        
    def __init__(self,graphics,screen,board):
        self.screen = screen
        self.background=graphics.background
        #title graphic
        self.screen.blit(graphics.title,graphics.sidebar_rect)
        
        #text for game messages
        self.fontsize = 20
        self.font = pygame.freetype.SysFont('Impact', self.fontsize)
        self.info_text, self.info_text_rect = self.font.render('Reach the flag with the', fgcolor=(0, 0, 0), bgcolor=None)
        self.info_text_line2, self.info_text_line2_rect = self.font.render('matching robot!', fgcolor=(0, 0, 0), bgcolor=None)
        self.active_text, self.active_text_rect = self.font.render('The %s robot is active' % board.active_robot, fgcolor=(0, 0, 0), bgcolor=None)
        self.moves_text, self.moves_text_rect = self.font.render('%d moves taken this turn' % board.moves_taken, fgcolor=(0, 0, 0), bgcolor=None)
                
        #create panes for the text displays
        
        self.info_box = pygame.Surface((graphics.sidebar_rect.width, 5*self.info_text_rect.height + 2*graphics.wallsize)).convert()
        self.info_box.fill(self.background) 
        self.info_box_rect = self.info_box.get_rect()
        self.info_box_rect = self.info_box_rect.move(graphics.sidebar_rect.left, graphics.title.get_height())
        
        self.active_box = pygame.Surface((graphics.sidebar_rect.width, 3*self.active_text_rect.height + 2*graphics.wallsize)).convert()
        self.active_box.fill(self.background)
        self.active_box_rect = self.active_box.get_rect()
        self.active_box_rect = self.active_box_rect.move(graphics.sidebar_rect.left, graphics.title.get_height() + self.info_box.get_height())
        
        self.moves_box = pygame.Surface((graphics.sidebar_rect.width, 3*self.moves_text_rect.height + 2*graphics.wallsize)).convert()
        self.moves_box.fill(self.background)
        self.moves_box_rect = self.moves_box.get_rect()
        self.moves_box_rect = self.moves_box_rect.move(graphics.sidebar_rect.left, graphics.title.get_height() + self.info_box.get_height() + self.active_box.get_height())        
        
        #initialise contents
        self.screen.blit(self.info_box, self.info_box_rect)
        self.screen.blit(self.active_box, self.active_box_rect)
        self.screen.blit(self.moves_box, self.moves_box_rect)
        
        self.info_text_rect=self.info_text_rect.move(self.info_box_rect.left + graphics.wallsize, self.info_box_rect.top + graphics.wallsize)
        self.screen.blit(self.info_text, self.info_text_rect)
        self.info_text_line2_rect=self.info_text_line2_rect.move(self.info_box_rect.left + graphics.wallsize, self.info_box_rect.top + 2*self.info_text_rect.height + graphics.wallsize)
        self.screen.blit(self.info_text_line2, self.info_text_line2_rect)
        self.active_text_rect=self.active_text_rect.move(self.active_box_rect.left + graphics.wallsize, self.active_box_rect.top + graphics.wallsize)
        self.screen.blit(self.active_text, self.active_text_rect)
        self.moves_text_rect=self.moves_text_rect.move(self.moves_box_rect.left + graphics.wallsize, self.moves_box_rect.top + graphics.wallsize)
        self.screen.blit(self.moves_text, self.moves_text_rect)

        