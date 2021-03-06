import numpy as np
import sys
import gym
import gym.spaces as spaces
import gym.utils.seeding as seeding
from game import Game, Board, TIE,X,O
from agents import SmartAgent, RandomAgent

class TicTacToeEnv(gym.Env):
    def __init__(self):
        self.reward_range = (-100, 1)
        self.action_space = spaces.Discrete(9)
        self.observation_space = spaces.Box(low=0, high=1, shape=(18,),dtype=np.bool)
        self.seed()
        return
    
    def seed(self, seed=None):
        self.np_random, seed = seeding.np_random(seed)
        return [seed]

    def step(self, action):
        move = int(action)
        emptySqares = self.game.emptySquares()
        nice = self.game.toNice()
        if move not in emptySqares:
            return self._get_observation(), -100.0, True, {'reason': 'badmove', 'move':move, 'nice':nice, 'winner':0 }
        self.game.move(move)
        winner = self.game.winner()

        if winner == TIE:
            return self._get_observation(), 0.01, True, {'reason': 'tie', 'move':move, 'nice':nice , "winner":1}
        
        if winner == self.game.turn:
            return self._get_observation(), -1, True, {'reason': 'loose', 'move':move, 'nice':nice , "winner":2}

        if winner:
            return self._get_observation(), 1.0, True, {'reason': 'win', 'move':move, 'nice':nice , "winner":3}

        oponentmove = self.oponent.getMove(self.game)

        self.game.move(oponentmove)
        winner = self.game.winner()

        if winner == TIE:
            return self._get_observation(), 0.01, True, {'reason': 'tie', 'move':move, 'nice':nice , "winner":1}

        if winner == self.game.turn:
            return self._get_observation(), 1.0, True, {'reason': 'win', 'move':move, 'nice':nice , "winner":3}

        if winner:
            return self._get_observation(), -0.99, True, {'reason': 'loose', 'move':move, 'nice':nice , "winner":2}

        return self._get_observation(), 0.0001, False, {'reason': 'move', 'move':move, 'nice':nice , "winner":4}

    def render(self, mode='human'):
        outfile = StringIO() if mode == 'ansi' else sys.stdout
        outfile.write(self.game.board.toNice())

        if mode != 'human':
            return outfile

    def _get_observation(self):
        b="{0:018b}".format(self.game.board.board)
        return np.array([1 if digit == '1' else 0 for digit in b])

    def reset(self):
        self.game = Game()
        self.oponent = self.np_random.choice([RandomAgent(self.np_random),SmartAgent(self.np_random)])
        #self.oponent = RandomAgent(self.np_random)
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
