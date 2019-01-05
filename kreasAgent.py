import random
import numpy
from game import Game
from agents import SmartAgent, RandomAgent
from tensorflow.python.client import device_lib

def get_available_gpus():
    local_device_protos = device_lib.list_local_devices()
    return [x.name for x in local_device_protos] # if x.device_type == 'GPU'

def bitfield(n):
    b="{0:018b}".format(n)
    return [1 if digit == '1' else 0 for digit in b]


empty = [0, 0, 0,
         0, 0, 0,
         0, 0, 0]

def bitindex(n):
    res=empty.copy()
    res[n]=1
    return res

def extractMove(game, step):
    board = game.history[step]
    square = game.movesHistory[step]
    final = game.board.board
    
    category = bitindex(square)
    features = bitfield(board)
    return (features, category, step, board, final, square) # 

def extractBoard(board):
    features = bitfield(board)
    return features 


class KerasModel:
    def __init__(self):
        return

    def build(self):
        import tensorflow as tf
        from tensorflow.python.keras import layers
        print(tf.VERSION)
        print(tf.keras.__version__)
        print(get_available_gpus())

        model = tf.keras.Sequential()
        model.add(layers.Dense(64, activation='relu'))
        model.add(layers.Dense(64, activation='relu'))
        model.add(layers.Dense(9, activation='softmax'))

        model.compile(optimizer=tf.train.AdamOptimizer(0.01),
                      loss='mse',       # mean squared error
                      metrics=['mae'])  # mean absolute error
        self.model = model

    def samples(self, dataSize=100):
        batch = []
        for i in range(dataSize):
            if i%100 == 0 : print ('game'+str(i))
            game = Game()
            x = SmartAgent() if random.randint(0, 10) % 2 == 0 else RandomAgent()
            y = SmartAgent() if random.randint(0, 10) % 2 == 0 else RandomAgent()
            winner = game.play(x, y)
            if (winner == 'X'):
                for j in range(0, len(game.history), 2):
                    batch.append(extractMove(game, j))
            else: # this is y winner moves or y tie moves
                for j in range(1, len(game.history), 2):
                    batch.append(extractMove(game, j))

            if len(game.history) == 9:
                batch.append(extractMove(game, 8))

        features = numpy.asarray([row[0] for row in batch]).astype(float)
        labels = numpy.asarray([row[1] for row in batch]).astype(float)
        meta = numpy.asarray([(row[2],row[3],row[4],row[5]) for row in batch])
        print ('game'+str(dataSize))

        return (features, labels, meta)
    
    def train(self, batchSize=32, dataSize=3200, epochs=10):
        trainingSamples  = self.samples(dataSize)
        validationSamples  = self.samples(int(dataSize/5))
        valSamples2 = (validationSamples[0],validationSamples[1])
        print(trainingSamples[0][0])
        print(trainingSamples[1][0])
        self.model.fit(trainingSamples[0], trainingSamples[1], epochs=10, batch_size=batchSize, validation_data=valSamples2)

    def predict(self, board):
        batch = []
        batch.append(extractBoard(board))
        features = numpy.asarray(batch).astype(float)
        label = self.model.predict_classes(features)
        return label

    def save(self):
        self.model.save_weights('./model/tictactoe.tfmodel')

    def load(self):
        self.model.load_weights('./model/tictactoe.tfmodel')

class KerasAgent:
    def __init__(self, model):
        self.model=model

    def getMoves(self, game):
        return game.emptySquares()

    def getMove(self, game):
        # moves = self.getMoves(game)
        square = int(self.model.predict(game.board.board)[0])
        #print(square)
        return square

