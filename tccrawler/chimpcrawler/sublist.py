# import libraries
import urlparser                            # personal library
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
import logging
import sys
from threading import Thread

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
                    datefmt='%m/%d/%Y %I:%M:%S %p',
                    filename='myapp.log',
                    filemode='a')
logging.info('Program executed.')

threads = 4
image_height = 500
image_width = 500

image_json = {}
final_json = {}

op_file = open('qqqqqq.json','a')


def sleeper(link):

    print('link.....', link)
    image_name = link.split('/').pop()
    try:
        urllib.request.urlretrieve(link, 'image/' + image_name)
        mime = urllib.request.urlopen(link).info()['Content-Type']

        infiles = glob.glob('image/' + image_name)
        infile = "".join(infiles)

        print('infile.:', infile)
        image_dict = dict()

        im = Image.open(infile)
        width, height = im.size  # image dimensions

        if width < image_width or height < image_height:
            print('size less than 500, by ')

        else:
            print("greater than 500")

            print('Found it.............. by')
            image_json['link'] = link
            image_json['height'] = height
            image_json['width'] = width
            del(image_list[0:len(image_list)])
            return mime, width, height

    except Exception as e:
        print('Error:', e)




with open('testurl.txt', 'r') as url_file:
    for url in url_file:
        print('url is....',url)
        page = urllib.request.urlopen(url)
        page.addheaders = [('User-agent', 'Mozilla/5.0')]
        soup = BeautifulSoup(page, 'lxml')
        body = soup.find('body')
        images = body.find_all('img')
        image_list = []

        for iterate in images:
            if iterate.get('src'):
                link = iterate.get('src')
                if 'http' in link:
                    image_list.append(link)

        image_json={}


        while image_list:
            if len(image_list) > threads:
                image_sublist = image_list[0:threads]
                del (image_list[0:threads])
            else:
                image_sublist = image_list[0:len(image_list)]
                del (image_list[0:len(image_list)])
            print('a', image_list)
            print('image_sublist', image_sublist)

            t = [Thread(target=sleeper, args=(url,)) for url in image_sublist]
            for thread in t:
                thread.start()
            for thread in t:
                thread.join()
            mime, height, width = target
            print (mime)
            print (height)
            print(width)


        final_json[url] = image_json
print(final_json)