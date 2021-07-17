import random
import copy as cpy
import math
import statistics

def printSudoku(sudoku):
    for i in range(0, 9, 1):
        selectedIndex = i - i % 3
        index = i%3
        index *= 3
        for j in range(0, 3, 1):
            selected = sudoku[selectedIndex + j]
            for k in range(0, 3, 1):
                print(selected[index + k], end = ' ')
            if (j != 2):
                print("|", end=' ')
        print()
        if (i == 2 or i == 5):
            print("---------------------")

def getFixed(sudoku):
    fixed = [[0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0],
             [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0],
             [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0]]
    for i in range(0, 9, 1):
        for j in range(0, 9, 1):
            if sudoku[i][j] != 0:
                fixed[i][j] = 1
    return fixed

def fillSudoku(sudoku):
    for i in range(0, 9, 1):
        selected = sudoku[i]
        free = [1, 2, 3, 4, 5, 6, 7, 8, 9]
        for j in range(0, 9, 1):
            if selected[j] != 0:
                free.remove(selected[j])
        length = len(free) - 1
        for j in range(0, 9, 1):
            if selected[j] == 0:
                index = random.randint(0, length)
                selected[j] = free[index]
                free.remove(free[index])
                length -= 1

def heuristic(sudoku):
    cost = 0
    for i in range(0, 9, 1):
        row = getRow(sudoku, i)
        column = getColumn(sudoku, i)
        takenRow = []
        takenColumn = []
        for j in range(0, 9, 1):
            if row[j] in takenRow:
                cost += 1
            else:
                takenRow.append(row[j])
            if column[j] in takenColumn:
                cost += 1
            else:
                takenColumn.append(column[j])
    return cost

def getRow(sudoku, index):
    row = []
    selectedIndex = index - index%3
    index %= 3
    index *= 3
    for j in range(0, 3, 1):
        selected = sudoku[selectedIndex + j]
        for k in range(0, 3, 1):
            row.append(selected[index + k])
    return row
def getColumn(sudoku, index):
    column = []
    selectedIndex = int(index/3)
    index %= 3
    for j in range(0, 7, 3):
        selected = sudoku[selectedIndex + j]
        for k in range(0, 7, 3):
            column.append(selected[index + k])
    return column

def newSudoku(sudoku, fixed):
    sudokuNew = cpy.deepcopy(sudoku)
    block = random.randint(0, 8)
    selected = sudokuNew[block]
    flip(selected, fixed[block])
    return sudokuNew

def flip(block, fixed):
    free = [0, 1, 2, 3, 4, 5, 6, 7, 8]
    for i in range(0, 9, 1):
        if fixed[i] == 1:
            free.remove(i)
    index1 = free[random.randint(0, len(free) - 1)]
    free.remove(index1)
    index2 = free[random.randint(0, len(free) - 1)]

    hulp = block[index1]
    block[index1] = block[index2]
    block[index2] = hulp

def chooseSudoku(sudoku, newSudoku, temp):
    precost = heuristic(sudoku)
    postcost = heuristic(newSudoku)

    delta = postcost - precost
    P = math.exp(-delta/temp)
    if (random.random() <= P):
        return newSudoku
    return sudoku

def numberIterations(fixed):
    numberIterations = 0
    for i in range(0, 9, 1):
        for j in range(0, 9, 1):
            if fixed[i][j] != 0:
                numberIterations += 1
    return numberIterations

def initialTemp(sudoku, fixed):
    costs = []
    for i in range(0, 10, 1):
        temporarySudoku = newSudoku(sudoku, fixed)
        costs.append(heuristic(temporarySudoku))
    initial = statistics.pstdev(costs)
    return initial

def solve(sudoku):
    fixed = getFixed(sudoku)
    fillSudoku(sudoku)
    temp = initialTemp(sudoku, fixed)
    iterations = numberIterations(fixed)
    coolingFactor = 0.99
    stuckCount = 0
    cost = heuristic(sudoku)
    if cost == 0:
        return True

    succes = False

    while succes == False:
        previousCost = cost
        for i in range(0, iterations, 1):
            newsudoku = newSudoku(sudoku, fixed)
            sudoku = chooseSudoku(sudoku, newsudoku, temp)
            cost = heuristic(sudoku)
            if cost == 0:
                succes = True
                break
        temp *= coolingFactor

        if cost >= previousCost:
            stuckCount += 1
        else:
            stuckCount = 0

        if stuckCount > 80:
            temp *= 2
    return sudoku



def main():
    sudoku =    [[0, 9, 0, 2, 0, 8, 7, 0, 3], [0, 0, 2, 0, 4, 0, 1, 0, 6], [0, 1, 0, 9, 3, 0, 8, 0, 0],
                [0, 0, 0, 1, 8, 5, 0, 7, 4], [3, 0, 0, 0, 2, 9, 0, 0, 1], [1, 4, 5, 6, 0, 0, 2, 0, 8],
                [0, 0, 0, 5, 0, 0, 8, 0, 0], [2, 0, 0, 9, 0, 0, 6, 0, 3], [0, 8, 0, 7, 6, 2, 0, 0, 0]]
    printSudoku(sudoku)
    print("\n")
    print("\n")
    print("\n")
    opl = solve(sudoku)
    printSudoku(opl)

main()