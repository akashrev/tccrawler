import re
import time
from threading import Thread
from .Image_data import Image_size
from.main import create_json
from .scraping import Scrape
from .url_fetch import Fetch


class Link_thread(Thread):
    def __init__(self, url, group=None, target=None, name=None, args=(), kwargs=None, *, daemon=None):
        Thread.__init__(self, group, target, name, args, kwargs, daemon=daemon)
        self.url = url
        self._return = None

    def run(self):
        scrape_obj = Scrape(self.url, base_url=re.search("https?://[^/]+", self.url).group(0))
        get_meta = scrape_obj.get_meta()

        parse_image_urls = scrape_obj.parse_image_urls()
        image_data = Image_size().get_best_images(urls=parse_image_urls)

        if get_meta["image"] is None or not get_meta["image"]:
            get_meta["image"] = image_data
        self._return = get_meta

    def get(self):
        return self._return


def main(input_url):
    meta = {}
    start = time.time()
    _url = input_url
    url = Fetch(_url).expand_url()
    meta["url"] = url
    thread = Link_thread(url=url["origin"])
    thread.start()
    thread.join()
    _dict = {**meta, **thread.get()}
    _dict.update({"time": time.time() - start})
    return create_json(_dict)


