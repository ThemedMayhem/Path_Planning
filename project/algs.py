from OpenList import *
from ClosedList import *
from Node import *
from Map import *


def AStar(gridMap: Map, iStart: int, jStart: int, iGoal: int, jGoal: int, hFunc=ManhattanDistance, diagonalMoves = True):
    OPEN = OpenList()
    CLOSED = ClosedList()
    start = Node(iStart, jStart)
    OPEN.AddNode(start)
    while not OPEN.isEmpty():
        curNode = OPEN.GetBestNode()
        CLOSED.AddNode(curNode)
        if ((curNode.i, curNode.j) == (iGoal, jGoal)):
            return (True, curNode, CLOSED, OPEN)
        neighbors = gridMap.GetNeighbors(curNode.i, curNode.j, diagonalMoves = True)
        for n in neighbors:
            newNode = Node(n[0], n[1])
            newNode.g = curNode.g + gridMap.ComputeCost(curNode.i, curNode.j, newNode.i, newNode.j)
            newNode.h = hFunc(newNode.i, newNode.j, iGoal, jGoal)
            newNode.F = newNode.g + newNode.h
            newNode.parent = curNode
            if CLOSED.WasExpanded(newNode):
                continue
            OPEN.AddNode(newNode)

    return (False, None, CLOSED, OPEN)

def drawMiniMap(gridMap : Map, curNode:Node, ds:list, fileName = ''):
    k = 50
    hIm = 5 * k
    wIm = 5 * k
    im = Image.new('RGB', (wIm, hIm), color='white')
    draw = ImageDraw.Draw(im)

    c = 0
    for ki in range(max(0, curNode.i-1), curNode.i+4):
        for kj in range(max(0, curNode.j-1), curNode.j+4):
            if (gridMap.cells[ki][kj] == 1):
                c += 1
                i = ki - max(0, curNode.i - 1)
                j = kj - (curNode.j - 1)
                draw.rectangle((j * k, i * k, (j + 1) * k - 1, (i + 1) * k - 1), fill=(70, 80, 80))
    if (curNode.parent is not None):
        df = gridMap.GetDirection((curNode.parent.i, curNode.parent.j), (curNode.i, curNode.j))
    else:
        df = (0, 1)
    if c>0: #and (abs(df[0]) + abs(df[1]) == 1):
        di = curNode.i - 1
        dj = curNode.j - 1
        draw.rectangle(((curNode.j - dj) * k, (curNode.i - di) * k, (curNode.j - dj + 1) * k - 1, (curNode.i - di + 1) * k - 1), fill=(255, 255, 255),
                       outline=(0, 255, 0), width=5)
        if (curNode.parent is not None):
            draw.rectangle(
                ((curNode.parent.j - dj) * k, (curNode.parent.i - di) * k,
                 (curNode.parent.j - dj + 1) * k - 1, (curNode.parent.i - di + 1) * k - 1), fill=(255, 255, 255),
                outline=(255, 0, 0), width=5)
            draw.line(
                ((curNode.parent.j - dj + 0.5) * k, (curNode.parent.i - di + 0.5) * k, (curNode.j - dj + 0.5) * k - 1, (curNode.i - di + 0.5) * k - 1),
                width=5, fill=(255, 0, 0))
        for i in ds:
            draw.rectangle(
                ((curNode.j - dj + i[1]) * k  + 5, (curNode.i - di + i[0]) * k + 5,
                 (curNode.j - dj + 1 + i[1]) * k - 1 - 5, (curNode.i - di + 1 + i[0]) * k - 1 - 5), fill=(0, 0, 255),
                outline=(255, 0, 0), width=0)

        fig, ax = plt.subplots(dpi=500)
        ax.axes.xaxis.set_visible(False)
        ax.axes.yaxis.set_visible(False)
        plt.imshow(np.asarray(im))
        plt.savefig(fileName)
    plt.close()

def JPS(gridMap : Map, iStart : int, jStart : int, iGoal : int, jGoal : int, hFunc = ManhattanDistance, diagonalMoves = True):

    OPEN = OpenList()
    CLOSED = ClosedList()
    start = Node(iStart, jStart)
    start.h = hFunc(iStart, jStart, iGoal, jGoal),
    goal = Node(iGoal, jGoal, g = math.inf)
    OPEN.AddNode(start)
    while not OPEN.isEmpty():
        curNode = OPEN.GetBestNode()
        CLOSED.AddNode(curNode)
        if (curNode == goal):
            return (True, curNode, CLOSED, OPEN)
        if (curNode.parent is None):
            ds = [(0, 1), (-1, 0), (0, -1), (1, 0), (-1, 1), (-1, -1), (1, -1), (1, 1)]
        else:
            prev = (curNode.parent.i, curNode.parent.j)
            cur = (curNode.i, curNode.j)
            d = gridMap.GetDirection(prev, cur)
            ds = [d]
            if (abs(d[0])+abs(d[1]))==2:
                ds.append((d[0], 0))
                ds.append((0, d[1]))
            ds.extend(gridMap.isForced(cur, d))
            ds = list(set(ds))
        #drawMiniMap(gridMap, curNode, ds, 'miniMaps/{:d}.png'.format(q))
        for n in ds:
            nn = gridMap.Jump((curNode.i, curNode.j), n, (iStart, jStart), (iGoal, jGoal))
            if (nn):
                newNode = Node(nn[0], nn[1])
                newNode.g = curNode.g + gridMap.ComputeCost(curNode.i, curNode.j, newNode.i, newNode.j)
                newNode.h = hFunc(newNode.i, newNode.j, iGoal, jGoal)
                newNode.F = newNode.g + newNode.h
                newNode.parent = curNode
                if CLOSED.WasExpanded(newNode):
                    continue
                OPEN.AddNode(newNode)

    return (False, None, CLOSED, OPEN)