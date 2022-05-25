import tensorflow as tf
from aiENV import *
from AI_module.DQN import *
import time
import numpy as np
import pickle
import matplotlib.pyplot as plt

with tf.device('/cpu:0'):
    max_step = 36
    agent = DQN_ZERO(0.9,1,8192,1048576)
    
    op1 = tf.keras.optimizers.RMSprop(learning_rate = 0.00025)
    agent.training_network.add(tf.keras.layers.Dense(2048, activation='relu', input_shape=(36,)))
    agent.training_network.add(tf.keras.layers.Dense(4096, activation='relu'))
    agent.training_network.add(tf.keras.layers.Dense(4096, activation='relu'))
    agent.training_network.add(tf.keras.layers.Dense(2048, activation='relu'))
    agent.training_network.add(tf.keras.layers.Dense(36 * 36, activation='linear'))
    agent.training_network.compile(optimizer=op1, loss=tf.keras.losses.mean_squared_error, metrics=['mse'])
    
    cpt_prefix = 'cp/cp_'
    cpt_postfix = '.pkl'
    record_results = {}
    
    # for cpt_num in range(0,1001,100):
    cpt_num = "1000"
    w = pickle.load(open(cpt_prefix + str(cpt_num) + cpt_postfix,'rb'))
    agent.training_network.set_weights(w)
    
    result_vs_random = {'won':0, 'lost':0, 'tie':0}
    env = isolationAIvsRandom()
    start = time.time()
    for ep in range(1000):
        player = np.random.choice([-1,1], 1)[0]
        done = False
        reward = 0
        state = env.reset(player)
        print("======================")
        print(ep)
        print("======================")
        for i in range(max_step):
            if player == -1:
                reward, done = env.env_act()
                state = env.board.copy()
                player = 1
            state_temp = [i for lst in state for i in lst]
            action = agent.observe(state_temp, action_space = env.get_act_space())
            # print("====")
            # print(action)
            # print("=====")
            # old,new = action//36,action%36
            # old,new = (old//6,old%6),(new//6,new%6)
            # action_temp = old,new
            state, reward, done = env.step(action)
            # print(state)
            if done: 
                break
        if reward > 0: 
            result_vs_random['won'] += 1
        elif reward < 0: 
            result_vs_random['lost'] += 1
        else: 
            result_vs_random['tie'] += 1
    print("Checkpoint:", cpt_num)
    print("Won games:", result_vs_random['won'])
    print("Tie games:", result_vs_random['tie'])
    print("Lost games:", result_vs_random['lost'])
    record_results[str(cpt_num)] = result_vs_random
    print("Total time", time.time() - start, 's.')
    # if cpt_num%1000 == 0:
    #     pickle.dump(record_results, open('performance/WRRD/zero.pkl','wb'))

    pickle.dump(record_results, open('performance/WRRD/zero.pkl','wb'))