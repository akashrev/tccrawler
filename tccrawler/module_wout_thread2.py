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
import logging

logging.basicConfig(format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p')
logging.warning('is when this event was logged.')


f_json = dict()
image = dict()
qlist = []

# q = queue.Queue()

json_file = 'json_file.json'


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
        print('head')
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

        f_json['title_desc_time'] = (time.time() - self.start_time)

        self.image_time = time.time()

        # image
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
            page.body_tag()



        # webpage description
        f_json['description'] = description                                 # dumps data in dictionary
        # dumping data in json
        f_json['url'] = self.url
        f_json['origin'] = self.origin
        f_json['provider_domain'] = self.provider_domain
        f_json['provider_name'] = self.provider_name
        f_json['title'] = title
        f_json['provider_url'] = self.provider_url
        # f_json['title_time'] = (time.time()-self.start_time)
        f_json['url_parsing_time'] = self.parsing_time

        #print(json.dumps(f_json))
        print(time.time()-self.start_time)


    def body_tag(self):
        body = self.soup.find('body')
        images = body.find_all('img')
        qlist = []

        def src_fun(images):
            for iterate in images:
                if iterate.get('src'):
                    link = iterate.get('src')
                    if 'http' in link:
                        qlist.append(link)
                else:
                    continue

        src_fun(images)
        WebData.image_details(self, qlist, 'body')


    def image_details(self,links, par3):
        if par3 == 'body':
            print (links)
            for link in links:
                image_name = link.split('/').pop()
                urllib.request.urlretrieve(link, 'image/' + image_name)
                mime = urllib.request.urlopen(link).info()['Content-Type']

                infiles = glob.glob('image/' + image_name)
                infile = "".join(infiles)

                print('infile.:',infile)
                image_dict = dict()

                im = Image.open(infile)
                width, height = im.size  # image dimensions

                if width <500 or height<500:
                    print('size less than 500')
                    continue
                else:
                    print("greater than 500")
                    break

        elif par3 == 'head':
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



        avg = numpy.average(im, axis=0)
        numavg = (numpy.average(avg, axis=0))

        image_dict['url'] = link
        image_dict['width'] = width

        image_dict['height'] = height
        image_dict['ratio'] = ((float(height) / float(width)) * 100.00)
        image_dict['size'] = os.stat('image/'+str(image_name)).st_size
        image_dict['mime'] = mime
        image_dict['color'] = (numavg.tolist())

        image[(image_name)] = image_dict
        f_json["images"] = image_dict
        # print (f_json)





with open ('testurl.txt', 'r') as url_file:
    for urll in url_file:
        try:
            print ('Url to fetch', urll)
            page = WebData(urll)
            page.head_tag()
        except Exception as e:
            print (e)
            continue
        print('Final Json file', json.dumps(f_json))
        with open(json_file,'a') as j_file:
            j_file.write(json.dumps(f_json))
            j_file.write('\n')
