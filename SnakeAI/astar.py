import time

from settings import *


class Node:
    def __init__(self, value):
        self.value = value
        self.gScore = ROWS * COLUMNS
        self.hScore = ROWS * COLUMNS
        self.fScore = self.gScore + self.hScore
        self.neighbors = []
        self.prevNode = None
        self.visited = False


class AStar:
    def __init__(self, game):
        self.gameInstce = game
        self.grid = self.gameInstce.grid
        self.headPos = self.gameInstce.snake.headPos
        self.tailPos = self.gameInstce.snake.tailPos
        self.foodPos = self.gameInstce.food.foodPos
        self.initNodes()

    def initNodes(self):
        self.nodes = []
        flattenGrid = [i for sub in self.grid for i in sub]

        for value in flattenGrid:
            node = Node(value)
            if value == self.headPos:
                node.gScore = 0
                node.hScore = self.manhattanDistance(node.value, self.foodPos)
                node.fScore = node.gScore + node.hScore
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

    def manhattanDistance(self, startPos, endPos):
        startRow, startCol = self.getGridIdx(startPos)
        endRow, endCol = self.getGridIdx(endPos)
        mhDist = abs(endRow - startRow) + abs(endCol - startCol)
        return mhDist

    def getDistance(self, startPos, endPos):
        startRow, startCol = self.getGridIdx(startPos)
        endRow, endCol = self.getGridIdx(endPos)
        dX = abs(endCol - startCol)
        dY = abs(endRow - startRow)
        return dX + dY

    def getGridIdx(self, pos):
        row = pos // COLUMNS
        col = pos % COLUMNS
        return row, col

    def getShortestPath(self):
        return self.findShortestPath()

    def findShortestPath(self):
        nodesList = [
            node
            for node in self.nodes
            if node.visited == False
            and node.value
            not in [self.tailPos[idx] for idx in range(len(self.tailPos) - 1)]
        ]
        try:
            minFGScoreNode = min(nodesList, key=lambda x: (x.fScore, x.gScore))
        except:
            return []
        for node in minFGScoreNode.neighbors:
            if self.isObstacle(node):
                continue
            elif node.gScore <= minFGScoreNode.gScore + 1:
                continue
            else:
                self.updateNode(minFGScoreNode, node, self.foodPos)
                if node.value == self.foodPos:
                    return self.reconstructPath(node)
        minFGScoreNode.visited = True
        return self.findShortestPath()

    def isObstacle(self, node):
        if node in self.tailPos:
            return True
        return False

    def updateNode(self, currNode, selectedNode, endPos):
        selectedNode.gScore = currNode.gScore + 1
        selectedNode.hScore = self.manhattanDistance(selectedNode.value, endPos)
        selectedNode.fScore = selectedNode.gScore + selectedNode.hScore
        selectedNode.prevNode = currNode

    def reconstructPath(self, node):
        path = [None] * (node.fScore + 1)
        path[-1] = node
        for idx in range(len(path) - 2, -1, -1):
            path[idx] = path[idx + 1].prevNode
        for idx in range(len(path)):
            path[idx] = path[idx].value
        return path

    def getLongestPath(self):
        self.resetNodesVisited(self.nodes)
        self.availableNodes = self.getAvailableNodes()
        startNode = self.availableNodes[0]
        endNode = self.getEndNode()
        self.resetNodesScores(endNode)
        self.availableNodes.append(endNode)
        self.resetNodesScores(
            startNode, 0, self.manhattanDistance(startNode.value, endNode.value)
        )
        return self.findLongestPath(startNode, endNode)

    def resetNodesVisited(self, nodeList):
        for node in nodeList:
            node.visited = False

    def resetNodesScores(self, node, gScore=ROWS * COLUMNS, hScore=ROWS * COLUMNS):
        node.gScore = gScore
        node.hScore = hScore
        node.fScore = gScore + hScore

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
        for node in availableNodes:
            self.resetNodesScores(node)
        return availableNodes

    def getEndNode(self):
        maxIdx = 0
        for node in self.availableNodes:
            for neighbor in node.neighbors:
                if neighbor.value in self.tailPos:
                    maxIdx = max(maxIdx, self.tailPos.index(neighbor.value))
        endNode = next(
            node for node in self.nodes if node.value == self.tailPos[maxIdx]
        )
        return endNode

    def findLongestPath(self, startNode, endNode):
        self.longestPath = []
        path = [startNode]
        startEndDistance = self.getDistance(startNode.value, endNode.value)
        lengthLeftOverTail = len(self.tailPos) - self.tailPos.index(endNode.value)
        if startEndDistance > lengthLeftOverTail:
            return self.buildLongestShortPath(endNode)
        else:
            startTime = time.time()
            self.buildLongestPath(endNode, path, startTime)
            path = [node.value for node in self.longestPath]
            if len(path) <= 1:
                return self.buildLongestShortPath(endNode)
            return path

    def buildLongestShortPath(self, endNode):
        nodesList = [node for node in self.availableNodes if node.visited == False]
        try:
            minFGScoreNode = min(nodesList, key=lambda x: (x.fScore, x.gScore))
        except:
            return []
        for node in minFGScoreNode.neighbors:
            if self.isObstacle(node) and node != endNode:
                continue
            elif node.gScore <= minFGScoreNode.gScore + 1:
                continue
            else:
                self.updateNode(minFGScoreNode, node, endNode.value)
                if node.value == endNode.value:
                    return self.reconstructPath(node)
        minFGScoreNode.visited = True
        return self.buildLongestShortPath(endNode)

    def buildLongestPath(self, endNode, path, startTime):
        if time.time() - startTime > 5:
            return []

        currNode = path[-1]
        p = [node for node in path]

        if currNode == endNode:
            if len(p) > len(self.longestPath):
                self.longestPath = p
            return p
        else:
            for node in currNode.neighbors:
                if node in path or node not in self.availableNodes:
                    continue
                path.append(node)
                p = self.buildLongestPath(endNode, path, startTime)
                if len(p) - 1 > len(self.tailPos) - self.tailPos.index(endNode.value):
                    return p
                path.remove(node)
        return []


"""
0   1   2   3   4
5   6   7   8   9
10  11  12  13  14
15  16  17  18  19

"""
