#from __future__ import unicode_literals
import random as rd
from tkinter import *
# from pynput.keyboard import Key, Listener
from parse import init_annotation_app
from parse import parse_tweet, parse_archive, write_archive, remove_emoji_file
import re

import sys
if len(sys.argv) > 1 :
	file_to_note = sys.argv[1]
else :
	file_to_note = "tw_db.data"


def check_annotations(values_dict) :
	to_ret = 0
	for key in values_dict :
		if values_dict[key]['tag'] != "???" :
			to_ret += 1
	return to_ret

# remove_emoji_file("corpus_macron.txt")

sizemax, keys, values, counts = init_annotation_app(file_to_note)
num_done = check_annotations(values)
active_tweet_id = 0

def clear_annotation() :
	values = parse_archive()
	for key in values :
		values[key]['tag'] = "???"
	write_archive(values)

def disp_counts(canvas) :
	canvas.create_text(500, 250, text="??? : " + str(counts[0]),font="Arial 20", width=700, fill="black", anchor=NW)
	canvas.create_text(500, 280, text="neu : " + str(counts[1]),font="Arial 20", width=700, fill="black", anchor=NW)
	canvas.create_text(500, 310, text="pos : " + str(counts[2]),font="Arial 20", width=700, fill="black", anchor=NW)
	canvas.create_text(500, 340, text="neg : " + str(counts[3]),font="Arial 20", width=700, fill="black", anchor=NW)
	canvas.create_text(500, 370, text="irr : " + str(counts[4]),font="Arial 20", width=700, fill="black", anchor=NW)

def pick_tweet(filestr="tw_db.data") :
	global active_tweet_id
	file = open(filestr, 'r')
	lines = file.readlines()
	tryint = 0
	
	tw = parse_tweet(lines[tryint])

	if tryint < sizemax and tw['tag'] == '???':
		active_tweet_id = tw['id']
		# return retrieve_tweet(active_tweet_id)
		return tw['text']

	else :
		tryint += 1
		tw = parse_tweet(lines[tryint])
		while tryint < sizemax and tw['tag'] != '???' :
			tryint += 1
			tw = parse_tweet(lines[tryint])
			
		# not annoted
		active_tweet_id = tw['id']
		return tw['text']


def write_emotion(id, emote, filestr="tw_db.data") :

	fileread = open(filestr, "r")
	read = fileread.read()
	fileread.close()
	print("replacing")
	print(str(id) + ",???")
	print("with")
	print(str(id) + "," + emote)
	filetest = open(filestr, "w")
	filetest.write(read.replace(str(id) + ",???", str(id)+ "," + emote))
	filetest.close()

can = Canvas(None, width=700, height=450, background='white')
can.pack()

def callback(event, active_text):
	global active_tweet_id
	global num_done
	if event.char == 'j' :
		#neu
		write_emotion(active_tweet_id, "neu", file_to_note)
		num_done += 1
		counts[1] += 1
		counts[0] -= 1
	elif event.char == 'k' :
		#pos
		write_emotion(active_tweet_id, "pos", file_to_note)
		num_done += 1
		counts[2] += 1
		counts[0] -= 1
	elif event.char == 'l' :
		#neg
		write_emotion(active_tweet_id, "neg", file_to_note)
		num_done += 1
		counts[3] += 1
		counts[0] -= 1
	elif event.char == 'm' :
		#irr
		write_emotion(active_tweet_id, "irr", file_to_note)
		num_done += 1
		counts[4] += 1
		counts[0] -= 1

	can.delete("all")
	draw_things(can)
	# can2.pack()
	can.focus_set()

def draw_things(can):
	try :
		active_text = can.create_text(0, 0, text=pick_tweet(file_to_note),font="Arial 20", width=700, fill="black", anchor=NW)
	except :
		active_text = can.create_text(0, 0, text="cannot display text, look in console",font="Arial 20", width=700, fill="black", anchor=NW)
		print(pick_tweet(file_to_note))

	can.create_text(0, 230, text=(str(num_done) + " / " + str(sizemax)), font="Arial 32", fill='black', anchor=W)
	can.pack()
	can.create_image(0, 400, image=img, anchor=W)
	disp_counts(can)
	can.pack()
	return active_text


img = PhotoImage(file="bindings.png")
can.bind("<Key>", lambda event : callback(event, active_text))
can.focus_set()
active_text = draw_things(can)
can.mainloop()

