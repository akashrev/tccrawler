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

f_json = dict()
image = dict()

url = 'http://tinyurl.com/ll4ujbm'
#print 'url:', url
f_json['url'] = url

starting_time = time.time()


page = urllib.request.urlopen(url)

origin = page.url
#print 'origin url:', origin
f_json['origin'] = origin

provider = urllib.parse.urlparse(origin).hostname
#print 'provider:',provider
f_json['provider'] = provider

provider_name = urllib.parse.urlparse(origin).hostname.split('.')[1]
#print 'provider_name:', provider_name
f_json['provider_name'] = provider_name

soup = BeautifulSoup(page, 'lxml')

head = soup.find('head')
title = head.find('title')
#print 'title:', title.text
f_json['title'] = title.text

if head.find('meta', {'name': 'description'}):
    decription = head.find('meta', {'name': 'description'})
    #print 'description:', decription.get('content')
    f_json['description'] = decription.get('content')

body = soup.find('body')
images = body.find_all('img')
for iterate in images:
    try:
        link = iterate.get('src')
        image_name = link.split('/').pop()
        if 'http' in link:
            #            print link
            urlretrieve(link, image_name)

            d = urllib.request.urlopen(link).info()['Content-Type']
            print ('mime: ',d)


            for infile in glob.glob(image_name):
                try:
                    image_dict = dict()

                    im = Image.open(infile)

                    width, height = im.size  # image dimensions

                    print(infile)
                    print ('width:', width)
                    print ('height:', height)
                    print ('ratio:', ((float(height)/float(width))*100.00))
                    print ('size', os.stat(infile).st_size, 'bytes')
                    print ('mime:', im.format)

                    #print 'color', im.getcolors()

                    #rgb_im = im.convert('RGB')
                    #r, g, b = rgb_im.getpixel((1, 1))
                    #print 'Image color:', r,g,b

                    image_dict['url'] = link
                    image_dict['width'] = width
                    image_dict['height'] = height
                    image_dict['ratio'] = ((float(height)/float(width))*100.00)
                    image_dict['size'] = os.stat(infile).st_size
                    image_dict['mime'] = d

                except Exception as e:
                    print(e)
                    continue
                image[(image_name)] = image_dict
                f_json["images"] = image

    except Exception as e:
        print ('Error: ', e)
        continue



print(json.dumps(f_json))
print('Total time taken: ', time.time()-starting_time)







'''


print head.find(property='fb:app_id') if head.find(property='fb:app_id') else 0


for i in meta:
    print i.has_attr('property')


if head.find('meta', {'property' : 'fb:app_id'}):
    print head.find('meta', {'property' : 'fb:app_id'})



meta = head.find_all('meta')
for iter in meta:
    if iter.find('meta',{'property' : 'fb:app_id'}):
        print iter
        break
    else:
        print 'some error',iter
'''
'''
body = soup.find_all('img')
#print body
for iter in body:
    print iter.get('src')
'''

'''
# downlaod images
image = body.find_all('src')
urllib.urlretrieve(image, image+".jpg")
print  image
'''


