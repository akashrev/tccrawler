# created by akash on 10 Jan 2017

#!/bin/env python3
# -*- coding: utf-8 -*-

# Program fetches webpage's title; description; url -provider, domain, origin; images - url, ratio, height, width, size, mime, color;

# tested on websites:  amazon.in, firstpost.com, ndtv.com, thehindu.com, timesofindia.com, cnn.com


# import libraries
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
#import tldextract

f_json = dict()
image = dict()

q = queue.Queue()

log_file = open('scrap_json_error.log', 'a')

#urll = 'http://www.amazon.in/Vaseline-Intensive-Restore-Lotion-300ml/dp/B00791E6TY/ref=sr_1_1?s=beauty&rps=1&ie=UTF8&qid=1484121261&sr=1-1&th=1'
#urll = 'http://tinyurl.com/jnhpa45' #  'http://tinyurl.com/ll4ujbm' #
#urll = 'https://www.scientificamerican.com/article/salsa-primeval-52-million-year-old-tomatillo-found/' #use


class WebData:
    def __init__(self, url):
        self.start_time = time.time()
        self.url = url
        req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        page = urllib.request.urlopen(req)
        self.origin = page.url                                                                   # source URL
        self.soup = BeautifulSoup(page, 'lxml')


    # function to fetch title and URL's stuffs
    def head_tag(self):
        try:
            start_time = self.start_time
#            starting_time = time.time()
            provider_domain = urllib.parse.urlparse(self.origin).hostname                        # provider_domain
            #provider_name = urllib.parse.urlparse(self.origin).hostname.split('.')[1]            # provider_name
            provider_name = tldextract.extract(self.origin).domain
            parsed_uri = urllib.parse.urlparse(self.origin)
            provider_url = '{uri.scheme}://{uri.netloc}/'.format(uri = parsed_uri)               # provider_url
            head = self.soup.find('head')
            title = head.find('title')                                                      # fetch webpage's title
            if head.find('meta', {'name': 'description'}):
                decription = head.find('meta', {'name': 'description'})                     # webpage description
                f_json['description'] = decription.get('content')                           # dumps data in dictionary
            # dumping data in json
            f_json['url'] = self.url
            f_json['origin'] = self.origin
            f_json['provider_domain'] = provider_domain
            f_json['provider_name'] = provider_name
            f_json['title'] = title.text
            f_json['provider_url'] = provider_url
            f_json['parsing_head_url_time'] = (time.time()-start_time)
            #print(f_json)
            print(time.time()-start_time)
        except Exception as e:
            log_file.write('Error in URL or in head')
            log_file.write('\n')
            print(e)


    # function to fetch images and it's details
    def body_tag(self):
        try:
            starting_time = time.time()
            body = self.soup.find('body')
            images = body.find_all('img')

            def src_fun(images):
                for iterate in images:
                    if iterate.get('src'):
                        link = iterate.get('src')
                        if 'http' in link:
                            q.put(link)
                    else:
                        continue

            def grab_data_from_queue():
                while not q.empty():
                    try:
                        link = q.get()
                        #print ('this is link, ',link)
                        image_name = link.split('/').pop()
                        urllib.request.urlretrieve(link, 'image/'+image_name)
                        mime = urllib.request.urlopen(link).info()['Content-Type']

                        for infile in glob.glob('image/'+image_name):
                            try:
                                image_dict = dict()
                                im = Image.open(infile)
                                width, height = im.size  # image dimensions
                                image_dict['url'] = link
                                image_dict['width'] = width
                                image_dict['height'] = height
                                image_dict['ratio'] = ((float(height) / float(width)) * 100.00)
                                image_dict['size'] = os.stat(infile).st_size
                                image_dict['mime'] = mime
                                avg = numpy.average(im, axis=0)
                                numavg = (numpy.average(avg, axis=0))
                                image_dict['color'] = (numavg.tolist())
                            except Exception as e:
                                print(e)
                                log_file.write('Error: fetching images from os')
                                log_file.write('\n')

                                continue

                            image[(image_name)] = image_dict

                    except Exception as e:
                        print(e)
                        log_file.write('Error Images')
                        log_file.write('\n')

                    q.task_done()

                src_fun(images)
            for i in range(5):
                t1 = threading.Thread(target=grab_data_from_queue)
                t1.start()  # start the thread
            q.join()
            print (time.time() - starting_time)
            image['parsing_image_time'] = time.time() - starting_time
            print(image['parsing_image_time'])
            print(json.dumps(f_json))
            f_json["images"] = image
            with open ('scrap_json_data.json','a') as json_file:
                json_file.write(json.dumps(f_json))
                json_file.write('\n')

            print(json.dumps(f_json))


        except Exception as e:
            log_file.write('Error in body tag')
            log_file.write('\n')
            print(e)


with open ('testurl.txt','r') as url_file:
    for urll in url_file:
        try:
            page = WebData(urll)
            page.head_tag()
            page.body_tag()
        except Exception as e:
            print (e)
            log_file.write('Error reading URL from text file')
            log_file.write('\n')
            continue
log_file.close()