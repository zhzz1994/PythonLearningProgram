import requests
from bs4 import BeautifulSoup
import time
import urllib
import os
import re
import pymysql


headers = {
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.106 BIDUBrowser/8.7 Safari/537.36',
    'Cookie':'__utmt=1; __utma=81379588.292354748.1490268308.1490605522.1490610588.5; __utmb=81379588.1.10.1490610588; __utmc=81379588; __utmz=81379588.1490603404.3.3.utmcsr=baidu|utmccn=(organic)|utmcmd=organic|utmctr=%E8%B1%86%E7%93%A3; ll="108309"; bid=Lca1RNgIRiY; viewed="26284925"; ps=y; dbcl2="136865962:xh/9+e+2kqk"; ck=c48h; push_noty_num=0; push_doumail_num=0; __utmt_douban=1; __utma=30149280.1163315445.1490003408.1490605522.1490610565.7; __utmb=30149280.1.10.1490610565; __utmc=30149280; __utmz=30149280.1490603130.5.5.utmcsr=baidu|utmccn=(organic)|utmcmd=organic; ap=1'
}
# urls = ['https://book.douban.com/annual2016/?source=navigation#{}'.format(str(i)) for i in range[1,10]]
url = 'https://book.douban.com/tag/%E4%B8%AD%E5%9B%BD%E6%96%87%E5%AD%A6'

def getpinlun(url,cursor):
    urls = geturl(url)
    for url in urls:
        time.sleep(0.5)
        wbdata = requests.get(url,headers=headers)
        soup = BeautifulSoup(wbdata.text,'lxml')
        title =  soup.title.text
        authors = soup.select('#info > a:nth-of-type(1)')
        author = authors[0].text
        author = author.lstrip('\n            '),
        intros = soup.find_all("div","intro")
        if len(intros)==2:
            bookintro = intros[0].text
            autintro = intros[1].text
        elif len(intros)==1:
            bookintro = intros[0].text
        else:
            bookintro = intros[1].text
            autintro = intros[2].text
        bookintro = bookintro.lstrip('\n')
        autintro = autintro.lstrip('\n')
        ratings = soup.select('#interest_sectl > div > div.rating_self.clearfix > strong')
        ratingstr = ratings[0].text
        infos = soup.select('#info')
        info = infos[0].text
        pagenumber = re.search('页数: (.*?)\n', info, re.S)
        pagenums = pagenumber.groups(0)
        pagenumstr = pagenums[0]
        rating = float(ratingstr)
        pagenum = int(pagenumstr)

        cursor.execute('insert into doubanbook4 (作者简介,评分,作者,书名,页数,网址,内容) value (%s,%s,%s,%s,%s,%s,%s)',[autintro,rating,author,title,pagenum,url,bookintro])
        db.commit()

        # print(bookintro)
        # cursor.execute('select * from doubanbook4')
        # data = cursor.fetchall()
        # print(data)
        # print(title)
        # print(info)
        print(title)

def geturl(url):
    urls = []
    wbdata = requests.get(url, headers=headers)
    soup = BeautifulSoup(wbdata.text, 'lxml')
    for link in soup.select('#subject_list > ul > li > div.info > h2 > a'):
        urls.append(link.get('href'))
    return urls


db = pymysql.connect(host='localhost', user='root', password='1094835165', db='zhzz', charset="utf8")
cursor = db.cursor()
getpinlun(url,cursor)
db.close()







