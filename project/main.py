from random import randint

import matplotlib.pyplot as plt

from algs import *
from Node import Node
from Map import *
from OpenList import *
from ClosedList import *
import time
import sys

def MakePath(goal):
    '''
    Creates a path by tracing parent pointers from the goal node to the start node
    It also returns path's length.
    '''

    length = goal.g
    current = goal
    path = []
    while current.parent:
        path.append(current)
        current = current.parent
    path.append(current)
    return path[::-1], length

def ReadTaskFromFile(path):
    '''
    Reads map, start/goal positions and true value of path length between given start and goal from file by path.
    '''

    tasksFile = open(path)
    count = 0
    height = int(tasksFile.readline())
    width = int(tasksFile.readline())
    cells = [[0 for _ in range(width)] for _ in range(height)]
    i = 0
    j = 0

    for l in tasksFile:
        j = 0
        for c in l:
            if c == '.':
                cells[i][j] = 0
            elif c == '#':
                cells[i][j] = 1
            else:
                continue

            j += 1

        if j != width:
            raise Exception("Size Error. Map width = ", j, ", but must be", width, "(map line: ", i, ")")

        i += 1
        if (i == height):
            break

    iStart = int(tasksFile.readline())
    jStart = int(tasksFile.readline())
    iGoal = int(tasksFile.readline())
    jGoal = int(tasksFile.readline())
    cardinalLength = float(tasksFile.readline())
    diagonalLength = float(tasksFile.readline())
    return (width, height, cells, iStart, jStart, iGoal, jGoal, cardinalLength, diagonalLength)

def SimpleTest(SearchFunction, task, *args):
    '''
    SimpleTest runs SearchFunction on one task (use a number from 0 to 25 to choose a certain debug task on simple map or None to choose a random task from this pool) with *args as optional arguments and displays:
     - 'Path found!' and some statistics -- path was found
     - 'Path not found!' -- path was not found
     - 'Execution error' -- an error occurred while executing the SearchFunction In first two cases function also draws visualisation of the task

    '''

    height = 15
    width = 30
    mapstr = '''
. . . . . . . . . . . . . . . . . . . . . # # . . . . . . .  
. . . . . . . . . . . . . . . . . . . . . # # . . . . . . . 
. . . . . . . . . . . . . . . . . . . . . # # . . . . . . . 
. . . # # . . . . . . . . . . . . . . . . # # . . . . . . . 
. . . # # . . . . . . . . # # . . . . . . # # . . . . . . . 
. . . # # . . . . . . . . # # . . . . . . # # # # # . . . . 
. . . # # . . . . . . . . # # . . . . . . # # # # # . . . . 
. . . # # . . . . . . . . # # . . . . . . . . . . . . . . . 
. . . # # . . . . . . . . # # . . . . . . . . . . . . . . . 
. . . # # . . . . . . . . # # . . . . . . . . . . . . . . . 
. . . # # . . . . . . . . # # . . . . . . . . . . . . . . . 
. . . # # . . . . . . . . # # . . . . . . . . . . . . . . . 
. . . . . . . . . . . . . # # . . . . . . . . . . . . . . . 
. . . . . . . . . . . . . # # . . . . . . . . . . . . . . .
. . . . . . . . . . . . . # # . . . . . . . . . . . . . . .
'''

    taskMap = Map()
    taskMap.ReadFromString(mapstr, width, height)
    starts = [(9, 0), (13, 0), (7, 28), (14, 29), (4, 1), (0, 17), (5, 6), (5, 20), (12, 2), (7, 28), (11, 9), (3, 2),
              (3, 17), (13, 20), (1, 1), (9, 10), (14, 6), (2, 0), (9, 28), (8, 6), (11, 6), (3, 0), (8, 9), (14, 7),
              (12, 4)]
    goals = [(11, 20), (2, 19), (6, 5), (4, 18), (9, 20), (7, 0), (2, 25), (12, 4), (3, 25), (0, 12), (4, 23), (2, 24),
             (9, 2), (1, 6), (13, 29), (14, 29), (2, 28), (14, 16), (13, 0), (1, 27), (14, 25), (10, 20), (12, 28),
             (2, 29), (1, 29)]
    diagLengths = [29.4558441227, 23.5563491861, 25.8994949366, 15.1421356237, 22.7279220614,
                   21.0710678119, 27.3137084990, 20.5563491861, 33.2132034356, 18.8994949366,
                   29.1421356237, 31.7279220614, 21.1421356237, 21.3137084990, 32.9705627485,
                   27.7989898732, 33.7989898732, 26.2426406871, 34.6274169980, 29.5563491861,
                   27.4558441227, 24.3137084990, 25.3847763109, 33.7989898732, 34.0416305603]

    if (task is None) or not (0 <= task < 25):
        task = randint(0, 24)

    start = Node(*starts[task])
    goal = Node(*goals[task])
    diagLength = diagLengths[task]
    #rs = AStar(taskMap, start.i, start.j, goal.i, goal.j, *args)
    #path = MakePath(rs[1])
    #diagLength = path[1]
    startTime = time.time()
    try:
        result = SearchFunction(taskMap, start.i, start.j, goal.i, goal.j, *args)
        nodesExpanded = result[2]
        nodesOpened = result[3]
        if result[0]:
            path = MakePath(result[1])
            correct = (abs(float(path[1]) - float(diagLength)) < 1e-6)
            taskMap.Draw(start, goal, path[0], nodesExpanded, nodesOpened, "SimpleTest/{}.png".format(task))
            # print("Path found! Length: " + str(path[1]) + ". Nodes created: " + str(len(nodesOpened) + len(nodesExpanded)) + ". Number of steps: " + str(len(nodesExpanded)) + ". Correct: " + str(correct))
            print("{:2d}) Path found! Length: {:7.3f}. Nodes created: {:8d}. Number of steps: {:8d}. Correct: {:5s}. Correct result: {:7.3f}".format(
                task, path[1], len(nodesOpened) + len(nodesExpanded), len(nodesExpanded), str(correct), diagLength))
        else:
            print("Path not found!")

    except Exception as e:
        print("Execution error")
        tb = sys.exc_info()[2]
        print(e)
        raise e.with_traceback(tb)
    finishTime = time.time()
    print('Execution time: {:8.3f} ms'.format((finishTime - startTime) * 1000))

def MassiveTest(SearchFunction, *args):
    '''
    MassiveTest runs SearchFunction on set of differnt tasks (from directory Data/) with *args as optional arguments and for every task displays one of these short reports:
     - 'Path found!' and some statistics -- path was found
     - 'Path not found!' -- path was not found
     - 'Execution error' -- an error occurred while executing the SearchFunction In first two cases function also draws visualisation of the task.

    Massive test return a dictionary with statistics of path finding. Dictionary contains next fields:
     - "corr" -- the correctness of every path length (True/False)
     - "len" -- the length of every path (0.0 if path not found)
     - "nc" -- the number of created nodes for every task execution
     - "st" -- the number of steps of algorithm for every task execution
    '''

    stat = dict()
    stat["corr"] = []
    stat["len"] = []
    stat["nc"] = []
    stat["st"] = []
    stat["time"] = []
    times = []
    taskNum = 9
    taskMap = Map()
    cor = 0
    for taskCount in range(taskNum):
        taskMap.visited.clear()
        taskFileName = "Data/" + str(taskCount) + ".map"
        width, height, cells, iStart, jStart, iGoal, jGoal, cardinalLength, diagonalLength = ReadTaskFromFile(
            taskFileName)
        taskMap.SetGridCells(width, height, cells)
        #rs = AStar(taskMap, iStart, jStart, iGoal, jGoal, *args)
        #path2 = MakePath(rs[1])
        #diagonalLength = path2[1]
        startTime = time.time()
        try:
            result = SearchFunction(taskMap, iStart, jStart, iGoal, jGoal, *args)
            nodesExpanded = result[2]
            nodesOpened = result[3]
            if result[0]:
                path = MakePath(result[1])
                stat["len"].append(path[1])
                correct = (int(path[1]) == int(cardinalLength) or abs(float(path[1]) - float(diagonalLength)) < 1e-6)
                stat["corr"].append(correct)
                #taskMap.Draw(Node(iStart, jStart), Node(iGoal, jGoal), path[0], nodesExpanded, nodesOpened, "MassiveTest/{}.png".format(taskCount))
                # print("Path found! Length: " + str(path[1]) + ". Nodes created: " + str(len(nodesOpened) + len(nodesExpanded)) + ". Number of steps: " + str(len(nodesExpanded)) + ". Correct: " + str(correct))
                print(
                    "{:2d}) Path found! Length: {:7.3f}. Nodes created: {:8d}. Number of steps: {:8d}. Correct: {:5s}. Correct result: {:7.3f}".format(
                        taskCount, path[1], len(nodesOpened) + len(nodesExpanded), len(nodesExpanded), str(correct), diagonalLength))
                cor += 1 if correct else 0
            else:
                #taskMap.Draw(Node(iStart, jStart), Node(iGoal, jGoal), [], nodesExpanded, nodesOpened, "MassiveTest/{}.png".format(taskCount))
                print("{:2d}) Path not found! Correct result: {:14.10f}".format(taskCount, diagonalLength))
                stat["corr"].append(False)
                stat["len"].append(0.0)

            stat["nc"].append(len(nodesOpened) + len(nodesExpanded))
            stat["st"].append(len(nodesExpanded))

        except Exception as e:
            print("Execution error")
            tb = sys.exc_info()[2]
            print(e)
            raise e.with_traceback(tb)

        finishTime = time.time()
        stat["time"].append(finishTime - startTime)
        print('Execution time: {:5.3f} ms'.format((finishTime - startTime) * 1000))
        times.append(finishTime-startTime)

    print("Statistic: {:1d}/{:1d} ({:5.2f}%). Execution time: {:5.3}s.".format(cor, 9, cor/9*100, sum(times)))
    return stat

print("Simple Tests:")
for i in range(25):
    SimpleTest(JPS, i, EuclideanDistance)

print("\n\nMassive Tests JPS:")
masJPS = MassiveTest(JPS, EuclideanDistance)
#
# print("\n\nMassive Tests AStar:")
# masAStar = MassiveTest(AStar, EuclideanDistance)
#
# fig, axs = plt.subplots(3, 3, figsize=(15,10))
# fig.suptitle('Average number of created nodes')
# for i in range(9):
#     ax = axs[i // 3, i % 3]
#     ax.set_title(str(i) + " task")
#     alg = ['A*', 'JPS']
#     lens = [masAStar['nc'][i], masJPS['nc'][i]]
#     ax.bar(alg, lens)
# plt.savefig("Average number of created nodes.png")
# plt.close()
#
# fig, axs = plt.subplots(3, 3, figsize=(15,10))
# fig.suptitle('Average number of steps')
# for i in range(9):
#     ax = axs[i // 3, i % 3]
#     ax.set_title(str(i) + " task")
#     alg = ['A*', 'JPS']
#     lens = [masAStar['st'][i], masJPS['st'][i]]
#     ax.bar(alg, lens)
# plt.savefig("Average number of steps.png")
# plt.close()
#
# fig, axs = plt.subplots(3, 3, figsize=(15,10))
# fig.suptitle('Average time')
# for i in range(9):
#     ax = axs[i // 3, i % 3]
#     ax.set_title(str(i) + " task")
#     alg = ['A*', 'JPS']
#     lens = [masAStar['time'][i], masJPS['time'][i]]
#     ax.bar(alg, lens)
# plt.savefig("Average time.png")
# plt.close()