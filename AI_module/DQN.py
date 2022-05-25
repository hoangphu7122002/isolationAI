from AI_module.baseModel import *
from AI_module.EpsilonGreedy import *
from AI_module.ExprienceReplay import *

import tensorflow as tf
import numpy as np
import time

def construct_from_a(action):
    old,new = action // 36,action % 36
    old,new = (old // 6,old % 6),(new // 6,new % 6)
    if old[0] == new[0] and old[1] == new[1]:
        return False
    return True

class DQN_ZERO(BaseModel):
    def __init__(self,discount_factor,epsilon,e_min,e_max):
        self.gamma = discount_factor
        self.epsilon_zero = EpsilonZero(epsilon)
        self.e_min = e_min
        self.exp_replay = ExperienceReplay(e_max)
        self.training_network = tf.keras.Sequential()
        self.target_network = tf.keras.Sequential()
        self.cache = []
    
    def observe(self,state,action_space = None):
        q_value = self.training_network.predict(np.array([state])).ravel()
        if action_space is not None:
            # distinct_as = []
            # print(action_space)
            # for a in action_space:
            #     if construct_from_a(a) == True:
            #         distinct_as.append(a)
                
            return max([[q_value[a], a] for a in action_space], key=lambda x: x[0])[1]
        return np.argmax(q_value)
        
    def observe_on_training(self,states,rewards,actions,done):
        n = len(states)
        for i in range(n-2):
            s,a,r,ns,done = states[i], actions[i], rewards[i], states[i+2], False
            self.cache.extend([list(s), a, r, list(ns), done])
            self.exp_replay.add_experience(self.cache.copy())
            self.cache.clear()
        if done:
            for i in [n-2,n-1]:
                s,a,r,ns,done = states[i], actions[i], rewards[i], None, done
                self.cache.extend([list(s), a, r, list(ns), done])
                self.exp_replay.add_experience(self.cache.copy())
                self.cache.clear()
               
    def take_reward(self, reward, next_state, done):
        return super().take_reward(reward, next_state, done)
        
    def train_network(self,sample_size,batch_size,epochs,verbose = 2,cer_mode = False):
        # print(self.exp_replay.get_size())
        if self.exp_replay.get_size() >= self.e_min:
            # time.sleep(1)
            s_batch, a_batch, r_batch, ns_batch, done_batch = self.exp_replay.sample_experience(sample_size, cer_mode)
            states, q_values = self.replay(s_batch, a_batch, r_batch, ns_batch, done_batch)
            
            history = self.training_network.fit(states, q_values, epochs=epochs, batch_size=batch_size, verbose=verbose)
            return history.history['loss']
        
    def replay(self,states,actions,rewards,next_states,terminals):
        q_values = self.target_network.predict(np.array(states))
        nq_values = self.target_network.predict(np.array(next_states))
        for i in range(len(states)):
            a = actions[i]
            done = terminals[i]
            r = rewards[i]
            if done:
                q_values[i][a] = r
            else:
                q_values[i][a] = r + self.gamma * np.max(nq_values[i])
        return states, q_values
        
    def update_target_network(self):
        self.target_network.set_weights(self.training_network.get_weights())