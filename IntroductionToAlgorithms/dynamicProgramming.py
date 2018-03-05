import random


def createArray(numRange,itemNum):
    A = list(range(1, numRange))
    randomList = []
    for i in range(0,itemNum):
        key = random.randint(0,len(A)-1)
        randomList.append(A[key])
        del A[key]
    randomList.insert(0, 0)
    return randomList

def matrixChainOrder(matrixSizeList):
    matrixNum = len(matrixSizeList) - 1
    costMatrix = [[0 for i in range(0,matrixNum)] for i in range(0,matrixNum)]
    positionMatrix = [[0 for i in range(0,matrixNum)] for i in range(0,matrixNum)]
    for chainSize in range(2,matrixNum+1):
        for startMatrix in range(0,matrixNum - chainSize + 1):
            endMatrix = startMatrix + chainSize - 1
            for divivepoint in range(startMatrix,endMatrix):
                cost = costMatrix[startMatrix][divivepoint] + costMatrix[divivepoint + 1][endMatrix] + \
                       matrixSizeList[startMatrix] * matrixSizeList[divivepoint + 1] * matrixSizeList[endMatrix + 1]
                if costMatrix[startMatrix][endMatrix] == 0:
                    costMatrix[startMatrix][endMatrix] = cost
                    positionMatrix[startMatrix][endMatrix] = divivepoint+1
                elif cost < costMatrix[startMatrix][endMatrix]:
                    costMatrix[startMatrix][endMatrix] = cost
                    positionMatrix[startMatrix][endMatrix] = divivepoint+1
    return costMatrix,positionMatrix

def LCSlength(listX,listY):
    lengthX = len(listX)
    lengthY = len(listY)
    LCStable = [[0 for i in range(0,lengthY + 1)] for i in range(0,lengthX + 1)]
    for x in range(0,lengthX):
        for y in range(0,lengthY):
            if listX[x] == listY[y]:
                LCStable[x + 1][y + 1] = LCStable[x][y] + 1

            elif LCStable[x][y + 1] < LCStable[x + 1][y]:
                LCStable[x + 1][y + 1] = LCStable[x + 1][y]
            else:
                LCStable[x + 1][y + 1] = LCStable[x][y + 1]

    return LCStable

list1 = [1,8,9,6,7,5,4,9,3,4,9,4,7,5,6,4,8,3,8,7]
list2 = [1,8,7,6,7,2,7,8,9,6,3,4,6,7,5,8,2,9,4,6,9]

