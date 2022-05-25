from AI_module.EpsilonGreedy import EpsilonGreedy,EpsilonZero
from Minimax_Interface_Isolation import *
from Minimax_Isolation import *
import numpy as np
import random
from parameter import *

def print_board(board):
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

class isolation_AIv0:
    def __init__(self,path={}):
        self.env = MinimaxII(4)
        self.epsilon = EpsilonZero(0)
        self.depth = 4
        self.depth2 = 0
        
        self.board = None
        self.current_turn = 1
        self.player_mark = 1
        
        self.path = path
        
    def reset(self,player,depth=4,depth2=0):
        self.env = MinimaxII(depth,self.path)
        self.board = self.env.board
        self.current_turn = player
        self.depth = depth
        self.depth2 = depth2
        
        return copy.deepcopy(self.board)
        
    def env_act(self):
        old,new = self.env.minimax_act(self.env.board,self.current_turn)
        self.board = self.env.board
        reward,done = self.check_win()
        self.current_turn = -1 * self.current_turn
        return reward,done

    def check_win(self):
        point,flag = self.env.check_win(self.board,self.current_turn)
        return point,flag
    
    def get_act_space(self,board,player):
        return self.env.get_act_space(board,player)
        
    def sample_act(self,board,player):
        action_space = self.get_act_space(board,player)
        cell = random.choice(action_space)
        
        old,new = cell
        self.env.move_piece(board,player,old,new)
        # self.board = board
        board = self.env.getBoard().copy()
        return old,new
    
    def play(self,max_steps,player):
        done = False
        reward = 0
        random_factor = np.random.choice([-1,1], 1)[0]
        state_lst, reward_lst, action_lst = [], [], []
        
        for z in range(max_steps * 2):
            # print("================================")
            # print(z)
            # print("================================")
            env_1 = MinimaxII(self.depth,self.path)
            env_2 = MinimaxII(self.depth2,self.path)
            
            state_lst += [self.env.getBoard(self.board.copy())]
            if player == 1:
                #fix erorr here
                reward_lst += [reward]                
            else:
                reward_lst += [-reward]
            
            self.board = self.env.board
            
            ret = random_factor==player
            if ret:
                action = env_1.minimax_act(self.board,player)
            else:
                action = env_2.minimax_act(self.board,player)
            
            reward,done = self.check_win()
            
            action_lst += [action] 
            player = -player
            if done:
                break
            # print(self.board)
        return state_lst,reward_lst, action_lst,done
        
class isolationAIvsRandom:
    def __init__(self,save_move={}):
        self.board = None
        self.env = MinimaxII(4,None)
        self.current_turn = 1
        self.player_mark = 1
        self.save_move = save_move
    
    def reset(self, player, depth=4):
        self.env = MinimaxII(depth,None)
        self.board = self.env.board
        self.current_turn = player
        # self.player_mark = 

        return self.board.copy()
    
    def check_win(self):
        point,flag = self.env.check_win(self.board,self.current_turn)
        return point,flag
    
    def env_act(self):
        action_space = self.get_act_space()
        random_idx = random.randint(0, len(action_space)-1)
        action = action_space[random_idx]
        old, new = action//36, action%36
        old, new = (old//6, old%6), (new//6, new%6)
        
        self.board[old[0]][old[1]] = FREE
        self.board[new[0]][new[1]] = self.current_turn
        
        new_comp = []
        for i in range(len(self.board)):
            for j in range(len(self.board)):
                if self.board[i][j] == FREE:
                    new_comp.append((i,j))
        new_comp_rand = random.choice(new_comp)
        self.board[new_comp_rand[0]][new_comp_rand[1]] = BLOCK
        
        self.env.board = self.board.copy()
        
        reward, done = self.check_win()
        self.current_turn = self.current_turn * -1
        
        return reward, done
        
    def step(self, action):
        old, new = action//36, action%36
        old, new = (old//6, old%6), (new//6, new%6)
        # if not self.is_valid(action):
        #     raise Exception('Invalid action')

        self.env.move_piece(self.board,self.current_turn, old, new)
        self.board = self.env.board
        
        reward, done = self.check_win()
        self.current_turn = self.current_turn * -1
    
        if done:
            return self.board.copy(), reward, done
        reward, done = self.env_act()
        return self.board.copy(), reward, done
    
    def get_act_space(self):
        return self.env.get_act_space(self.board,self.current_turn)
    
class isolation_AIvsAI:
    def __init__(self, save_move = {}):
        self.board = None
        self.mnm_env = MinimaxII(4)
        # self.trap_move = None
        self.current_turn = 1
        self.player_mark = 1
        self.save_move = save_move

    def reset(self, player, depth=4):
        self.mnm_env = MinimaxII(depth, None)
        self.board = self.mnm_env.board
        
        self.current_turn = player
        
        return self.board.copy()

    def check_win(self):
        point,flag = self.mnm_env.check_win(self.board,self.current_turn)
        return point,flag

    def step(self, action):
        old, new = action//36, action%36
        old, new = (old//6, old%6), (new//6, new%6)
        # if not self.is_valid(action):
        #     raise Exception('Invalid action')

        self.mnm_env.move_piece(self.board,self.current_turn, old, new)
        self.board = self.mnm_env.board
        
        reward, done = self.check_win()
        self.current_turn = self.current_turn * -1
    
        return self.board.copy(), reward, done

    def get_act_space(self):
        return self.mnm_env.get_act_space(self.board,self.current_turn)