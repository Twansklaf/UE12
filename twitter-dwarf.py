import twitter

c_key =
c_secret =
a_key =
a_secret =

api = twitter.Api(consumer_key=[c_key],
                  consumer_secret=[c_secret],
                  access_token_key=[a_key],
                  access_token_secret=[a_secret])

results = api.GetSearch(
    raw_query="q=@Macron&result_type=recent&count=10")
