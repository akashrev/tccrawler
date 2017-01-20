import re
import time
from .Image import Image_size
from .scraping1 import Scrape


def create_json(meta):
    data = {
        "Url": meta["url"],
        "Title": meta["title"],
        "Description": meta["description"],
        "Author": {
            "Name": meta["author"],
            "Url": meta["author_url"],
        },
        "Image": meta["image"],
        "Embed": {
            "Code": meta["code"],
            "Poster": "" if meta["video"] == ("",) else meta["image"],
        },
        "audio": meta["audio"],
        "time": meta["time"],
        # "raw_data": meta["raw"],
    }
    return data


def main(input_url, data):
    start = time.time()
    scrape_obj = Scrape(input_url["origin"], re.search("https?://[^/]+", input_url["origin"]).group(0), data)
    meta = scrape_obj.get_meta()
    meta_time = time.time() - start
    start2 = time.time()
    if meta["image"] is None or not meta["image"]:
        parse_image_urls = scrape_obj.parse_image_urls()
        meta["parse_image_urls_time"] = time.time() - start2
        start3 = time.time()
        image_data = Image_size().get_best_images(urls=parse_image_urls)
        meta["image"] = image_data
        meta["image_data"] = time.time() - start3

    meta["url"] = input_url
    meta["video"] = meta["video"] if "image" in meta.keys() else "",
    meta["image"] = meta["image"] if "image" in meta.keys() else "",
    meta["time"] = {
        "get_meta_time": meta_time,
        "image_data": meta["image_data"] if "image_data" in meta.keys() else "",
        "parse_image_urls_time": meta["parse_image_urls_time"] if "parse_image_urls_time" in meta.keys() else "",
        "total_time": time.time() - start,
    }
    return create_json(meta)
