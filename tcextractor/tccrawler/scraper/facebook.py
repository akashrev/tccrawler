import requests


class Facebook:
    def __init__(self, url):
        self.url = url["origin"]
        self.url_detail = url
        self.app_id = "818766041597574"
        self.app_secret = "a0b1498fdde5c082d48628247e199522"
        self.token = self.get_app_token()

    def get_app_token(self):
        payload = {
            'grant_type': 'client_credentials',
            'client_id': self.app_id,
            'client_secret': self.app_secret
        }
        file = requests.post('https://graph.facebook.com/oauth/access_token?', params=payload)
        return file.text.split("=")[1]

