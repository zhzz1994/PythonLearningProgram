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

class openAddressingHashTable():
    def __init__(self):
       pass

    def hash1(self,value):
        return (10 * value + 18) % 947

    def hash2(self,value):
        return (23 * value + 88) % 953

    def hash(self,value,i):
        result = (self.hash1(value) + i * self.hash2(value)) % 967
        return result

    def createHashTable(self,length):
        table = []
        for i in range(0 , length):
            table.append(0)
        return table

    def insertItem(self , item , Table):
        i = 0
        while i <= len(Table):
            if Table[self.hash(item , i)] == 0 :
                Table[self.hash(item , i)] = item
                break
            elif Table[self.hash(item , i)] == -1 :
                Table[self.hash(item, i)] = item
                break
            else:
                i = i+ 1
        return None

    def searchItem(self , item , Table):
        i = 0
        while i <= len(Table):
            if Table[self.hash(item , i)] == 0 :
                return 0 ,0
            elif Table[self.hash(item , i)] == item:
                return self.hash( item , i) , item
            else :
                i = i + 1
        return 0 , 0

    def deleteItem(self,item ,Table):
        key ,searchresult = self.searchItem(item,Table)
        if key == 0 :
            return None
        else:
            Table[key] = -1

class treeNode():
    def __init__(self ,key ,value , left = None ,right = None ,parent = None ,color = 'red'):
        self.key  = key
        self.value = value
        self.leftChild = left
        self.rightChild = right
        self.parent = parent
        self.color = color

    def hasLeftChild(self):
        return self.leftChild

    def hasRightChild(self):
        return self.rightChild

    def isLeftChild(self):
        return self.parent and self.parent.leftChild == self

    def isRightChild(self):
        return self.parent and self.parent.rightChild == self

    def isRoot(self):
        return not self.parent

    def isLeaf(self):
        return not (self.rightChild or self.leftChild)

    def hasAnyChildren(self):
        return self.rightChild or self.leftChild

    def hasBothChildren(self):
        return self.rightChild and self.leftChild

    def replaceNodeData(self,key,value,leftChild,rightChild):
        self.key = key
        self.value = value
        self.leftChild = leftChild
        self.rightChild = rightChild
        if self.hasLeftChild():
            self.leftChild.parent = self
        if self.hasRightChild():
            self.rightChild.parent = self

    def replaceNodeColor(self,color):
        self.color = color

class RBtree():
    def __init__(self):
        self.nil = self.createNil()
        self.root = self.nil
        self.size = 0

    def createNil(self):
        return treeNode(key= -1 , value= 'NIL' , color='black')

    def __len__(self):
        return self.size

    def leftRotate(self,node):
        childNode = node.right
        node.right = childNode.left
        if childNode.left != self.nil:
            childNode.left.parent = node
        childNode.parent = node.parent
        if node.parent == self.nil:
            self.root = childNode
        elif node.parent.left == node:
            childNode.parent.left = childNode
        else:
            childNode.parent.right = childNode
        childNode.right = node
        node.parent = childNode

    def rightRotate(self,node):
        childNode = node.left
        node.left = childNode.right
        if childNode.right != self.nil:
            childNode.right.parent = node
        childNode.parent = node.parent
        if node.parent == self.nil:
            self.root = childNode
        elif node.parent.left == node:
            childNode.parent.left = childNode
        else:
            childNode.parent.right = childNode
        childNode.left = node
        node.parent = childNode

    def RBtreeInsert(self,node):
        placeholder = self.nil
        find = self.root
        while find != self.nil:
            placeholder = find
            if node.key < find.key:
                find = find.left
            else:
                find = find.right
        node.parent = find
        if find == self.nil:
            self.root = node
        elif node.key < find.key:
            find.left = node
        else:
            find.right = node
        node.left = self.nil
        node.right = self.nil
        node.color = 'red'
        self.RBtreeInsertFixup(node)

    def RBtreeInsertFixup(self,node):
        while node.parent.color == 'red':
            if node.parent == node.parent.parent.left:
                uncle = node.parent.parent.right
                if uncle.color == 'red':
                    node.parent.color = 'black'
                    uncle.color = 'black'
                    node.parent.parent.color = 'red'
                    node = node.parent.parent
                elif node == node.parent.right:
                    node = node.parent
                    self.leftRotate(node)
                node.parent.color = 'black'
                node.parent.parent.color = 'red'
                self.rightRotate(node.parent.parent)
            else:
                uncle = node.parent.parent.left
                if uncle.color == 'red':
                    node.parent.color = 'black'
                    uncle.color = 'black'
                    node.parent.parent.color = 'red'
                    node = node.parent.parent
                elif node == node.parent.left:
                    node = node.parent
                    self.rightRotate(node)
                node.parent.color = 'black'
                node.parent.parent.color = 'red'
                self.leftRotate(node.parent.parent)
        self.root.color = 'black'

    def RBtransplant(self,nodebefore,nodefinish):
        if nodebefore.parent == self.nil:
            self.root = nodefinish
        elif nodebefore == nodebefore.parent.left:
            nodebefore.parent.left = nodefinish
        else:
            nodebefore.parent.right = nodefinish
        nodefinish.parent = nodebefore.parent

    def treeMinimum(self,subtree):
        while subtree.left != self.nil:
            subtree = subtree.left
        return subtree

    def RBtreeDelete(self,node):
        newnode = node
        newnodeOriginalColor = newnode.color
        nil = self.nil
        if node.left == nil:
            subtree = node.right
            self.RBtransplant(node,node.right)
        elif node.right == nil:
            subtree = node.left
            self.RBtransplant(node, node.left)
        else:
            newnode = self.treeMinimum(node.right)
            newnodeOriginalColor = newnode.color
            subtree = newnode.right
            if newnode.parent == node:
                subtree.parent = newnode
            else:
                self.RBtransplant(newnode,newnode.right)
                newnode.right = node.right
                newnode.right.parent = newnode
            self.RBtransplant(node,newnode)
            newnode.left = node.left
            newnode.left.parent = newnode
            newnode.color = node.color
        if newnodeOriginalColor == 'black':
            self.RBtreeDeleteFixup(subtree)

    def RBtreeDeleteFixup(self,subtree):
        while subtree != self.root and subtree.color == 'black':
            if subtree == subtree.parent.left:
                newbrother = subtree.parent.right
                if newbrother.color == 'red':
                    newbrother.color = 'black'
                    subtree.parent.color = 'red'
                    self.leftRotate(subtree.parent)
                    newbrother = subtree.parent.right
                if newbrother.left.color == 'black' and newbrother.right.color == 'black':
                    newbrother.color = 'red'
                    subtree = subtree.parent
                else:
                    if newbrother.right == 'black':
                        newbrother.left.color = 'black'
                        newbrother.color = 'red'
                        self.rightRotate(newbrother)
                        newbrother = subtree.parent.right
                    newbrother.color = subtree.parent.color
                    subtree.parent.color = 'black'
                    newbrother.right.color = 'black'
                    self.leftRotate(subtree.parent)
                    subtree = self.root
            if subtree == subtree.parent.right:
                newbrother = subtree.parent.left
                if newbrother.color == 'red':
                    newbrother.color = 'black'
                    subtree.parent.color = 'red'
                    self.leftRotate(subtree.parent)
                    newbrother = subtree.parent.right
                if newbrother.left.color == 'black' and newbrother.right.color == 'black':
                    newbrother.color = 'red'
                    subtree = subtree.parent
                else:
                    if newbrother.right == 'black':
                        newbrother.left.color = 'black'
                        newbrother.color = 'red'
                        self.rightRotate(newbrother)
                        newbrother = subtree.parent.right
                    newbrother.color = subtree.parent.color
                    subtree.parent.color = 'black'
                    newbrother.right.color = 'black'
                    self.leftRotate(subtree.parent)
                    subtree = self.root
        subtree.color = 'black'







