import os
import random
import time

import pygame
from pygame.constants import (K_DOWN, K_ESCAPE, K_KP_ENTER, K_LEFT, K_RETURN,
                              K_RIGHT, K_UP)


class Snake:
    def __init__(self, screen, blockSize, dir, length=1):
        self.screen = screen
        self.length = length
        self.blockSize = blockSize
        self.dir = dir
        self.snakeHead = pygame.image.load(
            os.path.join(self.dir, "greenOctagonOutline20.png")).convert()
        self.snakeTail = pygame.image.load(
            os.path.join(self.dir, "greenRect20.png")).convert()
        self.snakePosX = [self.blockSize] * length
        self.snakePosY = [self.blockSize] * length
        self.direction = "right"

    def draw(self):
        self.screen.fill((0, 0, 0))
        self.screen.blit(self.snakeHead,
                         (self.snakePosX[0], self.snakePosY[0]))
        for idx in range(1, self.length):
            self.screen.blit(self.snakeTail,
                             (self.snakePosX[idx], self.snakePosY[idx]))
        pygame.display.flip()

    def moveUp(self):
        if self.direction != "down":
            self.direction = "up"

    def moveDown(self):
        if self.direction != "up":
            self.direction = "down"

    def moveLeft(self):
        if self.direction != "right":
            self.direction = "left"

    def moveRight(self):
        if self.direction != "left":
            self.direction = "right"

    def autoWalk(self):
        if self.direction == "left":
            for idx in range(self.length - 1, 0, -1):
                self.snakePosX[idx] = self.snakePosX[idx - 1]
                self.snakePosY[idx] = self.snakePosY[idx - 1]
            self.snakePosX[0] -= self.blockSize
        elif self.direction == "right":
            for idx in range(self.length - 1, 0, -1):
                self.snakePosX[idx] = self.snakePosX[idx - 1]
                self.snakePosY[idx] = self.snakePosY[idx - 1]
            self.snakePosX[0] += self.blockSize
        elif self.direction == "up":
            for idx in range(self.length - 1, 0, -1):
                self.snakePosX[idx] = self.snakePosX[idx - 1]
                self.snakePosY[idx] = self.snakePosY[idx - 1]
            self.snakePosY[0] -= self.blockSize
        elif self.direction == "down":
            for idx in range(self.length - 1, 0, -1):
                self.snakePosX[idx] = self.snakePosX[idx - 1]
                self.snakePosY[idx] = self.snakePosY[idx - 1]
            self.snakePosY[0] += self.blockSize
        self.draw()


class Apple:
    def __init__(self, screen, screenSize, blockSize, dir):
        self.screen = screen
        self.screenSize = screenSize
        self.blockSize = blockSize
        self.dir = dir
        self.apple = pygame.image.load(
            os.path.join(self.dir, "redTriangle20.png")).convert()
        self.applePosX = 0
        self.applePosY = 0
        self.randomizePosition()

    def draw(self):
        self.screen.blit(self.apple, (self.applePosX, self.applePosY))
        pygame.display.flip()

    def randomizePosition(self):
        maxXMultiplier = self.screenSize[0] // self.blockSize
        maxYMultiplier = self.screenSize[1] // self.blockSize
        xMultiplier = random.randint(1, maxXMultiplier - 1)
        yMultiplier = random.randint(1, maxYMultiplier - 1)
        self.applePosX = self.blockSize * xMultiplier
        self.applePosY = self.blockSize * yMultiplier


class Game:
    def __init__(self, screenWidth, screenHeight, speed, blockSize=20):
        pygame.init()
        pygame.display.set_caption("Snake")
        self.screenSize = screenWidth, screenHeight
        self.screen = pygame.display.set_mode(self.screenSize)
        self.screen.fill((0, 0, 0))
        self.speed = speed
        self.blockSize = blockSize
        self.score = 0
        self.loadData()
        self.snake = Snake(self.screen, self.blockSize, self.dir)
        self.snake.draw()
        self.apple = Apple(self.screen, self.screenSize, self.blockSize,
                           self.dir)
        self.apple.draw()
        self.displayScore()

    def loadData(self):
        """load Highscore"""
        self.dir = os.path.dirname(__file__)
        with open(os.path.join(self.dir, "highscore.txt"), "r") as f:
            try:
                self.highscore = int(f.read())
            except:
                self.highscore = 0

    def saveData(self):
        """save Highscore"""
        with open(os.path.join(self.dir, "highscore.txt"), "w") as f:
            f.write(str(self.highscore))

    def displayScore(self):
        font = pygame.font.SysFont("verdana", self.blockSize)
        text = font.render(f"Score: {self.score}", True, (200, 200, 200))
        self.screen.blit(text, (0, 0))
        pygame.display.flip()

    def outOfBounds(self):
        if self.snake.snakePosX[0] < 0 or self.snake.snakePosX[
                0] >= self.screenSize[0] or self.snake.snakePosY[
                    0] < 0 or self.snake.snakePosY[0] >= self.screenSize[1]:
            return True
        return False

    def collisionWithSnake(self):
        for idx in range(1, self.snake.length):
            if self.snake.snakePosX[0] == self.snake.snakePosX[
                    idx] and self.snake.snakePosY[0] == self.snake.snakePosY[
                        idx]:
                return True
        return False

    def collisionWithApple(self):
        if self.snake.snakePosX[
                0] == self.apple.applePosX and self.snake.snakePosY[
                    0] == self.apple.applePosY:
            return True
        return False

    def growSnakeAndGetNewApple(self):
        self.score += 1
        self.snake.length += 1
        self.snake.snakePosX.append(self.snake.snakePosX[-1])
        self.snake.snakePosY.append(self.snake.snakePosY[-1])
        self.apple.randomizePosition()
        self.apple.draw()

    def newGame(self):
        self.screen.fill((0, 0, 0))
        self.score = 0
        self.snake.length = 1
        self.snake.snakePosX = [self.blockSize]
        self.snake.snakePosY = [self.blockSize]
        self.snake.direction = "right"
        self.snake.draw()
        self.apple.randomizePosition()
        self.apple.draw()
        self.displayScore()
        pygame.display.flip()
        self.run()

    def screen_GameOver(self):
        self.screen.fill((0, 0, 0))
        font1 = pygame.font.SysFont("verdana", self.blockSize * 2)
        font2 = pygame.font.SysFont("verdana", self.blockSize)
        line1 = font1.render("GAME OVER", True, (255, 0, 0))
        self.screen.blit(line1, (64, 32))
        line2 = font2.render(
            f"Your Score: {self.score}    Highscore: {self.highscore}", True,
            (255, 255, 255))
        self.screen.blit(line2, (40, 96))
        line3 = font2.render("Press ENTER to play again", True,
                             (255, 255, 255))
        self.screen.blit(line3, (55, 160))
        line4 = font2.render("or ESCAPE to quit", True, (255, 255, 255))
        self.screen.blit(line4, (90, 192))
        pygame.display.flip()

    def showScreen_GameOver(self):
        running = True

        while running:
            self.screen_GameOver()

            if self.score > self.highscore:
                self.highscore = self.score
                self.saveData()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == K_ESCAPE:
                        running = False
                    elif event.key == K_RETURN or event.key == K_KP_ENTER:
                        self.newGame()
                        running = False

    def run(self):
        running = True

        while running:

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == K_ESCAPE:
                        running = False
                    elif event.key == K_UP:
                        self.snake.moveUp()
                    elif event.key == K_DOWN:
                        self.snake.moveDown()
                    elif event.key == K_LEFT:
                        self.snake.moveLeft()
                    elif event.key == K_RIGHT:
                        self.snake.moveRight()

            self.snake.autoWalk()
            self.apple.draw()
            self.displayScore()

            if self.outOfBounds():
                running = False

            if self.collisionWithSnake():
                running = False

            if self.collisionWithApple():
                self.growSnakeAndGetNewApple()

            time.sleep(self.speed**-1)

        self.showScreen_GameOver()


game = Game(640, 480, 10)
game.run()
