from selenium import webdriver
import io
from selenium.webdriver import ActionChains
import time
from bs4 import BeautifulSoup
import urllib
import requests

url = 'http://cq.meituan.com/category/meishi/all/page2?mtt=1.index%2Fdefault%2Fpoi.0.0.j0wg1bkd'
headers = {
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.106 BIDUBrowser/8.7 Safari/537.36',
    'Cookie':'__mta=55990932.1490870853285.1490870855914.1490874369116.3; _lx_utm=utm_source%3Dbaidu%26utm_medium%3Dorganic%26utm_content%3Dhomepage%26utm_campaign%3Dbaidu; _lxsdk_s=c9824e235c7a2deb166bf09c1132%7C%7C0; domain=com; ci=45; abt=1490870850.0%7CBCF; rvct=45; ignore-zoom=true; __mta=55990932.1490870853285.1490874369116.1490876576386.4; uuid=b6c1368b6bba67005d4b.1490870850.0.0.0; oc=05k9VrkxiVJxHTRL0fWVP7_3IUvmUUeQSyCwAjZ96nnS8Ych5ly4PPGHcOb826JhX6A7OxrJ6dVS7iLlh35LaUN0HEpkye77xSv7Onhgg6TqtSfo99uADUoyqgat9v43zrGyidf0C6ejU5mjSicnVLrnnkiBMQBypOCELvKPSJk; __utma=211559370.1382170169.1490870853.1490874370.1490876576.3; __utmb=211559370.1.10.1490876576; __utmc=211559370; __utmz=211559370.1490874370.2.2.utmcsr=baidu|utmccn=baidu|utmcmd=organic|utmcct=homepage'
}

def rollpage(driver):
    js = "var q=document.body.scrollTop=5000"
    driver.execute_script(js)
    time.sleep(2)

def geturls(url) :
    driver = webdriver.PhantomJS()
    driver.viewportSize={'width':1024,'height':800}
    driver.maximize_window()
    driver.get(url)
    data = driver.title
    for n in range (1,15):
        rollpage(driver)
        print(n)
    print(data)
    time.sleep(10)
    driver.get_screenshot_as_file('G:\pypic\CCD4.jpg')
    return driver.page_source


def dnpic(title, url):
    time.sleep(1)
    local = 'g:\\pypic\\' + title + '.jpg'
    urllib.request.urlretrieve(url, local, callbackfunc)

def callbackfunc(blocknum, blocksize, totalsize):
    '''回调函数
    @blocknum: 已经下载的数据块
    @blocksize: 数据块的大小
    @totalsize: 远程文件的大小
    '''
    percent = 100.0 * blocknum * blocksize / totalsize
    if percent > 100:
        percent = 100
    print("%.2f%%" % percent)


def getpinlun(url):
    page_source = geturls(url)
    soup = BeautifulSoup(page_source,'lxml')
    imgs = soup.select('.J-webp')

    for img in imgs:
        title = img.get('alt')
        img = img.get('src')
        picname = str(title)
        dnpic(picname, img)
        f = open("G:\cccd.txt", "a+", encoding='utf-8')
        f.write(title)
        f.close()

getpinlun(url)


