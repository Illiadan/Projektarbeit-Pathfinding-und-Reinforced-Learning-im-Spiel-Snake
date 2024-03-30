import random
from collections import namedtuple
from enum import Enum

import numpy as np
import pygame
from pygame.draw import circle

pygame.init()
font = pygame.font.SysFont("verdana", 25)


class Direction(Enum):
    RIGHT = 1
    LEFT = 2
    UP = 3
    DOWN = 4


Point = namedtuple("Point", "x, y")

#   RGB Colors
WHITE = (255, 255, 255)
RED = (200, 0, 0)
GREEN = (0, 140, 0)
LGREEN = (0, 190, 0)
BLUE = (0, 0, 255)
LBLUE = (0, 100, 255)
BLACK = (0, 0, 0)

BLOCKSIZE = 20
SPACING = 4
SPEED = 500


class SnakeGameAI:
    def __init__(self, w=640, h=480):
        self.w = w
        self.h = h

        #   init display
        self.display = pygame.display.set_mode((self.w, self.h))
        pygame.display.set_caption("Snake")
        self.clock = pygame.time.Clock()

        self.reset()

    def reset(self):

        #   init game state
        self.direction = Direction.RIGHT

        self.head = Point(self.w / 2, self.h / 2)
        self.snake = [
            self.head,
            Point(self.head.x - BLOCKSIZE, self.head.y),
            Point(self.head.x - 2 * BLOCKSIZE, self.head.y)
        ]

        self.score = 0
        self.food = None
        self._placeFood()
        self.frameIteration = 0

    def _placeFood(self):
        x = random.randint(0, (self.w - BLOCKSIZE) // BLOCKSIZE) * BLOCKSIZE
        y = random.randint(0, (self.h - BLOCKSIZE) // BLOCKSIZE) * BLOCKSIZE
        self.food = Point(x, y)
        if self.food in self.snake:
            self._placeFood()

    def playStep(self, action):

        self.frameIteration += 1

        #   Get User Input
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

            # if event.type == pygame.KEYDOWN:
            #     if event.key == pygame.K_LEFT:
            #         self.direction = Direction.LEFT
            #     elif event.key == pygame.K_RIGHT:
            #         self.direction = Direction.RIGHT
            #     elif event.key == pygame.K_UP:
            #         self.direction = Direction.UP
            #     elif event.key == pygame.K_DOWN:
            #         self.direction = Direction.DOWN

        #   Move
        self._move(action)  #   Update the head
        self.snake.insert(0, self.head)

        #   Game Over Check
        reward = 0
        gameOver = False
        if self.isCollision() or self.frameIteration > 500 * len(self.snake):
            gameOver = True
            reward = -15
            return reward, gameOver, self.score

        #   Place New Food Or Just Move
        if self.head == self.food:
            self.score += 1
            reward = 10
            self._placeFood()
        else:
            self.snake.pop()

        #   Update UI and Clock
        self._updateUI()
        self.clock.tick(SPEED)

        #   Return Game Over And Score
        return reward, gameOver, self.score

    def isCollision(self, pt=None):

        if pt is None:
            pt = self.head

        #   Hits Boundary
        if pt.x > self.w - BLOCKSIZE or pt.x < 0 or pt.y > self.h - BLOCKSIZE or pt.y < 0:
            return True

        #   Hits Itself
        if pt in self.snake[1:]:
            return True

        return False

    def _updateUI(self):
        self.display.fill(BLACK)

        pygame.draw, circle(
            self.display, GREEN,
            (self.snake[0].x + BLOCKSIZE / 2, self.snake[0].y + BLOCKSIZE / 2),
            BLOCKSIZE / 2)

        for pt in self.snake[1:]:
            pygame.draw.rect(self.display, GREEN,
                             pygame.Rect(pt.x, pt.y, BLOCKSIZE, BLOCKSIZE))
            pygame.draw.rect(
                self.display, LGREEN,
                pygame.Rect(pt.x + SPACING, pt.y + SPACING,
                            BLOCKSIZE - 2 * SPACING, BLOCKSIZE - 2 * SPACING))

        pygame.draw.rect(
            self.display, RED,
            pygame.Rect(self.food.x, self.food.y, BLOCKSIZE, BLOCKSIZE))

        text = font.render(f"Score: {self.score}", True, WHITE)
        self.display.blit(text, [0, 0])
        pygame.display.flip()

    def _move(self, action):

        #   [straight, right turn, left turn]
        clockwiseOrder = [
            Direction.RIGHT, Direction.DOWN, Direction.LEFT, Direction.UP
        ]
        idx = clockwiseOrder.index(self.direction)

        if np.array_equal(action, [1, 0, 0]):
            #   straight; no change in directions
            newDirection = clockwiseOrder[idx]
        elif np.array_equal(action, [0, 1, 0]):
            #   right turn; change direction clockwise
            nextIdx = (idx + 1) % len(clockwiseOrder)
            newDirection = clockwiseOrder[nextIdx]
        else:
            #   left turn; change direction counter clockwise
            nextIdx = (idx - 1) % len(clockwiseOrder)
            newDirection = clockwiseOrder[nextIdx]

        self.direction = newDirection

        x = self.head.x
        y = self.head.y

        if self.direction == Direction.RIGHT:
            x += BLOCKSIZE
        elif self.direction == Direction.LEFT:
            x -= BLOCKSIZE
        elif self.direction == Direction.DOWN:
            y += BLOCKSIZE
        elif self.direction == Direction.UP:
            y -= BLOCKSIZE

        self.head = Point(x, y)


# if __name__ == "__main__":
#     game = SnakeGameAI()

#     while True:
#         gameOver, score = game.playStep()

#         if gameOver:
#             break

#     print(f"Final Score :: {score}")

#     pygame.quit()
