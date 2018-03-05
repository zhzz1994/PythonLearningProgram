import random
countfun = 0

def createArray(numRange,itemNum):
    A = list(range(1, numRange))
    randomList = []
    for i in range(0,itemNum):
        key = random.randint(0,len(A)-1)
        randomList.append(A[key])
        del A[key]
    randomList.insert(0, 0)
    return randomList

def exchangeitem(a,b):
    return b,a


def MaxHeapify(A,i,heapSize):
    leftSon = 2*i
    rightSon = 2*i+1
    largest = i
    if leftSon <= heapSize and (A[leftSon] > A[i]):
        largest = leftSon
    if rightSon <= heapSize and (A[rightSon] > A[largest]) :
        largest = rightSon
    if largest != i:
        n = A[i]
        A[i] = A[largest]
        A[largest] = n
        MaxHeapify(A,largest,heapSize)
    global countfun
    countfun = countfun + 1

def BuildMaxHeap(A,heapSize):
    if heapSize%2 == 0:
        length = heapSize/2
    else:
        length = (heapSize - 1)/2
    length = int(length)
    for item in range(length,0,-1):
        MaxHeapify(A,item,heapSize)

def heapSort(A):
    heapSize = len(A) - 1
    BuildMaxHeap(A,heapSize)
    for lastitem in range(heapSize,1,-1):
        n = A[lastitem]
        A[lastitem] = A[1]
        A[1] = n
        heapSize = heapSize - 1
        MaxHeapify(A,1,heapSize)

def quickSort(A,startitem,enditem):
    if startitem < enditem:
        divive = partition(A,startitem,enditem)
        quickSort(A,startitem,divive-1)
        quickSort(A,divive+1,enditem)

def partition(A,startitem,enditem):
    if startitem == enditem:
        return startitem
    middleitem = A[enditem]
    divive = startitem - 1
    for item in range(startitem,enditem):
        if A[item] <= middleitem:
            divive = divive + 1
            A[item], A[divive] = exchangeitem(A[item],A[divive])
        global countfun
        countfun = countfun + 1
    if (divive + 1) < enditem:
        A[divive + 1], A[enditem] = exchangeitem(A[divive +1],A[enditem])
    return divive+1

def countingSort(A,biggestnum):
    CountList = list(range(0,biggestnum))
    B = A.copy()   #列表复制
    for key in range(0,biggestnum):
        CountList[key] = 0
    for item in A:
        CountList[item] = CountList[item] + 1
    for i in range(1,biggestnum):
        CountList[i] = CountList[i] + CountList[i - 1]
    for key in range(0,biggestnum):
        CountList[key] = CountList[key] - 1
    print(CountList)
    print(A)
    for item in A:
        print('item = %s',item)
        B[CountList[item]] = item
    return B

def ramdomSelect(A,startitem,enditem,finditem):
    if startitem == enditem :
        return A[startitem]
    divive = partition(A, startitem, enditem)
    if finditem == (divive + 1):
        return A[divive]
    elif finditem <= divive + 1 :
        return ramdomSelect(A,startitem,divive - 1,finditem)
    else:
        return ramdomSelect(A,divive+1,enditem,finditem)





A = createArray(20,10)
print(A)
#heapSort(A)
# print(ramdomSelect(A,1,len(A)-1,11))
# quickSort(A,1,len(A)-1)
B = countingSort(A,20)


print(B)





