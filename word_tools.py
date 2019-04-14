import re
import sys
from parse import parse_tweet, parse_archive, write_archive

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
		tweet = re.sub(r'([a-z])([A-Z])','\\1 \\2', tweet)
		# Remove tickers
		tweet = re.sub(r'\$\w*', '', tweet)
		# To lowercase
		tweet = tweet.lower()
		# Remove hyperlinks
		tweet = re.sub(r'https:\/\/t.co\/.{9}', '', tweet)
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

def make_bagofwords(filestr, word_count) :
	values = parse_archive(filestr)
	bow = {}
	for id in values:
		for word in values[id]['text'].split(" ") :
			if word in bow :
				bow[word] += 1
			else :
				bow[word] = 1
	bowL = []
	for key in bow :
		bowL.append((key, bow[key]))
	bowL.sort(key=lambda x: x[1])
	return [x[0] for x in bowL[-word_count:]]

def copy_tweet_database(filestr, copystr) :
	file = open(filestr, 'r')
	fileout = open(copystr, 'w')
	for line in file.readlines() :
		tw = parse_tweet(line)
		fileout.write("(" + str(tw['id']) + "," + tw['tag'] + ")" + processTweet(tw['text']) + "\n")
	file.close()
	fileout.close()



def vectorize_tweets(filestr, dico) :
	values = parse_archive(filestr)
	vectors = {}
	import numpy as np
	max_tweet_size = np.max([len(values[id]['text'].split(' ')) for id in values])


	for id in values :
		if values[id]['tag'] != "???" : 
			vectors[id] = {'text' : values[id]['text']}
			if values[id]['tag'] == 'irr' :
				vectors[id]['label'] = [1, 0, 0, 0]
			elif values[id]['tag'] == 'neg' :
				vectors[id]['label'] = [0, 1, 0, 0]
			elif values[id]['tag'] == 'neu' :
				vectors[id]['label'] = [0, 0, 1, 0]
			elif values[id]['tag'] == 'pos' :
				vectors[id]['label'] = [0, 0, 0, 1]
			else :
				vectors[id]['label'] = [0, 0, 0, 0]
			vectors[id]['label'] = np.array(vectors[id]['label'])
			tmp_vect = []
			for word in vectors[id]['text'].split(' ') :
				try :
					tmp_vect.append(dico.index(word))
				except:
					tmp_vect.append(0)
			if len(tmp_vect) < max_tweet_size :
				tmp_vect += [0 for i in range(max_tweet_size - len(tmp_vect))]
			vectors[id]['vectorized'] = np.array(tmp_vect)

	return vectors


def vectorize_tweet(tw, tag, dico, input_size) :
	vector = {}
	import numpy as np
	max_tweet_size = input_size

	vector = {'text' : tw}
	if tag == 'irr' :
		vector['label'] = [1, 0, 0, 0]
	elif tag == 'neg' :
		vector['label'] = [0, 1, 0, 0]
	elif tag == 'neu' :
		vector['label'] = [0, 0, 1, 0]
	elif tag == 'pos' :
		vector['label'] = [0, 0, 0, 1]
	else :
		vector['label'] = [0, 0, 0, 0]

	vector['label'] = np.array(vector['label'])

	tmp_vect = []
	for word in vector['text'].split(' ') :
		try :
			tmp_vect.append(dico.index(word))
		except:
			tmp_vect.append(0)
	if len(tmp_vect) < max_tweet_size :
		tmp_vect += [0 for i in range(max_tweet_size - len(tmp_vect))]
	vector['vectorized'] = np.array(tmp_vect)

	return vector
	
			
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

if len(sys.argv) > 1 :
	if sys.argv[1] == '--rebuild' :
		copy_tweet_database(sys.argv[2])
		list_tweet = get_list_tweet(sys.argv[2])
		dico = build_dico(list_tweet)
		write_dictionary(dico)
	elif sys.argv[1] == '--buildic' :
		dico = load_dictionary("dico.txt")
	elif sys.argv[1] == '--update' :
		copy_tweet_database(sys.argv[2])


import sys
if len(sys.argv) > 1 :
	if sys.argv[1] == "--merge" :
		copy_tweet_database(sys.argv[2], sys.argv[3])


# print(len(dico))
# vects = vectorize_tweets("tw_db_prepared.data", "dico.txt")
# print(len([k for k in vects]))

# print(list_tweet[0])
# print(type(processTweet(list_tweet[0])))

# dico = build_dico(list_tweet)
# write_dictionary(dico)

# def load_dico(filestr) :
	
# 	file = open(filestr, 'r')

valuesA = parse_archive("g5remi.data")
valuesR = parse_archive("g5antoine.data")

idsA = [k for k in valuesA]
idsR = [k for k in valuesR]

iddiff = [id for id in idsA if valuesA[id]['tag'] != valuesR[id]['tag']]

print(len(iddiff))

wrong = {}

for k in iddiff :
	wrong[k] = valuesA[k]

for k in wrong :
	wrong[k]['tag'] = '???'

write_archive(wrong, "convergence.txt")