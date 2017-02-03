import requests
from re import search


class Fetch:
    def __init__(self, url, data):
        self.url = url
        self.url_data = data

    def expand_url(self):
        tld = ['com','org','net','int','edu','gov','mil','arpa']
        urlregex = "(((?:http|ftp)s?):\/\/(?:www)?\.?(([^\.]+)\.([^\/\.]+)\.?([^\/\.]+)?\.?([^\/\.]+)?))(?:.+)?"

        url_data = search(urlregex, self.url)
        dot_count = (url_data.group(3).count("."))
        if dot_count==1:
            provider_name = url_data.group(4)
        elif dot_count == 2:               # if the last word of url is of length 2
            provider_name = url_data.group(5) if len(url_data.group(5)) != 2 and url_data.group(5) not in tld else url_data.group(4)
        elif dot_count == 3:
            provider_name = url_data.group(5)
        print(url_data.groups())
        return provider_name


                # if 'com' in re.search(urlregex, origin).group(2).split('.'):  # if '.com' in the end of url, fetcjh just previous word
        #     com_index = (re.search(urlregex, origin).group(2).split('.')).index("com")
        #     provider_name = re.search(urlregex, origin).group(2).split('.')[com_index-1]
        #
        # elif origin.split('/')[2].split('.')[0] == 'www':
        #     provider_name = re.search(urlregex, origin).group(2).split('.')[0]
        #
        # elif len(re.search(urlregex, origin).group(2).split('.')) == 2:  # if len of url is 2 then fetch out first word
        #     provider_name = re.search(urlregex, origin).group(3)
        #
        # elif len(re.search(urlregex, origin).group(2).split('.')) == 3:  # if length of url is 3
        #     if len(re.search(urlregex, origin).group(5)) == 2:  # if the last word of url is of length 2
        #         if len(re.search(urlregex, origin).group(4)) != 2:
        #             provider_name = re.search(urlregex, origin).group(4)
        #         else:
        #             provider_name = re.search(urlregex, origin).group(3)
        #     else:
        #         provider_name = re.search(urlregex, origin).group(4)
        # elif len(re.search(urlregex, origin).group(2).split('.')) == 4:
        #     provider_name = re.search(urlregex, origin).group(4)
        # else:
        #     provider_name = re.search(urlregex, origin).group(3)
        #
        # # provider = re.search(urlregex, origin).group(2)
        # #
        # return {
        #     "scheme":url_data.group(1),
        #     "url": self.url,
        #     "origin": origin,
        #     "provider": origin.split('/')[2],
        #     "provider_name": provider_name,
        #     "provider_url":  re.search(urlregex, origin).group(1)+"://"+origin.split('/')[2]
        # }

    def get_url_data(self):
        response = ""
        if not self.url is None:
            try:
                response = requests.get(
                    self.url,
                    allow_redirects = True,
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

url = \
    "http://www.example.google.co.in/"

print(Fetch(url,"").expand_url())