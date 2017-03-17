"""
Main module
- read data in from data/ directory
#TODO
- do some preliminary calcs
- metrics of how interested the other person in a text conversation is.
- average time of response. 
- emoji usage comparison. 
- laughs. 
	- favorite way to express humor [lmao, lol, haha, loll]
	- average number of ha's in a laugh
- follow up questions asked. [how to quantify, not clear/dont really make sense]
- response text length to initial text length. 
- most terminated conversations
- analyze which times of the day are most active for conversation
- frequency of cursing 
- favorite emojis
- which day of the week is most active for conversation
- how do all of these metrics change depending on the day of the week
- or the time of the month
- period of the day
- are long periods of silence followed with a "sorry"? lmao.
- the use of punctuation to show effort score
- are links shared between the two?
- longest streak of consecutive days talked
- longest streak of consecutive days not talked
https://developers.google.com/edu/python/regular-expressions
not sure what else.
"""
"""
make the parsing flexible in case the format of text input
changes drastically. currently using 
https://github.com/PeterKaminski09/baskup to dump data
"""

#standard imports
import os
import datetime
import re
#module imports
from convo_objects.TextEquivalent import TextEquivalent

#########
#Read
#########
working_dir = os.getcwd()
data_folder = working_dir + os.sep + os.pardir + os.sep + "data" 
text_file_name = "anon_convo.txt"
full_path = data_folder + os.sep + text_file_name

#the amount of time between texts for them to be considered 'sequential'
BLOCK_TEXT_THRESHOLD_SECONDS = 90
text_equivs = []
with open(full_path,'r') as whole_ass_convo:
	raw_data = whole_ass_convo.readlines()
	i = 0
	for line in raw_data:
		# search for a couple of letters then a colon, before 
		sender = re.search(r'^\w+\:',line)
		# search for the timestamp in YYYY-MM-DD HH:MM:SS format.
		timestamp = re.search(r'\|\d+\-\d+\-\d+\s?\d+\:\d+\:\d+',line)
		if sender and timestamp:
			sender_name = sender.group()
			
			timestamp_string = timestamp.group()
			# slice the raw input such that sender & timestamp are gone.
			text_msg = line[len(sender_name):-len(timestamp_string)-1]
			# get rid of the identifier pipe, first character.
			te = TextEquivalent(sender_name,timestamp_string[1:],text_msg)
			
			if i >= 1:
				te_prev = text_equivs[i-1]
				diff = te.timestamp - te_prev.timestamp
				if (te_prev.sender==te.sender) and (abs(diff.seconds) < BLOCK_TEXT_THRESHOLD_SECONDS):
					#te_prev.append_sequential_text(text_msg)
					te_prev.merge_sequential_text_equiv(te)
				else:
					text_equivs.append(te)
					i += 1
			else:
				text_equivs.append(te)
				i += 1
		print line
		if i == 1000:
			break


print(str([str(g.date_day_of_week) for g in text_equivs]))


