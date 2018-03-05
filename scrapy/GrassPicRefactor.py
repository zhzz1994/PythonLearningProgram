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
import functools
import logging
import asyncio
import aiohttp

#logging.basicConfig(filename = os.path.join('G:\\20160916\\picdown\\', 'log.txt'), level = logging.DEBUG)

indexPagesNum = 90
guideIndexUrl = 'http://t66y.com/thread0806.php?fid=16'
keyWord = r'嫩妹'
groupSize = 40

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

def getPagesInOneIndexPage(url, titlelist, urllist, driver):
    driver.get(url)
    html = driver.page_source
    soup = BeautifulSoup(html,'lxml')
    titles = soup.find_all('h3')
    for line in titles:
        line = str(line)
        urlpattern = r'htm_data/([0-9]*/[0-9]*/[0-9]*\.html)'
        if re.search(urlpattern, line):
            url = re.search(urlpattern, line).group(1)
            urlhead = 'http://t66y.com/htm_data/'
            url = urlhead + url
            title = resolveTitle(line)
            if title:
                if re.search(keyWord,title):
                    print(str(url))
                    print(str(title))
                    urllist.append(url)
                    titlelist.append(title)
    return titlelist,urllist

def resolvePicturesSrc(html):
    picturesSrcList = []
    picturesTypeList = []
    soup = BeautifulSoup(html, 'lxml')
    body = soup.find('div', {'class': 't t2'})
    indixPagesType = 16
    if indixPagesType == 16:    #达盖尔
        urlPic = body.find_all('input')
    elif indixPagesType == 7:   #技术讨论区
        urlPic = body.find_all('img')
    for line in urlPic:
        line = str(line)
        if re.search(r'.jpg', line):
            pictype = '.jpg'
        elif re.search(r'.gif', line):
            pictype = '.gif'
        elif re.search(r'.jpeg', line):
            pictype = '.jpeg'
        elif re.search(r'.png', line):
            pictype = '.png'
        elif re.search(r'.JPG', line):
            pictype = '.JPG'
        else:
            pictype = '.jpg'
        picpattern = r'src="(.*)' + pictype
        if re.search(picpattern, line):
            picurl = re.search(picpattern, line).group(1) + pictype
            picturesSrcList.append(picurl)
            picturesTypeList.append(pictype)
    return picturesSrcList,picturesTypeList

@driversDecorator
def getPageHtml(url,driver):
    driver.get(url)
    html = driver.page_source
    return html

def downLoadAllPicturesInOnePage(url, picnum, title,loop):
    local = 'G:\\20160916\\picdown\\'+ keyWord + '\\'+ title + '\\'
    os.makedirs(local, exist_ok=True)
    try:
        html = getPageHtml(url)
        picturesSrcList, picturesTypeList = resolvePicturesSrc(html)
        picNameList = [local + keyWord + str(picnum + picOrder) + picturesTypeList[picOrder]
                       for picOrder in range(len(picturesTypeList)) ]

        tasks = [downpic(picturesSrcList[picOrder], picNameList[picOrder]) for picOrder
                 in range(len(picturesTypeList))]
        loop.run_until_complete(asyncio.wait(tasks))
    except Exception as ex:
        print(ex.__str__())

async def downpic(url,picname):
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:23.0) Gecko/20100101 Firefox/23.0'}
    try:
        img_file = open(picname,'wb')
        async with aiohttp.ClientSession().get(url,headers = headers) as web:
            img = await web.read()
        img_file.write(img)
        img_file.close()
    except Exception as ex:
        print('Exception',ex.__str__())
        print('no picture')
    finally:
        print(url)
        print(picname)

def downAllpicToOneDict(urllist):
    if urllist:
        picnum = 1000000
        n = 1
        for url in urllist:
            picnum = picnum + n * 100000
            print('第' + str(n) + '个页面')
            downLoadAllPicturesInOnePage(url, picnum, keyWord)
            n = n + 1

def generateIndexPagesList(guideIndexUrl, pagesNum):
    allurl = []
    for page in range(pagesNum):
        url = guideIndexUrl + '&search=&page=' + str(page + 1)
        allurl.append(url)
    return allurl

def downAllpicToDiffDict(pagesList, titlelist):
    picnum = 1000
    loop = asyncio.get_event_loop()
    if pagesList:
        for pagenum in range(len(pagesList)):
            print(titlelist[pagenum])
            print(pagesList[pagenum])
            downLoadAllPicturesInOnePage(pagesList[pagenum], 100000 + picnum * (pagenum + 1), titlelist[pagenum],loop)
    loop.close()

@driversDecorator
def groupResolveTitle(pagesList, titlelist, urllist, driver):
    for url in pagesList:
        print(str(url))
        titlelist, urllist = getPagesInOneIndexPage(url,titlelist,urllist,driver)
    return titlelist, urllist

def splitToGroup(allurl,groupSize):
    urlNum = len(allurl)
    titlelist = []
    urllist = []
    for block in range(int(urlNum/groupSize)):
        pagesList = []
        for n in range(groupSize):
            pagesList.append(allurl[0])
            allurl.remove(allurl[0])
        titlelist, urllist = groupResolveTitle(pagesList, titlelist, urllist)
    if allurl:
        titlelist, urllist = groupResolveTitle(allurl, titlelist, urllist)
    return titlelist, urllist

allurl = generateIndexPagesList(guideIndexUrl,indexPagesNum)
titlelist,urllist = splitToGroup(allurl,groupSize)
print(titlelist)
print(urllist)
downAllpicToDiffDict(urllist, titlelist)

# url = 'http://t66y.com/htm_data/16/1802/2962322.html'
# picnum = 100000
# title = '昨晚喝了点酒，睡得好香！好多人用异样的眼光看着我！'
# downLoadAllPicturesInOnePage(url, picnum, title)


