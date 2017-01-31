import tweepy,time,json
from django.conf import settings
from django.http import HttpResponse
from ..scrape_sdk.main import main
import logging


def tweet(request):
    query = "meshable"
    logging.basicConfig(filename="Image_data/Errorlogs/" + query + ".txt",level=logging.DEBUG)
    start = time.time()
    urls = []
    auth = tweepy.OAuthHandler(settings.TWITTER_APP_KEY, settings.TWITTER_APP_SECRET)
    auth.set_access_token(settings.TWITTER_TOKEN, settings.TWITTER_SECRET)
    api = tweepy.API(auth)
    for url in api.user_timeline(screen_name="mashable", count=10):
        if url.entities["urls"]:
            print(url.entities["urls"][0]["expanded_url"])
            try:
                urls.append(
                    {
                        "Url": url.entities["urls"][0]["expanded_url"],
                        "Time": main(url.entities["urls"][0]["expanded_url"])["time"],
                    }
                )
            except Exception as e:
                logging.debug(e)
    print(time.time() - start)
    return HttpResponse(json.dumps(urls), content_type="application/json")
