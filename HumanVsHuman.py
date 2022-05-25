from isolationEnv import *

if __name__ == '__main__':
    #initialize
    env = iHumanVSHuman()
    max_step = 17
    
    done = False
    print("==========ISOLATION========")
    env.print_board()
    
    for i in range(max_step * 2 + 1):
        state, reward, done = env.step()  
        if done:
            break
        env.print_board()
        print("REWARD",reward)
    if reward > 0:
        print("player1 WON!!!")
    elif reward < 0:
        print("player2 WON!!!") 
    else:
        print("TIE")
    print(reward)
    
    print("OUT_GAME")
        
    