from math import log
from numpy import *
import operator
import matplotlib.pyplot as plt

def calcShannonEnt(dataset):
    numEntries = len(dataset)
    labelCounts = {}
    for featvec in dataset:
        currentlabel = featvec[-1]
        if currentlabel not in labelCounts.keys():
            labelCounts[currentlabel] = 0
        labelCounts[currentlabel] += 1
    shannonEnt = 0.0
    for key in labelCounts:
        prob = float(labelCounts[key])/numEntries
        n = prob*math.log(prob,2)
        shannonEnt -= n
    #print(labelCounts)
    return shannonEnt

def splitDtaset(dataset,axis,value):
    retdataset = []
    for featvec in dataset:
        if featvec[axis] == value:
           reducedfeatvec = featvec[:axis]
           reducedfeatvec.extend(featvec[axis+1:])
           #把列表中axis位置元素去掉
           retdataset.append(reducedfeatvec)
    return retdataset

def chooseBestFeatureToSplit(dataset):
    numfeatures = len(dataset[0])-1
    baseentropy = calcShannonEnt(dataset)
    bestinfogain = 0.0
    bestfeature = -1
    for i in range(numfeatures):
        featlist = [example[i] for example in dataset]
        uniquevals = set(featlist)
        newentropy = 0.0
        for value in uniquevals:
            subdataset = splitDtaset(dataset,i,value)
            pron = len(subdataset)/float(len(dataset))
            newentropy += pron*calcShannonEnt(subdataset)
        infogain = baseentropy - newentropy
        if(infogain > bestinfogain):
            bestinfogain = infogain
            bestfeature = i
    return bestfeature

def majoritycut(classlist):
    classcount = {}
    for vote in classlist:
        if vote not in classcount.keys():
            classcount = 0
            classcount[vote] +=1
        sortedclasscount = sorted(classcount.items(),key = operator.itemgetter(1),reversed=True)
    return  sortedclasscount[0][0]

def createtree(dataset,labels):
    classlist = [example[-1] for example in dataset]
    if classlist.count(classlist[0]) == len(classlist):
        return classlist[0]
    if len(dataset[0]) == 1:
        return majoritycut(classlist)
    bestfeat = chooseBestFeatureToSplit(dataset)
    bestfeatlabels = labels[bestfeat]
    mytree = {bestfeatlabels:{}}
    del(labels[bestfeat])
    featvalues = [example[bestfeat] for example in dataset]
    uniquevals = set(featvalues)
    for value in uniquevals:
        sublabels = labels[:]
        mytree[bestfeatlabels][value] = createtree(splitDtaset(dataset,bestfeat,value),sublabels)
    return mytree

def classify(inputtree,featlabels,testvec):
    firstkeys = inputtree.keys()
    firststrs = list(firstkeys)
    firststr = firststrs[0]
    seconddict = inputtree[firststr]
    featindex = featlabels.index(firststr)
    for key in seconddict.keys():
        if testvec[featindex] == key:
            if type(seconddict[key]).__name__=='dict':
                classlabel = classify(seconddict[key],featlabels,testvec)
            else: classlabel = seconddict[key]
    return  classlabel

def file2dataset(filename):
    fr = open(filename)
    arrayoflines = fr.readlines()
    numberoflines = len(arrayoflines)
    returnmat = []
    classlabelvector = []
    index = 0
    for line in arrayoflines:
        line1 = line.strip()
        listfromline = line1.split('\t')
        returnmat.append(listfromline[0:5])
        lab = listfromline[-1]
        classlabelvector.append(lab)
        index += 1
    return returnmat





# dataset = [[1,1,'y'],[1,1,'y'],[1,0,'n'],[0,1,'n'],[0,1,'n']]
# labels = ['no surfacing','flippers']
#
# featlabel = ['no surfacing','flippers']
#
# thetree = createtree(dataset,labels)
# testvec = [1,1]
#
# print(thetree)
# n = classify(thetree,featlabel,testvec)
# print(n)

dataset  = file2dataset('G:\pyexam\lenses.txt')
print(dataset)
lables = ['age','prescript','astigmatic','tearrate']
thetree = createtree(dataset,lables)
print(thetree)




