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
image_height = 200
image_width = 200

image_json = {}
final_json = {}

op_file = open('scraper_op.json', 'a')



class WebData:
    def __init__(self, url):
        logging.info('Parsing URL')
        parse_stime = time.time()
        self.url = url
        print('before parser')
        self.page = urlparser.parser(url)
        print('after parser')
        self.origin = self.page.urlorigin()
        self.provider_domain = self.page.domain()  # provider_domain
        self.provider_name = self.page.providername()
        self.provider_url = self.page.providerurl()  # provider_url

        self.parsing_time = time.time()-parse_stime
        self.head_stime = time.time()
        logging.info('Requesting webpage through urllib library')
        page = urllib.request.urlopen(url)
        page.addheaders = [('User-agent', 'Mozilla/5.0')]
        self.soup = BeautifulSoup(page, 'lxml')


    # function to fetch title and URL's stuffs
    def head_tag(self):
        print('head')
        head = self.soup.find('head')
        logging.info('Fetching webpage\'s title')
        # title
        if head.find('meta', {'property': 'og:title'}):  # if meta tag having property 'og:title'
            title = head.find('meta', {'property': 'og:title'}).get('content')

        elif head.find('meta', {'name': 'twitter:title'}):
            title = head.find('meta', {'name': 'twitter:title'}).get('content')
        else:
            title = head.find('title').text  # fetch webpage's title

        print(title)
        logging.debug('Fetched Webpage title')

        # description
        logging.info('Fetching webpage\'s description')
        if head.find('meta', {'property': 'og:description'}):  # if meta tag having property 'og:title'
            description = (head.find('meta', {'property': 'og:description'})).get('content')

        elif head.find('meta', {'name': 'twitter:description'}):
            description = (head.find('meta', {'name': 'twitter:description'})).get('content')
        elif head.find('meta', {'name': 'description'}):
            description = (head.find('meta', {'name': 'description'})).get('content')  # webpage description
        else:
            logging.warning('Webpage\'s Description not available')
            description = ""
        logging.debug('Fetched Webpage title')
        print (description)

        final_json['title_desc_time'] = (time.time() - self.head_stime)

        self.image_time = time.time()

        # image
        logging.info('Fetching webpage\'s image')
        if head.find('meta', {'property': 'og:mage'}) and head.find('meta', {'property': 'og:mage'}).get('content') != "":
            image = (head.find('meta', {'property': 'og:image'})).get('content')
            print('og:image')
            WebData.image_details(self, image, 'head')

        elif head.find('meta', {'name': 'twitter:image'}):
            image = (head.find('meta', {'name': 'twitter:image'})).get('content')
            print('twitter:image')
            print (image)
            WebData.image_details(self, image, 'head')
        elif head.find('meta', {'name': 'image'}):
            image = (head.find('meta', {'name': 'image'})).get('content')  # webpage description
            print('meta image')
            WebData.image_details(self, image, 'head')
        else:
            print('body image')
            logging.warning('Image is not available inside head tag')
            logging.debug('Calling body_tag() function')
            page.body_tag()


        logging.info('Dumping URL parsing and description in json')
        # webpage description
        final_json['description'] = description                                 # dumps data in dictionary
        # dumping data in json
        final_json['url'] = self.url
        final_json['origin'] = self.origin
        final_json['provider_domain'] = self.provider_domain
        final_json['provider_name'] = self.provider_name
        final_json['title'] = title
        final_json['provider_url'] = self.provider_url
        final_json['url_parsing_time'] = self.parsing_time


    def body_tag(self):
        logging.info('Fetching img attribute from body tag')
        body = self.soup.find('body')
        images = body.find_all('img')
        qlist = []

        def src_fun(images):
            logging.info('fetching image links having http protocol and appending in a list')
            for iterate in images:
                if iterate.get('src'):
                    link = iterate.get('src')
                    if 'http' in link:
                        qlist.append(link)
                else:
                    continue
        logging.debug('Calling src_fun function')
        src_fun(images)

        logging.debug('Calling image_details function')
        WebData.image_details(self, qlist, 'body')

    def body_image_fetch(self, link):
        self.image_name = link.split('/').pop()
        urllib.request.urlretrieve(link, 'image/' + self.image_name)
        mime = urllib.request.urlopen(link).info()['Content-Type']
        logging.debug('Reading image from Secondary Memory')
        infiles = glob.glob('image/' + self.image_name)
        infile = "".join(infiles)

        print('infile.:', infile)
        image_json = dict()

        self.im = Image.open(infile)
        width, height = self.im.size  # image dimensions

        if width < image_width or height < image_height:
            print('image size is smaller')
            logging.warning('Image size is smaller')

        else:
            print("Suitable image found")
            logging.debug('Suitable image found')
            self.link = link
            del (self.image_list[0:len(self.image_list)])
            self.width = width
            self.height = height
            self.mime = mime
            # self.image_name = image_name

    def image_details(self, image_list, par3):
        try:
            if par3 == 'body':
                logging.debug('checking if function called by body tag section')
                if not image_list:
                    print('Image list is empty')
                    self.link = ""
                    logging.warning('No image link found inside body tag')
                else:
                    logging.info('Fetching image details')
                    print (image_list)

                    while image_list:
                        if len(image_list) > threads:
                            image_sublist = image_list[0:threads]
                            del (image_list[0:threads])
                        else:
                            image_sublist = image_list[0:len(image_list)]
                            del (image_list[0:len(image_list)])
                        print('a', image_list)
                        print('image_sublist', image_sublist)
                        self.image_list = image_list
                        t = [Thread(target=WebData.body_image_fetch, args=(self, url)) for url in image_sublist]
                        for thread in t:
                            thread.start()
                        for thread in t:
                            thread.join()

            elif par3 == 'head':
                logging.debug('checking if function called by head tag section')
                logging.info('Fetching image details')
                # print (links)
                self.link = image_list
                self.image_name = link.split('/').pop()
                urllib.request.urlretrieve(link, 'image/' + self.image_name)
                self.mime = urllib.request.urlopen(link).info()['Content-Type']
                infiles = glob.glob('image/' + self.image_name)
                infile = "".join(infiles)
                image_json = dict()
                self.im = Image.open(infile)
                self.width, self.height = self.im.size  # image dimensions

            else:
                self.link=""
                logging.error('Unexpected argument found')

            if self.link!="":
                logging.debug('Dumping image data in JSON')
                avg = numpy.average(self.im, axis=0)
                numavg = (numpy.average(avg, axis=0))
                image_json = dict()
                image_json['url'] = self.link
                image_json['width'] = self.width

                image_json['height'] = self.height
                image_json['ratio'] = ((float(self.height) / float(self.width)) * 100.00)
                image_json['size'] = os.stat('image/'+str(self.image_name)).st_size
                image_json['mime'] = self.mime
                image_json['color'] = (numavg.tolist())
                image_json['image_time'] = (time.time()-self.image_time)

                final_json[(self.image_name)] = image_json
                # final_json["image"] = image_json

        except Exception as e:
            print (e)
            logging.error('Error occured while fetching image details')


with open('testurl.txt', 'r') as url_file:
    logging.info('Reading input file')
    for url in url_file:
        if url.strip():
            try:
                logging.debug('Fetching URL from input file')
                print ('Url to fetch', url)
                page = WebData(url)
                page.head_tag()
            except Exception as e:
                print (e)
                logging.error('Error while fetching URL from input file')
                continue



    final_json[url] = image_json
print(json.dumps(final_json))