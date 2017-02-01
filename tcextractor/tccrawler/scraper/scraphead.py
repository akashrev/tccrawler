import re
# from urllib.parse import urlparse
from urlparse import urlparse
from .Image import Image_size
from .parser import Fetch


def search(pattern, string):
    _search = re.search(pattern=re.compile(pattern, re.I), string=string)
    return _search


class Scrape:
    def __init__(self, url, base_url, data):
        self.url = self.correct_url(url)
        self.raw_data = Fetch(url, data).get_content()
        self.base_url = base_url
        self.head = "<head([\S\D]+)</head>"
        self.meta_regex = "<meta(?:[^=]+)=(\"[^\"]+\")(?:([^=/>]+)=\"([^\"]+)\")?(?:([^=>/]+)=\"([^\"]+)\")?([^>]+)?>"
        self.title_regex = "<title>([^>]+)<\/title>"
        self.body = "<body([\S\D]+)<\/body>"
        self.image_regex = "<img[^\>]+(?:src|SRC)=\"([^\"]+\.(?=jpe?g|gif|png|tiff|bmp)[^\"]+)\"(?:[^\>]+)?>"

    def correct_url(self, url):
        if url:
            if url.startswith("//"):
                return urlparse(self.base_url).scheme + ":" + url.rstrip("\">")

            elif url.startswith("http"):
                return url
            else:
                return self.base_url + url

    def parse_image_urls(self):
        img_urls, comp_url = [], []
        string = search(self.body, self.raw_data)
        if string:
            img_urls.extend(re.findall(self.image_regex, string.group(1)))
            for url in set(img_urls):
                comp_url.append(self.correct_url(url))
        return comp_url

    def get_meta(self):
        result, res = {}, {}
        response = []
        metas = re.findall(self.meta_regex, self.raw_data)
        for meta in metas:
            if " content" in meta:
                res.update({meta[0]: meta[meta.index(" content") + 1]})
            elif "content" in meta:
                res.update({meta[0]: meta[meta.index("content") + 1]})

        key = res.keys()
        if '"og:title"' in key:
            result["title"] = res['"og:title"']
        elif '"twitter:title"' in key:
            result["title"] = res['"twitter:title"']
        elif search(self.title_regex, self.raw_data):
            result["title"] = search(self.title_regex, self.raw_data).group(1)
        else:
            result["title"] = ""

        if '"og:description"' in key:
            result["description"] = res['"og:description"']
        elif '"twitter:description"' in key:
            result["description"] = res['"twitter:description"']
        elif '"description"' in key:
            result["description"] = res['"description"']
        else:
            result["description"] = ""

        if '"og:video"' in key:
            result["video"] = res['"og:video"']
        elif '"og:video:url"' in key:
            result["video"] = res['"og:video:url"']
        elif '"og:video:secure_url"' in key:
            result["video"] = res['"og:video:secure_url"']
        else:
            result["video"] = ""

        if '"og:audio"' in key:
            result["audio"] = res['"og:audio"']
        elif '"og:audio:url"' in key:
            result["audio"] = res['"og:audio:url"']
        else:
            result["audio"] = ""

        if '"author"' in key:
            result["author"] = res['"author"']
        elif '"twitter:author"' in key:
            result["author"] = res['"twitter:author"']
        else:
            result["author"] = ""

        if '"article:author"' in key:
            result["author_url"] = res['"article:author"']
        else:
            result["author_url"] = ""

        if "code" in key:
            result["code"] = res["code"]
        else:
            result["code"] = ""

        if '"og:image"' in key:
            image = Image_size().get_image_dimension(self.correct_url(res['"og:image"']), response, 0)
            result["image"] = image
        elif '"twitter:image"' in key:
            image = Image_size().get_image_dimension(self.correct_url(res['"twitter:image"']), response, 0)
            result["image"] = image
        elif '"twitter:image:src"' in key:
            image = Image_size().get_image_dimension(self.correct_url(res['"twitter:image:src"']), response, 0)
            result["image"] = image
        else:
            result["image"] = ""
        return result
