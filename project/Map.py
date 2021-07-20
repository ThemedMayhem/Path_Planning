import math
import matplotlib.pyplot as plt
from PIL import Image, ImageDraw
from Node import Node
import numpy as np
from ClosedList import *
from OpenList import *

def DiagonalDistance(i1, j1, i2, j2):
    return abs(abs(i2 - i1) - abs(j2 - j1)) + math.sqrt(2) * min(abs(i2 - i1), abs(j2-j1))

def ManhattanDistance(i1, j1, i2, j2):
    return abs(i2 - i1) + abs(j2 - j1)

def EuclideanDistance(i1, j1, i2, j2):
    return math.sqrt((i1 - i2)**2 + (j1 - j2)**2)

class Map:

    def __init__(self):
        '''
        Default constructor
        '''

        self.width = 0
        self.height = 0
        self.cells = []
        self.visited = set()

    def ReadFromString(self, cellStr, width, height):
        '''
        Converting a string (with '#' representing obstacles and '.' representing free cells) to a grid
        '''
        self.width = width
        self.height = height
        self.cells = [[0 for _ in range(width)] for _ in range(height)]
        cellLines = cellStr.split("\n")
        i = 0
        j = 0
        for l in cellLines:
            if len(l) != 0:
                j = 0
                for c in l:
                    if c == '.':
                        self.cells[i][j] = 0
                    elif c == '#':
                        self.cells[i][j] = 1
                    else:
                        continue
                    j += 1
                if j != width:
                    raise Exception("Size Error. Map width = ", j, ", but must be", width)

                i += 1

        if i != height:
            raise Exception("Size Error. Map height = ", i, ", but must be", height)

    def SetGridCells(self, width, height, gridCells):
        '''
        Initialization of map by list of cells.
        '''
        self.width = width
        self.height = height
        self.cells = gridCells

    def inBounds(self, coords):
        '''
        Check if the cell is on a grid.
        '''
        return (0 <= coords[1] < self.width) and (0 <= coords[0] < self.height)

    def Traversable(self, coords):
        '''
        Check if the cell is not an obstacle.
        '''
        return not self.cells[coords[0]][coords[1]]

    def GetNeighbors(self, i, j, diagonalMoves = False):
        '''
        Get a list of neighbouring cells as (i,j) tuples.
        '''
        neighbors = []
        for ki in range(i - 1, i + 2):
            for kj in range(j - 1, j + 2):
                if ((i, j) != (ki, kj) and self.inBounds((ki, kj)) and self.Traversable((ki, kj))):
                    if (abs(ki + kj - i - j) == 1):
                        neighbors.append((ki, kj))
                    elif (diagonalMoves):
                        if (self.Traversable((i, kj)) or self.Traversable((ki, j))):
                            neighbors.append((ki, kj))
        return neighbors

    def GetDirection(self, x: tuple, n: tuple):
        di = n[0] - x[0]
        dj = n[1] - x[1]
        t = max(abs(di), abs(dj))

        return (int(di / t), int(dj / t))

    def isForced(self, n:tuple, d:tuple, transform = True):
        forced = []
        if (abs(d[0]) + abs(d[1]) == 1):
            if (d[0] == 0):
                upLeft = (n[0] + 1, n[1])
                upRight = (n[0] + 1, n[1] + d[1])

                downLeft = (n[0] - 1, n[1])
                downRight = (n[0] - 1, n[1] + d[1])

                if (self.inBounds(upLeft) and (not self.Traversable(upLeft))) \
                        and (self.inBounds(upRight) and self.Traversable(upRight)):
                    forced.append(upRight)
                else:
                    if (self.inBounds(downLeft) and (not self.Traversable(downLeft))) \
                            and (self.inBounds(downRight) and self.Traversable(downRight)):
                        forced.append(downRight)
            else:
                upLeft = (n[0], n[1] + 1)
                upRight = (n[0] + d[0], n[1] + 1)

                downLeft = (n[0], n[1] - 1)
                downRight = (n[0] + d[0], n[1] - 1)

                if (self.inBounds(upLeft) and (not self.Traversable(upLeft))) \
                        and (self.inBounds(upRight) and self.Traversable(upRight)):
                    forced.append(upRight)
                else:
                    if (self.inBounds(downLeft) and (not self.Traversable(downLeft))) \
                            and (self.inBounds(downRight) and self.Traversable(downRight)):
                        forced.append(downRight)
        else:
            dirs = [(d[0], 0), (0, d[1])]
            for i in dirs:
                n1 = self.Step(n, i, False)
                n2 = self.Step(n1, i, False)
                if (self.inBounds(n1) and (not self.Traversable(n1))) and (self.inBounds(n2) and self.Traversable(n2)):
                    forced.append(n2)

            for i in dirs:
                n1 = self.Step(n, i, False)
                a = self.isForced(n, i, transform=False)
                forced.extend(a)
        f = []
        if transform:
            for i in forced:
                f.append(self.GetDirection(n, i))
        else:
            f = forced
        return f

    def Step(self, x:tuple, d:tuple, check = True, back = False):
        if not back:
            t = (x[0] + d[0], x[1] + d[1])
            t1 = (x[0] + d[0], x[1])
            t2 = (x[0], x[1] + d[1])
        else:
            t = (x[0] - d[0], x[1] - d[1])
            t1 = (x[0] - d[0], x[1])
            t2 = (x[0], x[1] - d[1])
        if check:
            if (self.inBounds(t) and self.Traversable(t)):
                if (abs(d[0]) + abs(d[1]) == 1):
                    return t
                else:
                    if (self.inBounds(t1) and self.Traversable(t1) or self.inBounds(t2) and self.Traversable(t2)):
                        return t
            else:
                return None
        else:
            return t

    def Jump(self, x:tuple, d:tuple, start:tuple, goal:tuple):
        n = self.Step(x, d, check=True)
        if n is None:
            return None
        self.visited.add(n)
        if (n == goal):
            return n
        if (len(self.isForced(n, d)) != 0):
            return n
        if (abs(d[0]) + abs(d[1]) == 2):
            for di in [(d[0], 0), (0, d[1])]:
                if self.Jump(self.Step(n, di, check=False, back=True), di, start, goal):
                    return n
        return self.Jump(n, d, start, goal)

    def ComputeCost(self, i1, j1, i2, j2):
        '''
        Computes cost of simple moves between cells
        '''
        if abs(i1 - i2) == 0 or abs(j1 - j2) == 0:  # cardinal move
            return abs(i1 - i2) + abs(j1 - j2)
        else:  # diagonal move
            return math.sqrt(2) * abs(i1 - i2)

    def Draw(self, start: Node = None, goal: Node = None, path: list = None, nodesExpanded=None,
             nodesOpened=None, fileName = "test.png"):
        '''
        Auxiliary function that visualizes the enviromnet, the path and OPEN and CLOSED.
        '''
        k = 12
        hIm = self.height * k
        wIm = self.width * k
        im = Image.new('RGB', (wIm, hIm), color='white')
        draw = ImageDraw.Draw(im)
        for i in range(self.height):
            for j in range(self.width):
                if (self.cells[i][j] == 1):
                    draw.rectangle((j * k, i * k, (j + 1) * k - 1, (i + 1) * k - 1), fill=(70, 80, 80))

        if nodesOpened is not None:
            if (type(nodesOpened) == type(OpenList())):
                for h, node in nodesOpened.elements.items():
                    draw.rectangle((node.j * k, node.i * k, (node.j + 1) * k - 1, (node.i + 1) * k - 1),
                                   fill=(213, 219, 219), width=0)
            else:
                for node in nodesOpened:
                    draw.rectangle((node.j * k, node.i * k, (node.j + 1) * k - 1, (node.i + 1) * k - 1),
                                   fill=(213, 219, 219), width=0)

        if nodesExpanded is not None:
            if (type(nodesExpanded) == type(ClosedList())):
                for h, node in nodesExpanded.elements.items():
                    draw.rectangle((node.j * k, node.i * k, (node.j + 1) * k - 1, (node.i + 1) * k - 1),
                                   fill=(131, 145, 146), width=0)
            else:
                for node in nodesExpanded:
                    draw.rectangle((node.j * k, node.i * k, (node.j + 1) * k - 1, (node.i + 1) * k - 1),
                                   fill=(131, 145, 146), width=0)

        if path is not None:
            for step in path:
                if (step is not None):
                    if (self.Traversable((step.i, step.j))):
                        draw.rectangle((step.j * k, step.i * k, (step.j + 1) * k - 1, (step.i + 1) * k - 1),
                                       fill=(52, 152, 219), width=0)
                    else:
                        draw.rectangle((step.j * k, step.i * k, (step.j + 1) * k - 1, (step.i + 1) * k - 1),
                                       fill=(230, 126, 34), width=0)

        if (start is not None) and (self.Traversable((start.i, start.j))):
            draw.rectangle((start.j * k, start.i * k, (start.j + 1) * k - 1, (start.i + 1) * k - 1), fill=(40, 180, 99),
                           width=0)

        if (goal is not None) and (self.Traversable((goal.i, goal.j))):
            draw.rectangle((goal.j * k, goal.i * k, (goal.j + 1) * k - 1, (goal.i + 1) * k - 1), fill=(231, 76, 60),
                           width=0)

        for i in self.visited:
            draw.rectangle((i[1] * k + int(k/3), i[0] * k + int(k/3), (i[1] + 1) * k - 1 - int(k/3), (i[0] + 1) * k - 1 - int(k/3)),
                           fill=(255, 255, 100), width=0)

        if path is not None:
            for i in range(len(path) - 1):
                draw.line(((path[i].j + 0.5) * k, (path[i].i + 0.5) * k, (path[i+1].j + 0.5) * k, (path[i+1].i + 0.5) * k),
                                       fill=(0, 0, 255), width=5)

        fig, ax = plt.subplots(dpi=300)
        ax.axes.xaxis.set_visible(False)
        ax.axes.yaxis.set_visible(False)
        plt.imshow(np.asarray(im))
        #plt.show()
        plt.savefig(fileName)
        plt.close()



