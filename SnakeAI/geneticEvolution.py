import math
import random

from settings import *


class Node:
    def __init__(self, value):
        self.value = value
        self.neighbors = []
        self.visited = False


class GeneticEvolution:
    def __init__(self, game):
        self.gameInstce = game
        self.moves = 0
        self.updateHeadPos()
        self.updateTailPos()
        self.updateDirection()
        self.updateFoodPos()
        self.getFoodAngle()
        self.initNodes()
        self.getReachabilityOfHeadNodeNeighbors()
        self.getShareOfReachableNodes()
        self.inputLayer = self.buildInputLayer()
        self.hl1Size = 6
        self.buildHiddenLayer1()
        self.hl2Size = 6
        self.buildHiddenLayer2()
        self.olSize = 4
        self.buildOutputLayer()

    def updateHeadPos(self):
        self.headPos = self.gameInstce.snake.headPos

    def updateTailPos(self):
        self.tailPos = self.gameInstce.snake.tailPos

    def updateDirection(self):
        self.direction = self.gameInstce.snake.direction

    def updateFoodPos(self):
        self.foodPos = self.gameInstce.food.foodPos

    def getFoodAngle(self):
        headRow, headCol = self.getGridIdx(self.headPos)
        foodRow, foodCol = self.getGridIdx(self.foodPos)
        x = foodCol - headCol
        y = foodRow - headRow
        r = math.sqrt(x ** 2 + y ** 2)
        self.xAngle = round(x / r, 4)
        self.yAngle = round(y / r, 4)

    def initNodes(self):
        self.nodes = []
        flattenGrid = [i for sub in self.gameInstce.grid for i in sub]

        for value in flattenGrid:
            node = Node(value)
            self.nodes.append(node)

        self.getNodeNeighbors()

    def getNodeNeighbors(self):
        for node in self.nodes:
            row, col = self.getGridIdx(node.value)

            if row - 1 >= 0:
                node.neighbors.append(self.getNode((row - 1) * COLUMNS + col))
            if row + 1 < ROWS:
                node.neighbors.append(self.getNode((row + 1) * COLUMNS + col))
            if col - 1 >= 0:
                node.neighbors.append(self.getNode(row * COLUMNS + col - 1))
            if col + 1 < COLUMNS:
                node.neighbors.append(self.getNode(row * COLUMNS + col + 1))

    def getNode(self, pos):
        return next(node for node in self.nodes if node.value == pos)

    def getGridIdx(self, pos):
        row = pos // COLUMNS
        col = pos % COLUMNS
        return row, col

    def getReachabilityOfHeadNodeNeighbors(self):
        self.neighborNorth = 0
        self.neighborEast = 0
        self.neighborSouth = 0
        self.neighborWest = 0

        headNode = self.getNode(self.headPos)
        headRow, headCol = self.getGridIdx(headNode.value)

        for node in headNode.neighbors:
            row, col = self.getGridIdx(node.value)

            if headRow == row:
                if headCol - 1 == col:
                    if self.direction == 1 or node.value in self.tailPos:
                        continue
                    self.neighborWest = 1
                elif headCol + 1 == col:
                    if self.direction == 3 or node.value in self.tailPos:
                        continue
                    self.neighborEast = 1

            if headCol == col:
                if headRow - 1 == row:
                    if self.direction == 2 or node.value in self.tailPos:
                        continue
                    self.neighborNorth = 1
                elif headRow + 1 == row:
                    if self.direction == 0 or node.value in self.tailPos:
                        continue
                    self.neighborSouth = 1

    def getShareOfReachableNodes(self):
        self.availableNodes = self.getAvailableNodes()
        lenMaxNodes = len(self.gameInstce.grid) - len(self.tailPos)
        lenReachableNodes = len(self.availableNodes)
        self.shareOfReachableNodes = round(lenReachableNodes / lenMaxNodes, 4)

    def getAvailableNodes(self):
        availableNodes = []
        queue = [node for node in self.nodes if node.value == self.headPos]

        while len(queue) > 0:
            currNode = queue.pop(0)
            availableNodes.append(currNode)
            currNode.visited = True

            for node in currNode.neighbors:
                if (
                    node.visited == False
                    and node.value not in self.tailPos
                    and node not in queue
                ):
                    queue.append(node)

        self.resetNodesVisited(availableNodes)
        return availableNodes

    def resetNodesVisited(self, nodeList):
        for node in nodeList:
            node.visited = False

    def buildInputLayer(self):
        """
        Input Layer:
        [
            NeighborNorth,
            NeighborEast,
            NeighborSouth,
            NeighborWest,
            xAngle,
            yAngle,
            ShareOfReachableNodes,
        ]
        """

        input = []
        input.append(self.neighborNorth)
        input.append(self.neighborEast)
        input.append(self.neighborSouth)
        input.append(self.neighborWest)
        input.append(self.xAngle)
        input.append(self.yAngle)
        input.append(self.shareOfReachableNodes)

        return input

    def buildHiddenLayer1(self):
        self.hl1Weights = [
            [random.uniform(-1, 1) for i in range(len(self.inputLayer) + 1)]
            for j in range(self.hl1Size)
        ]
        self.hl1Bias = [1]

    def buildHiddenLayer2(self):
        self.hl2Weights = [
            [random.uniform(-1, 1) for i in range(len(self.hl1Size) + 1)]
            for j in range(self.hl2Size)
        ]
        self.hl2Bias = [1]

    def buildOutputLayer(self):
        self.olWeights = [
            [random.uniform(-1, 1) for i in range(len(self.hl2Size) + 1)]
            for j in range(self.olSize)
        ]

    def forwardPropagation(self):
        pass
