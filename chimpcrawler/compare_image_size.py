import requests
from PIL import Image
from io import BytesIO
import time
import urllib
from bs4 import BeautifulSoup

def get_image_size(url):
    rtime = time.time()
    data = requests.get(url).content

    '''
    print('requests', data)
    data = requests.get('http://www.google.co.in/').content

    print('req time', time.time()-rtime)
    utime = time.time()
    data1 = urllib.request.urlopen(url)
    print('urllib:', data1)
    soup = BeautifulSoup(urllib.request.urlopen('http://www.google.co.in/'), 'lxml')
    print (soup)
    print('url time', time.time()-utime)
    '''
    im = Image.open(BytesIO(data))
    return im.size


if __name__ == "__main__":
    stime = time.time()
    while True:
        url = "https://logo.clearbit.com/amazon.com"
        width, height = get_image_size(url)
        print (width, height)
        print(time.time()-stime)




