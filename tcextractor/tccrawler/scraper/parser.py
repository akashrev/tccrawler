# from urllib2.parse import urlparse
from urlparse import urlparse
# import urlparse
import requests
import re


class Fetch:
    def __init__(self, url, data):
        self.url = url
        self.url_data = data

    def expand_url(self):
        origin = requests.head(self.url, allow_redirects=True).url

        urlregex = "((?:http|ftp)s?):\/\/(?:www)?\.?(([^\.]+)\.([^\/\.]+)\.?([^\/\.]+)?\.?([^\/\.]+)?)(.+)?"

        if 'com' in re.search(urlregex, origin).group(2).split('.'):  # if '.com' in the end of url, fetcjh just previous word
            provider_name = re.search(urlregex, origin).group(2).split('.')[-2]



        elif origin.split('/')[2].split('.')[0] == 'www':
            provider_name = re.search(urlregex, origin).group(2).split('.')[0]



        elif len(re.search(urlregex, origin).group(2).split('.')) == 2:  # if len of url is 2 then fetch out first word
            provider_name = re.search(urlregex, origin).group(3)


        elif len(re.search(urlregex, origin).group(2).split('.')) == 3:  # if length of url is 3
            if len(re.search(urlregex, origin).group(5)) == 2:  # if the last word of url is of length 2
                if len(re.search(urlregex, origin).group(4)) != 2:
                    provider_name = re.search(urlregex, origin).group(4)
                else:
                    provider_name = re.search(urlregex, origin).group(3)
            else:
                provider_name = re.search(urlregex, origin).group(4)
        elif len(re.search(urlregex, origin).group(2).split('.')) == 4:
            provider_name = re.search(urlregex, origin).group(4)
        else:
            provider_name = re.search(urlregex, origin).group(3)


        # provider = re.search(urlregex, origin).group(2)

        return {
            "url": self.url,
            "origin": origin,
            "provider": origin.split('/')[2],
            "provider_name": provider_name,
            "provider_url":  re.search(urlregex, origin).group(1)+"://"+origin.split('/')[2]
            # a.split('q=').pop().split('&')[0]
            # "provider_url": re.search(urlregex, origin).group(1)+"://"+provider
        }

    def get_url_data(self):
        response = ""
        if not self.url is None:
            try:
                response = requests.get(
                    self.url,
                    headers={
                        'User-Agent': "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) "
                                      "Chrome/55.0.2883.87 Safari/537.36"
                    }
                )
            except Exception as e:
                print(e)
        return response






    def get_header(self):
        header = ""
        if self.url_data:
            head = self.url_data.headers
            header = {
                "status": self.url_data.status_code,
                "type": head["content-type"] if "content-type" in head.keys() else "",
                "length": head["content-length"] if "content-length" in head.keys() else 0,
            }
        else:
            head = requests.head(self.url).headers
            header = head["content-length"] if "content-length" in head.keys() else 0
        return header

    def get_content(self, raw=False):
        if self.url_data:
            if not raw:
                return self.url_data.content.decode(self.url_data.encoding)
            return self.url_data.content
