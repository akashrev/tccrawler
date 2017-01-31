from urllib.request import Request
import urllib
import urlparser
from bs4 import BeautifulSoup

url = 'http://tinyurl.com/hwmy5yp'

page = urlparser.parser(url)

page1 = page.urlorigin()
print (page1)


provider_name = page.providername()
print (provider_name)

provider_url = page.providerurl()
print (provider_url)


provider_domain = page.domain()
print (provider_domain)

#
page = urllib.request.urlopen(url)
page.addheaders = [('User-agent', 'Mozilla/5.0')]
#


soup = BeautifulSoup(page, 'lxml')

head = soup.find('head')

title = head.find('title')  # fetch webpage's title
print (title)
