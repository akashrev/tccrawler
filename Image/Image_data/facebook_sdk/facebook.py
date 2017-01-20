import requests
import logging
from ..scrape_sdk.Image import Image_size
from ..scrape_sdk.scraping1 import search
from ..scrape_sdk.main import main
from ..scrape_sdk.Url import Fetch


class Facebook:
    def __init__(self, url):
        self.url = url["origin"]
        self.url_detail = url
        self.FACEBOOK_APP_KEY = "818766041597574"
        self.FACEBOOK_APP_SECRET = "a0b1498fdde5c082d48628247e199522"
        self.token = self.get_app_token()

    def get_app_token(self):
        payload = {
            'grant_type': 'client_credentials',
            'client_id': self.FACEBOOK_APP_KEY,
            'client_secret': self.FACEBOOK_APP_SECRET
        }
        file = requests.post('https://graph.facebook.com/oauth/access_token?', params=payload)
        return file.text.split("=")[1]

    def posts(self, _id):
        field = 'description,feed_targeting,from,icon,instagram_eligibility,is_hidden,is_instagram_eligible,' \
                'is_published,link,message,message_tags,with_tags,updated_time,type,to,targeting,story_tags,story,' \
                'status_type,source,shares,properties,privacy,place,picture,permalink_url,parent_id,object_id,name,id,' \
                'admin_creator,application,call_to_action,caption,created_time'
        response = requests.get(
            "https://graph.facebook.com/" + str(_id) + "/?fields=" + field + "&access_token=" + self.token)
        data = response.json()
        return data

    def video(self, _id):
        data = {"title": ""}
        field = "title,length,format,embed_html"
        response = requests.get(
            'https://graph.facebook.com/' + str(_id) + "/?fields=" + field + "&access_token=" + self.token)
        data = response.json()
        image = Image_size().get_image_dimension(data["format"][-1]["picture"], [], 0)
        res = {
            # "title": data["title"],
            "length": data["length"],
            "embed_code": data["embed_html"],
            "image": image
        }
        return res

    def picture(self, _id):
        field = "images"
        response = requests.get(
            "https://graph.facebook.com/" + str(_id) + "/?fields=" + field + "&access_token=" + self.token)
        data = response.json()
        return Image_size().get_image_dimension(data["images"][0]["source"], [], 0)

    def url_parse(self):
        _id, check = "", ""
        regexs = [
            "https?:/\/[^\/]+\/[^/]+\/(posts)\/([0-9]+)",
            "https?:\/\/[^\/]+\/[^/]+\/(videos)\/([0-9]+)",
            "https?:\/\/[^\/]+\/(photo.php)\?fbid=([0-9]+).+",
            "https?:\/\/[^\/]+\/[^/]+\/(photos)\/a\.[0-9]+\.[0-9]+\.[0-9]+\/([0-9]+)\/\?",
            "https?:\/\/[^\/]+\/pg\/[^/]+\/(photos)\/\?[^_]+_id=([0-9]+)",
            "https?:\/\/[^\/]+\/(video.php)\?v=([0-9]+)",
            "https?:\/\/[^\/]+\/(groups)\/[0-9]+\?[^&]+&id=([0-9]+)"
        ]
        for regex in regexs:
            data = search(regex, self.url)
            if data:
                check, _id = data.group(1), data.group(2)
                break
        try:
            if check == "videos" or check == "video.php":
                return self.video(_id)
            elif check == "photos" or check == "photo.php":
                return self.picture(_id)
            elif check == "posts":
                pass
            elif check == "groups":
                pass
            else:
                return main(self.url_detail, Fetch(self.url, "").get_url_data())
        except Exception:
            logging.exception("Error in Facebook")
