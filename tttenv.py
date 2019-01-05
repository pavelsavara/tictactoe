import numpy as np
import sys
import gym
import gym.spaces as spaces
import gym.utils.seeding as seeding
from game import Game, Board, TIE,X,O
from agents import SmartAgent, RandomAgent

class TicTacToeEnv(gym.Env):
    def __init__(self):
        self.reward_range = (-1, 1)
        self.action_space = spaces.Discrete(9)
        self.observation_space = spaces.Box(low=0, high=2, shape=(9,),dtype=np.int32)
        self.seed()
        return
    
    def seed(self, seed=None):
        self.np_random, seed = seeding.np_random(seed)
        return [seed]

    def step(self, move):
        emptySqares = self.game.emptySquares()
        if move not in emptySqares:
            self.reset()
            return self._get_observation(), -1.0, True, 
        self.game.move(move)
        winner = self.game.winner()

        if winner == TIE:
            self.reset()
            return self._get_observation(), 0.01, True, {'reason': 'tie1!'}
        
        if winner == self.game.turn:
            self.reset()
            return self._get_observation(), -0.99, True, {'reason': 'you loose1!'}

        if winner:
            self.reset()
            return self._get_observation(), 1.0, True, {'reason': 'you win1!'}

        oponentmove = self.oponent.getMove(self.game)

        self.game.move(oponentmove)
        winner = self.game.winner()

        if winner == TIE:
            self.reset()
            return self._get_observation(), 0.01, True, {'reason': 'tie2!'}

        if winner == self.game.turn:
            self.reset()
            return self._get_observation(), 1.0, True, {'reason': 'you win2!'}

        if winner:
            self.reset()
            return self._get_observation(), -0.99, True, {'reason': 'you loose2!'}

        return self._get_observation(), 0.0, False, {'reason': 'not settled'}

    def render(self, mode='human'):
        outfile = StringIO() if mode == 'ansi' else sys.stdout
        outfile.write(self.game.board.toNice())

        if mode != 'human':
            return outfile

    def _get_observation(self):
        return self.game.board.allSquares012()

    def reset(self):
        self.game = Game()
        self.oponent = self.np_random.choice([RandomAgent(self.np_random),SmartAgent(self.np_random)])
        if self.np_random.choice([0,1]) == 1 :
            oponentmove = self.oponent.getMove(self.game)
            self.game.move(oponentmove)

        return self._get_observation()


from gym.envs.registration import register
def register():
    register(
        id='tic-tac-toe-v0',
        entry_point='TicTacToeEnv',
    )
