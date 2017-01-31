
import time
import urllib
from urllib.request import Request
from bs4 import BeautifulSoup, SoupStrainer

s_time = time.time()
print(time.time()-s_time)
url = "http://www.amazon.in/"
print(time.time()-s_time)
page = urllib.request.urlopen(url)
print(time.time()-s_time)
page.addheaders = [('User-agent', 'Mozilla/5.0')]
print(time.time()-s_time)

only_meta_tags = SoupStrainer("title")
print(time.time()-s_time)

print(BeautifulSoup(page, "lxml", parse_only=only_meta_tags))
print(time.time()-s_time)



ss_time = time.time()
print(time.time()-ss_time)
page = urllib.request.urlopen(url)
print(time.time()-ss_time)
page.addheaders = [('User-agent', 'Mozilla/5.0')]
print(time.time()-ss_time)
soup = BeautifulSoup(page, 'lxml')
print(time.time()-ss_time)
head = soup.find('head')
print(time.time()-ss_time)
title = head.find('title').text  # fetch webpage's title
print(time.time()-ss_time)
print (title)
print(time.time()-ss_time)