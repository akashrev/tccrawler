import json
import time
from django.http import HttpResponse
from django.shortcuts import render
from .scraper.main import main
from .scraper.parser import Fetch
from .scraper.json import create_json
from .scraper.Image import Image_size


def call(request):
    allow_types = ['image/jpeg', 'image/jpg', 'image/png', 'image/gif', 'image/webp', 'image/tiff',
                   'image/bmp', ""]

    if request.method == "POST" and request.POST.get("textfield") != "":
        start = time.time()
        url = request.POST.get("textfield", None)
        raw_data = Fetch(url, '').get_url_data()  # fetch url data
        end = time.time()
        # print((Fetch(url, raw_data).get_header()))
        if Fetch(url, raw_data).get_header() and Fetch(url, raw_data).get_header()['status'] in [200, '200, 200 OK', '200 OK']:
            print('test')
            if Fetch(url, raw_data).get_header()['type'] in allow_types:
                data = {
                    "url": url,
                    "image": Image_size().body_image_fetch(raw_data.url, []),
                    "time": time.time() - start
                }
            else:
                url_parsing = Fetch(raw_data.url,"").expand_url(url)  # URL parsing details
                meta = main(url_parsing, raw_data)
                if meta["image"] is None or not meta["image"]:
                    meta["image"] = Image_size().body_image_fetch("https://logo.clearbit.com/"+url_parsing['provider_url']+"?s=300")
                data = create_json(meta)
                data["time"]["page_fetch"] = end - start
                data["time"]["total_time"] += data["time"]["page_fetch"]

            return HttpResponse(json.dumps(data), content_type="application/json")
        else:
            return render(request, "index.html")

    else:
        return render(request, "index.html")

