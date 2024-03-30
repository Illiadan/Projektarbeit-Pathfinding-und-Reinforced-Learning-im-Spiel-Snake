import time
from os import path

import pygame as pg
from pygame.constants import (K_DOWN, K_ESCAPE, K_KP_DIVIDE, K_KP_MINUS,
                              K_KP_MULTIPLY, K_KP_PLUS, K_LEFT, K_RIGHT, K_UP)

from ai import AI
from food import Food
from settings import *
from snake import Snake


class Game:
    def __init__(self, mode):
        pg.init()
        pg.display.set_caption("SnakeAI")
        self.screen = pg.display.set_mode((SCREENWIDTH, SCREENHIGHT))
        self.grid = self.initGrid()
        self.gameMode = mode
        self.snake = Snake(self.screen, self.grid)
        self.food = Food(self.screen, self.grid, self.snake)
        self.score = self.snake.length - 1
        self.highscore = self.loadHighscore()
        self.speed = DEFAULTSPEED
        self.state = 1
        self.updateScreen()
        self.initGameMode()

    def initGrid(self):
        """Function takes in the width, height and blockSize and returns a grid.
        The number of vertices of a row or column is achieved by dividing the width/height by the blockSize.
        The grid is then numbered from the top-left corner from left-to-right and top-to-bottom, beginning with 0 and
        ending at the bottom-right corner as the field with the highest number."""
        grid = []
        for i in range(ROWS):
            grid.append([i * COLUMNS + j for j in range(COLUMNS)])
        return grid

    def initGameMode(self):
        if self.gameMode != 1:
            self.ai = AI(self, self.gameMode)
        else:
            self.run()

    def loadHighscore(self):
        """load Highscore from file"""
        if self.gameMode == 1:
            file = HS_MANUAL
        elif self.gameMode == 2:
            file = HS_HAMILTON
        elif self.gameMode == 3:
            file = HS_ASTAR
        elif self.gameMode == 4:
            file = HS_ASTARLONG

        with open(path.join(DIRECTORY, file), "r") as f:
            try:
                return int(f.read())
            except:
                return 0

    def saveData(self):
        """save Highscore"""
        if self.gameMode == 1:
            file = HS_MANUAL
        elif self.gameMode == 2:
            file = HS_HAMILTON
        elif self.gameMode == 3:
            file = HS_ASTAR
        elif self.gameMode == 4:
            file = HS_ASTARLONG

        with open(path.join(DIRECTORY, file), "w") as f:
            f.write(str(self.highscore))

    def saveScore(self):
        if self.gameMode == 1:
            file = S_MANUAL
        elif self.gameMode == 2:
            file = S_HAMILTON
        elif self.gameMode == 3:
            file = S_ASTAR
        elif self.gameMode == 4:
            file = S_ASTARLONG

        with open(path.join(DIRECTORY, file), "a") as f:
            f.write(f"{str(self.score)}\n")

    def updateScreen(self):
        """States:
        0 - Main Menu TODO
        1 - Ingame Screen
        2 - Win Screen
        3 - GameOver Screen
        """
        self.screen.fill(BLACK)
        if self.state == 1:
            self.drawGameInfo()
            self.snake.draw()
            self.food.draw()
        elif self.state == 2:
            self.screen_Win()
        elif self.state == 3:
            self.screen_GameOver()
        pg.display.flip()

    def drawGameInfo(self):
        self.displayScore()
        self.displaySpeed()

    def displayScore(self):
        font = pg.font.SysFont("verdana", TEXTSIZE)
        text = font.render(f"Score: {self.score}", True, LGREY)
        self.screen.blit(text, (0, 0))

    def displaySpeed(self):
        font = pg.font.SysFont("verdana", TEXTSIZE)
        text = font.render(f"Speed: {self.speed}", True, LGREY)
        self.screen.blit(text, (8 * TEXTSIZE, 0))

    def speedUp(self, multiply):
        if multiply is True:
            self.speed *= 10
        else:
            self.speed += 1

    def speedDown(self, multiply):
        if multiply is True:
            self.speed = self.speed // 10 if self.speed // 10 > 0 else 1
        else:
            self.speed = self.speed - 1 if self.speed - 1 > 0 else 1

    def collisionWithFood(self):
        if self.snake.headPos == self.food.foodPos:
            return True
        return False

    def collisionWithTail(self):
        if self.snake.headPos in self.snake.tailPos:
            return True
        return False

    def growSnake(self):
        self.snake.length += 1
        self.score = self.snake.length - 1
        if self.snake.length == 2:
            self.snake.tailPos.append(self.snake.headPos)
        else:
            self.snake.tailPos.append(self.snake.tailPos[-1])

    def spawnNewFood(self):
        self.food.getNewFoodPosition()

    def showScreen_Win(self):
        running = True
        self.state = 2

        while running:
            self.updateScreen()

            if self.score > self.highscore:
                self.highscore = self.score
                self.saveData()

            for event in pg.event.get():
                if event.type == pg.QUIT:
                    running = False
                elif event.type == pg.KEYDOWN:
                    if event.key == K_ESCAPE:
                        running = False

    def screen_Win(self):
        font1 = pg.font.SysFont("verdana", TEXTSIZE * 2)
        font2 = pg.font.SysFont("verdana", TEXTSIZE)
        line1 = font1.render("VICTORY", True, RED)
        self.screen.blit(
            line1,
            (
                int((SCREENWIDTH - VICTORYWIDTH) /
                    (2 * SCREENWIDTH) * SCREENWIDTH),
                int(TITLEHEIGHTMULT * SCREENHIGHT),
            ),
        )
        line2 = font2.render(
            f"Your Score: {self.score}    Highscore: {self.highscore}",
            True,
            WHITE,
        )
        self.screen.blit(
            line2,
            (
                int((SCREENWIDTH - SCOREWIDTH) /
                    (2 * SCREENWIDTH) * SCREENWIDTH),
                int(SCOREHEIGHTMULT * SCREENHIGHT),
            ),
        )
        line3 = font2.render("Press ESCAPE to quit", True, WHITE)
        self.screen.blit(
            line3,
            (
                int((SCREENWIDTH - INFOWIDTH) /
                    (2 * SCREENWIDTH) * SCREENWIDTH),
                int(INFOHEIGHTMULT * SCREENHIGHT),
            ),
        )

    def showScreen_GameOver(self):
        running = True
        self.state = 3

        while running:
            self.updateScreen()

            if self.score > self.highscore:
                self.highscore = self.score
                self.saveData()

            for event in pg.event.get():
                if event.type == pg.QUIT:
                    running = False
                elif event.type == pg.KEYDOWN:
                    if event.key == K_ESCAPE:
                        running = False

    def screen_GameOver(self):
        font1 = pg.font.SysFont("verdana", TEXTSIZE * 2)
        font2 = pg.font.SysFont("verdana", TEXTSIZE)
        line1 = font1.render("DEFEAT", True, RED)
        self.screen.blit(
            line1,
            (
                int((SCREENWIDTH - DEFEATWIDTH) /
                    (2 * SCREENWIDTH) * SCREENWIDTH),
                int(TITLEHEIGHTMULT * SCREENHIGHT),
            ),
        )
        line2 = font2.render(
            f"Your Score: {self.score}    Highscore: {self.highscore}",
            True,
            WHITE,
        )
        self.screen.blit(
            line2,
            (
                int((SCREENWIDTH - SCOREWIDTH) /
                    (2 * SCREENWIDTH) * SCREENWIDTH),
                int(SCOREHEIGHTMULT * SCREENHIGHT),
            ),
        )
        line3 = font2.render("Press ESCAPE to quit", True, WHITE)
        self.screen.blit(
            line3,
            (
                int((SCREENWIDTH - INFOWIDTH) /
                    (2 * SCREENWIDTH) * SCREENWIDTH),
                int(INFOHEIGHTMULT * SCREENHIGHT),
            ),
        )

    def run(self):
        """game loop"""
        length = ROWS * COLUMNS
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
                    elif event.key == K_UP:
                        if self.snake.direction != 2:
                            self.snake.direction = 0
                    elif event.key == K_DOWN:
                        if self.snake.direction != 0:
                            self.snake.direction = 2
                    elif event.key == K_LEFT:
                        if self.snake.direction != 1:
                            self.snake.direction = 3
                    elif event.key == K_RIGHT:
                        if self.snake.direction != 3:
                            self.snake.direction = 1

                    # speed modifier
                    if event.key == K_KP_PLUS:
                        self.speedUp(False)
                    elif event.key == K_KP_MINUS:
                        self.speedDown(False)
                    elif event.key == K_KP_MULTIPLY:
                        self.speedUp(True)
                    elif event.key == K_KP_DIVIDE:
                        self.speedDown(True)

            self.snake.autoWalk()

            if self.snake.outOfBounds == True:
                gameOver = True
                running = False
                break

            self.updateScreen()

            if self.collisionWithTail():
                gameOver = True
                running = False
                break
            elif self.collisionWithFood():
                self.growSnake()
                if self.snake.length == length:
                    victory = True
                    running = False
                else:
                    self.spawnNewFood()
                    self.updateScreen()

            time.sleep(self.speed**-1)

        if victory == True:
            self.saveScore()
            self.showScreen_Win()
        elif gameOver == True:
            self.saveScore()
            self.showScreen_GameOver()
