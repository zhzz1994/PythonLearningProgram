from functools import cmp_to_key
import sys

class Ponit():
    def __init__(self,x,y,name):
        self.x = x
        self.y = y
        self.isLeft = False
        self.isRight = False
        self.line = None
        self.name = name

class Line():
    def __init__(self, p1, p2):
        self.p1 = p1
        self.p2 = p2
        self.pleft = self.theLeftPoint()
        self.pright = self.theRightPoint()
        self.p1.line = self
        self.p2.line = self

    def theLeftPoint(self):
        if self.p1.x <= self.p2.x:
            self.p1.isLeft = True
            return self.p1
        else:
            self.p2.isLeft = True
            return self.p2

    def theRightPoint(self):
        if self.p1.x > self.p2.x:
            self.p1.isRight = True
            return self.p1
        else:
            self.p2.isRight = True
            return self.p2

class Node():
    def __init__(self , content):
        self.content = content
        self.prev = None
        self.next = None

class sortedLinklist():
    def __init__(self):
        self.head = None


    def insert(self):

        pass

def lineCrossed(p1,p2,p3,p4):
    d1 = direction(p1, p2, p3)
    d2 = direction(p1, p2, p4)
    d3 = direction(p3, p4, p1)
    d4 = direction(p3, p4, p2)
    if d1 * d2 < 0 and d3 * d4 < 0:
        return True
    elif  onSegment(p1, p2, p3) or onSegment(p1, p2, p4) or onSegment(p3, p4, p1) or onSegment(p3, p4, p2):
        return True
    else:
        return False

def direction(lp1,lp2,p):
    result = (lp2.x - lp1.x) * (p.y - lp1.y) - (p.x - lp1.x) * (lp2.y - lp1.y)
    return result

def onSegment(lp1,lp2,p):
    d = direction(lp1, lp2, p)
    if d == 0 and ( min(lp1.x,lp2.x) <= p.x <= max(lp1.x,lp2.x) and min(lp1.y,lp2.y) <= p.y <= max(lp1.y,lp2.y)):
        return True
    else:
        return False

def onTheTop(lp1,lp2,p):
    d = direction(lp1,lp2,p)
    if d > 0:
        return True
    else:
        return False


def grahm(points):
    start = min(points,key = lambda point:point.y)
    points.remove(start)
    pointRelate = points.copy()
    for point in pointRelate:
        point.x = point.x - start.x
        point.y = point.y - start.y
    pointRelate = sorted(pointRelate,key = cmp_to_key(lambda p1,p2: (p2.x * p1.y) - (p1.x * p2.y)))
    print(list(map(lambda point: point.name, pointRelate)))
    rtn = [start,pointRelate[0],pointRelate[1]]
    for index in range(2,len(pointRelate)):
        if onTheTop(rtn[-2],rtn[-1],pointRelate[index]) == False:
            rtn.pop()
            rtn.append(pointRelate[index])
        else:
            rtn.append(pointRelate[index])
    return rtn

def anySegmentIntersect(lines):
    comapareList = []
    pointList = []
    for line in lines:
        pointList.append(line.p1)
        pointList.append(line.p2)
    pointList = sorted(pointList,key = lambda point: point.x)
    for point in pointList:
        if point.isLeft:
            if len(comapareList) == 0:
                comapareList.append(point.line)
            else:
                index = 0
                while index <= (len(comapareList) - 1) and onTheTop(comapareList[index].pleft,comapareList[index].pright
                        ,point) == False:
                    index = index + 1
                comapareList.insert(index,point.line)
                if index != (len(comapareList) - 1):
                    if lineCrossed(comapareList[index].pleft,comapareList[index].pright,comapareList[index + 1].pleft,
                                   comapareList[index + 1].pright):
                        return True
                if index != 0:
                    if lineCrossed(comapareList[index].pleft,comapareList[index].pright,comapareList[index - 1].pleft,
                                   comapareList[index - 1].pright):
                        return True
        if point.isRight:
            index = comapareList.index(point.line)
            if index != 0 and index != (len(comapareList) - 1):
                if lineCrossed(comapareList[index + 1].pleft,comapareList[index + 1].pright,comapareList[index - 1].pleft,
                                   comapareList[index - 1].pright):
                    return True
            del comapareList[index]
    return False

def anySegmentIntersectTest():
    p1 = Ponit(1,1,'p1')
    p2 = Ponit(2,4,'p2')
    p3 = Ponit(5,5,'p3')
    p4 = Ponit(4,2,'p4')
    p5 = Ponit(3,3,'p5')
    p6 = Ponit(6,3,'p6')

    line1 = Line(p1,p3)
    line2 = Line(p2,p4)
    line3 = Line(p5,p6)

    lines = [line1,line2,line3]

    print(anySegmentIntersect(lines))

# p1 = Ponit(1,1,'p1')
# p2 = Ponit(5,1,'p2')
# p3 = Ponit(5, 5, 'p3')
# p4 = Ponit(1, 5, 'p4')
# p5 = Ponit(3, 3, 'p5')
# p6 = Ponit(3,4,'p6')
# p7 = Ponit(2,4,'p7')
# p8 = Ponit(6,6,'p6')
#
# points = [p1,p2,p3,p4,p5,p6,p7,p8]
# print(list(map(lambda point: point.name ,grahm(points))))





