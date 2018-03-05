import sys
import types
import pickle
import gc
import weakref
import psutil
import os
import itertools
import timeit
import pprint
import inspect
import itertools
from contextlib import contextmanager
import functools
from weakref import WeakKeyDictionary
from heapq import *

def analyse():
    a = sys.maxsize
    print(a)
    b  = a * 10000
    pprint.pprint(b)
    pprint.pprint(b.__class__)
    c = 1 << 0xFFFF
    pprint.pprint(c)
    print(sys.getsizeof(c))
    print(c.__class__)
    p = psutil.Process(os.getpid())
    pprint.pprint(p.memory_info())
    pprint.pprint(p.cpu_times())
    print(sys.getrecursionlimit())
    def s():
        pprint.pprint(inspect.stack())
    s()

class MyDescriptor():
    def __init__(self,default):
        self.default = default
        self.data = WeakKeyDictionary()

    def __get__(self, instance, owner):
        if instance is None:
            return self
        print('get',instance,owner)
        return self.data.get(instance,self.default)

    def __set__(self, instance, value):
        print('set',instance,value)
        if value < 0:
            print('Num should bigger than zero.')
            self.data[instance] = self.default
        else:
            self.data[instance] = value

    def __delete__(self, instance):
        print('del',instance)
        del self.data[instance]





@functools.total_ordering
class Point():
    index = 0
    def __new__(cls, *args, **kwargs):
        cls.increaseIndex()
        return object.__new__(cls)

    def __init__(self,x,y,name):
        self.x = x
        self.y = y
        self.name = name
        self.index = self.index

    def __eq__(self, other):
        mydistance = (self.x ** 2) + (self.y ** 2)
        otherdistance = (other.x ** 2) + (other.y ** 2)
        return mydistance == otherdistance

    def __lt__(self, other):
        mydistance = (self.x ** 2) + (self.y ** 2)
        otherdistance = (other.x ** 2) + (other.y ** 2)
        return mydistance < otherdistance

    @classmethod
    def increaseIndex(cls):
        cls.index = cls.index + 1






p1 = Point(2,3,'p1')
p2 = Point(3,3,'p2')
p3 = Point(7,3,'p3')
p4 = Point(9,7,'p4')
p5 = Point(4,1,'p5')

li = sorted([p1,p2,p3,p4,p5])
li1 = list(map(lambda x:x.name,li))
print(li1)
print(list([p1,p2,p3,p4,p5]))
largest = nlargest(2,[p1,p2,p3,p4,p5],lambda p:p.index)
print(largest[1].name)
print(p2.index)



