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
startUrl = 'http://t66y.com/thread0806.php?fid=20'
pagesNum = 24
local = 'G:\\20160916\\小说下载\\'
logposition = local + 'log.txt'

def logWrite(text):
    os.makedirs(local,exist_ok=True)
    logs = open(logposition, 'ab+')
    logN = str(text) + '\r\n'
    logs.write(logN.encode())
    logs.close()

def driversDecorator(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        chromePath = "G:\pythonpro\chrome\chromedriver.exe"
        # driver = webdriver.Chrome(executable_path=path)
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument("--headless")
        prefs = {"profile.managed_default_content_settings.images": 2}  # 不加载图片
        chrome_options.add_experimental_option("prefs", prefs)
        driver = webdriver.Chrome(chrome_options=chrome_options, executable_path=chromePath)
        backs = func(*args, **kwargs,driver = driver)
        driver.close()
        return backs
    return wrapper

def tradition2simple(line):
    # 将繁体转换成简体
    line = langconv.Converter('zh-hans').convert(line)
    return line

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

def resolveTitle(title):
    title = str(title)
    title = re.search(r'target="_blank"(.*)</a>',title)
    if title:
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
    else:
        title = None
    return title

class Novel():
    def __init__(self,line):
        self.novelTitle = self.getNovelTitle(line)
        self.novelUrl = self.getNovelUrl(line)
        self.novelPageNum = self.getNovelPageNum(line)
        self.novelAuthor = self.getNovelAuthor(line)
        self.novelType = self.getNovelType(line)
        self.novelPageList = self.getNovelPageList(line)

    def getNovelTitle(self,line):
        line = line.find('h3')
        title = resolveTitle(line)
        if title:
            title = tradition2simple(title)
        return title

    def getNovelUrl(self,line):
        line = line.find('h3')
        url = re.search(r'htm_data/([0-9]*/[0-9]*/([0-9]*))\.html', str(line))
        if url:
            url = url.group(1)
            url = 'http://t66y.com/htm_data/' + url + '.html'
        return url

    def getNovelPageNum(self,line):
        pageNum = re.search(r'blank">([0-9]*)</a></span>', str(line))
        if pageNum:
            pageNum = pageNum.group(1)
            pageNum = int(pageNum)
        return pageNum

    def getNovelPageList(self,line):
        urlTrail = re.search(r'htm_data/[0-9]*/[0-9]*/([0-9]*)\.html', str(line))
        if urlTrail:
            urlTrail = urlTrail.group(1)
            urlList = [self.novelUrl]
            urlhead = 'http://t66y.com/read.php?tid='
            if self.novelPageNum:
                for page in range(2, self.novelPageNum + 1):
                    url = str(urlhead + str(urlTrail) + '&page=' + str(page))
                    urlList.append(url)
            return urlList
        else:
            return None

    def getNovelAuthor(self,line):
        author = line.find('a', {'class': 'bl'})
        author = re.search(r'>(.*)</a>', str(author))
        author = author.group(1)
        return author

    def getNovelType(self,line):
        type = re.search(r'\[(.*)]', str(line))
        if type:
            type = type.group(1)
            type = str(type)
            if len(type) < 5:
                type = type
            else:
                type = '类型不明'
        return type

@driversDecorator
def getOneNovelContent(novel,driver):
    novelContentList = []
    urlList = novel.novelPageList
    for url in urlList:
        getOnePageText(url,novel.novelAuthor,novelContentList,driver)
    return novelContentList

def downOneNovelContent(local, novel,novelContentList):
    dirlocal = local + novel.novelType + '\\'
    os.makedirs(dirlocal, exist_ok=True)
    local = dirlocal + novel.novelTitle + '.txt'
    file = open(local,'wb')
    enterKey = str('\r\n').encode()
    file.write(str(novel.novelType).encode())
    file.write(enterKey)
    for novelContent in novelContentList:
        if novelContent:
            print(novelContent)
            file.write(novelContent.encode())
            file.write(enterKey)
    file.close()

def getOnePageText(url,author,novelContentList,driver):
    driver.get(url)
    print(url)
    html = driver.page_source
    soup = BeautifulSoup(html, 'lxml')
    body = soup.find_all('div',{'class':'t t2'})
    authorPattern = r'<b>' + author + '</b>'
    for div in body:
        if re.search(authorPattern,str(div)):
            div = div.find_all('div',{'class':'tpc_content'})
            div = formationPassage(div)
            novelContentList.append(div)
            print(div)

@driversDecorator
def getNovelList(url,driver):
    novels = []
    driver.get(url)
    html = driver.page_source
    soup = BeautifulSoup(html,'lxml')
    lines = soup.find_all('tr',{'class':'tr3 t_one tac'})
    for line in lines:
        novel = Novel(line)
        novels.append(novel)
    return novels

def novelsCutted(novels):
    novelsCutted = []
    for novel in novels:
        if novel.novelAuthor not in ['Diss','tsq456','lj413025','vonder','administrator']:
            novelsCutted.append(novel)
    return novelsCutted

def generateIndexPagesList(guideIndexUrl, pagesNum):
    allurl = []
    for page in range(23,pagesNum):
        url = guideIndexUrl + '&search=&page=' + str(page + 1)
        allurl.append(url)
    return allurl

def downBunchNovles(novels,local):
    n = 1
    for novel in novels:
        try:
            logWrite(novel.novelTitle)
            print(novel.novelTitle)
            logWrite(novel.novelUrl)
            print(novel.novelUrl)
            logWrite(n)
            print(n)
            novelContentList = getOneNovelContent(novel)
            downOneNovelContent(local, novel,novelContentList)
        except Exception as ex:
            print(ex)
        finally:
            n = n + 1

allurl = generateIndexPagesList(startUrl,pagesNum)
for url in allurl:
    logWrite(url)
    print(url)
    novels = getNovelList(url)
    novels = novelsCutted(novels)
    novels = novels[25:]
    downBunchNovles(novels,local)






