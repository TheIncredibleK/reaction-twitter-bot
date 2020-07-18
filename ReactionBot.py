import os
from os import environ
from os import listdir
from os.path import isfile, join
import random
import tweepy
import re
from google_images_search import GoogleImagesSearch

#creds

API_KEY = environ["API_KEY"]
API_SHH_KEY = environ["API_SHH_KEY"]
ACCESS = environ["ACCESS"]
ACCESS_SECRET = environ["ACCESS_SECRET"]

GOOGL_DEV_API_KEY = environ["GOOGL_DEV_API_KEY"]
CX_API_KEY = environ["CX_API_KEY"]


consumer_key = API_KEY
consumer_secret = API_SHH_KEY
access_token = ACCESS
access_token_secret = ACCESS_SECRET
# OAuth process, using the keys and tokens
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

# Creation of the actual interface, using authentication
API = tweepy.API(auth)
MY_NAME = "reactor_bot"
class StreamListener(tweepy.StreamListener):
    def on_status(self, status):
        process_tweet(status, API)


## Twitter Helpers ##
def __resolve_responding_to(tweet):
    if(tweet.in_reply_to_screen_name !=None):
        return "@{} @{}".format(tweet.author.screen_name, tweet.in_reply_to_screen_name)
    else:
        return "@{}".format(tweet.author.screen_name)

def process_tweet(tweet, api):
    tweet_id = tweet.id
    response_text = __resolve_responding_to(tweet)
    username = tweet.author.screen_name
    text = re.sub('@[^\s]+','',tweet.text.lower())

    if(username != MY_NAME):
        image_path = find_image(text, username)
        reply_with_image(api, image_path, username, tweet_id, response_text)
        return
    else:
        print("Not doing it for myself you dingus")

def reply_with_image(api, image_path, username, tweet_id, beginning_of_tweet):
    print("Path: {}\n Username:{}\n, tweet_id:{}\n".format(image_path, username, tweet_id))
    api.update_with_media(filename=image_path, status=beginning_of_tweet, in_reply_to_status_id=tweet_id)
    __remove_file(image_path)


def __remove_file(filename):
    if isfile(filename):
        os.remove(filename)

def find_image(search_param, username):
    search_param_fill = "{} reaction meme".format(search_param)
    gis = GoogleImagesSearch(GOOGL_DEV_API_KEY, CX_API_KEY)

    # define search params:
    _search_params = {
        'q': '{}'.format(search_param_fill),
        'num': 10,
    }

    gis.search(search_params=_search_params)
    images = gis.results()
    image_index = random.randint(0, images.__len__() - 1)
    image = images[image_index]
    dl_location = os.path.join(os.getcwd(), "images\\{}".format(username))
    print(dl_location)
    if os.path.isdir(dl_location) == False:
        os.mkdir(dl_location)

    image.download(dl_location)
    onlyfiles = [f for f in listdir(dl_location) if isfile(join(dl_location, f))]
    if onlyfiles.__len__() > 1:
        print("There should be only one file, but there are {}".format(onlyfiles.__len__()))
    filename = join(dl_location, onlyfiles[0])
    return filename

def main_loop():
    while True:
        a = 1
    return

if __name__ == "__main__":
    streamListener = StreamListener()
    myStream = tweepy.Stream(auth=API.auth, listener=StreamListener())
    print("ONLINE: ")
    myStream.filter(track=['@reactor_bot '])
    main_loop()
