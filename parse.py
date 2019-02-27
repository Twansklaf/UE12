import sys
import json
file = open('twitterdata2.txt', 'r')
file2= open('twitterdata.txt', 'r')
file3= open('twitterdata3.txt', 'r')


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

# values = parse_file(file)
# values2 = parse_file(file2)
# file.close()		
# file2.close()

# values = {**values, **values2}
# values = {**values, **parse_file(file3)}

# file3.close()

# ids = [key for key in values]
# # print(values['1100706495421992961'])

# file = open('formatted.data', 'w')
# for key in values :
# 	file.write(json.dumps(values[key]) + "\n")

# file.close()

def parse_archive() :
	values = {}
	file = open('formatted.data', 'r')
	for line in file.readlines() :
		# print(line[:-1]) # to remove cr
		strdump = json.loads(line[:-1])
		values[strdump['id']] = strdump['text']
	return values

def create_annot() :
	file = open("annotation.data","w")
	for key in dumped :
		file.write("(" + key + ",???,collected by group 5)" + dumped[key].replace("\n", "") + "\n")
	file.close()

dumped = parse_archive()
create_annot()

def init_annotation_app() :
	values = parse_archive()
	keys = [key for key in values]

	return len(keys), keys, values

def parse_tweet(text):
	import re
	regex = r"^\(([0-9]+),(\?\?\?|neu|pos|neg|irr)(,([^,\)]*))*\)(.*)$"

	matches = re.finditer(regex, text, re.MULTILINE)
	for matchNum, match in enumerate(matches, start=1):
		groups = match.groups()
	return {'id': groups[0], 'tag': groups[1], 'params': groups[2], 'text': groups[-1]}

def write_archive(dict_tw) :
	
	file = open("tw_db.data", "w")
	for key in dict_tw :
		file.write(("(" + key + "," + dict_tw[key]['tag'] + dict_tw[key]['params'] +")" + dict_tw[key]['text'].replace("\n", "") + "\n"))
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
			file.write(("(" + key + "," + "???" + ",collected by group 5" +")" + newvalues[key]['text'].replace("\n", "") + "\n"))
			file.close()

	old_ids = ids
	ids = []
	file = open("tw_db.data", "r")
	for line in file.readlines() :
		ids.append(parse_tweet(line)['id'])
	file.close()	
	
	print(str(len(ids) - len(old_ids)) + " insertions, new number of tweets is : " + str(len(ids)) )

merge_new_data("newd.txt")