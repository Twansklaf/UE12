import re
import sys
from parse import parse_tweet, parse_archive

def get_list_tweet(filestr) :
	list_tw = []
	file = open(filestr, "r")
	for line in file.readlines() :
		tw = parse_tweet(line)
		if tw['tag'] != "irr" :
			list_tw.append(tw['text'])
	return list_tw


def format_sentence(sentence):
	toReturn = []
	for word in re.sub(r'[^\w\s]', '', sentence).split(" ") :
		# print(word)
		if len(word) > 0 and word[0] != "@" :
			if len(word) > 0 and word[0] == "#" :
				toReturn.append(word[1:].lower())
			else :
				toReturn.append(word.lower())
	return toReturn

def parse_sentence(sentence, dictionary) :
	for word in sentence :
		if not word in dictionary :
			dictionary.append(word)

def build_dico(list_tweet) : # text is a list of sentences.
	dictionary = []
	for tw in list_tweet :
		processed = processTweet(tw).split(" ")
		for word in processed :
			if not word in dictionary :
				dictionary.append(word)

	return dictionary		

# helper function to clean tweets
def processTweet(tweet):
		from string import punctuation
		# Remove HTML special entities (e.g. &amp;)
		tweet = re.sub(r'\&\w*;', '', tweet)
		#Convert @username to AT_USER
		tweet = re.sub(r'@[^\s]+','',tweet)
		# remove numbers
		tweet = re.sub(r'\d+', ' ', tweet)
		# Remove tickers
		tweet = re.sub(r'\$\w*', '', tweet)
		# To lowercase
		tweet = tweet.lower()
		# Remove hyperlinks
		tweet = re.sub(r'https?:\/\/.*\/\w*', '', tweet)
		# Remove hashtags
		tweet = re.sub(r'#', ' ', tweet)
		# Remove Punctuation and split 's, 't, 've with a space for filter
		tweet = re.sub(r'[' + punctuation.replace('@', '') + ']+', ' ', tweet)
		tweet = re.sub(r'[^\w\s]', ' ', tweet)
		# Remove words with 2 or fewer letters
		tweet = re.sub(r'\b\w{1,2}\b', '', tweet)
		# Remove whitespace (including new line characters)
		tweet = re.sub(r'\s\s+', ' ', tweet)
		# Remove single space remaining at the front of the tweet.
		tweet = tweet.lstrip(' ') 
		# Remove characters beyond Basic Multilingual Plane (BMP) of Unicode:
		tweet = ''.join(c for c in tweet if c <= '\uFFFF') 
		return tweet


def copy_tweet_database(filestr) :
	file = open(filestr, 'r')
	fileout = open('tw_db_prepared.data', 'w')
	for line in file.readlines() :
		tw = parse_tweet(line)
		fileout.write("(" + str(tw['id']) + "," + tw['tag'] + tw['params'] + ")" + processTweet(tw['text']) + "\n")
	file.close()
	fileout.close()



def vectorize_tweets(tweetstr, dicostr) :
	vects = {}
	tags = []
	dico = load_dictionary("dico.txt")
	file = open(tweetstr, 'r')
	# print(sizedico)
	for linetweet in file.readlines() :
		twt = parse_tweet(linetweet)
		if twt['tag'] != "???" and twt['tag'] != "irr" :
			vects[twt['id']] = [0 for x in dico]
			tags.append(twt['tag'])
			for word in twt['text'].split(" ") :
				vects[twt['id']][int(dico[word])] = 1
	return vects, tags
			
def load_dictionary(filestr) :
	dico = {}
	file = open(filestr, 'r')
	for line in file.readlines() :
		if line != " " :
			dico[line.split("=")[0]] = line.split("=")[1].split("\n")[0]
	file.close()
	return dico

def write_dictionary(dictionary) :
	file = open("dico.txt", "w", encoding='utf-8')
	count = 1
	dictionary.sort()
	for word in dictionary :
		file.write(word + "=" + str(count) + "\n")
		count +=1
	file.close()

# if len(sys.argv) > 1 :
# 	if(sys.argv[1] == '--rebuild') :
# 		copy_tweet_database(sys.argv[2])
# 		list_tweet = get_list_tweet(sys.argv[2])
# 		dico = build_dico(list_tweet)
# 		write_dictionary(dico)
# else :
# 	dico = load_dictionary("dico.txt")


# print(len(dico))
# vects = vectorize_tweets("tw_db_prepared.data", "dico.txt")
# print(len([k for k in vects]))

# print(list_tweet[0])
# print(type(processTweet(list_tweet[0])))

# dico = build_dico(list_tweet)
# write_dictionary(dico)

# def load_dico(filestr) :
	
# 	file = open(filestr, 'r')

copy_tweet_database(sys.argv[1])
