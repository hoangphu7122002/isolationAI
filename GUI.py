import os
import pygame
from pygame.transform import scale
import time
from parameter import *
import numpy as np

#define global variables
FREE = 0
BLOCK = 2
ACTIVE_P1 = 1 #component
ACTIVE_P2 = -1 #component

class Gui(object):
    def __init__(self,board):
        self.board = board
        self.dim = len(board)
        self.row_constraint = [*range(0,self.dim)]
        self.col_constraint = [*range(0,self.dim)]
        print(self.row_constraint)
        pygame.init()
        self.window = pygame.display.set_mode((1100,800))
        self.game_font = pygame.font.Font('FileGame/04B_19.TTF',40)
        self.window.fill(white)
        
    def draw_board(self):
        dim = self.dim
        width = 800
        height = 800
        offset = 50
        margin = 4
        
        cell_size = int((width - 2 * offset - (dim - 1) * margin) / dim)
        step = cell_size + 5
        font = pygame.font.SysFont("ubuntumono", cell_size // 2)
        coord_x = offset
        for y in range(dim):
            coord_y = offset
            for x in range(dim):
                cell = pygame.Rect(coord_x, coord_y, cell_size, cell_size)
                if self.board[x][y] == FREE:
                    pygame.draw.rect(self.window, yellow, cell)
                elif self.board[x][y] == BLOCK:
                    pygame.draw.rect(self.window, black, cell)
                elif self.board[x][y] == ACTIVE_P1:
                    pygame.draw.rect(self.window, red_first, cell)
                elif self.board[x][y] == ACTIVE_P2:
                    pygame.draw.rect(self.window, blue_second, cell)
                coord_y += step
            coord_x += step
        
        # Draw cells borders
        for x in range(offset, height - offset, step):
            for y in range(offset, width - offset, step):
                cell = pygame.Rect(x, y, cell_size, cell_size)
                pygame.draw.rect(self.window, black, cell, 2)

        start = offset + (cell_size // 4)
        stop = height - cell_size

        # Display row constraints
        # print(self.row_constraint)
        for y, row_constraint in zip(range(start, stop, step), self.row_constraint):
            text = font.render(str(row_constraint), True, black)
            self.window.blit(text, [offset - 2 * text.get_width(), y])

        start = offset + (cell_size // 3)
        stop = width - cell_size
        
        # Display col constraints
        # print(self.col_constraint)
        for x, col_constraint in zip(range(start, stop, step), self.col_constraint):
            text = font.render(str(col_constraint), True, black)
            self.window.blit(text, [x, offset - text.get_height()])
        
        
    def render_font(self,turn = 0,time = 0):
        intro_surface = self.game_font.render(f'ISOLATION',True,red)
        intro_rect = intro_surface.get_rect(center = (925,300))
        self.window.blit(intro_surface,intro_rect)
        
        score_surface = self.game_font.render(f'LEVEL: {self.dim}x{self.dim}',True,black)
        score_rect = score_surface.get_rect(center = (925,450))
        self.window.blit(score_surface,score_rect)
        
        high_score_surface = self.game_font.render(f'TURN: {turn:5d}',True,black)
        high_score_rect = high_score_surface.get_rect(center = (925,520))
        self.window.blit(high_score_surface,high_score_rect)
        
        time_surface = self.game_font.render('TIME: {:.2f}s'.format(time),True,black)
        time_rect = time_surface.get_rect(center = (925,590))
        self.window.blit(time_surface,time_rect)
    # def interupt(self,run):
    #     for event in pygame.event.get():
    #         if event.type == pygame.QUIT:
    #             # throw: Exception("interupt program")
    #             return False
    #         if event.type == pygame.KEYUP:
    #             if event.key == pygame.K_ESCAPE:
    #                 # throw: Exception("interupt program")
    #                 return False
    #     return True
    
    def display(self, step = 0,time_ = 0, second = 1):
        # pygame.init()
        self.render_font(step,time_)
        self.draw_board()
        pygame.display.flip()  # Refresh display
        # if second != 0:
        #     time.sleep(second)
        # run = True
        # while run:
        #     for event in pygame.event.get():
        #         if event.type == pygame.QUIT:
        #         # throw: Exception("interupt program")
        #             run = False
        #         elif event.type == pygame.KEYUP:
        #             if event.key == pygame.K_ESCAPE:
        #                 # throw: Exception("interupt program")
        #                 run = False
        #         else:
        time.sleep(second)
        # else:
            # while self.interupt():
            #     time.sleep(1)
            # pygame.quit()
            # pygame.display.quit()

if __name__ == "__main__":
    board = np.zeros((6,6))
    
    board[0][1] = ACTIVE_P1
    board[5][2] = ACTIVE_P2
    board[3][3] = BLOCK
    board[4][2] = BLOCK
    board[3][1] = BLOCK
    
    a = Gui(board)
    a.display()