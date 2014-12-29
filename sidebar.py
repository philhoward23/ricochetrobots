# -*- coding: utf-8 -*-
"""
Created on Mon Dec 29 15:53:55 2014

@author: Phil.Howard
"""
import pygame
import pygame.freetype

class Sidebar(object):
    def update_active_text(self,active_colour):
        #clear
        self.screen.blit(self.message_box, self.active_box_rect)
        #update
        self.active_text, new_text_rect = self.font.render('The %s robot is active' % active_colour, fgcolor=(0, 0, 0), bgcolor=None)
        self.active_text_rect.height = new_text_rect.height
        self.active_text_rect.width = new_text_rect.width
        self.screen.blit(self.active_text, self.active_text_rect)
        pygame.display.update(self.active_box_rect)
    
    def __init__(self,graphics,screen,board):
        self.screen = screen
        self.background=graphics.background
        #title graphic
        self.screen.blit(graphics.title,graphics.sidebar_rect)
        
        #text for game messages
        self.fontsize = 20
        self.font = pygame.freetype.SysFont('Impact', self.fontsize)
        self.info_text, self.info_text_rect = self.font.render('Reach the flag with the matching robot!', fgcolor=(0, 0, 0), bgcolor=None)
        self.active_text, self.active_text_rect = self.font.render('The %s robot is active' % board.active_robot, fgcolor=(0, 0, 0), bgcolor=None)
                
        #create panes for the text displays
        self.message_box = pygame.Surface((graphics.sidebar_rect.width, 3*self.info_text_rect.height + 2*graphics.wallsize)).convert()
        self.message_box.fill(self.background)
        self.active_box_rect = self.message_box.get_rect()
        self.active_box_rect = self.active_box_rect.move(graphics.sidebar_rect.left, graphics.title.get_height() + self.message_box.get_height())
        self.info_box_rect = self.message_box.get_rect()
        self.info_box_rect = self.info_box_rect.move(graphics.sidebar_rect.left, graphics.title.get_height())
        
        #initialise contents
        self.info_text_rect=self.info_text_rect.move(self.info_box_rect.left + graphics.wallsize, self.info_box_rect.top + graphics.wallsize)
        self.screen.blit(self.info_text, self.info_text_rect)
        self.active_text_rect=self.active_text_rect.move(self.active_box_rect.left + graphics.wallsize, self.active_box_rect.top + graphics.wallsize)
        self.screen.blit(self.active_text, self.active_text_rect)

        