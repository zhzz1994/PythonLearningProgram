import requests
from bs4 import BeautifulSoup
import time
import urllib
import os

def callbackfunc(blocknum, blocksize, totalsize):
    '''回调函数
  @blocknum: 已经下载的数据块
  @blocksize: 数据块的大小
  @totalsize: 远程文件的大小
  '''
    percent = 100.0 * blocknum * blocksize / totalsize
    if percent > 100:
        percent = 100
    print ("%.2f%%"% percent)
count = 1
count + 1
coutr = str(count)
url = 'http://img.blog.csdn.net/20150320164058150'
local = 'g:\\pypic\\pic'+coutr+'.jpg'

urllib.request.urlretrieve(url,local,callbackfunc)