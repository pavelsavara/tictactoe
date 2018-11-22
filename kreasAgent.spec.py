import unittest
from game import Game
from game import Board
from agents import RandomAgent, SmartAgent
from kreasAgent import KerasAgent, KerasModel


class TestStringMethods(unittest.TestCase):

    def test_keras(self):
        km = KerasModel()
        samples = km.samples(10)
        for row in samples:
            print(row)
            # bo = Board(row[3])
            # fi = Board(row[4])
            # print(bo.toNice())
            # print(fi.toNice())

if __name__ == '__main__':
    unittest.main()
