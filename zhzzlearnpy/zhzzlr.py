import requests
from bs4 import BeautifulSoup
import time
import urllib
import os

headers = {
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.106 BIDUBrowser/8.7 Safari/537.36',
    'Cookie':'__mta=55990932.1490870853285.1490870855914.1490874369116.3; _lx_utm=utm_source%3Dbaidu%26utm_medium%3Dorganic%26utm_content%3Dhomepage%26utm_campaign%3Dbaidu; _lxsdk_s=c9824e235c7a2deb166bf09c1132%7C%7C0; domain=com; ci=45; abt=1490870850.0%7CBCF; rvct=45; ignore-zoom=true; __mta=55990932.1490870853285.1490874369116.1490876576386.4; uuid=b6c1368b6bba67005d4b.1490870850.0.0.0; oc=05k9VrkxiVJxHTRL0fWVP7_3IUvmUUeQSyCwAjZ96nnS8Ych5ly4PPGHcOb826JhX6A7OxrJ6dVS7iLlh35LaUN0HEpkye77xSv7Onhgg6TqtSfo99uADUoyqgat9v43zrGyidf0C6ejU5mjSicnVLrnnkiBMQBypOCELvKPSJk; __utma=211559370.1382170169.1490870853.1490874370.1490876576.3; __utmb=211559370.1.10.1490876576; __utmc=211559370; __utmz=211559370.1490874370.2.2.utmcsr=baidu|utmccn=baidu|utmcmd=organic|utmcct=homepage'
}
url = 'http://cq.meituan.com/category/meishi?mtt=1.index%2Ffloornew.lz.3-38022.j0wc3tt4'

wbdata = requests.get(url,headers = headers)
soup = BeautifulSoup(wbdata.text,'lxml')
imgs = soup.select('.J-webp')

for img in imgs:
    img = img.get('alt')
print(img)