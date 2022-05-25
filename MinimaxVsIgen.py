from doctest import DONT_ACCEPT_BLANKLINE
from isolationEnv import *
from helper_function import *
from time import sleep
from GUI import *

if __name__ == "__main__":
    env = iGenVSMinimax(1000)
    max_step = 36
        
    for ep in range(1):
        depth1 = int(input('depth for maximizer: '))
        igen = int(input('igen go first <-> 1, otherwise -1'))
        done = False
        env.reset(depth1,igen)
        
        print("START ISOLATION")
        
        for i in range(max_step):
            state,reward,done = env.step()
            if done:
                break
            print_board(env.board)
            a = Gui(state)
            a.display()
            # sleep(2)
        if reward > 0:
            print("player1 WON!!!: ",reward)
        elif reward < 0:
            print("player2 WON!!!: ",reward)
        else:
            print("GAME TIE!!!")
        
        print("log out")