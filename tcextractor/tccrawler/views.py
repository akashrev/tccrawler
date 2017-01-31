import json
import time
import requests
from django.http import HttpResponse
from django.shortcuts import render
from .scraper.main import main
from .scraper.parser import Fetch

# Create your views here.

def call(request):
    if request.method == "POST":
        # start = time.time()

        url = Fetch(request.POST.get("textfield", None), "").expand_url()

        raw_data = Fetch(url["origin"], "").get_url_data()

        data = json(url, raw_data)

        return HttpResponse(json.dumps(data), content_type="application/json")
    else:
        return render(request, "index.html")
