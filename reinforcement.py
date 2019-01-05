import sys
sys.path.append('d:/Dev/FOSS/spinningup/')
sys.path.append('/foss/spinningup/')
import spinup
import tttenv
import spinup.algos.vpg as vpg
import numpy as np
from game import Game, Board
import gym

vpg.vpg.vpg(lambda:tttenv.TicTacToeEnv(), steps_per_epoch=500, epochs=2)
