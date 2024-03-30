from settings import *


class HamiltonCycle:
    def __init__(self):
        self.startPos = ROWS * COLUMNS - 1
        self.totalVertices = ROWS * COLUMNS
        self.tupleDict = {}

    def getHamiltonCycle(self):
        """Function checks if the given grid has any hamilton cycles and returns one, if there are any."""
        if not self.hasHamiltonCycle():
            return "The given grid has no hamilton cycles."
        self.cycle = [self.startPos]
        if self.buildHamiltonCycle():
            return self.cycle

    def hasHamiltonCycle(self):
        """Function checks if the given grid can possibly have hamilton cycles."""
        if (ROWS == 1 or COLUMNS == 1 or self.totalVertices <= 3
                or self.totalVertices % 2 == 1):
            return False
        return True

    def buildHamiltonCycle(self):
        if len(self.cycle) == self.totalVertices:
            if self.getDistance(self.cycle[-1], self.startPos) == 1:
                return True
            else:
                return False
        else:
            for nextVertex in range(self.totalVertices):
                if self.isValidVertex(nextVertex):
                    self.cycle.append(nextVertex)

                    if self.buildHamiltonCycle():
                        return True

                    self.cycle.remove(nextVertex)
            return False

    def isValidVertex(self, pos):
        if self.getDistance(self.cycle[-1],
                            pos) == 1 and pos not in self.cycle:
            return True
        return False

    def getDistance(self, lastPosInCycle, newPos):
        tupA = (self.tupleDict[lastPosInCycle] if lastPosInCycle
                in self.tupleDict else self.getTuple(lastPosInCycle))
        tupB = (self.tupleDict[newPos]
                if newPos in self.tupleDict else self.getTuple(newPos))
        dX = abs(tupA[0] - tupB[0])
        dY = abs(tupA[1] - tupB[1])
        return dX + dY

    def getTuple(self, pos):
        tup = (pos // COLUMNS, pos % COLUMNS)
        self.tupleDict[pos] = tup
        return tup


"""
0   1   2   3   4   5 
6   7   8   9   10  11
12  13  14  15  16  17
18  19  20  21  22  23
24  25  26  27  28  29
30  31  32  33  34  35

"""
