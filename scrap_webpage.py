# created by akash on 10 Jan 2017

#!/bin/env python3
# -*- coding: utf-8 -*-

# Program fetches webpage's title; description; url -provider, domain, origin; images - url, ratio, height, width, size, mime, color;

# tested on websites:  amazon.in, firstpost.com, ndtv.com, thehindu.com, timesofindia.com, cnn.com


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
import tldextract

f_json = dict()
image = dict()

q = queue.Queue()

log_file = open('scrap_json_error.log', 'a')

#urll = 'http://www.amazon.in/Vaseline-Intensive-Restore-Lotion-300ml/dp/B00791E6TY/ref=sr_1_1?s=beauty&rps=1&ie=UTF8&qid=1484121261&sr=1-1&th=1'
#urll = 'http://tinyurl.com/jnhpa45' #  'http://tinyurl.com/ll4ujbm' #
#urll = 'https://www.scientificamerican.com/article/salsa-primeval-52-million-year-old-tomatillo-found/' #use


class WebData:
    def __init__(self, url):

        parse_stime = time.time()
        self.url = url

        self.page = urlparser.parser(url)
        self.origin = self.page.urlorigin()
        self.provider_domain = self.page.domain()  # provider_domain
        self.provider_name = self.page.providername()
        self.provider_url = self.page.providerurl()  # provider_url

        self.parsing_time = time.time()-parse_stime
        self.start_time = time.time()

        page = urllib.request.urlopen(url)
        page.addheaders = [('User-agent', 'Mozilla/5.0')]
        self.soup = BeautifulSoup(page, 'lxml')


    # function to fetch title and URL's stuffs
    def head_tag(self):
        try:

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
                description = (head.find('meta', {'name': 'description'})).get('content')  # webpage description
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
                image = (head.find('meta', {'name': 'image'})).get('content')  # webpage description
                print('3')
            else:
                page.body_tag()
                # TODO body_fun_call()
                pass



            # webpage description
            f_json['description'] = description                                 # dumps data in dictionary
            # dumping data in json
            f_json['url'] = self.url
            f_json['origin'] = self.origin
            f_json['provider_domain'] = self.provider_domain
            f_json['provider_name'] = self.provider_name
            f_json['title'] = title
            f_json['provider_url'] = self.provider_url
            f_json['title_time'] = (time.time()-self.start_time)
            f_json['url_parsing_time'] = self.parsing_time
            #print(f_json)
            print(time.time()-self.start_time)
        except Exception as e:
            log_file.write('Error in URL or in head')
            log_file.write('\n')
            print(e)


    # function to fetch images and it's details
    def body_tag(self):
        try:
            body_starting_time = time.time()
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
            print (time.time() - body_starting_time)
            image['parsing_image_time'] = time.time() - body_starting_time
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


with open ('urls.txt','r') as url_file:
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