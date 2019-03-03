import ray
import ray.tune as tune
from ray.rllib.agents import ppo
from gym_hls.envs.hls_env import HLSEnv
from gym_hls.envs.hls_multi_env import HLSMultiEnv

ray.init()
env_config = {'normalize': 1,  
    'verbose':True, 
    'bm_name':'random', 
    'num_pgms':100}

tune.run_experiments({
    "my_experiment": {
        "run": "PPO",
        "env":HLSMultiEnv,
        "checkpoint_freq": 4,
        "stop": {"episode_reward_mean": 1000000},
        "config": {
            "sample_batch_size": 100,
            "train_batch_size": 700,
            "sgd_minibatch_size": 70,
            "model": {"use_lstm": True, "max_seq_len":5, "lstm_use_prev_action_reward":True},
            "horizon": 24,
            "num_gpus": 2,
            "num_workers": 5,
            #"lr": tune.grid_search([0.01, 0.001, 0.0001]),
            "env_config": env_config,
        },
    },
})
