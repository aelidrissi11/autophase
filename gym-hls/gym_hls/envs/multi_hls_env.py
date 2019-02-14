import getcycle
import os
import getfeatures
import datetime
import glob
import shutil
import numpy as np
import gym
from gym.spaces import Discrete, Box
from hls_env import HLSEnv

# Init: 8 progs, 8 envs 
# Reset: reset pgm_count 
# Step: (prog++) % #prog
class HLSMultiEnv(gym.Env):
  def __init__(self, env_config):
    self.action_space = Discrete(45)
    self.observation_space= Box(0.0,1.0,shape=(56,),dtype = np.float32)

    self.num_pgms = 8 
    self.envs = []
    self.idx = np.random.randint(self.num_pgms) 

    from chstone_bm import get_chstone, get_others
    bms = get_chstone(N=self.num_pgms)
    for i, bm in enumerate(bms):
      pgm, path = bm
      env_config = {}
      env_config['pgm'] = pgm
      env_config['pgm_dir'] = path
      env_config['run_dir'] = str(i)
      self.envs.append(HLSEnv(env_config))

  def get_cycles(self):
    done = False ## TODO What to do here
    cycle = self.envs[self.idx].get_cycles()
    return cycle,done

  def get_obs(self):
    feat = self.envs[self.idx].get_obs()
    return feat

  def reset(self):
    self.idx = np.random.randint(self.num_pgms)
    obs, reward = self.envs[self.idx].reset()
    return obs

  def step(self, action):
    self.idx = (self.idx + 1)  % self.num_pgms  
    obs, reward = self.envs[self.idx].step(action)
    info = {}
    done = False ## TODO What to do here
    return obs, reward, done, info

