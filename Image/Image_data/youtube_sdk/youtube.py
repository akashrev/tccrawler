import json
import requests
import time
from urllib.parse import urlsplit,parse_qs
from ..scrape_sdk.Image import Image_size
from django.conf import settings
from django.http import HttpResponse

APP_KEY = settings.YOUTUBE_APP_KEY


def youtube_video(request, input_url):
    start = time.time()
    base_url = "https://www.googleapis.com/youtube/v3/videos"
    part = "snippet"
    try:
        _id = parse_qs(urlsplit(input_url).query)["v"][0]
    except KeyError:
        return "KeyError: video does not have video id"
    url = base_url + "?part=" + part + "&id=" + _id + "&key=" + APP_KEY
    snippet = json.loads(requests.get(url).content.decode())["items"][0]["snippet"]
    image = {
            "url": snippet["thumbnails"]["maxres"]["url"],
            "width": snippet["thumbnails"]["maxres"]["width"],
            "height": snippet["thumbnails"]["maxres"]["height"],
            "ratio": (snippet["thumbnails"]["maxres"]["height"]/snippet["thumbnails"]["maxres"]["width"]) * 100,
            "size": "",
            "mime": "",
        }
    embed = "<iframe width=" + str(image["width"]) + " height=" + str(image["height"]) + " src=" + "https://www.youtube.com/embed/" + _id + " frameborder=\"0\" allowfullscreen></iframe>"
    output = {
        "url": input_url,
        "title": snippet["title"],
        "description": snippet["description"],
        "image": image,
        "embed": {
            "code": embed,
            "poster": image,
        },
        # "raw": requests.get(input_url).content.decode(),
        "time": time.time() - start,
    }
    return HttpResponse(json.dumps(output), content_type="application/json")


def youtube_channel(request, input_url="https://www.youtube.com/channel/UCT9RaKymKaSOV1jC_DpVpqw"):
    output = []
    start = time.time()
    base_url = "https://www.googleapis.com/youtube/v3/channels"
    part = "snippet"
    _id = urlsplit(input_url).path.split("/")[2]
    url = base_url + "?part=" + part + "&id=" + _id + "&key=" + APP_KEY
    snippet = json.loads(requests.get(url).content.decode())["items"][0]["snippet"]
    image = Image_size().get_image_dimension(snippet["thumbnails"]["high"]["url"], output, 0)
    output = {
        "url": input_url,
        "title": snippet["title"],
        "description": snippet["description"],
        "image": image,
        # "raw": requests.get(input_url).content.decode(),
        "time": time.time() - start,
    }
    return HttpResponse(json.dumps(output), content_type="application/json")
