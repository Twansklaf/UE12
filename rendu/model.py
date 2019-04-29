from parse import *
from word_tools import *

from word_tools import make_bagofwords

from sys import argv

corpus_str = ""
file_to_annot_str = ""

if len(argv) > 2 :
	print("Making bag of words and vectorizing corpus (~15 seconds)")
	corpus_str = argv[1]
	file_to_annot_str = argv[2]
else :
	print("Need two args : corpus file, test file to annot.")
	exit(0)

nb_words = 10000

bow = make_bagofwords(corpus_str, 10000)

from word_tools import vectorize_tweets
vect = vectorize_tweets(corpus_str, bow)

import numpy as np
keys = [k for k in vect]

input_len = np.shape(vect[keys[0]]['vectorized'])[0]

def extract_data(vectsdict):
		import numpy as np
		vects = []
		labels = []
		
		for key in vectsdict :
				if not np.all(vectsdict[key]['label'] == 0) :
						vects.append(vectsdict[key]['vectorized'])
						labels.append(vectsdict[key]['label'])
		return np.array(vects), np.array(labels)

def decode_output(out_array_arg) :
	irrscore = out_array_arg[0]
	negscore = out_array_arg[1]
	neuscore = out_array_arg[2]
	posscore = out_array_arg[3]

	maxscore = np.max(out_array_arg)

	if irrscore == maxscore :
		return 'irr'
	elif negscore == maxscore :
		return 'neg'
	elif neuscore == maxscore :
		return 'neu'
	elif posscore == maxscore : 
		return 'pos'
	else :
		return 'err'

data, labels = extract_data(vect)


percentage_train = 0.85
borne = int(percentage_train*len(data))
X_train = data[:borne]
Y_train = labels[:borne]
X_test = data[borne:]
Y_test = labels[borne:]

print("Train set : ", len(X_train), " elements, Test_set : ", len(X_test))

from keras.models import Sequential
from keras.layers import Dense, Flatten
from keras.layers.embeddings import Embedding

# define the model
model = Sequential()
model.add(Embedding(input_dim=nb_words, output_dim=8, input_length=input_len))
model.add(Flatten())
model.add(Dense(4, activation='sigmoid'))

# compile the model

model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['acc'])
# print(model.summary())
# batch = 50
batch = 100
model.fit(X_train, Y_train, epochs=70, batch_size=batch, verbose=1)


loss, accuracy = model.evaluate(X_test, Y_test, verbose=0)
# loss, accuracy = model.evaluate(X_train, Y_train)
print("Model accuracy : ",accuracy)

dict_to_annot = parse_archive(file_to_annot_str)

file = open(file_to_annot_str + ".annot", 'w')

for tw in dict_to_annot:
	prepared_text = processTweet(dict_to_annot[tw]['text'])
	# print(prepared_text)
	vec = (vectorize_tweet(prepared_text, '???', bow, input_len))
	vec['vectorized'] = vec['vectorized'].reshape((1,49))
	response = model.predict(vec['vectorized'])
	file.write(("(" + tw + "," + decode_output(response[0]) +")" + dict_to_annot[tw]['text'] + "\n"))

print("Evaluations written to file : " + file_to_annot_str + ".annot")

file.close() 