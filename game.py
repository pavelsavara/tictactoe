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
