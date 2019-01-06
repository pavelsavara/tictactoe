import sys
import os
sys.path.append('d:/Dev/FOSS/spinningup/')
sys.path.append('/foss/spinningup/')
import spinup
import tttenv
import spinup.algos.vpg as vpg
import numpy as np
from game import Game, Board
import gym

os.environ['CUDA_VISIBLE_DEVICES'] = '-1'

import spinup.utils.test_policy as test_policy



#env, get_action = test_policy.load_policy('d:/tmp/experiments/1546722277', '', False)
#test_policy.run_policy(env, get_action, 10, 10, False)

vpg.vpg.vpg(lambda:tttenv.TicTacToeEnv(), steps_per_epoch=100, epochs=5000)
