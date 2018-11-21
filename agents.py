import math
import random
from collections import namedtuple
from game import X
from game import O
from game import TIE


def arrayRand(a):
    idx = math.floor(random.random() * len(a))
    return a[idx]


TopScoringRes = namedtuple('TopScoringRes', ['score', 'moves'])

def topScoring(moves, evaluator):
    max = -math.inf
    top = []

    for move in moves:
        value = evaluator(move)
        if (value > max):
            max = value
            top = [move]
        elif (value == max):
            top.append(move)

    return TopScoringRes(
        score= max,
        moves= top
    )


def sign(piece):
    return 0 if piece == 0 else (1 if piece == X else -1)


def sumsign(a, b, c):
    return sign(a) + sign(b) + sign(c)


class RandomAgent:
    def getMoves(self, game):
        return game.emptySquares()

    def getMove(self, game):
        moves = self.getMoves(game)
        return arrayRand(moves)


class SmartAgent:
    def __init__(self, maxDepth=None):
        self.maxDepth = maxDepth or 7

    def getMove(self, game):
        return arrayRand(self.getMoves(game))

    def getMoves(self, game):
        if (game.isEmpty()):
            return [4]

        if (len(game.emptySquares()) == 8):
            return self.getSecondMoves(game.board)

        return self.negamax(game.board, game.turn, 0)

    # A small lookup table for the second move, so we don't have to go through
    # the whole algorithm just to pick the corners or the middle.

    def getSecondMoves(self, board):
        if (board.getPiece(4)):
            return [0, 2, 6, 8]

        return [4]

    # Basic negamax implementation, with a few modifications (see
    # <http:#en.wikipedia.org/wiki/Negamax> or
    # <http:#www.hamedahmadi.com/gametree/>).  We don't use alpha-beta
    # pruning because we don't just want to find the first valid move with the
    # best score, we want to find all valid moves with the same (and best)
    # score, so we can choose among them.  We pick from the best scoring moves
    # with a simple heuristic (see resolveTies()).  Because we also use this
    # to instruct us as to which move to make, if we're at the top level we
    # return the list of best moves instead of their score.

    def negamax(self, board, turn, depth):
        winner = board.winner()
        if (depth == self.maxDepth or winner):
            return sign(turn) * self.evaluate(board, winner)

        def la(move): return 0 - self.negamax(board.move(move, turn),
                                              (O if turn == X else X), depth + 1)
        topScore = topScoring(board.emptySquares(), la)

        return (topScore.score if depth else self.resolveTies(board, topScore.moves, turn))

    # We give a winning position a high score, then count the number of ways a
    # player could win at the current position.
    def evaluate(self, board, winner):
        winner = board.winner() if (winner is None) else winner

        if (winner is not None):
            return sign(0 if winner == TIE else winner) * 100

        return self.countNearWins(board) * 10 + self.countPotentialWins(board)

    # The moves are all equal as far as negamax is concerned, so we've got to
    # choose the best one to play now.  If any moves are are an immediate win,
    # we return them.  Otherwise, we choose moves blocking an opponent's win,
    # then we just pick the square with the highest evaluation.

    def resolveTies(self, board, moves, turn):
        if (len(moves) > 1):
            la = lambda move: 1 if (board.move(move, turn).winner() == turn) else 0
            moves = topScoring(moves, la).moves
            if (len(moves) > 0):
                return moves

        la = lambda move: 1 if self.blocksOpponent(board, move, turn) else 0
        if (len(moves) > 1):
            moves = topScoring(moves, la).moves
        
        # TODO self.evaluate(
        la = lambda move: sign(turn) * board.move(move, turn)
        if (len(moves) > 1):
            moves = topScoring(moves, la).moves

        return moves

    def blocksOpponent(self, board, move, turn):
        opponent = O if turn == X else X
        a = self.countNearWinsForPlayer(board.move(move, turn), opponent)
        b = self.countNearWinsForPlayer(board, opponent)
        return a < b

    def countScoringMoves(self, board, scorer):
        pieces = board.toArray()
        scoringMoves = 0

        for i in range(3):
            scoringMoves += scorer(
                pieces[i * 3 + 0],
                pieces[i * 3 + 1],
                pieces[i * 3 + 2]
            )
            scoringMoves += scorer(
                pieces[i + 0],
                pieces[i + 3],
                pieces[i + 6]
            )

        scoringMoves += scorer(pieces[0], pieces[4], pieces[8])
        scoringMoves += scorer(pieces[2], pieces[4], pieces[6])

        return scoringMoves

    def countNearWins(self, board):
        la = lambda a, b, c: 1 if sumsign(a, b, c) > 0 else (-1 if math.fabs(sumsign(a, b, c)) == 2 else 0)
        return self.countScoringMoves(board, la)

    def countNearWinsForPlayer(self, board, player):
        la = lambda a, b, c: 1 if (math.fabs(sumsign(a, b, c)) == 2 and sumsign(a, b, c) / 2 == sign(player)) else 0
        return self.countScoringMoves(board, la)

    def countPotentialWins(self, board):
        la = lambda a, b, c: sumsign(a, b, c) if (math.fabs(sumsign(a, b, c)) == 1 and not (a and b and c)) else 0
        return self.countScoringMoves(board, la)
