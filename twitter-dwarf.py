import twitter

c_key = 'P6OXKneDo1VgIsLaf7Hfz71pb',
c_secret = 'ggdOmpO0m6IMBDLal6CKijWWAc1nR6XoM9eA2jC1LcJ9yEaiRD',
a_key = '4096983503-9GUudKy0I0E4mNENQDAvNwHvKvL2pujSERjYZcU',
a_secret = 'dxxIXULVExrOy74EJ2UOZI8tmXytyo089h4TyliJ8AxQj'

api = twitter.Api(consumer_key=[c_key],
                  consumer_secret=[c_secret],
                  access_token_key=[a_key],
                  access_token_secret=[a_secret])

results = api.GetSearch(
    raw_query="q=@Macron&result_type=recent&count=10")
