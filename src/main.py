"""
Main module
- read data in from data/ directory
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
import metric_calculations as mc 

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


r = mc.calculate_all_metrics(text_equivs)
print(str(r))


