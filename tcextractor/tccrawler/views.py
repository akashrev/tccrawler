import json
import time
import requests
from django.http import HttpResponse
from django.shortcuts import render
from .scraper.main import main
from .scraper.parser import Fetch
from .scraper.json import create_json

# Create your views here.

def call(request):
    if request.method == "POST" and request.POST.get("textfield") != "":
        # start = time.time()
        url = Fetch(request.POST.get("textfield", None), "").expand_url()           # fetch url details

        raw_data = Fetch(url["origin"], "").get_url_data()                          # fetch url data
        meta = main(url, raw_data)

        data = create_json(meta)

        return HttpResponse(json.dumps(data), content_type="application/json")
    else:
        return render(request, "index.html")
