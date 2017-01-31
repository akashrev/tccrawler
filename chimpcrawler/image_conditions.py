import requests
from PIL import Image
from io import BytesIO
import time
import urllib
from bs4 import BeautifulSoup
#import urlparser                            # personal library
import io
from urllib.parse import urlparse

# https://www.mituniversity.edu.in/


def expand_url(url):
    print('goorigin')
    origin = requests.head(url, allow_redirects=True).url
    print('origin is ',origin)
    provider = urlparse(origin).netloc
    provider_name = provider.split(".")[-2]
    print('p',provider)
    print ('pn',provider_name)
    provider_url = urlparse(origin).scheme + "://" + urlparse(origin).netloc
    return url, origin,provider,provider_name,provider_url



def image_details(data):
    fd = urllib.request.urlopen(data)
    image_file = io.BytesIO(fd.read())
    im = Image.open(image_file)
    print(im)
    print(image_file)
    print(im.size)
    im.show()
    # i = Image.open(BytesIO(data))


def fetch_image(url):
    print('iserror?')
    print('ishere')
    url, origin, provider_domain, provider_name, provider_url = expand_url(url)
    #
    # page = urlparser.parser(url)
    # print('iserror?')
    # origin = page.urlorigin()
    # print('iserror?')
    #
    # provider_domain = page.domain()  # provider_domain
    # print('iserror?')
    # provider_name = page.providername()
    # print('iserror?')
    # provider_url = page.providerurl()  # provider_url
    #
    print('iserror? burllib')
    page = urllib.request.urlopen(url)
    print("maybe")
    page.addheaders = [('User-agent', 'Mozilla/5.0')]
    soup = BeautifulSoup(page, 'lxml')
    print (provider_domain,provider_name,provider_url)

    head = soup.find('head')

    if head.find('meta', {'property': 'og:image'}) and (head.find('meta', {'property': 'og:image'}).get('content') != "" and 'http' in head.find('meta', {'property': 'og:image'}).get('content') ):
        image = (head.find('meta', {'property': 'og:image'})).get('content')
        print('og:image')
        image_details(image)

    elif head.find('meta', {'name': 'twitter:image'}):
        image = (head.find('meta', {'name': 'twitter:image'})).get('content')
        print('twitter:image')
        print (image)
        image_details(image)
    elif head.find('meta', {'name': 'image'}):
        image = (head.find('meta', {'name': 'image'})).get('content')  # webpage description
        print('meta image')
        image_details(image)
    else:
        print('clearbit')
        print(provider_domain)
        print(len(provider_domain.split(".")))
        if len(provider_domain.split(".")) ==3:
            urlForApi = (".".join(provider_domain.split(".")[1:3]))
        elif len(provider_domain.split(".")) ==2:
            urlForApi = (".".join(provider_domain.split(".")[0:2]))
        elif len(provider_domain.split(".")) == 4:
            urlForApi = (".".join(provider_domain.split(".")[1:4]))
            print (urlForApi)
        else:
            print(len(provider_domain.split(".")))

        url = "https://logo.clearbit.com/" + urlForApi
        print(url)
        image_details(url)

    # print (width, height)

if __name__ == "__main__":
    stime = time.time()
    url = "http://www.northwestern.edu/"
    print('iserror?')

    fetch_image(url)
