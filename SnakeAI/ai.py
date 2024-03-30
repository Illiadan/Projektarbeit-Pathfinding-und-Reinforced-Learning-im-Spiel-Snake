import time

import pygame as pg
from pygame.constants import K_ESCAPE, K_KP_DIVIDE, K_KP_MINUS, K_KP_MULTIPLY, K_KP_PLUS

from astar import AStar
from hamiltonCycle import HamiltonCycle
from settings import *


class AI:
    def __init__(self, game, gameMode):
        self.gameInstce = game
        self.gameMode = gameMode
        self.train()

    def train(self):
        if self.gameMode == 2:
            self.initHamilton()
            if type(self.hamCycle) is str:
                print(
                    "The current game instance has no hamilton cycles, thus it can not be solved by this method."
                )
            else:
                self.prepareHamiltonTraining()
                self.trainHamilton()
        elif self.gameMode == 3:
            self.initAStar()
            self.prepareAStarTraining()
            self.trainAStar()
        elif self.gameMode == 4:
            self.initAStar()
            self.prepareAStarTraining()
            self.trainAStarWithAlternative()

    def initHamilton(self):
        hamiltonInstance = HamiltonCycle()
        self.hamCycle = hamiltonInstance.getHamiltonCycle()

    def prepareHamiltonTraining(self):
        self.sortHamCycle()
        self.convertHamCycleToDirections()

    def trainHamilton(self):
        length = ROWS * COLUMNS
        idx = 0 % length
        running = True
        gameOver = False
        victory = False

        while running:

            if self.gameInstce.collisionWithFood():
                self.gameInstce.growSnake()
                if self.gameInstce.snake.length == length:
                    victory = True
                    running = False
                else:
                    self.gameInstce.spawnNewFood()
                    self.gameInstce.updateScreen()

            for event in pg.event.get():

                # quit application
                if event.type == pg.QUIT:
                    running = False
                elif event.type == pg.KEYDOWN:
                    if event.key == K_ESCAPE:
                        running = False

                    # speed modifier
                    if event.key == K_KP_PLUS:
                        self.gameInstce.speedUp(False)
                    elif event.key == K_KP_MINUS:
                        self.gameInstce.speedDown(False)
                    elif event.key == K_KP_MULTIPLY:
                        self.gameInstce.speedUp(True)
                    elif event.key == K_KP_DIVIDE:
                        self.gameInstce.speedDown(True)

            self.walkHamilton(idx)
            self.gameInstce.updateScreen()
            time.sleep(self.gameInstce.speed ** -1)
            idx = (idx + 1) % length

        if victory == True:
            self.gameInstce.saveScore()
            self.gameInstce.showScreen_Win()
        elif gameOver == True:
            self.gameInstce.saveScore()
            self.gameInstce.showScreen_GameOver()

    def sortHamCycle(self):
        idx = self.hamCycle.index(self.gameInstce.snake.headPos)
        self.hamCycle = self.hamCycle[idx:] + self.hamCycle[:idx]

    def convertHamCycleToDirections(self):
        self.hamCycleDirs = []
        for idx in range(len(self.hamCycle)):
            diff = self.hamCycle[(idx + 1) % len(self.hamCycle)] - self.hamCycle[idx]
            if diff == 1:
                self.hamCycleDirs.append("E")
            elif diff == -1:
                self.hamCycleDirs.append("W")
            elif diff > 1:
                self.hamCycleDirs.append("S")
            elif diff < -1:
                self.hamCycleDirs.append("N")

    def walkHamilton(self, idx):
        if self.hamCycleDirs[idx] == "E":
            self.gameInstce.snake.walkEast()
        elif self.hamCycleDirs[idx] == "W":
            self.gameInstce.snake.walkWest()
        elif self.hamCycleDirs[idx] == "S":
            self.gameInstce.snake.walkSouth()
        elif self.hamCycleDirs[idx] == "N":
            self.gameInstce.snake.walkNorth()

    def initAStar(self):
        self.aStarInstance = AStar(self.gameInstce)
        self.aStarPath = self.aStarInstance.getShortestPath()

    def prepareAStarTraining(self):
        self.convertAStarPathToDirections()

    def getNewAStarPath(self):
        self.aStarInstance.headPos = self.gameInstce.snake.headPos
        self.aStarInstance.foodPos = self.gameInstce.food.foodPos
        self.aStarInstance.tailPos = self.gameInstce.snake.tailPos
        self.aStarInstance.initNodes()
        self.aStarPath = self.aStarInstance.getShortestPath()
        self.convertAStarPathToDirections()

    def trainAStar(self):
        length = len(self.aStarPath)
        idx = 0 % length
        running = True
        gameOver = False
        victory = False

        while running:

            for event in pg.event.get():

                # quit application
                if event.type == pg.QUIT:
                    running = False
                elif event.type == pg.KEYDOWN:
                    if event.key == K_ESCAPE:
                        running = False

                    # speed modifier
                    if event.key == K_KP_PLUS:
                        self.gameInstce.speedUp(False)
                    elif event.key == K_KP_MINUS:
                        self.gameInstce.speedDown(False)
                    elif event.key == K_KP_MULTIPLY:
                        self.gameInstce.speedUp(True)
                    elif event.key == K_KP_DIVIDE:
                        self.gameInstce.speedDown(True)

            self.walkAStar(idx)
            self.gameInstce.updateScreen()

            if self.gameInstce.collisionWithTail():
                gameOver = True
                running = False
                break
            elif self.gameInstce.collisionWithFood():
                self.aStarPath = None
                self.gameInstce.growSnake()
                if self.gameInstce.snake.length == ROWS * COLUMNS:
                    victory = True
                    running = False
                else:
                    self.gameInstce.spawnNewFood()
                    self.gameInstce.updateScreen()
                    self.getNewAStarPath()
                    length = len(self.aStarPath)
                    if length == 0:
                        gameOver = True
                        running = False
                        break
                    else:
                        idx = 0 % length
            else:
                idx = (idx + 1) % length

            time.sleep(self.gameInstce.speed ** -1)

        if victory == True:
            self.gameInstce.saveScore()
            self.gameInstce.showScreen_Win()
        elif gameOver == True:
            self.gameInstce.saveScore()
            self.gameInstce.showScreen_GameOver()

    def getNewAStarPathWithAlternative(self):
        self.aStarInstance.headPos = self.gameInstce.snake.headPos
        self.aStarInstance.foodPos = self.gameInstce.food.foodPos
        self.aStarInstance.tailPos = self.gameInstce.snake.tailPos
        self.aStarInstance.initNodes()
        self.aStarPath = self.aStarInstance.getShortestPath()
        isShortPath = True
        if len(self.aStarPath) == 0:
            self.aStarPath = self.aStarInstance.getLongestPath()
            isShortPath = False
        self.convertAStarPathToDirections()
        return isShortPath

    def trainAStarWithAlternative(self):
        length = len(self.aStarPath)
        idx = 0 % length
        running = True
        gameOver = False
        victory = False
        isShortPath = True

        while running:

            for event in pg.event.get():

                # quit application
                if event.type == pg.QUIT:
                    running = False
                elif event.type == pg.KEYDOWN:
                    if event.key == K_ESCAPE:
                        running = False

                    # speed modifier
                    if event.key == K_KP_PLUS:
                        self.gameInstce.speedUp(False)
                    elif event.key == K_KP_MINUS:
                        self.gameInstce.speedDown(False)
                    elif event.key == K_KP_MULTIPLY:
                        self.gameInstce.speedUp(True)
                    elif event.key == K_KP_DIVIDE:
                        self.gameInstce.speedDown(True)

            self.walkAStar(idx)
            self.gameInstce.updateScreen()

            if self.gameInstce.collisionWithTail():
                gameOver = True
                running = False
                break
            elif self.gameInstce.collisionWithFood():
                self.aStarPath = None
                self.gameInstce.growSnake()
                if self.gameInstce.snake.length == ROWS * COLUMNS:
                    victory = True
                    running = False
                else:
                    self.gameInstce.spawnNewFood()
                    self.gameInstce.updateScreen()
                    isShortPath = self.getNewAStarPathWithAlternative()
                    length = len(self.aStarPath)
                    idx = 0 % length
            elif isShortPath == False and idx == length - 2:
                self.aStarPath = None
                isShortPath = self.getNewAStarPathWithAlternative()
                length = len(self.aStarPath)
                idx = 0 % length
            else:
                idx = (idx + 1) % length

            time.sleep(self.gameInstce.speed ** -1)

        if victory == True:
            self.gameInstce.saveScore()
            self.gameInstce.showScreen_Win()
        elif gameOver == True:
            self.gameInstce.saveScore()
            self.gameInstce.showScreen_GameOver()

    def convertAStarPathToDirections(self):
        self.aStarPathDirs = []
        for idx in range(len(self.aStarPath) - 1):
            diff = self.aStarPath[(idx + 1) % len(self.aStarPath)] - self.aStarPath[idx]
            if diff == 1:
                self.aStarPathDirs.append("E")
            elif diff == -1:
                self.aStarPathDirs.append("W")
            elif diff > 1:
                self.aStarPathDirs.append("S")
            elif diff < -1:
                self.aStarPathDirs.append("N")

    def walkAStar(self, idx):
        if self.aStarPathDirs[idx] == "E":
            self.gameInstce.snake.walkEast()
        elif self.aStarPathDirs[idx] == "W":
            self.gameInstce.snake.walkWest()
        elif self.aStarPathDirs[idx] == "S":
            self.gameInstce.snake.walkSouth()
        elif self.aStarPathDirs[idx] == "N":
            self.gameInstce.snake.walkNorth()
