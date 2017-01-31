#!/bin/env python3
# -*- coding: utf-8 -*-


# import libraries
from bs4 import BeautifulSoup
import urllib
#from urllib.parse import urlparse
#from urllib.request import urlopen
from urllib.request import urlretrieve
import glob
from PIL import Image
import os
import json
import threading
from threading import Thread
import time
import numpy

f_json = dict()
image = dict()

urll = 'http://www.thoughtchimp.com/'

#urll = 'http://tinyurl.com/jnhpa45' #  'http://tinyurl.com/ll4ujbm' #



class page_head:
    def __init__(self, url):
        self.url = url
        page = urllib.request.urlopen(url)
        self.origin = page.url                                                                   # source URL
        self.soup = BeautifulSoup(page, 'lxml')

    def head_tag(self):
        try:
            starting_time = time.time()
            provider_domain = urllib.parse.urlparse(self.origin).hostname                        # provider_domain
            provider_name = urllib.parse.urlparse(self.origin).hostname.split('.')[1]            # provider_name
            parsed_uri = urllib.parse.urlparse(self.origin)
            provider_url = '{uri.scheme}://{uri.netloc}/'.format(uri = parsed_uri)               # provider_url
            head = self.soup.find('head')
            title = head.find('title')                                                      # fetch webpage's title
            if head.find('meta', {'name': 'description'}):
                decription = head.find('meta', {'name': 'description'})                     # webpage description
                f_json['description'] = decription.get('content')                           # dumps data in dictionary
            f_json['url'] = self.url
            f_json['origin'] = self.origin
            f_json['provider_domain'] = provider_domain
            f_json['provider_name'] = provider_name
            f_json['title'] = title.text
            f_json['provider_url'] = provider_url

            print(f_json)
            print(time.time()-starting_time)
        except Exception as e:
            print(e)


    def body_tag(self):
        try:
            starting_time = time.time()
            body = self.soup.find('body')
            images = body.find_all('img')
            for iterate in images:
                if iterate.get('src'):
                    link = iterate.get('src')
                else:
                    continue
                image_name = link.split('/').pop()
                if 'http' in link:
                    urlretrieve(link, image_name)
                    mime = urllib.request.urlopen(link).info()['Content-Type']
                    for infile in glob.glob(image_name):
                        try:
                            image_dict = dict()
                            im = Image.open(infile)
                            width, height = im.size                                   # image dimensions
                            image_dict['url'] = link
                            image_dict['width'] = width
                            image_dict['height'] = height
                            image_dict['ratio'] = ((float(height)/float(width))*100.00)
                            image_dict['size'] = os.stat(infile).st_size
                            image_dict['mime'] = mime
                            avg = numpy.average(im, axis=0)
                            numavg = (numpy.average(avg, axis=0))
                            # print(numavg.tolist())
                            image_dict['color'] = (numavg.tolist())
                        except Exception as e:
                            print(e)
                            continue
                        image[(image_name)] = image_dict
                        f_json["images"] = image
            print(json.dumps(f_json))

            print (time.time()-starting_time)
        except Exception as e:
            print(e)


page = page_head(urll)
page.head_tag()
page.body_tag()