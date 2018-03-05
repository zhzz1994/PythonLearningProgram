import math

class fibNode():
    def __init__(self,key,value,left=None,right=None,parent=None,child=None,mark=False,degree=0):
        self.key = key
        self.value = value
        self.parent = parent
        self.left = left
        self.right = right
        self.child = child
        self.mark = mark
        self.degree = degree

class linkList():
    def __init__(self):
        self.size = 0
        self.head = None

    def insert(self,node):
        if self.head:
            next = self.head.right
            node.left = self.head
            node.right = next
            next.left = node
            self.head.right = node
        else:
            self.head = node
            self.head.left = node
            self.head.right = node
        self.size = self.size + 1

    def remove(self,node):
        if self.head:
            if node == self.head:
                if self.head.right == self.head:
                    self.head = None
                else:
                    node.right.left = node.left
                    node.left.right = node.right
                    self.head = node.left
            else:
                node.right.left = node.left
                node.left.right = node.right
            self.size = self.size + 1

class FIBheap():
    def __init__(self):
        self.min = None
        self.rootList = linkList()
        self.nodeNum = 0

    def heapInsert(self,node):
        if self.min:
            self.rootList.insert(node)
            if node.key < self.min.key:
                self.min = node
        else:
            self.rootList.insert(node)
            self.min = node
        self.nodeNum =  self.nodeNum + 1

    def heapExtractMin(self):
        minNode = self.min
        if minNode:
            while minNode.child:
                self.rootList.insert(minNode.child.head.left)
                minNode.child.head.left.parent = None
            if minNode.left == minNode:
                self.rootList.remove(minNode)
                self.min = None
            else:
                newNode = minNode.right
                self.rootList.remove(minNode)
                self.min = newNode
                self.CONSOLIDATE()
            self.nodeNum = self.nodeNum - 1
        return minNode

    def CONSOLIDATE(self):
        deep = int(math.log(self.nodeNum,1.6)) + 1
        deepArray = [None for num in range(0,deep)]
        lastNode = self.min.left
        nextNode = self.min
        while lastNode != nextNode:
            print(nextNode.value)
            node = nextNode
            degree = node.degree
            if deepArray[degree]:
                beforeNode = deepArray[degree]
                if beforeNode.key < node.key:
                    self.linkFibHeap(beforeNode,node)
                    node = beforeNode
                else:
                    self.linkFibHeap(node,beforeNode)
                deepArray[degree] = None
                degree = node.degree
                degree = degree + 1
            deepArray[degree] = node
            nextNode = nextNode.right
            print(deepArray)
        if lastNode == nextNode:
            print(nextNode.value)
            node = nextNode
            degree = node.degree
            if deepArray[degree]:
                beforeNode = deepArray[degree]
                if beforeNode.key < node.key:
                    self.linkFibHeap(beforeNode, node)
                    node = beforeNode
                else:
                    self.linkFibHeap(node, beforeNode)
                deepArray[degree] = None
                degree = node.degree
                degree = degree + 1
            deepArray[degree] = node
            print(deepArray)
        self.min = None
        for node in deepArray:
            if node:
                if self.min:
                    self.rootList.insert(node)
                    if node.key < self.min.key:
                        self.min = node
                else:
                    self.rootList = linkList()
                    self.rootList.insert(node)
                    self.min = node

    def linkFibHeap(self,parent,child):
        if parent.child == None:
            parent.child = linkList()
        self.rootList.remove(child)
        parent.child.insert(child)
        parent.degree = parent.degree + 1
        child.mark = False

    def fibHeapDecreaseKey(self,node,key):
        if key > node.key:
            print('new key bigger than before')
        node.key = key
        parent = node.parent
        if parent and node.key < parent.key:
            self.heapCut(node,parent)
            self.heapCascadingCut(parent)
        if node.key < self.min.key:
            self.min = node

    def heapCut(self,node,parent):
        parent.child.remove(node)
        if parent.degree == node.degree + 1:
            if parent.child.head:
                lastNode = parent.child.head.left
                degree = 0
                while lastNode != parent.child.head:
                    if degree < parent.child.head.degree:
                        degree = parent.child.head.degree
                    parent.child.head = parent.child.head.right
                parent.degree = degree + 1
            else:
                parent.degree = 0
                parent.child = None
        self.rootList.insert(node)
        node.parent = None
        node.mark = False

    def heapCascadingCut(self,parent):
        grandpa = parent.parent
        if grandpa:
            if parent.mark == False:
                parent.mark = True
            else:
                self.heapCut(parent,grandpa)
                self.heapCascadingCut(grandpa)

def fibHeapUnion(heap1,heap2):
    heapNew = FIBheap()
    heapNew.min = heap1.min
    if (heap1.min == None) or (heap2.min == None and heap2.min.key < heap1.min.key):
        heapNew.min = heap2.min
    heapNew.mainHeapSize = heap1.mainHeapSize + heap2.mainHeapSize
    if heap1.min and heap2.min:
        heap1.min.left.right = heap2.min.left
        heap2.min.left.left = heap1.min.left
        heap1.min.left = heap2.min
        heap2.min.right = heap1.min
    return heapNew




list = FIBheap()
for i in range(1,40):
    list.heapInsert(fibNode(i,i))



print(list.heapExtractMin().value)
print(list.heapExtractMin().value)













