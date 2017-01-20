    # import libraries
#import urlparser                            # personal library
import time
import requests
import urllib
from urllib.parse import urlparse
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
import logging
import sys
#logging.basicConfig(format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p')
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
                    datefmt='%m/%d/%Y %I:%M:%S %p',
                    filename='myapp.log',
                    filemode='a')
logging.info('Program executed.')

f_json = dict()
image = dict()
qlist = []

# q = queue.Queue()

json_file = 'json_file.json'


def expand_url(url):
    origin = requests.head(url, allow_redirects=True).url
    provider = urlparse(origin).netloc
    provider_name = provider.split(".")[-2]
    provider_url = urlparse(origin).scheme + "://" + urlparse(origin).netloc
    return url, origin,provider,provider_name,provider_url



class WebData:
    def __init__(self, url):
        logging.info('Parsing URL')
        parse_stime = time.time()


        self.url, self.origin, self.provider_domain, self.provider_name, self.provider_url = expand_url(url)
        # self.page = urlparser.parser(url)
#        self.origin = self.page.urlorigin()
#        self.provider_domain = self.page.domain()  # provider_domain
 #       self.provider_name = self.page.providername()
 #       self.provider_url = self.page.providerurl()  # provider_url

        self.parsing_time = time.time()-parse_stime
        self.head_stime = time.time()
        logging.info('Requesting webpage through urllib library')

        j_time = time.time()
        page = urllib.request.urlopen(url)
        page.addheaders = [('User-agent', 'Mozilla/5.0')]

        # page = requestst.get(url,headers={
        #                'User-Agent': "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) "
        #                              "Chrome/51.0.2704.106 Safari/537.36",
        #                'Accept-Language': 'en-GB,en-US,en;q=0.8'})
        #
        print(time.time() - j_time)

        self.soup = BeautifulSoup(page, 'html.parser')

        print('soup',time.time() - j_time)

    # function to fetch title and URL's stuffs
    def head_tag(self):
        hbtime= time.time()
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

        f_json['title_desc_time'] = (time.time() - self.head_stime)
        print(time.time()-hbtime)
        self.image_time = time.time()

        # image
        logging.info('Fetching webpage\'s image')
        if head.find('meta', {'property': 'og:image'}) and head.find('meta', {'property': 'og:image'}).get('content') != "":
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
        f_json['description'] = description                                 # dumps data in dictionary
        # dumping data in json
        f_json['url'] = self.url
        f_json['origin'] = self.origin
        f_json['provider_domain'] = self.provider_domain
        f_json['provider_name'] = self.provider_name
        f_json['title'] = title
        f_json['provider_url'] = self.provider_url
        f_json['url_parsing_time'] = self.parsing_time


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


    def image_details(self, links, par3):
        try:
            if par3 == 'body':
                logging.debug('checking if function called by body tag section')
                if not links:
                    print('Image list is empty')
                    link=""
                    logging.warning('No image link found inside body tag')
                else:
                    logging.info('Fetching image details')
                    print (links)
                    for link in links:
                        image_name = link.split('/').pop()
                        urllib.request.urlretrieve(link, 'image/' + image_name)
                        mime = urllib.request.urlopen(link).info()['Content-Type']
                        logging.debug('Reading image from Secondary Memory')
                        infiles = glob.glob('image/' + image_name)
                        infile = "".join(infiles)

                        print('infile.:',infile)
                        image_dict = dict()

                        im = Image.open(infile)
                        width, height = im.size  # image dimensions

                        if width <200 or height<200:
                            print('size less than 500')
                            logging.warning('Image size is smaller')
                            continue
                        else:
                            print("greater than 200")
                            logging.debug('Suitable image found')
                            break

            elif par3 == 'head':
                logging.debug('checking if function called by head tag section')
                logging.info('Fetching image details')
                print (links)
                link = links
                image_name = link.split('/').pop()
                urllib.request.urlretrieve(link, 'image/' + image_name)
                mime = urllib.request.urlopen(link).info()['Content-Type']
                infiles = glob.glob('image/' + image_name)
                infile = "".join(infiles)
                image_dict = dict()
                im = Image.open(infile)
                width, height = im.size  # image dimensions

            else:
                link=""
                logging.error('Unexpected argument found')

            if link!="":
                logging.debug('Dumping image data in JSON')
                avg = numpy.average(im, axis=0)
                # numavg = (numpy.average(avg, axis=0))

                image_dict['url'] = link
                image_dict['width'] = width

                image_dict['height'] = height
                image_dict['ratio'] = ((float(height) / float(width)) * 100.00)
                image_dict['size'] = os.stat('image/'+str(image_name)).st_size
                image_dict['mime'] = mime
                # image_dict['color'] = (numavg.tolist())
                image_dict['color'] = ""
                image_dict['image_time'] = (time.time()-self.image_time)

                image[(image_name)] = image_dict
                f_json['total_time'] = time.time() - s_time
                f_json["image"] = image_dict

        except Exception as e:
            print (e)
            logging.error('Error occured while fetching image details')


with open ('testurl.txt', 'r') as url_file:
    logging.info('Reading input file')
    s_time = time.time()
    for urll in url_file:
        if urll.strip():
            try:
                logging.debug('Fetching URL from input file')
                print ('Url to fetch', urll)
                page = WebData(urll)
                page.head_tag()
            except Exception as e:
                print (e)
                logging.error('Error while fetching URL from input file')
                continue
            print('Final Json file', json.dumps(f_json))
            with open(json_file,'a') as j_file:
                logging.info('Dumping json in json file')
                j_file.write(json.dumps(f_json))
                j_file.write('\n')
                logging.info('URL\'s task finished\n')
        else:
            logging.warning('Input file\'s line is blank')
            continue
