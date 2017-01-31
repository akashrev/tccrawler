#!/bin/env python3
# -*- coding: utf-8 -*-

###################################################################################################################
###################################################################################################################
## created by Akash on 12 Jan 2017
## Program to fetch URL's origin-URL, provider_domain, provider_url, provider_name,
#
## Usage:
#    # initialize your URL to a variable,
#        # say: < yourvariable = urlparser.parser('www.yoururl.com') >
#
#    # URL origin : yourvariable.origin()
#    # Provider Domain: yourvariable.domain()
#    # Provider Name: yourvaribale.providername()
#    # Provider URL: yourvariable.providerurl()
#
###################################################################################################################
###################################################################################################################


import urllib
from urllib.request import Request
import tldextract


class parser:
    def __init__(self,url):
        self.url = url
        page = urllib.request.urlopen(self.url)
        page.addheaders = [('User-agent', 'Mozilla/5.0')]
        self.origin = page.url                                              # source URL


    def urlorigin(self):
        try:
            return self.origin
        except Exception as e:
            return e


    def domain(self):
        try:
            return urllib.parse.urlparse(self.origin).hostname  # provider_domain i.e thoughtchimp.com
        except Exception as e:
            return e

    def providername(self):
        try:
            return tldextract.extract(self.origin).domain       # provider_name i.e thoughtchimp
        except Exception as e:
            return e

    def providerurl(self):
        try:
            parsed_uri = urllib.parse.urlparse(self.origin)
            return '{uri.scheme}://{uri.netloc}/'.format(uri=parsed_uri)  # provider_url i.e http://www.thoughtchimp.com/
        except Exception as e:
            return e


