from __future__ import unicode_literals
from TwitterAPI import TwitterAPI
import json

consumer_key = 'P6OXKneDo1VgIsLaf7Hfz71pb'
consumer_secret = 'ggdOmpO0m6IMBDLal6CKijWWAc1nR6XoM9eA2jC1LcJ9yEaiRD'
access_token_key = '4096983503-9GUudKy0I0E4mNENQDAvNwHvKvL2pujSERjYZcU'
access_token_secret = 'dxxIXULVExrOy74EJ2UOZI8tmXytyo089h4TyliJ8AxQj'

api = TwitterAPI(consumer_key, consumer_secret, access_token_key, access_token_secret)

r = api.request('search/tweets', {'q':'macron', 'count':200, 'tweet_mode': 'extended'})
for item in r.get_iterator():
  if 'retweeted_status' in item:
    tweetId = item['id']
    tweetText = item['retweeted_status']['full_text']
    print("id : " + str(tweetId))
    print("text : " + tweetText)