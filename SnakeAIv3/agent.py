import random
from collections import deque

import matplotlib.pyplot as plt
import numpy as np
import torch

from game import BLOCKSIZE, Direction, Point, SnakeGameAI
from model import LinearQNet, QTrainer

MAX_MEMORY = 100000
BATCHSIZE = 1000
LEARNINGRATE = 0.001
EPSILONCEIL = 80


class Agent:
    def __init__(self):
        self.numberOfGames = 0
        #   randomness variable
        self.epsilon = 0
        #   discount rate (must be < 1)
        self.gamma = 0.9
        #   deque: popleft() if length exceeds maxlen (MAX_MEMORY)
        self.memory = deque(maxlen=MAX_MEMORY)
        self.model = LinearQNet(11, 256, 3)
        self.trainer = QTrainer(self.model, LEARNINGRATE, self.gamma)

    def getState(self, game):
        head = game.snake[0]

        ptLeft = Point(head.x - BLOCKSIZE, head.y)
        ptRight = Point(head.x + BLOCKSIZE, head.y)
        ptUp = Point(head.x, head.y - BLOCKSIZE)
        ptDown = Point(head.x, head.y + BLOCKSIZE)

        dirLeft = game.direction == Direction.LEFT
        dirRight = game.direction == Direction.RIGHT
        dirUp = game.direction == Direction.UP
        dirDown = game.direction == Direction.DOWN

        state = [
            #   Danger straight
            (dirRight and game.isCollision(ptRight))
            or (dirLeft and game.isCollision(ptLeft))
            or (dirUp and game.isCollision(ptUp))
            or (dirDown and game.isCollision(ptDown)),

            #   Danger right turn
            (dirRight and game.isCollision(ptDown))
            or (dirLeft and game.isCollision(ptUp))
            or (dirUp and game.isCollision(ptRight))
            or (dirDown and game.isCollision(ptLeft)),

            #   Danger left turn
            (dirRight and game.isCollision(ptUp))
            or (dirLeft and game.isCollision(ptDown))
            or (dirUp and game.isCollision(ptLeft))
            or (dirDown and game.isCollision(ptRight)),

            #   Move Directions
            dirLeft,
            dirRight,
            dirUp,
            dirDown,

            #   Food Location
            game.food.x < game.head.x,  #   Food left
            game.food.x > game.head.x,  #   Food right
            game.food.y < game.head.y,  #   Food up
            game.food.y > game.head.y,  #   Food down
        ]

        return np.array(state, dtype=int)

    def remember(self, state, action, reward, nextState, gameOver):
        self.memory.append((state, action, reward, nextState, gameOver))

    def trainLongMemory(self):
        if len(self.memory) > BATCHSIZE:
            miniSample = random.sample(self.memory, BATCHSIZE)
        else:
            miniSample = self.memory

        states, actions, rewards, nextStates, gameOvers = zip(*miniSample)
        self.trainer.trainStep(states, actions, rewards, nextStates, gameOvers)

    def trainShortMemory(self, state, action, reward, nextState, gameOver):
        self.trainer.trainStep(state, action, reward, nextState, gameOver)

    def getAction(self, state):
        #   random moves:   tradeoff exploration and exploitation
        self.epsilon = EPSILONCEIL - self.numberOfGames
        currMove = [0, 0, 0]

        if random.randint(0, 200) < self.epsilon:
            move = random.randint(0, 2)
            currMove[move] = 1
        else:
            state0 = torch.tensor(state, dtype=torch.float)
            prediction = self.model(state0)
            move = torch.argmax(prediction).item()
            currMove[move] = 1

        return currMove


def train():
    plotScores = []
    plotMeanScores = []
    totalScore = 0
    highScore = 0
    agent = Agent()
    game = SnakeGameAI()

    while True:

        #   get current State
        currState = agent.getState(game)

        #   get move
        currMove = agent.getAction(currState)

        #   perform move and get new state
        reward, gameOver, score = game.playStep(currMove)
        newState = agent.getState(game)

        #   train short memory
        agent.trainShortMemory(currState, currMove, reward, newState, gameOver)

        #   remember
        agent.remember(currState, currMove, reward, newState, gameOver)

        if gameOver:

            #   train long memory, plot result
            game.reset()
            agent.numberOfGames += 1
            agent.trainLongMemory()

            if score > highScore:
                highScore = score
                agent.model.save()

            print(
                f"Game :: {agent.numberOfGames}\nScore :: {score}\tHighscore :: {highScore}"
            )

            plotScores.append(score)
            totalScore += score
            meanScore = round(totalScore / agent.numberOfGames, 4)
            plotMeanScores.append(meanScore)

            print(f"Mean :: {meanScore}")

            plt.ion()

            fig = plt.figure(1)
            plt.subplot(111)
            plt.clf()
            plt.title("Training")
            plt.xlabel("Number of Games")
            plt.ylabel("Score")
            plt.plot(plotScores)
            plt.plot(plotMeanScores)
            plt.ylim(ymin=0)
            plt.text(len(plotScores) - 1, plotScores[-1], str(plotScores[-1]))
            plt.text(
                len(plotMeanScores) - 1, plotMeanScores[-1],
                str(plotMeanScores[-1]))
            fig.canvas.draw()
            fig.canvas.flush_events()


if __name__ == "__main__":
    train()
