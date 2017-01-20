import time
import urllib
from urllib.request import Request
from bs4 import BeautifulSoup
import glob
from PIL import Image
import numpy
import queue
from threading import Thread
import sys, json

q = queue.Queue()
f_dict = {}
l_dict = {}

ll = open('qqqqqq.json','a')


def sleeper(i,q):
    print ("thread %d sleeps for 5 seconds" % i)
    #time.sleep(1)
    print("thread %d woke up" % i)


    while not q.empty():
        link = q.get()
        print('link.....',link)
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

            if width < 500 or height < 500:
                print('size less than 500, by %d' %i)


            else:
                print("greater than 500")
    #                    q=queue.Queue
                print('Found it.............. by %d'%i)
                f_dict['link'] = link
                f_dict['height'] = height
                f_dict['width'] = width
                q.queue.clear()
                q.task_done()

                #print('!!!',q.get())


        except:
            continue
        q.task_done()

    print (f_dict)


with open('testurl.txt', 'r') as url_file:
    for url in url_file:
        print('url is....',url)
        page = urllib.request.urlopen(url)
        page.addheaders = [('User-agent', 'Mozilla/5.0')]
        soup = BeautifulSoup(page, 'lxml')
        body = soup.find('body')
        images = body.find_all('img')
        qlist = []
        for iterate in images:
            if iterate.get('src'):
                link = iterate.get('src')
                if 'http' in link:
                    qlist.append(link)
                    q.put(link)
        print(url)
        f_dict={}
        #print('list', qlist)

        for i in range(2):
            t = Thread(target=sleeper, args=(i,q))
            t.setDaemon(True)
            t.start()
            t.join(i)
        #print(q.get())

        if not q.empty():
            print('/////////q nt empty')
            q.join()
        else:
            print('/////////q empty')
            print (f_dict)
            print (f_dict)
            l_dict[url] = f_dict
            ll.write(json.dumps(l_dict))



print(l_dict)
ll.close()
