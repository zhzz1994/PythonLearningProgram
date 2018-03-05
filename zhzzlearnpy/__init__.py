import requests
from bs4 import BeautifulSoup
import time
import urllib
import os
url = 'https://book.douban.com/subject/1082154/'
wbdata = requests.get(url)
soup = BeautifulSoup(wbdata.text, 'lxml')
img = soup.select('#mainpic > a > img')
print(img[0].get('src'))