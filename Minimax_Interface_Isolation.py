from interface_game.Minmax_class import *
from Minimax_Isolation import *
import random

class MinimaxII(MinimaxInterface):
    def __init__(self,depth,path = {}):
        self.env = MinimaxIsolation(depth,None)
        self.path = path
        self.depth = depth
        self.board = self.env.board
        
    def get_act_space(self,board,player):
        # print(board)
        player_pos = self.env.get_pos(board,player)
        new_space = self.env.get_all_empty_cell(board,player_pos[0],player_pos[1])
         
        # print(new_space)
        action_space = [(player_pos[0]*6 + player_pos[1])*36 + cell[0]*6 + cell[1] for cell in new_space]
        return action_space
        
    def sample_act(self,board,player):
        action_space = self.get_act_space(board,player)
        action = random.choice(action_space)
        
        old, new = action//36, action%36
        old, new = (old//6, old%6), (new//6, new%6)
        self.env.move_piece(board,player,old,new)
        # self.board = board
        board = self.env.board.copy()
        self.board = board
        return action
    
    def act(self,board,action,player):
        # old,new = action
        old, new = action//36, action%36
        old, new = (old//6, old%6), (new//6, new%6) 
        self.env.move_piece(board,player,old,new)
        board = self.env.board.copy()
        self.board = board
        
    def minimax_act(self,board,player):
        if self.depth == 0:
            return self.sample_act(board,player)
        # print("Board-pre: ",board)
        old,new = self.env.aimove(board,player)
        # print("===============")
        # print(old,new)
        # print("===============")
        action = (old[0]*6+old[1])*36 + new[0]*6+new[1]
        board = self.env.board.copy()
        self.board = board
        # print("Board-after: ",board)
        return action
    
    def check_win(self,board,player):
        return self.env.evaluate_board(board,player),self.env.checkEnd(board,player)
    
    def player_act(self,board,player):
        self.env.player_move(board,player)
        board = self.env.board
        self.board = board
    
    def getBoard(self,board):
        # print(board)
        return [i for lst in board for i in lst]
        
    def move_piece(self,board,player,old,new):
        self.env.move_piece(board,player,old,new)
        board = self.env.board
        self.board = board