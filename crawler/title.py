# import libraries
import urlparser  # personal library
import time
import urllib
from urllib.request import Request
from bs4 import BeautifulSoup
import glob
import os
from PIL import Image
import json
import threading
import queue
import numpy
import tldextract



# urll = 'http://www.amazon.in/Vaseline-Intensive-Restore-Lotion-300ml/dp/B00791E6TY/ref=sr_1_1?s=beauty&rps=1&ie=UTF8&qid=1484121261&sr=1-1&th=1'
# urll = 'http://tinyurl.com/jnhpa45' #  'http://tinyurl.com/ll4ujbm' #
# urll = 'https://www.scientificamerican.com/article/salsa-primeval-52-million-year-old-tomatillo-found/' #use


class WebData:
    def __init__(self, url):

        self.url = url

        self.page = urlparser.parser(url)


        page = urllib.request.urlopen(url)
        page.addheaders = [('User-agent', 'Mozilla/5.0')]
        self.soup = BeautifulSoup(page, 'lxml')

    # function to fetch title and URL's stuffs
    def head_tag(self):


        head = self.soup.find('head')

        # title
        if head.find('meta', {'property': 'og:title'}):  # if meta tag having property 'og:title'
            title = head.find('meta', {'property': 'og:title'}).get('content')

        elif head.find('meta', {'name': 'twitter:title'}):
            title = head.find('meta', {'name': 'twitter:title'}).get('content')
        else:
            title = head.find('title').text  # fetch webpage's title

        print(title)

        # description
        if head.find('meta', {'property': 'og:description'}):  # if meta tag having property 'og:title'
            description = (head.find('meta', {'property': 'og:description'})).get('content')

        elif head.find('meta', {'name': 'twitter:description'}):
            description = (head.find('meta', {'name': 'twitter:description'})).get('content')
        elif head.find('meta', {'name': 'description'}):
            description = (head.find('meta', {'name': 'description'})).get('content')                     # webpage description
        else:
            description = ""

        print (description)

        # image
        if head.find('meta', {'property': 'og:image'}):
            image = (head.find('meta', {'property': 'og:image'})).get('content')
            print('1')
        elif head.find('meta', {'name': 'twitter:image'}):
            image = (head.find('meta', {'name': 'twitter:image'})).get('content')
            print('2')
        elif head.find('meta', {'name': 'image'}):
            image = (head.find('meta', {'name': 'image'})).get('content')                     # webpage description
            print('3')
        else:
            image = ('no')

        print(image)


page = WebData('http://www.amazon.in/')
page.head_tag()
