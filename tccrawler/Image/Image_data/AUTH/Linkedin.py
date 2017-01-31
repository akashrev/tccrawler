import requests
import random
from django.conf import settings
from django.http import HttpResponse


class Auth:
    def __init__(self, callback_url):
        self.api_key = settings.LINKEDIN_APP_KEY
        self.auth_url = "https://www.linkedin.com/oauth/v2/authorization"
        self.response_type = "code"
        self.grant_type = "authorization_code"
        self.callback_url = callback_url
        self.scope = "r_fullprofile"
        self.state = "".join(
            random.sample("qwertyuiopasdfghjklzxcvbnmQWERTYUIOPASDFGHJKLZXCVBNM1023456789", random.randint(5, 15)))

    def linked_in(self):
        url = self.auth_url + "?response_type=" + self.response_type + "&client_id=" + self.api_key + "&redirect_uri=" + \
              self.callback_url + "&state=" + self.state
        return requests.get(url)

    def linkedin_callback(self, code):
        data = {"grant_type": self.grant_type, "code": code, "redirect_uri": self.callback_url, "client_id": self.api_key, "client_secret":settings.LINKEDIN_APP_SECRET}
        return requests.post(url="https://www.linkedin.com/uas/oauth2/accessToken", data=data, headers={"Content-Type": "application/x-www-form-urlencoded" })


def call(request):
    return HttpResponse(Auth("http://127.0.0.1:8000/Image/callback").linked_in())


def token(code):
    return HttpResponse(Auth("http://127.0.0.1:8000/Image/callback").linkedin_callback(code))


def callback(request):
    return token(request.GET["code"])
