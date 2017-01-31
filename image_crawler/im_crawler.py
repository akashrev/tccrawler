import requests
from PIL import Image

import urllib
from bs4 import BeautifulSoup
import io
from urllib.parse import urlparse

import glob
import os

qlist=[]
url = "http://www.amazon.in/"

page = urllib.request.urlopen(url)
page.addheaders = [('User-agent', 'Mozilla/5.0')]

soup = BeautifulSoup(page, 'html.parser')


body = soup.find('body')
images = soup.find_all('img')

for iterate in images:
    if iterate.get('src'):
        link = iterate.get('src')
        if 'http' in link:
            qlist.append(link)
    else:
        continue



def image_details(links):

    if not links:
        print('Image list is empty')
    else:
        # print (links)
        for link in links:
            image_name = link.split('/').pop()
            urllib.request.urlretrieve(link, 'image/' + image_name)
        print("Done!!!")
image_details(qlist)

