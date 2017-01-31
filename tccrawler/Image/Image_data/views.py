import json
import time
import requests
from django.http import HttpResponse
from django.shortcuts import render
from .scrape_sdk.Image import Image_size
from .scrape_sdk.main import main
from .scrape_sdk.Url import Fetch
from .facebook_sdk.facebook import Facebook


def call(request):
    _data = []
    allow_types = ['image/jpeg', 'image/jpg', 'image/png', 'image/gif', 'image/webp', 'image/tiff',
                   'image/bmp', ""]
    if request.method == "POST":
        start = time.time()
        url = Fetch(request.POST.get("textfield", None), "").expand_url()
        if requests.head(url["origin"]).headers["content-type"] in allow_types:
            data = {
                "url": url,
                "image": Image_size().get_image_dimension(url["origin"], _data, 0),
                "time": time.time() - start
            }
        elif url["provider_name"] == "facebook":
            data = {
                "image": Facebook(url).url_parse(),
                "time": time.time() - start,
                "url": url,
            }
        # elif url["provider_name"] == "twitter":
        #     twitter_regex = "https?:\/\/[^\/]+\/[^\/]+\/status\/([0-9])+"

        else:
            raw_data = Fetch(url["origin"], "").get_url_data()
            data = main(url, raw_data)
        return HttpResponse(json.dumps(data), content_type="application/json")
    else:
        return render(request, "index.html")
