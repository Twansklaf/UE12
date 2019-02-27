from TwitterSearch import *
try:
  tso = TwitterSearchOrder() # create a TwitterSearchOrder object
  tso.set_keywords(['Macron']) # let's define all words we would like to have a look for
  tso.set_language('fr') # we want to see German tweets only
  tso.set_include_entities(False) # and don't give us all those entity information

  # it's about time to create a TwitterSearch object with our secret tokens
  ts = TwitterSearch(
    consumer_key = 'P6OXKneDo1VgIsLaf7Hfz71pb',
    consumer_secret = 'ggdOmpO0m6IMBDLal6CKijWWAc1nR6XoM9eA2jC1LcJ9yEaiRD',
    access_token = '4096983503-9GUudKy0I0E4mNENQDAvNwHvKvL2pujSERjYZcU',
    access_token_secret = 'dxxIXULVExrOy74EJ2UOZI8tmXytyo089h4TyliJ8AxQj'
  )
  count=0
  for tweet in ts.search_tweets_iterable(tso):
    if count < 1000 :
      # print( '@%s tweeted: %s' % ( tweet['user']['screen_name'], tweet['text'] ) )
      print(tweet['text'])
      print(tweet['truncated'])
      for key in tweet :
        print(key)
      count += 1
    else :
      break

except TwitterSearchException as e: # take care of all those ugly errors if there are some
  print(e)