from numpy import *
import re
import feedparser
import jieba
import requests
from bs4 import BeautifulSoup
import time

def loadDataSet():
    postingList=[['my', 'dog', 'has', 'flea', 'problems', 'help', 'please'],
                 ['maybe', 'not', 'take', 'him', 'to', 'dog', 'park', 'stupid'],
                 ['my', 'dalmation', 'is', 'so', 'cute', 'I', 'love', 'him'],
                 ['stop', 'posting', 'stupid', 'worthless', 'garbage'],
                 ['mr', 'licks', 'ate', 'my', 'steak', 'how', 'to', 'stop', 'him'],
                 ['quit', 'buying', 'worthless', 'dog', 'food', 'stupid']]
    classVec = [0,1,0,1,0,1]    #1 is abusive, 0 not
    return postingList,classVec

def createVocabList(dataset):
    vocabset = set([])
    for document in dataset:
        vocabset = vocabset | set(document)
    return list(vocabset)

def setOfWords2Vec(vocablist,inputset):
    returnVec = [0]*len(vocablist)
    for word in inputset:
        if word in vocablist:
            returnVec[vocablist.index(word)] = 1
        else:print('the word: %s is not in my Vocabulary!'%word)
    return returnVec

def trainNB0(trainmatrix,traincategory):
    numTrainDocs = len(trainmatrix)
    numWords = len(trainmatrix[0])
    pAbusive = sum(traincategory)/float(numTrainDocs)
    p0Num = ones(numWords)
    p1Num = ones(numWords)
    p0Denom = 1.0
    p1Denom = 1.0
    for i in range(numTrainDocs):
        if traincategory[i] == 1:
            p1Num += trainmatrix[i]
            p1Denom += sum(trainmatrix[i])
        else:
            p0Num += trainmatrix[i]
            p0Denom += sum(trainmatrix[i])
    p1Vect = log(p1Num/p1Denom)
    p0Vect = log(p0Num/p0Denom)
    return p0Vect,p1Vect,pAbusive

def classifyNB(vec2classify,p0vec,p1vec,pClass1):
    p1 = sum(vec2classify*p1vec) + log(pClass1)
    p0 = sum(vec2classify*p0vec) + log(1.0 - pClass1)
    if p1 > p0:
        return 1
    else:
        return 0

def bagOfWords2Vec(vocablist,inputset):
    returnVec = [0] * len(vocablist)
    for word in inputset:
        if word in vocablist:
            returnVec[vocablist.index(word)] += 1
        else:
            print('the word: %s is not in my Vocabulary!' % word)
    return returnVec

def textParse(bigstring):
    listoftokens = re.split(r'\W*',bigstring)
    return [tok.lower() for tok in listoftokens if len(tok) > 2]

def spamTest():
    doclist = []
    classlist = []
    fulltext = []
    for i in range(1,26):
        wordlist = textParse(open('G:\pyexam\email\spam\%d.txt' % i).read())
        doclist.append(wordlist)
        fulltext.extend(wordlist)
        classlist.append(1)
        wordlist = textParse(open('G:\pyexam\email\ham\%d.txt' % i).read())
        doclist.append(wordlist)
        fulltext.extend(wordlist)
        classlist.append(0)
    vocablist = createVocabList(doclist)
    trainingset = list(range(50))
    testset = []
    for i in range(10):
        randindex = int(random.uniform(0,len(trainingset)))
        testset.append(trainingset[randindex])
        del(trainingset[randindex])
    trainmat = []
    trainclass = []
    for docindex in trainingset:
        trainmat.append(setOfWords2Vec(vocablist,doclist[docindex]))
        trainclass.append(classlist[docindex])
    p0v,p1v,pspam = trainNB0(array(trainmat),array(trainclass))
    errorcount = 0
    for docindex in testset:
        wordvector = setOfWords2Vec(vocablist,doclist[docindex])
        if classifyNB(array(wordvector),p0v,p1v,pspam) != classlist[docindex]:
            errorcount += 1
    print('the error rate is:',float(errorcount)/len(testset))
    print(testset)

def test():
    listofpost,listclass = loadDataSet()
    myvocallist = createVocabList(listofpost)
    print(myvocallist)
    print(listofpost[0])
    print(setOfWords2Vec(myvocallist,listofpost[0]))
    trainmat = []
    for list in listofpost:
        trainmat.append(setOfWords2Vec(myvocallist,list))
    p0v,p1v,pab = trainNB0(trainmat,listclass)
    print(pab)
    print(p0v)
    print(p1v)
    tsetEntry = ['love','my','dalmation']
    thisDoc = array(setOfWords2Vec(myvocallist,tsetEntry))
    print(classifyNB(thisDoc,p0v,p1v,pab))
    tsetEntry = ['stupid']
    thisDoc = array(setOfWords2Vec(myvocallist, tsetEntry))
    print(classifyNB(thisDoc, p0v, p1v, pab))

def chinesefenci(text):
    seg = jieba.cut(text,cut_all=True)  #全模式，词汇更多
    seglist = list(seg)
    return [tok.lower() for tok in seglist if len(tok) > 1]

def gettext():
    def geturl(url):
        urls = []
        wbdata = requests.get(url, headers=headers)
        soup = BeautifulSoup(wbdata.text, 'lxml')
        for link in soup.select('#subject_list > ul > li > div.info > h2 > a'):
            urls.append(link.get('href'))
        return urls

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.106 BIDUBrowser/8.7 Safari/537.36',
        'Cookie': '__utmt=1; __utma=81379588.292354748.1490268308.1490605522.1490610588.5; __utmb=81379588.1.10.1490610588; __utmc=81379588; __utmz=81379588.1490603404.3.3.utmcsr=baidu|utmccn=(organic)|utmcmd=organic|utmctr=%E8%B1%86%E7%93%A3; ll="108309"; bid=Lca1RNgIRiY; viewed="26284925"; ps=y; dbcl2="136865962:xh/9+e+2kqk"; ck=c48h; push_noty_num=0; push_doumail_num=0; __utmt_douban=1; __utma=30149280.1163315445.1490003408.1490605522.1490610565.7; __utmb=30149280.1.10.1490610565; __utmc=30149280; __utmz=30149280.1490603130.5.5.utmcsr=baidu|utmccn=(organic)|utmcmd=organic; ap=1'
    }
    url = 'https://book.douban.com/tag/%E5%B0%8F%E8%AF%B4?start=60&type=T'
    urls = geturl(url)
    f = open("G:\pyexam\chinesenov.txt", "a+", encoding='utf-8')
    for url in urls:
        time.sleep(0.5)
        wbdata = requests.get(url,headers=headers)
        soup = BeautifulSoup(wbdata.text,'lxml')
        intros = soup.find_all("div", "intro")
        intro = intros[0].text
        intro = intro.lstrip('\n')
        f.write(str(intro)+'\n')
        print(url)
    f.close

def readthetext():
    doclist = []
    classlist = []
    fulltext = []
    fr1 = open('G:\pyexam\chinesenov.txt',encoding= 'UTF-8')
    fr2 = open('G:\pyexam\chinesepeo.txt',encoding= 'UTF-8')
    arrayoflines1 = fr1.readlines()
    numberoflines1 = len(arrayoflines1)
    arrayoflines2 = fr2.readlines()
    numberoflines2 = len(arrayoflines2)
    for i in range(0,numberoflines1):
        wordlist = chinesefenci(arrayoflines1[i])
        doclist.append(wordlist)
        fulltext.extend(wordlist)
        classlist.append(1)
    for i in range(0,numberoflines2):
        wordlist = chinesefenci(arrayoflines2[i])
        doclist.append(wordlist)
        fulltext.extend(wordlist)
        classlist.append(0)
    vocablist = createVocabList(doclist)
    trainingset = list(range(numberoflines1 + numberoflines2))
    testset = []
    for i in range(5):
        randindex = int(random.uniform(0,len(trainingset)))
        testset.append(trainingset[randindex])
        del(trainingset[randindex])
    trainmat = []
    trainclass = []
    for docindex in trainingset:
        trainmat.append(bagOfWords2Vec(vocablist,doclist[docindex]))
        trainclass.append(classlist[docindex])
    p0v,p1v,pspam = trainNB0(array(trainmat),array(trainclass))
    errorcount = 0
    for docindex in testset:
        wordvector = bagOfWords2Vec(vocablist,doclist[docindex])
        if classifyNB(array(wordvector),p0v,p1v,pspam) != classlist[docindex]:
            errorcount += 1
    print('the error rate is:',float(errorcount)/len(testset))
    print(testset)

    fr3 = open('G:\pyexam\chinesefenci.txt').read()

    print(vocablist)
    print(len(vocablist))
    # tsetEntry = chinesefenci(fr3)
    # print(tsetEntry)
    # thisDoc = array(bagOfWords2Vec(vocablist, tsetEntry))
    # print(classifyNB(thisDoc, p0v, p1v, pspam))

readthetext()