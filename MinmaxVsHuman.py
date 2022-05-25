from isolationEnv import *

if __name__ == '__main__':
    env = iMinimaxVSHuman(1000)
    max_step = 18
    
    done = False
    print("=======ISOLATION=======")
    env.print_board()
    
    print("do you want to go first?")
    
    player_turn = None
    while player_turn != 1 and player_turn != -1:
        player_turn = int(input('press 1 => to go first and -1 => to go second: '))
    state = env.reset(player_turn,1000,{})
    
    for i in range(max_step):
        
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
    
    pass