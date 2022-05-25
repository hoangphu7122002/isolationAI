import tensorflow as tf
from aiENV import *
from AI_module.DQN import *
import time
import numpy as np
import pickle
import matplotlib.pyplot as plt

if __name__ == '__main__':
    env = isolation_AIv0(5)
    agent = DQN_ZERO(0.95,1,8192,1048576)
    
    op1 = tf.keras.optimizers.RMSprop(learning_rate = 0.00025)
    agent.training_network.add(tf.keras.layers.Dense(2048, activation='relu', input_shape=(36,)))
    agent.training_network.add(tf.keras.layers.Dense(4096, activation='relu'))
    agent.training_network.add(tf.keras.layers.Dense(4096, activation='relu'))
    agent.training_network.add(tf.keras.layers.Dense(2048, activation='relu'))
    agent.training_network.add(tf.keras.layers.Dense(36 * 36, activation='linear'))
    agent.training_network.compile(optimizer=op1, loss=tf.keras.losses.mean_squared_error, metrics=['mse'])
    
    op2 = tf.keras.optimizers.RMSprop(learning_rate=0.00025)
    agent.target_network.add(tf.keras.layers.Dense(2048, activation='relu', input_shape=(36,)))
    agent.target_network.add(tf.keras.layers.Dense(4096, activation='relu'))
    agent.target_network.add(tf.keras.layers.Dense(4096, activation='relu'))
    agent.target_network.add(tf.keras.layers.Dense(2048, activation='relu'))
    agent.target_network.add(tf.keras.layers.Dense(36 * 36, activation='linear'))
    agent.target_network.compile(optimizer=op2, loss=tf.keras.losses.mean_squared_error, metrics=['mse'])
    
    agent.update_target_network()
    
    reward_records = list()
    loss_records = list()
    target_update = 500
    epoch_per_eps = 10
    max_steps = 36
    record = 0
    count = 0
    
    print("=====START GAME=====")
    total_time = 0
    for ep in range(3001):
        print(ep)
        start = time.time()
        
        player = np.random.choice([-1,1], 1)[0]
        state = env.reset(player,3)
        done = False
        
        state_lst,reward_lst,action_lst,done = env.play(max_steps,player)
        # print(action_lst)
        agent.observe_on_training(state_lst, reward_lst, action_lst, done)
        
        hist = [agent.train_network(64 ,64,1,verbose=0, cer_mode=True) for _ in range(epoch_per_eps)]
        if hist is not None:
            loss_records += hist
            reward_records.append(reward_lst[-1])
        
        if ep%target_update == 0: 
            agent.update_target_network()
    
        
        total_time += time.time() - start
        if ep%100 == 0:
            with open('cp/cp_' + str(ep) + '.pkl', 'wb') as f:
                pickle.dump(agent.training_network.get_weights(), f, pickle.HIGHEST_PROTOCOL)
        if ep%100 == 0:
            print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")
            print("Total time after", ep, "episodes:", total_time)
            total_time = 0
        ### save performance plotings
        if ep%100 == 0:
            plt.plot(range(len(reward_records)),  reward_records)
            plt.title('Checkpoint: ' + str(ep))
            plt.xlabel('Training steps')
            plt.ylabel('Reward')
            plt.savefig('performance/reward/image/reward_' + str(ep) + '.png')
            plt.close()
        
            loss = [(sum(loss)/len(loss)) for loss in loss_records if loss != None]
            plt.plot(range(len(loss)),  loss)
            plt.title('Checkpoint: ' + str(ep))
            plt.xlabel('Training steps')
            plt.ylabel('MSE')
            plt.savefig('performance/mse/image/mse_' + str(ep) + '.png')
            plt.close()
        
            pickle.dump(loss_records, open('performance/mse/pickle/mse_'+str(ep)+'.pkl', 'wb'))
            pickle.dump(reward_records, open('performance/reward/pickle/reward_'+str(ep)+'.pkl', 'wb'))