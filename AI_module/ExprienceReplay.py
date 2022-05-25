import random
import numpy as np

class ExperienceReplay(object):
    def __init__(self,e_max):
        if e_max <= 0:
            raise ValueError('Invalid value for memory size')
        self.e_max = e_max
        self.memory = []
        self.index = 0
    
    def add_experience(self,sample):
        if len(sample) != 5:
            raise Exception('Invalid sample')
        if len(self.memory) < self.e_max:
            self.memory.append(sample)
        else:
            self.memory[self.index] = sample
        self.index = (self.index + 1) % self.e_max
    
    def sample_experience(self,sample_size,cer_mode):
        samples = random.sample(self.memory,sample_size)
        if cer_mode:
            samples[-1] = self.memory[self.index - 1]
        s_batch, a_batch, r_batch, ns_batch, done_batch = map(np.array, zip(*samples))
        return s_batch, a_batch, r_batch, ns_batch, done_batch
        
    def get_size(self):
        return len(self.memory)