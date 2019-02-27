from __future__ import unicode_literals
import random as rd
from tkinter import *
# from pynput.keyboard import Key, Listener
from parse import init_annotation_app
from parse import parse_tweet

sizemax, keys, values = init_annotation_app()
active_tweet_id = 0

# def retrieve_tweet(id) :
# 	return values[id]

def pick_tweet() :
	global active_tweet_id
	file = open("tw_db.data", 'r')
	lines = file.readlines()
	tryint = rd.randint(0, sizemax)
	
	tw = parse_tweet(lines[tryint])

	if tw['tag'] == '???':
		active_tweet_id = tw['id']
		# return retrieve_tweet(active_tweet_id)
		return tw['text']

	else :
		tryint = rd.randint(0, sizemax)
		while tw['tag'] != '???' :
			tryint = rd.randint(0, sizemax)
		
		# not annoted
		active_tweet_id = tw['id']
		return tw['text']


def write_emotion(id, emote) :

	fileread = open("tw_db.data", "r")
	read = fileread.read()
	fileread.close()
	print("replacing")
	print(str(id) + ",???")
	print("with")
	print(str(id) + "," + emote)
	filetest = open("tw_db.data", "w")
	filetest.write(read.replace(str(id) + ",???", str(id)+ "," + emote))
	filetest.close()


can = Canvas(None, width=1200, height=100, background='white')
can.pack()
active_text = can.create_text(0, 0, text=pick_tweet(),font="Arial 16", width=1000, fill="black", anchor=NW)

def callback(event, active_text):
	global active_tweet_id
	if event.char == 'j' :
		#neu
		write_emotion(active_tweet_id, "neu")
	elif event.char == 'k' :
		#pos
		write_emotion(active_tweet_id, "pos")
	elif event.char == 'l' :
		#neg
		write_emotion(active_tweet_id, "neg")
	elif event.char == 'm' :
		#irr
		write_emotion(active_tweet_id, "irr")

	can.delete("all")
	active_text = can.create_text(0, 0, text=pick_tweet(),font="Arial 16", width=1000, fill="black", anchor=NW)
	can.pack()
	can.focus_set()


can.bind("<Key>", lambda event : callback(event, active_text))
can.focus_set()
can.mainloop()
# win.mainloop()
