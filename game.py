import numpy as np
import sys
from gym.envs.toy_text import discrete

X = 1 # starts all games
O = 3 
TIE = -1

Players={
    1: "X",
    3: "O",
    -1: "T",
}

class Board:
    def __init__(self, board=None):
        if type(board) is int:
            self.board = board
        elif type(board) is Board:
            self.board = board.board
        else:
            self.board = 0

    def isEmpty(self):
        return (self.board == 0)

    def getPiece(self, square):
        board = self.board
        return ((board >> (square << 1)) & 3)

    def toArray(self):
        board = self.board
        a = []
        for i in range(9):
            board >>= 2
            a[i] = (board & 3)
        return a

    def toString(self):
        board = self.board
        s = ''
        for i in range(9):
            if i > 0 and (i % 3) == 0:
                s += '/'
            s += '-' if (board & 3) == 0 else ('X' if (board & 3)
                                               == X else 'O')
            board >>= 2
        return s

    def toNice(self):
        board = self.board
        s = ''
        for i in range(9):
            if i > 0 and (i % 3) == 0:
                s += '\n'
            s += '-' if (board & 3) == 0 else ('X' if (board & 3)
                                               == X else 'O')
            board >>= 2
        return s

    def emptySquares(self):
        board = self.board
        empty = []
        for i in range(9):
            if (board & 3) == 0:
                empty.append(i)
            board >>= 2
        return empty

    def move(self, square, piece):
        board = self.board
        return Board(board | (piece << (square << 1)))

    def winner(self, extra=None):
        board = self.board
        # extra gets its line property set if a player has won.  It's used to
        # draw an appropriate line indicating the win.
        extra = extra or {}

        if (board & 0o000077) == 0o000025:
            extra['line'] = 0
            return X
        if (board & 0o000077) == 0o000077:
            extra['line'] = 0
            return O
        if (board & 0o007700) == 0o002500:
            extra['line'] = 1
            return X
        if (board & 0o007700) == 0o007700:
            extra['line'] = 1
            return O
        if (board & 0o770000) == 0o250000:
            extra['line'] = 2
            return X
        if (board & 0o770000) == 0o770000:
            extra['line'] = 2
            return O
        if (board & 0o030303) == 0o010101:
            extra['line'] = 3
            return X
        if (board & 0o030303) == 0o030303:
            extra['line'] = 3
            return O
        if (board & 0o141414) == 0o040404:
            extra['line'] = 4
            return X
        if (board & 0o141414) == 0o141414:
            extra['line'] = 4
            return O
        if (board & 0o606060) == 0o202020:
            extra['line'] = 5
            return X
        if (board & 0o606060) == 0o606060:
            extra['line'] = 5
            return O
        if (board & 0o601403) == 0o200401:
            extra['line'] = 6
            return X
        if (board & 0o601403) == 0o601403:
            extra['line'] = 6
            return O
        if (board & 0o031460) == 0o010420:
            extra['line'] = 7
            return X
        if (board & 0o031460) == 0o031460:
            extra['line'] = 7
            return O
        if (board & 0o252525) == 0o252525:
            return TIE
        return 0


class Game:
    def __init__(self, board=None, turn=None, history=None, movesHistory=None):
        if type(board) is int:
            self.board = Board(board)
        elif type(board) is Board:
            self.board = board
        else:
            self.board = Board()

        self.turn = turn or (O if (len(self.board.emptySquares()) % 2 == 0) else X)
        self.history = history or []
        self.movesHistory = movesHistory or []

    def clone(self):
        return Game(self.board, self.turn, self.history.copy(), self.movesHistory.copy())

    def equals(self, other):
        # Ignore history.
        return (self.board == other.board and self.turn == other.turn)

    def getPiece(self, square):
        return self.board.getPiece(square)

    def toString(self):
        return "" + ("X" if self.turn == X else "O") + "@" + self.board.toString()

    def emptySquares(self):
        return self.board.emptySquares()

    def isEmpty(self):
        return self.board.isEmpty()

    def move(self, square):
        self.history.append(self.board.board)
        self.movesHistory.append(square)
        self.board = self.board.move(square, self.turn)
        self.turn ^= 2

    def undo(self):
        self.board = self.history.pop()
        self.turn ^= 2

    def winner(self):
        return self.board.winner()

    def play(self, x, o):
        players = {}
        players[X] = x
        players[O] = o

        winner = None

        while True:
            move = players[self.turn].getMove(self)
            if move < 0 or move >= 9 or self.getPiece(move) != 0 :
                text ="AI chose invalid move " + str(move)+ " in " + self.toString()
                raise Exception(text)

            self.move(move)
            winner = self.winner()
            if winner:
                return Players[winner]

class TicTacToeEnv(gym.Env):
    def __init__(self):
        self.action_space = spaces.Discrete(1)
        self.observation_space = spaces.Discrete(1)
        return
    
    def seed(self, seed=None):
        self.np_random, seed = seeding.np_random(seed)
        return [seed]

    def step(self, action):
        assert self.action_space.contains(action)
        return self._get_obs(), reward, done, {}

    def render(self, mode='human'):
        return

    def _get_obs(self):
        return (sum_hand(self.player), self.dealer[0], usable_ace(self.player))

    def reset(self):
        self.game = Game()
        self.oponent = SmartAgent()
        return self._get_obs()




class TicTacToeEnv(discrete.DiscreteEnv):
    """
    TODO
    """
    metadata = {'render.modes': ['human', 'ansi']}

    def __init__(self):
        self.shape = (3, 3)
        nS = np.prod(self.shape)
        nA = nS

        # Calculate transition probabilities and rewards
        P = {}
        for s in range(nS):
            position = np.unravel_index(s, self.shape)
            P[s] = {a: [] for a in range(nA)}
            P[s][UP] = self._calculate_transition_prob(position, [-1, 0])
            P[s][RIGHT] = self._calculate_transition_prob(position, [0, 1])
            P[s][DOWN] = self._calculate_transition_prob(position, [1, 0])
            P[s][LEFT] = self._calculate_transition_prob(position, [0, -1])

        # Calculate initial state distribution
        # We always start in state (3, 0)
        isd = np.zeros(nS)
        isd[self.start_state_index] = 1.0

        super(TicTacToeEnv, self).__init__(nS, nA, P, isd)

    def _limit_coordinates(self, coord):
        """
        Prevent the agent from falling out of the grid world
        :param coord: 
        :return: 
        """
        coord[0] = min(coord[0], self.shape[0] - 1)
        coord[0] = max(coord[0], 0)
        coord[1] = min(coord[1], self.shape[1] - 1)
        coord[1] = max(coord[1], 0)
        return coord

    def _calculate_transition_prob(self, current, delta):
        """
        Determine the outcome for an action. Transition Prob is always 1.0. 
        :param current: Current position on the grid as (row, col) 
        :param delta: Change in position for transition
        :return: (1.0, new_state, reward, done)
        """
        new_position = np.array(current) + np.array(delta)
        new_position = self._limit_coordinates(new_position).astype(int)
        new_state = np.ravel_multi_index(tuple(new_position), self.shape)
        if self._cliff[tuple(new_position)]:
            return [(1.0, self.start_state_index, -100, False)]

        terminal_state = (self.shape[0] - 1, self.shape[1] - 1)
        is_done = tuple(new_position) == terminal_state
        return [(1.0, new_state, -1, is_done)]

    def render(self, mode='human'):
        outfile = sys.stdout

        for s in range(self.nS):
            position = np.unravel_index(s, self.shape)
            if self.s == s:
                output = " x "
            # Print terminal state
            elif position == (3, 11):
                output = " T "
            elif self._cliff[position]:
                output = " C "
            else:
                output = " o "

            if position[1] == 0:
                output = output.lstrip()
            if position[1] == self.shape[1] - 1:
                output = output.rstrip()
                output += '\n'

            outfile.write(output)
        outfile.write('\n')


