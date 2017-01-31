# created by akash on 12 Jan 2017

#Import libraries
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
import json

# Akash's twitter credentials for authentication
consumer_key="Zf6OKZ1CKJ8asXOkHv2nANaQy"
consumer_secret="ZyIt86TIm3o8u2vl4w7hTUffIRUKlQKUGXRX9jxmwB7osZSu4j"
access_token="722762309857185793-VRe4FGILkon9wxVZgFt45jmjrvn9CVu"
access_token_secret="RaBWS177JorNbWXSnqJIT8xJCvcnVXvJGACWIhaB5Yv4q"

# output file path assigned in a variable
tweets_data_path = 'twitter_data/twitter_data.json'

with open(tweets_data_path, "a") as twitter_file:
    # Class that reads and dumps the data in json file
    class StdOutListener(StreamListener):
        def on_data(self, twitter):
            print(twitter)
            tweet = json.loads(twitter)
            if tweet['entities']:
                entities = tweet['entities']
                urls = entities['urls']
                for iterator in urls:
                    expanded_url = (iterator['expanded_url'])
                    print (expanded_url)
                    if expanded_url != None:
                        with open('urls.txt','a') as urlfile:
                            urlfile.write(expanded_url)
                            urlfile.write('\n')

            twitter_file.write(twitter),
        def on_error(self, status):
            print (status)

    # execute code if the file was run directly, not imported
    if __name__ == '__main__':
        #authentification and the connection to Twitter API
        l = StdOutListener()
        auth = OAuthHandler(consumer_key, consumer_secret)
        auth.set_access_token(access_token, access_token_secret)
        stream = Stream(auth, l)

        # capture data by the keywords
        stream.filter(track=['Obama'])