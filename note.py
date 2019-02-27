from __future__ import unicode_literals
import random as rd
from tkinter import *
# from pynput.keyboard import Key, Listener
from parse import init_annotation_app
from parse import parse_tweet
import re

def check_annotations(values_dict) :
	to_ret = 0
	for key in values_dict :
		if values_dict[key]['tag'] != "???" :
			to_ret += 1
	return to_ret

sizemax, keys, values = init_annotation_app()
num_done = check_annotations(values)
active_tweet_id = 0

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
	global num_done
	if event.char == 'j' :
		#neu
		write_emotion(active_tweet_id, "neu")
		num_done += 1
	elif event.char == 'k' :
		#pos
		write_emotion(active_tweet_id, "pos")
		num_done += 1
	elif event.char == 'l' :
		#neg
		write_emotion(active_tweet_id, "neg")
		num_done += 1
	elif event.char == 'm' :
		#irr
		write_emotion(active_tweet_id, "irr")
		num_done += 1

	can.delete("all")
	active_text = can.create_text(0, 0, text=pick_tweet(),font="Arial 16", width=1000, fill="black", anchor=NW)
	can2.delete("all")
	can2.create_text(0, 50, text=(str(num_done) + "/" + str(sizemax)), font="Arial 32", fill='black', anchor=W)
	can.pack()
	can2.pack()
	can.focus_set()

def toplevel():
  top = Toplevel()
  top.geometry("200x100+100+100")
  can2 = Canvas(top, width=200, height=100, background="white")
  txt = can2.create_text(0, 50, text=(str(num_done) + "/" + str(sizemax)), font="Arial 32", fill='black', anchor=W)
  can2.pack()
  return can2

can.bind("<Key>", lambda event : callback(event, active_text))
can.focus_set()
can2 = toplevel()
can.mainloop()




# can2 = Canvas(None, width=200, height=200, background='white')
# can2.pack()
# can2.pack
# can2.mainloop()
# win.mainloop()
