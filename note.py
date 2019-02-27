from __future__ import unicode_literals
import random as rd
from tkinter import *
# from pynput.keyboard import Key, Listener
from parse import init_annotation_app

sizemax, keys, values = init_annotation_app()
active_tweet_id = 0

def retrieve_tweet(id) :
	return values[id]

def pick_tweet() :
	global active_tweet_id
	file = open("annotation.data", 'r')
	lines = file.readlines()
	tryint = rd.randint(0, sizemax)
	
	if len(lines[tryint].split(",")) > 1 and lines[tryint].split(",")[1][0] == '_' :
		active_tweet_id = lines[tryint].split(",")[0][1:]
		return retrieve_tweet(active_tweet_id)

	else :
		tryint = rd.randint(0, sizemax)
		while len(lines[tryint].split(",")) > 1 and lines[tryint].split(",")[1][0] != '_' :
			tryint = rd.randint(0, sizemax)
		
		# not annoted
		active_tweet_id = lines[tryint].split(",")[0][1:]
		return retrieve_tweet(active_tweet_id)


def write_emotion(id, emote) :
	fileread = open("annotation.data")
	read = fileread.read()
	fileread.close()
	print("replacing")
	print("(" + str(id) + ",_)")
	print("with")
	print("(" + str(id) + "," + emote + ")")
	filetest = open("annotation.data", "w")
	filetest.write(read.replace("(" + str(id) + ",_)", "(" + str(id) + "," + emote + ")"))
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
