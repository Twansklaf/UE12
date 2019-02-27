file = open('twitterdata2.txt', 'r')

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

file.close()

ids = [key for key in values]
print(len(ids))
print(values['1100706495421992961'])

