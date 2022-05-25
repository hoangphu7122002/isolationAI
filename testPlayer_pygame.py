import numpy as np
import math
import pygame
import sys
import copy

### CONSTANT
EDGE = 100
SHAPE = (8, 6)
WIDTH = SHAPE[0] * EDGE
HEIGHT = SHAPE[1] * EDGE
### COLOR
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
YELLOW = (255, 255, 0)
BLACK = (0, 0, 0)

screen = pygame.display.set_mode((WIDTH, HEIGHT))
screen.fill(YELLOW)
board_game = np.ones((SHAPE[1], SHAPE[0])) * (-1)

INVALID = -1
EMPTY = 0
FIRE = 1
ICE = 2

POS = {'FIRE': [int((SHAPE[1] - 1) / 2),0], 
        'ICE': [int((SHAPE[1] + 1) / 2), SHAPE[0] - 1], 
        'SELECT': [0, 0]
} # [row,col]
board_game[POS['FIRE'][0]][POS['FIRE'][1]] = FIRE
board_game[POS['ICE'][0]][POS['ICE'][1]] = ICE
TURN = 0
### HELPER FUNCTION
def drawGrid():
    thickness = 2
    for r in range(0, SHAPE[1]):
        for c in range(0, SHAPE[0]):
            rect = pygame.Rect(c * EDGE, r * EDGE, EDGE, EDGE)
            if board_game[r][c] == INVALID:                
                pygame.draw.rect(screen, YELLOW, rect)
            elif board_game[r][c] == EMPTY:
                pygame.draw.rect(screen, BLACK, rect)
            pygame.draw.rect(screen, BLACK, rect, thickness)
    rect = pygame.Rect(POS['SELECT'][1] * EDGE, POS['SELECT'][0] * EDGE, EDGE, EDGE)      
    pygame.draw.rect(screen, GREEN, rect)  
    pygame.draw.circle(screen, RED, (POS['FIRE'][1] * EDGE + int(EDGE / 2), POS['FIRE'][0] * EDGE + int(EDGE / 2)), int(EDGE / 2 - thickness)) 
    pygame.draw.circle(screen, BLUE, (POS['ICE'][1] * EDGE + int(EDGE / 2), POS['ICE'][0] * EDGE + int(EDGE / 2)), int(EDGE / 2 - thickness))  
    # print(POS['SELECT'])

def getKeyboard():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key  == pygame.K_DOWN or event.key  == pygame.K_s:
                rect = pygame.Rect(POS['SELECT'][1] * EDGE, POS['SELECT'][0] * EDGE, EDGE, EDGE)   
                pygame.draw.rect(screen, YELLOW, rect)
                prev = copy.deepcopy(POS['SELECT'][0])
                POS['SELECT'][0] = min(POS['SELECT'][0] + 1, SHAPE[1] - 1)
                if (board_game[POS['SELECT'][0]][POS['SELECT'][1]] == EMPTY):
                    POS['SELECT'][0] = prev
            if event.key  == pygame.K_UP or event.key  == pygame.K_w:
                rect = pygame.Rect(POS['SELECT'][1] * EDGE, POS['SELECT'][0] * EDGE, EDGE, EDGE)   
                pygame.draw.rect(screen, YELLOW, rect)
                prev = copy.deepcopy(POS['SELECT'][0])
                POS['SELECT'][0] = max(POS['SELECT'][0] - 1, 0)
                if (board_game[POS['SELECT'][0]][POS['SELECT'][1]] == EMPTY):
                    POS['SELECT'][0] = prev
            if event.key  == pygame.K_RIGHT or event.key  == pygame.K_d:
                rect = pygame.Rect(POS['SELECT'][1] * EDGE, POS['SELECT'][0] * EDGE, EDGE, EDGE)   
                pygame.draw.rect(screen, YELLOW, rect)
                prev = copy.deepcopy(POS['SELECT'][1])
                POS['SELECT'][1] = min(POS['SELECT'][1] + 1, SHAPE[0] - 1)
                if (board_game[POS['SELECT'][0]][POS['SELECT'][1]] == EMPTY):
                    POS['SELECT'][1] = prev
            if event.key  == pygame.K_LEFT or event.key  == pygame.K_a:
                rect = pygame.Rect(POS['SELECT'][1] * EDGE, POS['SELECT'][0] * EDGE, EDGE, EDGE)   
                pygame.draw.rect(screen, YELLOW, rect)
                prev = copy.deepcopy(POS['SELECT'][1])
                POS['SELECT'][1] = max(POS['SELECT'][1] - 1, 0)
                if (board_game[POS['SELECT'][0]][POS['SELECT'][1]] == EMPTY):
                    POS['SELECT'][1] = prev
            if event.key  == pygame.K_SPACE:
                # TURN 0 (FIRE move) -> 1 (FIVE choose) -> 2 (ICE move) -> 3 (ICE choose)
                # print(1)
                rect = pygame.Rect(POS['SELECT'][1] * EDGE, POS['SELECT'][0] * EDGE, EDGE, EDGE)   
                pygame.draw.rect(screen, YELLOW, rect)
                global TURN
                valid = False
                if TURN == 0:
                    if (abs(POS['SELECT'][0] - POS['FIRE'][0]) + abs(POS['SELECT'][1] - POS['FIRE'][1]) == 1):
                        board_game[POS['FIRE'][0]][POS['FIRE'][1]] = INVALID
                        POS['FIRE'] = copy.deepcopy(POS['SELECT'])
                        board_game[POS['FIRE'][0]][POS['FIRE'][1]] = FIRE
                        ### move selected quickly
                        POS['SELECT'] = copy.deepcopy(POS['ICE'])
                        #####
                        valid = True
                elif TURN == 1 or TURN == 3:
                    if (board_game[POS['SELECT'][0]][POS['SELECT'][1]] == INVALID):
                        board_game[POS['SELECT'][0]][POS['SELECT'][1]] = EMPTY
                        ### move selected quickly
                        if TURN == 1:
                            POS['SELECT'] = copy.deepcopy(POS['ICE'])
                        elif TURN == 3:
                            POS['SELECT'] = copy.deepcopy(POS['FIRE'])
                        #####
                        valid = True
                elif TURN == 2:
                    if (abs(POS['SELECT'][0] - POS['ICE'][0]) + abs(POS['SELECT'][1] - POS['ICE'][1]) == 1):
                        board_game[POS['ICE'][0]][POS['ICE'][1]] = INVALID
                        POS['ICE'] = copy.deepcopy(POS['SELECT'])
                        board_game[POS['ICE'][0]][POS['ICE'][1]] = ICE
                        valid = True
                        ### move selected quickly
                        POS['SELECT'] = copy.deepcopy(POS['FIRE'])
                        #####
                if valid:
                    TURN = (TURN + 1) % 4
            # print(board_game)

### MAIN
def main():    
    # print(board_game)
    ### move selected quickly
    POS['SELECT'] = copy.deepcopy(POS['FIRE'])
    #####
    while True:
        drawGrid()
        getKeyboard()
        pygame.display.update()
main()