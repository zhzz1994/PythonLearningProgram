from selenium import webdriver
import io
from selenium.webdriver import ActionChains
import time
from bs4 import BeautifulSoup
import urllib
import urllib.request
import base64
import requests
from selenium.webdriver.chrome.options import Options
import re
from urllib.request import urlretrieve
import functools
import logging
import asyncio
import aiohttp
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait
import sys
import os
from PIL import Image, ImageDraw, ImageFont, ImageFilter

List = []

<<<<<<< HEAD
posterNameList = ['']
=======
posterNameList = ['madam-w','liliko99','hatsuneyuko','mysexpet']
#'cnllm'
>>>>>>> 1a873b06183948a12a0cac1fed684583f0516d9a
# 'maydaylxy' 'miaotutu' 'yinminwansui' 'hitagiplus' 'slz841126' 'fkfkcf11' 'lofsj'
#'babadexiaom' 'hentaiying' ‘kitmen83’ 'dazai-ying' 'luoliuuu' 'anapapapa'
# 'binbin0505' 'zhling1994' 'kotori950422' 'shuimuqingfeng' 'liniang520','gluteipaffuto',
# 'madam-w' 'x-nvshen' 'liliko99' ,'hatsuneyuko' 'mysexpet'


local = 'G:\\20160916\\tumblr下载\\'

downPicTrue = True
downVideoTrue = True
downOriginTrue = True


class Iframe():
    def __init__(self,frameType,frameId,frameText,frameSrc,articalId):
        self.frameType = frameType
        self.frameId = frameId
        self.frameText = frameText
        self.frameSrc = frameSrc
        self.articalId = articalId

class PhotoSet():
    def __init__(self,html,text):
        self.text =  text
        self.photos = self.getPhotos(html)

    def getPhotos(self,html):
        imgs = []
        soup = BeautifulSoup(html, 'lxml')
        for a in soup.find_all('a'):
            img = a.get('href','href')
            imgs.append(img)
        return imgs

    def downLoad(self,local,picnum):
        text = formationTextInPic(self.text)
        if len(text) > 20 :
            textlocal = local + '\\' + str(picnum) + '文字.jpg'
            textToPic(text, textlocal)
        text = formationText(self.text)
        for photourl in self.photos:
            picnum = picnum + 1
            name = str(text)
            type = getPhotoType(photourl)
            type = str(type)
            picname = local + '\\' + str(picnum) + '图片'+ name + type
            downPic(photourl, picname)

class PhotoSheet():
    def __init__(self,text,photo):
        self.text = text
        self.photo = photo
        self.type = self.getType()

    def downLoad(self,local,picnum):
        text = formationTextInPic(self.text)
        if len(text) > 20 :
            textlocal = local + '\\' + str(picnum) + '文字.jpg'
            textToPic(text, textlocal)
        text = formationText(self.text)
        name = str(text)
        picname = local + '\\' + str(picnum) +  '图片'+ str(name) + str(self.type)
        downPic(self.photo, picname)

    def getType(self):
        type = getPhotoType(self.photo)
        type = str(type)
        return type

class Video():
    def __init__(self,html,text):
        self.text = text
        self.videoUrl = self.getVideoUrl(html)

    def downLoad(self,local,videonum):
        text = formationTextInPic(self.text)
        if len(text) > 20:
            textlocal = local + '\\' + str(videonum) + '文字.jpg'
            textToPic(text, textlocal)
        text = formationText(self.text)
        name = str(text)
        filename = local + '\\'+ str(videonum) + '视频' +  name + '.mp4'
        print(filename)
        print(self.videoUrl)
        urlretrieve(url=self.videoUrl, filename=filename, reporthook=self.cbk)

    def getVideoUrl(self,html):
        soup = BeautifulSoup(html, 'lxml')
        video = soup.find('video')
        source = video.find('source')
        if source:
            url = source.get('src','src')
            return url
        else:
            return None

    def cbk(self,a, b, c):
        per = 100.0 * a * b / c
        if per > 100:
            per = 100
        print('%.2f%%' % per)

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

@driversDecorator
def tumblrDownload(posterNameList,local,driver):
    logined = loginRepeat(driver,repeat = 0)
    if logined:
        for posterName in posterNameList:
            try:
                downLoadAllObjects(posterName, driver, local)
            except Exception as ex:
                print(ex)
            finally:
                logWrite(posterName)
                print(posterName)

def loginRepeat(driver,repeat):
    logined = login(driver)
    if logined:
        return True
    elif repeat > 5:
        return False
    else:
        repeat = repeat + 1
        loginRepeat(driver,repeat)

def login(driver):
    url = 'https://www.tumblr.com'
    email = '1094835165@qq.com'
    password = '1994212ggbf'
    try:
        driver.get(url)
        driver.find_element_by_id('signup_login_button').click()
        elem = driver.find_element_by_id('signup_determine_email')
        elem.clear()
        elem.send_keys(email)
        driver.find_element_by_id('signup_forms_submit').click()
        time.sleep(1)
        elem = driver.find_element_by_id('signup_password')
        elem.clear()
        elem.send_keys(password)
        driver.find_element_by_id('signup_forms_submit').click()
        print('login sucesses')
        logWrite('login sucesses')
        return True
    except Exception as ex:
        print(ex)
        print('login failed')
        logWrite('login failed')
        return False

def downLoadAllObjects(posterName, driver, local):
    photosheetsList = []
    photosetsList = []
    videosList = []
    url = 'https://' + str(posterName) + '.tumblr.com'
    postlocal = local + posterName
    os.makedirs(postlocal,exist_ok=True)
    pages = getAllPages(url, driver)
    for page in pages:
        # photosheets, photosets, videos = getObjectsInOnePage(page, driver)
        # photosheetsList = photosheetsList + photosheets
        # photosetsList = photosetsList + photosets
        # videosList = videosList + videos
        try:
            photosheets,photosets,videos = getObjectsInOnePage(page,driver)
            photosetsList = photosetsList + photosets
            photosheetsList = photosheetsList + photosheets
            videosList = videosList + videos
        except Exception as ex:
            print(ex)
            print('error in downLoadAllObjects')
        print(page)
    printAndLog(photosetsList, photosheetsList, videosList)
    if downPicTrue:
        downLoadPhotoSets(photosetsList,postlocal)
        downLoadPhotoSheets(photosheetsList,postlocal)
    if downVideoTrue:
        downLoadVideos(videosList,postlocal)

def getAllPages(url, driver):
    driver.get(url)
    html = driver.page_source
    soup = BeautifulSoup(html, 'lxml')
    pages = [url]
    if soup.find('footer', {'class': 'content clearfix'}):
        footer = soup.find('footer', {'class': 'content clearfix'})
        footer = footer.find('a')
        if footer:
            totalpage = footer.get('data-total-pages','1')
            totalpage = int(totalpage)
            print(totalpage)
            logWrite('totalpages')
            logWrite(totalpage)
            pages = [url + '/page/' + str(num) for num in range(1, totalpage + 1)]
    return pages

def getObjectsInOnePage(page,driver):
    driver.get(page)
    html = driver.page_source
    soup = BeautifulSoup(html, 'lxml')
    articles = getAllArticals(soup)
    if downOriginTrue:
        articles = getOriginalArticals(articles)
    iframes = getFrames(articles)
    photosheets = getPhotoSheet(articles)
    photosets = getPhotoSets(iframes, driver)
    videos = getVideos(iframes, driver)
    return photosheets,photosets,videos

def getAllArticals(soup):
    articles = soup.find_all('article')
    return articles

def getOriginalArticals(articles):
    originalarticals = []
    for article in articles:
        if isOriginalArtical(article):
            originalarticals.append(article)
    return originalarticals

def isOriginalArtical(article):
    header = article.find('header')
    if header:
        if  header.find('a'):
            return False
        else:
            return True
    else:
        return True

def getFrames(originalarticals):
    iframes = []
    for artical in originalarticals:
        if artical.find('iframe'):
            articalId = artical.get('data-post-id','data-post-id')
            frameId = artical.find('iframe').get('id','id')
            frameType = artical.find('iframe').get('class','class')
            frameSrc = artical.find('iframe').get('src', 'src')
            frameText = artical.find('figcaption')
            if frameText:
                frameText = frameText.find('p')
            iframes.append(Iframe(frameType,frameId,frameText,frameSrc,articalId))
    return iframes

def getPhotoSheet(originalarticals):
    photosheets = []
    for artical in originalarticals:
        if artical.find('div',{'class','photo-wrapper-inner'}):
            text = artical.find('figcaption')
            if text:
                text = text.find('p')
            photo = artical.find('div',{'class','photo-wrapper-inner'}).find('img').get('src','src')
            photosheet = PhotoSheet(text,photo)
            photosheets.append(photosheet)
    return photosheets

def getPhotoSets(iframes,driver):
    photosets = []
    for iframe in iframes:
        if 'photoset' in iframe.frameType:
            if iframe.frameId:
                driver.switch_to.frame(iframe.frameId)
                html = driver.page_source
                photoset = PhotoSet(html,iframe.frameText)
                photosets.append(photoset)
                driver.switch_to.parent_frame()
    return photosets

def getVideos(iframes,driver):
    videos = []
    for iframe in iframes:
        if 'tumblr_video_iframe' in iframe.frameType:
            if iframe.frameSrc:
                xpath = '//iframe[contains(@src,\'' + iframe.frameSrc + '\')]'
                driver.switch_to.frame(driver.find_element_by_xpath(xpath))
                html = driver.page_source
                video = Video(html, iframe.frameText)
                videos.append(video)
                driver.switch_to.parent_frame()
    return videos

def downLoadVideos(videosList,postlocal):
    print('start downLoadVideos')
    videonum = 300000000
    for video in videosList:
        try:
            video.downLoad(postlocal,videonum)
        except Exception as ex:
            print(ex)
            print('error in downLoadVideos')
        finally:
            videonum = videonum + 1

def downLoadPhotoSets(photosetsList,postlocal):
    print('start downLoadPhotoSets')
    picnum = 100000000
    for photoset in photosetsList:
        # photoset.downLoad(postlocal,picnum,)
        # picnum = picnum + 1000
        try:
            photoset.downLoad(postlocal,picnum)
        except Exception as ex:
            print(ex)
            print('error in downLoadPhotoSets')
        finally:
            picnum = picnum + 1000

def downLoadPhotoSheets(photosheetsList,postlocal):
    print('start downLoadPhotoSheets')
    picnum = 200000000
    for photoset in photosheetsList:
        # photoset.downLoad(postlocal,picnum)
        # picnum = picnum + 1
        try:
            photoset.downLoad(postlocal,picnum)
        except Exception as ex:
            print(ex)
            print('error in downLoadPhotoSheets')
        finally:
            picnum = picnum + 1

def downPic(url,picname):
    try:
        req = urllib.request.Request(url = url)
        img = urllib.request.urlopen(req).read()
        img_file = open(picname, 'wb')
        img_file.write(img)
        img_file.close()
    except Exception as ex:
        print(ex)
    finally:
        print(url)
        print(picname)

def textToPic(text,local):
    CharactersInOneLine = 24
    LinesInOnePage = 16
    TotalLines = int(len(text) / CharactersInOneLine) + 1
    TotalPages = int(TotalLines / LinesInOnePage) + 1
    width = 1000
    height = 600 * TotalPages
    Imagetext = ''
    for line in range(int(TotalLines) + 1):
        start = line * CharactersInOneLine
        linetext = text[start:24 + start]
        linetext = linetext+ '\n'
        Imagetext = Imagetext + linetext
    image = Image.new('RGB', (width, height), (255, 255, 255))
    font = ImageFont.truetype('C:\\WINDOWS\\Fonts\\STXINWEI.TTF', 40)
    draw = ImageDraw.Draw(image)
    draw.text((30, 30), Imagetext, font=font, fill=(0, 0, 0))
    image.save(local)
    print('text image')

def formationText(Text):
    Text = str(Text)
    Text = re.sub(r'<a(.*)</a>', '', Text)
    Text = re.sub(r'<p>','',Text)
    Text = re.sub(r'</p>','', Text)
    Text = re.sub(r'<br/>', '', Text)
    Text = re.sub(r' ', '', Text)
    Text = re.sub(r'\n', '', Text)
    Text = re.sub(r'“', '', Text)
    Text = re.sub(r'”', '', Text)
    Text = re.sub(r'（', '', Text)
    Text = re.sub(r'）', '', Text)
    Text = re.sub(r'\(', '', Text)
    Text = re.sub(r'\)', '', Text)
    Text = re.sub(r'。','', Text)
    Text = re.sub(r'！', '', Text)
    Text = re.sub(r'，', '', Text)
    Text = re.sub(r',', '', Text)
    Text = re.sub(r'；', '', Text)
    Text = re.sub(r'<b>', '', Text)
    Text = re.sub(r'</b>', '', Text)
    Text = re.sub(r'<pstyle="">', '', Text)
    Text = re.sub(r'<', '', Text)
    Text = re.sub(r'>', '', Text)
    Text = re.sub(r'"', '', Text)
    Text = re.sub(r'\.', '', Text)
    Text = re.sub(r'】', '', Text)
    Text = re.sub(r'【', '', Text)
    Text = re.sub(r'~', '', Text)
    Text = re.sub(r'\*', '', Text)
    Text = re.sub(r'…', '', Text)
    Text = re.sub(r'：', '', Text)
    Text = Text[:20]
    return Text

def formationTextInPic(Text):
    Text = str(Text)
    Text = re.sub(r'<a(.*)</a>', '', Text)
    Text = re.sub(r'<p>','',Text)
    Text = re.sub(r'</p>','', Text)
    Text = re.sub(r' ', '', Text)
    Text = re.sub(r'<br/>', '  ', Text)
    Text = re.sub(r'<b>', '', Text)
    Text = re.sub(r'</b>', '', Text)
    Text = re.sub(r'<pstyle="">', '', Text)
    Text = re.sub(r'<', '', Text)
    Text = re.sub(r'>', '', Text)
    return Text

def getPhotoType(photourl):
    photourl = str(photourl)
    if re.search(r'.jpg', photourl):
        pictype = '.jpg'
    elif re.search(r'.gif', photourl):
        pictype = '.gif'
    elif re.search(r'.jpeg', photourl):
        pictype = '.jpeg'
    elif re.search(r'.png', photourl):
        pictype = '.png'
    elif re.search(r'.JPG', photourl):
        pictype = '.JPG'
    else:
        pictype = '.jpg'
    return pictype

def logWrite(text):
    logposition = local + 'log.txt'
    os.makedirs(local,exist_ok=True)
    logs = open(logposition, 'ab+')
    logN = str(text) + '\r\n'
    logs.write(logN.encode())
    logs.close()

def printAndLog(photosetsList,photosheetsList,videosList):
    print(len(photosetsList))
    print(len(photosheetsList))
    print(len(videosList))
    logWrite('photosetsList')
    logWrite(len(photosetsList))
    logWrite('photosheetsList')
    logWrite(len(photosheetsList))
    logWrite('videosList')
    logWrite(len(videosList))

<<<<<<< HEAD
def main():
    tumblrDownload(posterNameList,local)

if __name__ == '__main__':
    main()
=======
tumblrDownload(posterNameList,local)


>>>>>>> 1a873b06183948a12a0cac1fed684583f0516d9a
