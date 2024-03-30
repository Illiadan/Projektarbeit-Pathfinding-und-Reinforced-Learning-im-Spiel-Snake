import random
from os import path

import pygame as pg

from settings import *


class Food:
    def __init__(self, screen, grid, snake):
        self.screen = screen
        self.grid = grid
        self.snake = snake
        self.loadFoodImages()
        self.getNewFoodPosition()

    def loadFoodImages(self):
        if BLOCKSIZE >= 48:
            food = "redTriangle48.png"
        elif BLOCKSIZE >= 32:
            food = "redTriangle32.png"
        elif BLOCKSIZE >= 24:
            food = "redTriangle24.png"
        elif BLOCKSIZE >= 20:
            food = "redTriangle20.png"
        else:
            food = "redTriangle16.png"

        self.food = pg.image.load(path.join(DIRECTORY, "Images",
                                            food)).convert()

    def draw(self):
        self.screen.blit(self.food, self.convertPosInPx(self.foodPos))

    def convertPosInPx(self, pos):
        row = pos // COLUMNS
        col = pos % COLUMNS
        px = (col * BLOCKSIZE, row * BLOCKSIZE)
        return px

    def getNewFoodPosition(self):
        listFoodPos = [i for sub in self.grid for i in sub]
        listFoodPos.remove(self.snake.headPos)
        for idx in range(len(self.snake.tailPos) - 1):
            listFoodPos.remove(self.snake.tailPos[idx])
        length = len(listFoodPos)
        self.foodPos = listFoodPos[(random.randint(0, length - 1))]
