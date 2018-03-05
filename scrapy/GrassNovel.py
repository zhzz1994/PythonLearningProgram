from selenium import webdriver
import io
from selenium.webdriver import ActionChains
import time
from bs4 import BeautifulSoup
import urllib
import urllib.request
import base64
import requests
import os
from selenium.webdriver.chrome.options import Options
import re
from urllib.request import urlretrieve
from languagecn import langconv
import logging
import functools

#logging.basicConfig(filename = os.path.join('G:\\20160916\\小说下载\\', 'log.txt'), level = logging.DEBUG)
firsturl = 'http://t66y.com/thread0806.php?fid=20'
pagesNum = 24
logposition = 'G:\\20160916\\小说下载\\log.txt'





def logWrite(text):
    logs = open(logposition, 'ab+')
    logN = str(text) + '\r\n'
    logs.write(logN.encode())
    logs.close()

def driversDecorator(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        path = "G:\pythonpro\chrome\chromedriver.exe"
        # driver = webdriver.Chrome(executable_path=path)
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument("--headless")
        prefs = {"profile.managed_default_content_settings.images": 2}  # 不加载图片
        chrome_options.add_experimental_option("prefs", prefs)
        driver = webdriver.Chrome(chrome_options=chrome_options, executable_path=path)
        backs = func(*args, **kwargs,driver = driver)
        driver.close()
        return backs
    return wrapper

def tradition2simple(line):
    # 将繁体转换成简体
    line = langconv.Converter('zh-hans').convert(line)
    return line

def getInOnePage(url,divers,entireNovle,author):
    divers.get(url)
    html = divers.page_source
    soup = BeautifulSoup(html, 'lxml')
    body = soup.find_all('div',{'class':'t t2'})
    authorPattern = r'<b>' + author + '</b>'
    for div in body:
        if re.search(authorPattern,str(div)):
            div = div.find_all('div',{'class':'tpc_content'})
            div = formationPassage(div)
            entireNovle.append(div)
            print(div)

def formationPassage(div):
    div = str(div)
    div = re.sub(r'<div class="tpc_content do_not_catch">', '', div)
    div = re.sub(r']', '', div)
    div = re.sub(r'</div>', '\r\n\r\n', div)
    div = re.sub(r'\[', '', div)
    div = re.sub(r'<br/><br/>', '\r\n', div)
    div = re.sub(r'<br/>', '', div)
    div = re.sub(r'</span>', '', div)
    div = re.sub(r'<div class="tpc_content">', '\r\n', div)
    div = re.sub(r'<span class="f16">', '\r\n', div)
    div = tradition2simple(div)
    return div

def initDrivers(urlList,typenv,title,author):
    entireNovle = []
    local = 'G:\\20160916\\小说下载\\'
    path = "G:\pythonpro\chrome\chromedriver.exe"
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("--headless")
    prefs = {"profile.managed_default_content_settings.images": 2}  # 不加载图片
    chrome_options.add_experimental_option("prefs", prefs)
    divers = webdriver.Chrome(chrome_options=chrome_options, executable_path=path)
    for url in urlList:
        print(url)
        getInOnePage(url, divers,entireNovle,author)
    divers.close()
    local = local + typenv + '\\'
    os.makedirs(local, exist_ok=True)
    name = local + title + '.txt'
    name = str(name)
    flie = open(name, 'wb')
    for paragraph in entireNovle:
        flie.write(paragraph.encode())
    flie.close()

def getAllPages(pagenum,url,pageindex):
    urlList = [url]
    urlhead = 'http://t66y.com/read.php?tid='
    for page in range(2,pagenum + 1):
        url = str(urlhead + str(pageindex) + '&page=' + str(page))
        urlList.append(url)
    return urlList

def resolveTitle(title):
    title = str(title)
    title = re.search(r'target="_blank"(.*)</a>',title)
    title = title.group(1)
    title = re.sub(r' ','',title)
    title = re.sub(r'id>', '', title)
    title = re.sub(r'fontcolor="green"', '', title)
    title = re.sub(r'fontcolor="red"', '', title)
    title = re.sub(r'fontcolor="orange"', '', title)
    title = re.sub(r'</font>', '', title)
    title = re.sub(r'</b>', '', title)
    title = re.sub(r'<b>', '', title)
    title = re.sub(r'<', '', title)
    title = re.sub(r'>', '', title)
    return title

def getTitles(url):
    typenvList = []
    titleList = []
    pageList = []
    pageindexList = []
    pageNumList = []
    authorList = []
    path = "G:\pythonpro\chrome\chromedriver.exe"
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("--headless")
    prefs = {"profile.managed_default_content_settings.images": 2}  # 不加载图片
    chrome_options.add_experimental_option("prefs", prefs)
    divers = webdriver.Chrome(chrome_options=chrome_options, executable_path=path)
    divers.get(url)
    html = divers.page_source
    divers.close()
    soup = BeautifulSoup(html,'lxml')
    novels = soup.find_all('tr',{'class':'tr3 t_one tac'})
    for novel in novels:
        urlnv = novel.find('h3')
        author = novel.find('a',{'class':'bl'})
        author = re.search(r'>(.*)</a>',str(author))
        urlindex = re.search(r'htm_data/([0-9]*/[0-9]*/([0-9]*))\.html',str(urlnv))
        title = resolveTitle(urlnv)
        typenv =re.search(r'\[(.*)]',str(novel))
        pageNum = re.search(r'blank">([0-9]*)</a></span>',str(novel))
        if urlindex and title and pageNum and author and typenv:
            titleList.append(title)
            pageList.append(urlindex.group(1))
            pageindexList.append(urlindex.group(2))
            if len(typenv.group(1)) < 10:
                typenvList.append(typenv.group(1))
            else:
                typenv = '类型不明'
                typenvList.append(typenv)
            pageNumList.append(int(pageNum.group(1)))
            authorList.append(author.group(1))
    return typenvList,titleList,pageList,pageindexList,pageNumList,authorList

def delectGuide(typenvList, titleList, pageList, pageindexList, pageNumList, authorList):
    newtypenvList = []
    newtitleList = []
    newpageList = []
    newpageindexList = []
    newpageNumList = []
    newauthorList = []
    for n in range(len(typenvList)):
        if authorList[n] not in ['Diss','tsq456','lj413025','vonder','administrator']:
            newtypenvList.append(typenvList[n])
            newtitleList.append(titleList[n])
            newpageList.append(pageList[n])
            newpageindexList.append(pageindexList[n])
            newpageNumList.append(pageNumList[n])
            newauthorList.append(authorList[n])
    return newtypenvList, newtitleList, newpageList, newpageindexList, newpageNumList, newauthorList

def getAllNovelsInOnePage(indexurl):
    typenvList, titleList, pageList, pageindexList, pageNumList, authorList = getTitles(indexurl)
    typenvList, titleList, pageList, pageindexList, pageNumList, authorList = \
        delectGuide(typenvList, titleList, pageList, pageindexList, pageNumList, authorList)
    print(len(typenvList))
    print(len(titleList))
    print(len(pageList))
    print(len(pageindexList))
    print(len(pageNumList))
    print(len(authorList))
    for n in range(len(typenvList)):
        pageOneUrl = 'http://t66y.com/htm_data/' + pageList[n] + '.html'
        urlList = getAllPages(pageNumList[n],pageOneUrl,pageindexList[n])
        logWrite(titleList[n])
        logWrite(n)
        print(n)
        try:
            initDrivers(urlList,typenvList[n],titleList[n],authorList[n])
        except Exception as ex:
            print(ex)


def generateIndexPagesList(guideIndexUrl, pagesNum):
    allurl = []
    for page in range(4,pagesNum):
        url = guideIndexUrl + '&search=&page=' + str(page + 1)
        allurl.append(url)
    return allurl

allurl = generateIndexPagesList(firsturl, pagesNum)
print(allurl)
for url in allurl:
    logWrite(url)
    getAllNovelsInOnePage(url)








