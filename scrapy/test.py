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


def bigger(n):
    if n > 5:
        return True
    else:
        return False


def add(n):
    return n + 1

def rip(n):
    n = add(n)
    result = bigger(n)
    if result:
        print('111')
    else:
        print('222')
        rip(n)

rip(3)