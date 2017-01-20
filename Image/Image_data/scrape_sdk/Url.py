from urllib.parse import urlparse
import requests


class Fetch:
    def __init__(self, url, data):
        self.url = url
        self.url_data = data

    def expand_url(self):
        origin = requests.head(self.url, allow_redirects=True).url
        provider = urlparse(origin).netloc
        provider_name = provider.split(".")[-2]
        provider_url = urlparse(origin).scheme + "://" + urlparse(origin).netloc
        return {
            "url": self.url,
            "origin": origin,
            "provider": provider,
            "provider_name": provider_name,
            "provider_url": provider_url
        }

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

    def get_url_data(self):
        response = ""
        if not self.url is None:
            try:
                response = requests.get(
                    self.url,
                    headers={
                        'User-Agent': "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) "
                                      "Chrome/51.0.2704.106 Safari/537.36",
                        'Accept-Language': 'en-GB,en-US,en;q=0.8'}
                )
            except Exception as e:
                print(e)
        return response
