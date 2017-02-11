# import re
import time
from .Image import Image_size
from .scraphead import Scrape
# from .json import create_json
# from .scraper.main import main


def main(input_url, data):
    start = time.time()

    scrape_obj = Scrape(input_url, data)

    meta = scrape_obj.get_meta()
    # print(meta)# fetch webpage details from meta tag
    meta_time = time.time() - start
    start2 = time.time()
    if meta["image"] is None or not meta["image"]:
        # print('.................')
        parse_image_urls = scrape_obj.parse_image_urls()            # all image URLs
        print(parse_image_urls)
        meta["parse_image_urls_time"] = time.time() - start2
        start3 = time.time()
        image_data = Image_size().get_best_image(urls=parse_image_urls)
        meta["image"] = image_data
        meta["image_data"] = time.time() - start3

    meta["url"] = input_url,
    meta["video"] = meta["video"] if "image" in meta.keys() else "",
    print(meta['video'])
    meta["image"] = meta["image"] if "image" in meta.keys() else "",
    meta["time"] = {
        "get_meta_time": meta_time,
        "image_data": meta["image_data"] if "image_data" in meta.keys() else "",
        "parse_image_urls_time": meta["parse_image_urls_time"] if "parse_image_urls_time" in meta.keys() else "",
        "total_time": time.time() - start,
    }
    print((meta['video']))
    meta["poster"] = "" if meta["video"] in [None, (None,)] else meta["image"]
    return meta
