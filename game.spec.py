import unittest
from game import Game
from game import Board
from game import play
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
        winner = play(x,o)
        print ('Winner '+winner)

    def test_play_smart(self):
        x=RandomAgent()
        o=SmartAgent()
        winner = play(x,o)
        print ('Winner '+winner)

if __name__ == '__main__':
    unittest.main()
