import sys
import json
import re


emoji_pattern = re.compile("["
        u"\U0001F600-\U0001F64F"  # emoticons
        u"\U0001F300-\U0001F5FF"  # symbols & pictographs
        u"\U0001F680-\U0001F6FF"  # transport & map symbols
        u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
                           "]+", flags=re.UNICODE)


def remove_emoji(inputstr) :
	return emoji_pattern.sub(r'', inputstr)

def remove_emoji_file(filestr) :
	file = open(filestr, "r")
	filer = file.read()
	file.close()
	filer = bytes(filer, 'utf-8').decode('utf-8', 'ignore').encode('utf-8').decode('utf-8')
	file = open(filestr, "w")
	file.write(filer)
	file.close()
	values = parse_archive(filestr)
	write_archive(values, filestr)

def parse_file(file) :
	values = {}
	tmpvalue = {}
	for line in file.readlines() :
		if(len(line.split('id: ')) > 1) :
			tmpvalue['id'] = line.split('id: ')[1].split("\n")[0]
		elif (len(line.split('text: ')) > 1) :
			reading = True
			tmpvalue['text'] = ""
			tmpvalue['text'] += line.split('text: ')[1].split('\n')[0]
		elif (len(line.split('end: ')) > 1) :
			reading = False
			values[tmpvalue['id']] = tmpvalue
			tmpvalue = {}
		else :
			if reading :
				tmpvalue['text'] += line.split('_n')[0]
	return values


def parse_archive(filestr="tw_db.data") :
	values = {}
	file = open(filestr, 'r', encoding='utf-8')
	for line in file.readlines() :
		obj = parse_tweet(line)
		values[obj['id']] = obj
	return values

def create_annot() :
	file = open("annotation.data","w")
	for key in dumped :
		file.write("(" + key + ",???,collected by group 5)" + dumped[key].replace("\n", "") + "\n")
	file.close()

# dumped = parse_archive()
# create_annot()

def init_annotation_app(filestr="tw_db.data") :
	values = parse_archive(filestr)
	keys = [key for key in values]
	count_tab = [0, 0, 0, 0, 0]
	for key in keys : 
		if values[key]['tag'] == '???' :
			count_tab[0] += 1
		elif values[key]['tag'] == 'neu' :
			count_tab[1] += 1
		elif values[key]['tag'] == 'pos' :
			count_tab[2] += 1
		elif values[key]['tag'] == 'neg' :
			count_tab[3] += 1
		else :
			count_tab[4] += 1

	return len(keys), keys, values, count_tab

def parse_tweet(text):
	import re
	regex = r"^\(([0-9]+),(\?\?\?|neu|pos|neg|irr)(,([^,\)]*))*\)(.*)$"

	matches = re.finditer(regex, text, re.MULTILINE)
	for matchNum, match in enumerate(matches, start=1):
		groups = match.groups()
	return {'id': groups[0], 'tag': groups[1], 'params': groups[2], 'text': groups[-1]}

def write_archive(dict_tw, filestr="tw_db.data") :
	file = open(filestr, "w")
	for key in dict_tw :
		file.write(("(" + key + "," + dict_tw[key]['tag'] + dict_tw[key]['params'] +")" + remove_emoji(dict_tw[key]['text'].replace("\n", "")) + "\n"))
	file.close()


def parse_whole() :

	values = []

	file = open("more_tweet.data", "r")
	for line in file.readlines() :
		values.append(parse_tweet(line))

	file = open("annotation.data", "r")
	for line in file.readlines() :
		values.append(parse_tweet(line))

	values_dict = {}
	for value in values :
		values_dict[value['id']] = value

	print(len([key for key in values_dict]))
	write_archive(values_dict)

def two_pass() :
	values = parse_archive()
	list_text = []
	values_to_write = {}
	for key in values :
		if not values[key]['text'] in list_text :
			list_text.append(values[key]['text'])
			values_to_write[key] = values[key]

	write_archive(values_to_write)

# parse_whole()

def merge_new_data(filestr) :
	# first, list existing data

	ids = []

	file = open("tw_db.data", "r")
	for line in file.readlines() :
		ids.append(parse_tweet(line)['id'])
	# print(len(ids))
	file.close()

	file = open(filestr, "r")
	newvalues = parse_file(file)
	file.close()

	for key in newvalues :
		if not key in ids :
			file = open("tw_db.data", "a")
			file.write(("(" + key + "," + "???" + ",collected by group 5" +")" + remove_emoji(newvalues[key]['text'].replace("\n", "")) + "\n"))
			file.close()

	old_ids = ids
	ids = []
	file = open("tw_db.data", "r")
	for line in file.readlines() :
		ids.append(parse_tweet(line)['id'])
	file.close()	
	
	print(str(len(ids) - len(old_ids)) + " insertions, new number of tweets is : " + str(len(ids)) )
	two_pass()
	print("Eliminating doublons")
	values = parse_archive()

	print(str(len([key for key in values])) + " entries in the dump file")

# two_pass()

import sys
if len(sys.argv) > 1 and sys.argv[1] == "--merge" :
	merge_new_data("data.txt")
