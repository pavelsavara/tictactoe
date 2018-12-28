import unittest
from game import Board, Game
from agents import RandomAgent, SmartAgent


class TestStringMethods(unittest.TestCase):

    def test_board(self):
        board = Board()
        print (board.toString())
        board = Board(0x77777777)
        print (board.toString())
        # self.assertEqual('foo'.upper(), 'FOO')

    def test_play_random(self):
        x=RandomAgent()
        o=RandomAgent()
        game = Game()
        winner = game.play(x,o)
        print ('Winner '+winner)

    def test_play_smart(self):
        x=RandomAgent()
        o=SmartAgent()
        game = Game()
        winner = game.play(x,o)
        print ('Winner '+winner)
        print (game.history)
        print (game.movesHistory)

if __name__ == '__main__':
    unittest.main()
