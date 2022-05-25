from re import I
from time import time
import numpy as np
import random
from parameter import *
import copy
from interface_game.Minmax_class import *
import random

class MinimaxIsolation(Minimax):
    def __init__(self,depth,board = None):
        self.MINIMAX_DEPTH = depth
        if board != None:
            self.board = board
        else:
            self.board = np.zeros((WIDTH,WIDTH))
        self.pos_agent = [(0,0),(0,0),(0,0)]
        self.pos_agent[1] = (0,3)
        self.pos_agent[-1] = (5,2)
        self.board[0][3] = ACTIVE_P1
        self.board[5][2] = ACTIVE_P2
    
    def get_all_nearby_cell(self,x,y):
        cells = []
        for i in range(len(dx)):
            x_nei = x + dx[i]
            y_nei = y + dy[i]
            if self.in_board(x_nei,y_nei):
                cells.append((x_nei,y_nei))
        return cells            
        
    def print_board(self,board):
        head_col = "      "
        for ele in range(0,len(board)):
            head_col += str(ele)
            head_col += '  '
        line = "    "
        line += "-" * 19
        line += '\n'
        head_col += '\n'
        head_col += line
        row = [""] * len(board)
        index = 0
        for i in range(len(board)):
            row[i] += str(i)
            row[i] += '   |'
            for ele in board[index]:
                if ele == 1:
                    row[i] += 'P1|'
                elif ele == -1:
                    row[i] += 'P2|'
                elif ele == 0:
                    row[i] += '  |'
                else:
                    row[i] += 'XX|'
            row[i] += '\n'
            index += 1
        for ele in row:
            head_col += ele
        line = "    "
        line += "-" * 19
        line += '\n'
        head_col += line
        print(head_col)
    
    def get_all_empty_cell(self,board,x,y):
        cells = self.get_all_nearby_cell(x,y)
        emp_cells = [c for c in cells if board[c[0]][c[1]] == FREE]
        
        return emp_cells
        
    def move(self,board,player): 
        # print("player: ",player)
        maximizer = int(player == 1)
        result = self.minimax(board,player,maximizer,alpha=float('-inf'),beta=float('inf'),depth=self.MINIMAX_DEPTH)
        if result[1] is None:
            temp_move = self.get_pos(board,player)
            return self.get_pos(board,player),self.get_pos(board,player)
        
        return result[1]
    
    def aimove(self,board,player):
        move = self.move(board,player)
        # if move is (None,None):
        #     return None,None
        self.move_piece(self.board,player,move[0],move[1])
        return move[0],move[1]
    
    def evaluate_board(self,board,agent_flag):
        # x,y = self.pos_agent[-agent_flag]
        x,y = self.get_pos(board,-agent_flag)
        emp_cells = self.get_all_empty_cell(board,x,y)
        
        return (8 - len(emp_cells)) * agent_flag
    
    def check_win(self,board,current_turn):
        return self.evaluate_board(board,current_turn),self.checkEnd(board,current_turn)
        
    def in_board(self,x,y):
        if x < 0 or x >= WIDTH:
            return False
        if y < 0 or y >= WIDTH:
            return False
        return True

    def checkEnd(self,board,agent_flag):
        x,y = self.get_pos(board,-agent_flag)
        # x,y = self.pos_agent[-agent_flag]         
        emp_cells = self.get_all_empty_cell(board,x,y)
        if len(emp_cells) == 0:
            #lose
            return True
        return False
            
    def clone_board(self,board):
        return copy.deepcopy(board)
            
    def minimax(self,board,player,maximizer,alpha,beta,depth):
        if depth == 0:
            value = self.evaluate_board(board,player)
            return (value,None,depth)
        # self.print_board(board)
        component_pieces = self.get_player_piece(board,-1 * player)
        player_pieces = self.get_player_piece(board,player)
        #winner
        # print('component_pieces: ',component_pieces,len(component_pieces))
        if len(component_pieces) == 0:
            value = float('inf')
            return (value,None,depth)
        # print('player_pieces: ',player_pieces,len(player_pieces))
        if len(player_pieces) == 0:
            # print("here")
            value = float('-inf')
            return (value,None,depth)
        #maximizer <-> 1 -> player(1); 0 -> player(1); 
        # print("maximizer: ",maximizer)
        if maximizer == 1:
            best_value = float('-inf')
            best_move = None
            best_depth = float('-inf')
            # save_now_cell = None
            for cell in player_pieces:
                new_board = self.clone_board(board)
                # save_now_cell = self.pos_agent[player]
                cur = self.get_pos(new_board,player)
                self.move_piece(new_board,player,cur,cell)
                result = self.minimax(new_board,-player,0,alpha,beta,depth - 1)
                
                if best_value < result[0] or (best_value == result[0] and result[2] > best_depth):
                    best_value = result[0]
                    best_move = (cur,cell)
                    best_depth = result[2]
                
                if result[0] >= beta:
                    # self.pos_agent[player] = save_now_cell
                    return (result[0],(cur,cell),best_depth)
                
                if alpha < result[0]:
                    alpha = result[0]
            # self.pos_agent[player] = save_now_cell
            return (best_value,best_move,best_depth)
        else:
            best_value = float('inf')
            best_move = None
            best_depth = float('-inf')
            # save_now_cell = None
            for cell in player_pieces:
                new_board = self.clone_board(board)
                # save_now_cell = self.pos_agent[player]
                cur = self.get_pos(new_board, player)
                self.move_piece(new_board,player,cur,cell)
                result = self.minimax(new_board,-player,1,alpha,beta,depth - 1)
                
                if best_value > result[0] or (best_value == result[0] and result[2] > best_depth):
                    best_value = result[0]
                    best_move = (cur,cell)
                    best_depth = result[2]
                
                if alpha >= result[0]:
                    # self.pos_agent[player] = save_now_cell
                    return (result[0],(cur,cell),best_depth)
                if beta > result[0]:
                    beta = result[0]
                    
            # self.pos_agent[player] = save_now_cell
            return (best_value,best_move,best_depth)
    
    def get_player_piece(self,board,agent_flag):
        # x,y = self.pos_agent[agent_flag]
        x,y = self.get_pos(board,agent_flag)
        return self.get_all_empty_cell(board,x,y)
    
    def strategy1_check_point(self,board,component_flag,cell):
        x,y = self.get_pos(board,component_flag)
        #left condition
        x_cell,y_cell = cell
        point = 0
        if x_cell == 0 or y_cell == 0:
            point = point - 2
        if x_cell == WIDTH - 1 or y_cell == WIDTH - 1:
            point = point - 2
        #left condition
        board[x_cell][y_cell] = BLOCK
        for label in DIRECTION_LABEL:
            direction_lst = DIRECTION[label]
            for direct in direction_lst:
                x_nei = x + direct[0]
                y_nei = y + direct[1]
                if self.in_board(x_nei,y_nei) and board[x_nei][y_nei] != FREE:
                    point += 1
        
        board[x_cell][y_cell] = FREE
        return point
    
    def strategy1_block_move(self,board,component_flag,component_cell):
        if len(component_cell) == 8:
            # print(component_cell)
            return random.choice(component_cell)
        elif len(component_cell) == 1:
            return component_cell[0]
        else:
            # x,y = self.pos_agent[component_flag]
            max_point = -1000
            save_cell = None
            for cell in component_cell:
                if self.strategy1_check_point(board,component_flag,cell) > max_point:
                    max_point = self.strategy1_check_point(board,component_flag,cell)
                    save_cell = cell
            return save_cell
                    
    def player_move(self,board,player):
        valid_move = False
        
        while not valid_move:
            if player == 1:
                name = 'P1'
            else:
                name = 'P2'
            print("your turn {} with value:".format(name))
            x_now,y_now = self.get_pos(board,player)
            print("now:",x_now,y_now)
            x_new,y_new = input('pos: ').split(' ')
            x_new = int(x_new)
            y_new = int(y_new)
            if self.in_board(x_new,y_new) == False or board[x_new][y_new] != FREE:
                print('ERROR because block not free')
                continue
            print("new: ",x_new,y_new)
            available_move = self.get_all_empty_cell(board,x_now,y_now)
            print(available_move)
            if (x_new,y_new) in available_move:
                valid_move = True
                print('valid_move!!!')
                #self.move_piece(board,player,(x_now,y_now),(x_new,y_new))
                board[x_new][y_new] = ACTIVE[player]
                board[x_now][y_now] = FREE
                # self.pos_agent[player] = (x_new,y_new)
                
                #componet BLOCK
                print("remove block for component")
                x_comp,y_comp = self.get_pos(board,-player)
                print("comp:",x_comp,y_comp)
                comp_flag = True
                while comp_flag:
                    x_comp,y_comp = input('block_comp: ').split(' ')
                    x_comp = int(x_comp)
                    y_comp = int(y_comp)
                    # y_comp = int(input('y_comp: '))
                    if self.in_board(x_comp,y_comp) == False or board[x_comp][y_comp] != FREE:
                        print("try again")
                        continue
                    else:
                        board[x_comp][y_comp] = BLOCK
                        comp_flag = False
                self.board = board
            else:
                print('try_again')
        
    # def strategy2_block_move(self,component_flag,component_cell):
    #     pass
        
    def get_pos(self,board,flag):
        for i in range(WIDTH):
            for j in range(WIDTH):
                if board[i][j] == flag:
                    return (i,j)
        return None
        
    def move_piece(self,board,player_flag,old_cell,new_cell):
        if old_cell == new_cell:
            return
        # print(old_cell,new_cell)
        # print("player:",player_flag)
        # print("cell pos: ",old_cell,new_cell)
        component_flag = -player_flag
        # print("old_cell: ",old_cell)
        # print("new_cell: ",new_cell)
        assert(board[old_cell[0]][old_cell[1]] == player_flag and board[new_cell[0]][new_cell[1]] == FREE)
                
        board[new_cell[0]][new_cell[1]] = player_flag
        board[old_cell[0]][old_cell[1]] = FREE
        
        # self.pos_agent[player_flag] = new_cell
        #strategy for remove block around component
        component_cell = self.get_player_piece(board,component_flag)
        if component_cell == []:
            return None

        component_cell_strategy1 = self.strategy1_block_move(board,component_flag,component_cell)
        board[component_cell_strategy1[0]][component_cell_strategy1[1]] = BLOCK 
        # self.print_board(board)