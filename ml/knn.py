from numpy import *
import operator
import matplotlib
import matplotlib.pyplot as plt

def createDataSet():
    group = array([[1.0,1.1],[1.0,1.0],[0,0],[0,0.1]])
    labels = ['A','A','B','B']
    return group,labels

def file2matrix(filename):
    fr = open(filename)
    arrayoflines = fr.readlines()
    numberoflines = len(arrayoflines)
    returnmat = zeros((numberoflines,3))
    classlabelvector = []
    index = 0
    for line in arrayoflines:
        line = line.strip()
        listfromline = line.split('\t')
        returnmat[index, :] = listfromline[0:3]
        if listfromline[-1] == 'largeDoses':
            lab = 3
        elif listfromline[-1] == 'smallDoses':
            lab = 2
        elif listfromline[-1] == 'didntLike':
            lab = 1
        else:
            lab = 0
        classlabelvector.append(lab)
        index += 1
    return returnmat,classlabelvector

def showdata(dtmat,dtlb):
    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.scatter(dtmat[:,0],dtmat[:,1],10.0*array(dtlb),10.0*array(dtlb))
    plt.show()

def autoNorm(dataset):
    minVals = dataset.min(0)
    maxVals = dataset.max(0)
    ranges = maxVals - minVals
    normDataset = zeros(shape(dataset))
    m = dataset.shape[0]
    normDataset = dataset - tile(minVals,(m,1))
    normDataset = normDataset/tile(ranges,(m,1))
    return normDataset,ranges,minVals

def classify0(inX,dataset,labels,k):
    dataSetSize = dataset.shape[0]
    diffmat = tile(inX,(dataSetSize,1)) - dataset
    sqdiffmat = diffmat**2
    sqdistances = sqdiffmat.sum(axis=1)
    distances = sqdistances**0.5
    sorteddistances = distances.argsort()
    #argsort:排序
    classcount = {}
    for i in range(k):
        votelabel = labels[sorteddistances[i]]
        classcount[votelabel] = classcount.get(votelabel,0) + 1
    sortedClassCount = sorted(classcount.items(),key=operator.itemgetter(1),reverse=True)
    return sortedClassCount[0][0]

def datingClassTest():
    hoRatio = 0.10
    dtmat, dtlb = file2matrix('G:\pyexam\datingTestSet.txt')
    normmat,ranges,minVals = autoNorm(dtmat)
    m = normmat.shape[0]
    numtestvecs = int(m*hoRatio)
    errorcount = 0.0
    for i in range(numtestvecs):
        classfierresult = classify0(normmat[i,:],normmat[numtestvecs:m,:],dtlb[numtestvecs:m],3)
        print('comeback: %d,real answer is: %d'%(classfierresult,dtlb[i]))
        if(classfierresult != dtlb[i]): errorcount += 1.0
    print('total error rate is:%f'%(errorcount/float(numtestvecs)))

def classifyperson():
    resultlist = ['not at all','in small doses','in large doses']
    percenttats = float(input('time of play games?'))
    ffmiles = float(input('how long have you fly?'))
    icecream = float(input('how many icecream have you eat?'))
    dtmat, dtlb = file2matrix('G:\pyexam\datingTestSet.txt')
    normmat, ranges, minVals = autoNorm(dtmat)
    inArr = array([percenttats,ffmiles,icecream])
    classifierresult = classify0((inArr-minVals)/ranges,normmat,dtlb,3)
    print('the probably is:',resultlist[classifierresult-1])

