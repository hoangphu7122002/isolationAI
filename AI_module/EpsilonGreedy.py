import numpy as np
import pandas as pd

class EpsilonGreedy:
    def __init__(self,epsilon):
        self.epsilon = epsilon
    
    def perform(self,q_value,action_space):
        prob = np.random.sample()
        if prob <= self.epsilon: #take random action
            if action_space is None:
                return np.random.randint(len(q_value))
            return np.random.choice(action_space)
        else: #take greedy action
            if action_space is None:
                return np.argmax(q_value)
            return max([[q_value[a], a] for a in action_space], key=lambda x: x[0])[1]

    def decay(self,decay_value,lower_bound):
        self.epsilon = max(self.epsilon * decay_value, lower_bound)

class EpsilonZero:
    def __init__(self,epsilon):
        self.epsilon = epsilon
            
    def perform(self):
        prob = np.random.sample()
        if prob <= self.epsilon:
            return True
        else:
            return False
    
    def decay(self,decay_value, lower_bound):
        self.epsilon = max(self.epsilon * decay_value, lower_bound)
    