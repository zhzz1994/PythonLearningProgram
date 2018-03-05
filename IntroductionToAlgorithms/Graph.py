import copy


class linkList():
    def __init__(self):
        self.size = 0
        self.head = None

    def insertOne(self, node):
        if self.head:
            if self.head.next:
                node.next = self.head.next
                self.head.next.prev = node
            self.head.next = node
            node.prev = self.head
        else:
            self.head = node
        self.size = self.size + 1

    def insert(self, *nodes):
        for node in nodes:
            self.insertOne(node)

    def linkList2List(self):
        list = []
        find = self.head
        while find:
            list.append(find)
            find = find.next
        return list

    def remove(self, node):
        pass

class queue():
    def __init__(self, size):
        self.size = size
        self.items = [None for num in range(0, self.size)]
        self.headkey = 0
        self.tailkey = 0

    def enQueue(self, item):
        if self.items[self.tailkey] != None:
            print('queue is full')
        else:
            self.items[self.tailkey] = item
            if self.tailkey == self.size - 1:
                self.tailkey = 0
            else:
                self.tailkey = self.tailkey + 1

    def deQueue(self):
        if self.items[self.headkey] == None:
            print('queue is empty')
        else:
            find = self.items[self.headkey]
            if self.headkey == self.size - 1:
                self.headkey = 0
            else:
                self.headkey = self.headkey + 1
            return find

    def isEmpty(self):
        return self.items[self.headkey] == None

    def hasItems(self):
        return self.items[self.headkey] != None

class PointNode():
    def __init__(self, point, weight=1):
        self.point = point
        self.prev = None
        self.next = None
        self.weight = weight

class Point():
    def __init__(self, name):
        self.color = 'white'
        self.deep = -1
        self.before = None
        self.neighbor = linkList()
        self.neighborInverse = linkList()
        self.name = name
        self.findTime = 0
        self.finishTime = 0
        self.setParent = None
        self.setRank = 0
        self.distance = 1000000

    def addEdge(self, point , weight = 1):
        self.neighbor.insert(PointNode(point,weight))

    def Point2PointNode(self):
        return PointNode(self)

    def addInverseEdge(self, *edges):
        for point in edges:
            self.neighborInverse.insert(PointNode(point))

    def findSet(self):
        if self.setParent == None:
            return self
        else:
            return self.setParent.findSet()

    def unionSet(self, other):
        mySet = self.findSet()
        otherSet = other.findSet()
        if mySet.setRank < otherSet.setRank:
            mySet.setParent = otherSet
        elif mySet.setRank == otherSet.setRank:
            otherSet.setParent = mySet
            mySet.setRank = mySet.setRank + 1
        else:
            otherSet.setParent = mySet

class Edge():
    def __init__(self, head, tail, weight=1, direct=False):
        self.head = head
        self.tail = tail
        self.weight = weight
        self.direct = direct
        self.flow = 0

    def appendOnPoint(self):
        self.head.addEdge(self.tail,self.weight)
        if self.direct == False:
            self.tail.addEdge(self.head,self.weight)

    def printEdge(self):
        print(self.head.name, '----->', self.tail.name, 'weight = ', self.weight)

class MinHeap():
    def __init__(self,firstSmaller):
        self.heap = []
        self.size = 0
        self.firstSmaller = firstSmaller

    def heapInsert(self,*items):
        for item in items:
            self.heap.append(item)
            self.size = self.size + 1

    def mimHeapify(self,index):
        leftSon = 2 * index
        rightSon = 2 * index + 1
        mininum = index-1
        if leftSon < self.size -1 and self.firstSmaller(self.heap[leftSon-1],self.heap[mininum]):
            mininum = leftSon-1
        if rightSon < self.size - 1 and self.firstSmaller(self.heap[rightSon - 1],self.heap[mininum]):
            mininum = rightSon - 1
        if index-1 != mininum:
            top = self.heap[index - 1]
            self.heap[index - 1] = self.heap[mininum]
            self.heap[mininum] = top
            self.mimHeapify(mininum)

    def buildMimHeap(self):
        length = int(self.size/2)
        for item in range(length, 0, -1):
            self.mimHeapify(item)

    def extractMin(self):
        min = self.heap[0]
        self.heap[0] = self.heap[-1]
        self.heap.pop()
        self.mimHeapify(1)
        self.size = self.size - 1
        return min

class Graph():
    def __init__(self, queunSize=10):
        self.point = None
        self.pointSize = 0
        self.points = []
        self.queun = queue(queunSize)
        self.start = None
        self.timeStamp = 0
        self.SCCs = {}
        self.SCCindex = []
        self.edegs = []
        self.weightArray = [[]]
        self.fastPath = [[]]
        self.fastPathParent = [[]]

    def insertPoint(self, *points):
        for point in points:
            self.points.append(point)

    def BFS(self, start):
        self.start = start
        start.color = 'gray'
        start.deep = 0
        self.queun.enQueue(start)
        while self.queun.hasItems():
            standPoint = self.queun.deQueue()
            if standPoint.neighbor.head:
                watchPoint = standPoint.neighbor.head
                if watchPoint.point.color == 'white':
                    watchPoint.point.color = 'gray'
                    watchPoint.point.deep = standPoint.deep + 1
                    watchPoint.point.before = standPoint
                    self.queun.enQueue(watchPoint.point)
                while watchPoint.next:
                    watchPoint = watchPoint.next
                    if watchPoint.point.color == 'white':
                        watchPoint.point.color = 'gray'
                        watchPoint.point.deep = standPoint.deep + 1
                        watchPoint.point.before = standPoint
                        self.queun.enQueue(watchPoint.point)
            standPoint.color = 'black'

    def BFSprintPath(self, From, To):
        if From == To:
            print(From.name)
        elif To.before == None:
            print('there is no way from', From.name, 'to', To.name)
        else:
            self.printPath(From, To.before)
            print(To.name)

    def DFS(self):
        for point in self.points:
            point.color = 'white'
            point.before = None
        self.timeStamp = 0
        for point in self.points:
            if point.color == 'white':
                self.DFSvisit(point)

    def DFSvisit(self, point):
        self.timeStamp = self.timeStamp + 1
        point.findTime = self.timeStamp
        point.color = 'gray'
        if point.neighbor.head:
            for neighborPointNode in point.neighbor.linkList2List():
                if neighborPointNode.point.color == 'white':
                    neighborPointNode.point.before = point
                    self.DFSvisit(neighborPointNode.point)
        point.color = 'black'
        self.timeStamp = self.timeStamp + 1
        point.finishTime = self.timeStamp

    def inverseGraph(self):
        for point in self.points:
            if point.neighbor.head:
                for neighborPointNode in point.neighbor.linkList2List():
                    neighborPointNode.point.addInverseEdge(point)

    def DFSinverse(self):
        self.inverseGraph()
        sortedPoints = sorted(self.points, key=lambda point: point.finishTime, reverse=True)
        for point in sortedPoints:
            point.color = 'white'
            point.before = None
            point.finishTime = 0
            point.findTime = 0
        self.timeStamp = 0
        for point in sortedPoints:
            if point.color == 'white':
                self.SCCindex.append(point)
                self.DFSinverseVisit(point)

    def DFSinverseVisit(self, point):
        self.timeStamp = self.timeStamp + 1
        point.findTime = self.timeStamp
        point.color = 'gray'
        if point.neighborInverse.head:
            for neighborPointNode in point.neighborInverse.linkList2List():
                if neighborPointNode.point.color == 'white':
                    neighborPointNode.point.before = point
                    self.DFSinverseVisit(neighborPointNode.point)
        point.color = 'black'
        self.timeStamp = self.timeStamp + 1
        point.finishTime = self.timeStamp

    def findSCC(self):
        self.DFS()
        self.DFSinverse()
        sortedPoints = sorted(self.points, key=lambda point: point.finishTime, reverse=False)  # reverse=False 为从小到大排序
        for index in self.SCCindex:
            self.SCCs[index.name] = {}
            self.SCCs[index.name][index.name] = index
        index = 0
        for point in sortedPoints:
            if point != self.SCCindex[index]:
                self.SCCs[self.SCCindex[index].name][point.name] = point
            else:
                index = index + 1

    def addWeightEdges(self,*edges):
        for edge in edges:
            edge.appendOnPoint()
            self.edegs.append(edge)

    def MST(self):
        sortedEdges = sorted(self.edegs, key=lambda edge : edge.weight, reverse=False)
        edgeSet = []
        for edge in sortedEdges:
            if edge.head.findSet() != edge.tail.findSet():
                edge.head.unionSet(edge.tail)
                edgeSet.append(edge)
        return edgeSet

    def MSTtree(self):
        edgeSet = self.MST()
        pass

    def Dijkstra(self,start):
        for point in self.points:
            point.distance = 1000000
            point.before = None
        start.distance = 0
        heap = MinHeap(firstSmaller)
        heap.heapInsert(*self.points)
        heap.buildMimHeap()
        while heap.size >0:
            point = heap.extractMin()
            for join in point.neighbor.linkList2List():
                if join.point.distance > point.distance + join.weight:
                    join.point.distance = point.distance + join.weight

    def creatByArray(self,points,array):
        self.weightArray = array
        for point in points:
            self.points.append(Point(point))
        for row in range(0,len(self.points)):
            for column in range(0,len(self.points)):
                if array[row][column] and row != column:
                    self.points[row].addEdge(self.points[column],array[row][column])

    def creatGraphArray(self):
        self.weightArray = [[1000000 for num in range(0,len(self.points))] for num in range(0,len(self.points))]
        for num in range(0, len(self.points)):
            self.weightArray[num][num] = 0
        for edge in self.edegs:
            indexrow = self.points.index(edge.head)
            indexcolumn = self.points.index(edge.tail)
            self.weightArray[indexrow][indexcolumn] = edge.weight
        return self.weightArray

    def fastPathForAllPoints(self):
        self.fastPath = self.weightArray.copy()
        self.fastPathParent = [[None for num in range(0,len(self.points))] for num in range(0,len(self.points))]
        for edge in self.edegs:
            indexrow = self.points.index(edge.head)
            indexcolumn = self.points.index(edge.tail)
            self.fastPathParent[indexrow][indexcolumn] = edge.head
        for point in range(0,len(self.points)):
            fastPath = copy.deepcopy(self.fastPath)
            for row in range(0, len(self.points)):
                for column in range(0, len(self.points)):
                    self.fastPath[row][column] = min(fastPath[row][column],fastPath[row][point] +
                                                     fastPath[point][column] )
                    if self.fastPath[row][column] != fastPath[row][column] :
                        self.fastPathParent[row][column] = self.fastPathParent[point][column]

    def EKstream(self,start,end):
        self.residualNetwork = self.weightArray
        for edge in self.edegs:
            edge.flow = 0
        while self.DFS():
            path = self.DFS()
            flow =100000
            for edge in path:
                flow = min(flow,edge.flow)
            for edge in path:
                if edge in self.edegs:
                    edge.flow = edge.flow - flow
                else:
                    pass

















def firstSmaller(point1,point2):
    if point1.distance < point2.distance:
        return True
    else:
        return False

def BFStest():
    r = Point('r')
    s = Point('s')
    t = Point('t')
    u = Point('u')
    v = Point('v')
    w = Point('w')
    x = Point('x')
    y = Point('y')
    r.addEdge(v, s)
    s.addEdge(r, w)
    t.addEdge(w, x, u)
    u.addEdge(t, x, y)
    v.addEdge(r)
    w.addEdge(s, t, x)
    x.addEdge(w, t, u, y)
    y.addEdge(x, u)
    graph = Graph()
    graph.insertPoint(r, s, t, u, v, w, x, y)
    graph.BFS(s)
    print(x.deep)
    graph.BFSprintPath(s, y)

def DFStest():
    u = Point('u')
    v = Point('v')
    w = Point('w')
    x = Point('x')
    y = Point('y')
    z = Point('z')
    u.addEdge(x, v)
    v.addEdge(y)
    w.addEdge(y, z)
    x.addEdge(v)
    y.addEdge(x)
    z.addEdge(z)
    graph = Graph()
    graph.insertPoint(u, v, w, x, y, z)
    graph.DFS()
    print(u.findTime, u.finishTime)
    li = [u, v, w, x, y, z]
    print(li)
    newli = sorted(li, key=lambda point: point.finishTime, reverse=False)
    print(newli)

def creatPoints(points):
    pointsDict = {}
    for point in points:
        pointsDict[point] = Point(point)
    return pointsDict

def SCCtest():
    u = Point('u')
    v = Point('v')
    w = Point('w')
    x = Point('x')
    y = Point('y')
    z = Point('z')
    u.addEdge(x, v)
    v.addEdge(y)
    w.addEdge(y, z)
    x.addEdge(v)
    y.addEdge(x)
    z.addEdge(z)
    graph = Graph()
    graph.insertPoint(u, v, w, x, y, z)
    graph.findSCC()
    print(graph.SCCs)

def MSTtest():
    points = creatPoints('abcdefghi')
    graph = Graph()
    for key in points:
        graph.insertPoint(points[key])
    edges = [Edge(points['a'], points['b'], 4),
             Edge(points['a'], points['h'], 8),
             Edge(points['b'], points['h'], 11),
             Edge(points['b'], points['c'], 8),
             Edge(points['h'], points['i'], 7),
             Edge(points['h'], points['g'], 1),
             Edge(points['i'], points['c'], 2),
             Edge(points['i'], points['g'], 6),
             Edge(points['c'], points['d'], 7),
             Edge(points['c'], points['f'], 4),
             Edge(points['g'], points['f'], 2),
             Edge(points['d'], points['f'], 14),
             Edge(points['d'], points['e'], 9),
             Edge(points['f'], points['e'], 10),
             ]
    graph.addWeightEdges(*edges)
    path = graph.MST()
    for edge in path:
        edge.printEdge()

def Dijkstratest():
    points = creatPoints('stxyz')
    graph = Graph()
    for key in points:
        graph.insertPoint(points[key])
    edges = [Edge(points['s'], points['t'], 10),
             Edge(points['s'], points['y'], 5),
             Edge(points['t'], points['y'], 2),
             Edge(points['t'], points['x'], 1),
             Edge(points['y'], points['t'], 3),
             Edge(points['y'], points['x'], 9),
             Edge(points['y'], points['z'], 2),
             Edge(points['x'], points['z'], 5),
             Edge(points['z'], points['x'], 6),
             Edge(points['z'], points['s'], 7),
             ]
    graph.addWeightEdges(*edges)
    #graph.Dijkstra(points['s'])
    # print(points['y'].distance)
    graph.creatGraphArray()
    # print(array)
    graph.fastPathForAllPoints()
    for line in graph.fastPath:
        print(line)
    for line in graph.fastPathParent:
        print(line)


Dijkstratest()



