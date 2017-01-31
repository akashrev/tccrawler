import tldextract

list = tldextract.extract('http://twitter.com').domain

print(list)