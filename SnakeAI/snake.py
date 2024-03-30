from os import path

import pygame as pg

from settings import *


class Snake:
    def __init__(self, screen, grid):
        self.screen = screen
        self.grid = grid
        self.outOfBounds = False
        self.length = 1
        self.direction = 1  #   0 - North, 1 - East, 2 - South, 3 - West
        self.loadSnakeImages()
        self.initStartingPosition()

    def loadSnakeImages(self):
        if BLOCKSIZE >= 48:
            head = "greenOctagonOutline48.png"
            tail = "greenRect48.png"
        elif BLOCKSIZE >= 32:
            head = "greenOctagonOutline32.png"
            tail = "greenRect32.png"
        elif BLOCKSIZE >= 24:
            head = "greenOctagonOutline24.png"
            tail = "greenRect24.png"
        elif BLOCKSIZE >= 20:
            head = "greenOctagonOutline20.png"
            tail = "greenRect20.png"
        else:
            head = "greenOctagonOutline16.png"
            tail = "greenRect16.png"

        self.snakeHead = pg.image.load(path.join(DIRECTORY, "Images",
                                                 head)).convert()
        self.snakeTail = pg.image.load(path.join(DIRECTORY, "Images",
                                                 tail)).convert()

    def initStartingPosition(self):
        """Snake starts by default at position (1,1) in the grid with no tail."""
        self.headPos = self.grid[1][1]
        self.tailPos = []

    def convertPosInPx(self, pos):
        row, col = self.getGridIdx(pos)
        px = (col * BLOCKSIZE, row * BLOCKSIZE)
        return px

    def getGridIdx(self, pos):
        row = pos // COLUMNS
        col = pos % COLUMNS
        return row, col

    def draw(self):
        self.screen.blit(self.snakeHead, self.convertPosInPx(self.headPos))
        for idx in range(self.length - 1):
            self.screen.blit(self.snakeTail,
                             self.convertPosInPx(self.tailPos[idx]))

    def walkNorth(self):
        if self.length > 1:
            for idx in range(self.length - 2, 0, -1):
                self.tailPos[idx] = self.tailPos[idx - 1]
            self.tailPos[0] = self.headPos
        row, col = self.getGridIdx(self.headPos)
        try:
            self.headPos = self.grid[(row - 1) % row][col]
        except:
            self.outOfBounds = True
        self.direction = 0

    def walkEast(self):
        if self.length > 1:
            for idx in range(self.length - 2, 0, -1):
                self.tailPos[idx] = self.tailPos[idx - 1]
            self.tailPos[0] = self.headPos
        row, col = self.getGridIdx(self.headPos)
        try:
            self.headPos = self.grid[row][col + 1]
        except:
            self.outOfBounds = True
        self.direction = 1

    def walkSouth(self):
        if self.length > 1:
            for idx in range(self.length - 2, 0, -1):
                self.tailPos[idx] = self.tailPos[idx - 1]
            self.tailPos[0] = self.headPos
        row, col = self.getGridIdx(self.headPos)
        try:
            self.headPos = self.grid[row + 1][col]
        except:
            self.outOfBounds = True
        self.direction = 2

    def walkWest(self):
        if self.length > 1:
            for idx in range(self.length - 2, 0, -1):
                self.tailPos[idx] = self.tailPos[idx - 1]
            self.tailPos[0] = self.headPos
        row, col = self.getGridIdx(self.headPos)
        try:
            self.headPos = self.grid[row][(col - 1) % col]
        except:
            self.outOfBounds = True
        self.direction = 3

    def autoWalk(self):
        if self.direction == 0:
            self.walkNorth()
        elif self.direction == 1:
            self.walkEast()
        elif self.direction == 2:
            self.walkSouth()
        elif self.direction == 3:
            self.walkWest()
