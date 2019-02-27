import json
file = open('twitterdata2.txt', 'r')
file2= open('twitterdata.txt', 'r')

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

values = parse_file(file)
values2 = parse_file(file2)

file.close()		
file2.close()
values = {**values, **values2}

ids = [key for key in values]
print(len(ids))
# print(values['1100706495421992961'])

file = open('formatted.data', 'w')
for key in values :
	file.write(json.dumps(values[key]) + "\n")

file.close()