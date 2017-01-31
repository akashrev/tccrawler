import urlparser
from bs4 import BeautifulSoup

page = urlparser.parser('http://tinyurl.com/hwmy5yp')

page1 = page.urlorigin()
print (page1)


provider_name = page.providername()
print (provider_name)

provider_url = page.providerurl()
print (provider_url)


provider_domain = page.domain()
print (provider_domain)


soup = BeautifulSoup(page.request(), 'lxml')

print (soup)