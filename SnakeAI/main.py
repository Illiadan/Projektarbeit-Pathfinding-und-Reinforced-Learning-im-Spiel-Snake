import enum
import os
import sys

from game import *


class GameMode(enum.Enum):
    MANUALLY = 1
    HAMILTON = 2
    ASTAR = 3
    ASTARLONG = 4


def clearConsole():
    return os.system("cls")


if __name__ == "__main__":
    clearConsole()
    sys.setrecursionlimit(2100)
    # for i in range(20):
    #     game = Game(GameMode(4).value)
    game = Game(GameMode(1).value)
