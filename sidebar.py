# -*- coding: utf-8 -*-
"""
Created on Mon Dec 29 15:53:55 2014

@author: Phil.Howard
"""
import pygame
import pygame.freetype
from textwrap import render_textrect

class Sidebar(object):
    def update_moves_text(self,moves):
        #clear
        self.screen.blit(self.moves_box, self.moves_box_rect)
        #update
        self.moves_text, new_text_rect = self.font.render('%d moves taken this flag' % moves, fgcolor=(0, 0, 0), bgcolor=None)
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
        
    def __init__(self,graphics,board):
        self.screen = graphics.screen
        self.background=graphics.background
        #title graphic
        self.screen.blit(graphics.title,graphics.sidebar_rect)
        
        #text for game messages
        self.fontsize = 20
        self.docs_fontsize = 14
        self.font = pygame.freetype.SysFont('Impact', self.fontsize)
        self.docs_font = pygame.font.SysFont('Impact',self.docs_fontsize)
        self.info_text, self.info_text_rect = self.font.render('Reach the flag with the', fgcolor=(0, 0, 0), bgcolor=None)
        self.info_text_line2, self.info_text_line2_rect = self.font.render('matching robot!', fgcolor=(0, 0, 0), bgcolor=None)
        self.active_text, self.active_text_rect = self.font.render('The %s robot is active' % board.active_robot, fgcolor=(0, 0, 0), bgcolor=None)
        self.moves_text, self.moves_text_rect = self.font.render('%d moves taken this flag' % board.moves_taken, fgcolor=(0, 0, 0), bgcolor=None)
        self.turns_text, self.turns_text_rect = self.font.render('Flag %d of 17 this game' % min(1+board.turn,17), fgcolor=(0, 0, 0), bgcolor=None)
        self.controls_text, self.controls_text_rect = self.font.render('Controls:', fgcolor=(0, 0, 0), bgcolor=None)
        
        #create panes for the text displays
        
        self.info_box = pygame.Surface((graphics.sidebar_rect.width, 4*self.info_text_rect.height + 2*graphics.wallsize)).convert()
        self.info_box.fill(self.background) 
        self.info_box_rect = self.info_box.get_rect()
        self.info_box_rect = self.info_box_rect.move(graphics.sidebar_rect.left, graphics.title.get_height())
        
        self.active_box = pygame.Surface((graphics.sidebar_rect.width, 2*self.active_text_rect.height + 2*graphics.wallsize)).convert()
        self.active_box.fill(self.background)
        self.active_box_rect = self.active_box.get_rect()
        self.active_box_rect = self.active_box_rect.move(graphics.sidebar_rect.left, graphics.title.get_height() + self.info_box.get_height())
        
        self.moves_box = pygame.Surface((graphics.sidebar_rect.width, 2*self.moves_text_rect.height + 2*graphics.wallsize)).convert()
        self.moves_box.fill(self.background)
        self.moves_box_rect = self.moves_box.get_rect()
        self.moves_box_rect = self.moves_box_rect.move(graphics.sidebar_rect.left, graphics.title.get_height() + self.info_box.get_height() + self.active_box.get_height())        
        
        self.turns_box = pygame.Surface((graphics.sidebar_rect.width, 2*self.turns_text_rect.height + 2*graphics.wallsize)).convert()
        self.turns_box.fill(self.background)
        self.turns_box_rect = self.turns_box.get_rect()
        self.turns_box_rect = self.turns_box_rect.move(graphics.sidebar_rect.left, graphics.title.get_height() + self.info_box.get_height() + self.active_box.get_height() + self.moves_box.get_height())        

        self.controls_box = pygame.Surface((graphics.sidebar_rect.width, 2*self.controls_text_rect.height + 2*graphics.wallsize)).convert()
        self.controls_box.fill(self.background)
        self.controls_box_rect = self.controls_box.get_rect()
        self.controls_box_rect = self.controls_box_rect.move(graphics.sidebar_rect.left, graphics.title.get_height() + self.info_box.get_height() + self.active_box.get_height() + self.moves_box.get_height() + self.turns_box.get_height())        
        
        self.docs_box_rect = pygame.Rect(graphics.sidebar_rect.left + graphics.wallsize, self.controls_box_rect.bottom, graphics.sidebar_rect.width - graphics.wallsize, graphics.sidebar_rect.height - self.controls_box_rect.bottom)
        #self.docs_box_text = "Please press:\n1-5 to activate that robot\nPress r to restart this flag\nPress f for the next flag\nPress n for a new game"
        self.docs_box_text = "1-5 to activate that robot\nr to (r)estart this flag\nf for the next (f)lag\nn for a (n)ew game\nu to (u)ndo the last move\nhold s to (s)how the flag"
        self.docs_box = render_textrect(self.docs_box_text, self.docs_font, self.docs_box_rect, (0, 0, 0), self.background, justification=0)
        
        #initialise contents
        self.screen.blit(self.info_box, self.info_box_rect)
        self.screen.blit(self.active_box, self.active_box_rect)
        self.screen.blit(self.moves_box, self.moves_box_rect)
        self.screen.blit(self.turns_box, self.turns_box_rect)
        
        self.info_text_rect=self.info_text_rect.move(self.info_box_rect.left + graphics.wallsize, self.info_box_rect.top + graphics.wallsize)
        self.screen.blit(self.info_text, self.info_text_rect)
        self.info_text_line2_rect=self.info_text_line2_rect.move(self.info_box_rect.left + graphics.wallsize, self.info_box_rect.top + 2*self.info_text_rect.height + graphics.wallsize)
        self.screen.blit(self.info_text_line2, self.info_text_line2_rect)
        self.active_text_rect=self.active_text_rect.move(self.active_box_rect.left + graphics.wallsize, self.active_box_rect.top + graphics.wallsize)
        self.screen.blit(self.active_text, self.active_text_rect)
        self.moves_text_rect=self.moves_text_rect.move(self.moves_box_rect.left + graphics.wallsize, self.moves_box_rect.top + graphics.wallsize)
        self.screen.blit(self.moves_text, self.moves_text_rect)
        self.turns_text_rect=self.turns_text_rect.move(self.turns_box_rect.left + graphics.wallsize, self.turns_box_rect.top + graphics.wallsize)
        self.screen.blit(self.turns_text, self.turns_text_rect)
        self.controls_text_rect=self.controls_text_rect.move(self.controls_box_rect.left + graphics.wallsize, self.controls_box_rect.top + graphics.wallsize)
        self.screen.blit(self.controls_text, self.controls_text_rect)
        self.screen.blit(self.docs_box,self.docs_box_rect)
        