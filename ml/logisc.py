from numpy import *


def sigmoid(inX):
    return longfloat(1.0/(1+exp(-inX)))

def classifyVector(inX,weights):
    prob = sigmoid(sum(inX*weights))
    if prob > 0.5 :
        return 1.0
    else:
        return 0.0

def stocGradAscent1(dataMatrix,classLabels,numIter = 150):
    m,n = shape(dataMatrix)
    weights = ones(n)
    for j in range(numIter):
        dataIndex = list(range(m))
        for i in range(m):
            alpha = 4/(1.0+j+0.05*i) + 0.01
            randIndex = int(random.uniform(0,len(dataIndex)))
            h = sigmoid(sum(dataMatrix[randIndex]*weights))
            error = classLabels[randIndex] - h
            weights = weights + alpha*error*dataMatrix[randIndex]
            del(dataIndex[randIndex])
    return weights



def colicTest():
    frtrain = open('G:\pyexam\horseColicTraining.txt')
    frtest = open('G:\pyexam\horseColicTest.txt')
    trainingSet = []
    trainingLabels = []
    for line in frtrain.readlines():
        currline = line.strip().split('\t')
        linearr = []
        for i in range(21):
            linearr.append(float(currline[i]))
        trainingSet.append(linearr)
        trainingLabels.append(float(currline[21]))
    trainWeights = stocGradAscent1(array(trainingSet),trainingLabels,500)
    errorcount = 0
    numTestVec = 0.0
    for line in frtest.readlines():
        numTestVec += 1
        currline = line.strip().split('\t')
        linearr = []
        for i in range(21):
            linearr.append(float(currline[i]))
        if int(classifyVector(array(linearr),trainWeights)) != int(currline[21]):
            errorcount += 1
    errorrate = (float(errorcount)/numTestVec)
    print('the error rate of the test is : %f' %errorrate)
    return errorrate

def multiTest():
    numTests = 10
    errorSum = 0.0
    for k in  range(numTests):
        errorSum += colicTest()
    print('the new error rate is %f' %(errorSum/float(numTests)))

multiTest()