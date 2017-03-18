#think abuot how to make this extensible for group conversations
#think about how to make it extensible for meta data
	#things like likes, hearts, dislikes in imessage
######
#Parse
######

"""
things to consider when analyzing

how do emojis look in unicode or whatever string format

what is the criteria for a conversation being terminated and starting anew
versus just an extended pause.

"""

#TODO
# - do some preliminary calcs
# - metrics of how interested the other person in a text conversation is.
# - average time of response. 
# - emoji usage comparison. 
# - laughs. 
# 	- favorite way to express humor [lmao, lol, haha, loll]
# 	- average number of ha's in a laugh
# - follow up questions asked. [how to quantify, not clear/dont really make sense]
# - response text length to initial text length. 
# - most terminated conversations
# - analyze which times of the day are most active for conversation
# - frequency of cursing 
# - favorite emojis
# - which day of the week is most active for conversation
# - how do all of these metrics change depending on the day of the week
# - or the time of the month
# - period of the day
# - are long periods of silence followed with a "sorry"? lmao.
# - the use of punctuation to show effort score
# - are links shared between the two?
# - longest streak of consecutive days talked
# - longest streak of consecutive days not talked
# https://developers.google.com/edu/python/regular-expressions
# not sure what else.

import numpy as np
import datetime
import re

#one method for all metrics so the loop only happens once
#tes will likely be a dictionary with some meta data
#what are the names of the conversation participants
def calculate_all_metrics(tes):
	PARTICPANT_1 = "Me"
	PARTICPANT_2 = "Friend"

	master_metrics = {
	'texts_sent_s1':None,
	'texts_sent_s2':None,
	'response_rate_s1':None,
	'response_rate_s2':None,
	'response_rate_mean_s1':None,
	'response_rate_mean_s2':None,
	'double_text_rate_s1':None,
	'double_text_rate_s2':None,
	'emoji_rate_s1':None,
	'emoji_rate_s2':None,
	'average_length_s1':None,
	'average_length_s2':None,
	'top_5_emojis_s1':None,
	'top_5_emojis_s2':None,
	'curse_rate_s1':None,
	'curse_rate_s2':None,
	'laugh_rate_s1':None,
	'laugh_rate_s2':None,
	'big_words_rate_s1':None,
	'big_words_rate_s2':None,
	'longest_steak':None,
	'longest_drought':None,
	'punctuation_s1':None,
	'punctuation_s2':None,
	'link_rate_s1':None,
	'link_rate_s2':None
	}
	# will there be a new dictionary thats mostly the same, but for days of week?
	# for days of the month
	# for messages that start with sender 1 versus sender 2 ?
	# all of these lists are lists of dictionaries
	time_diffs_s1 = []
	time_diffs_s2 = []
	avg_lengths_s1 = []
	avg_lengths_s2 = []
	laughs_s1 = []
	laughs_s2 = []

	number_of_text_eqs_sent_s1 = 0
	number_of_text_eqs_sent_s2 = 0
	# loop through the Text Equivalent Objects
	for i in range(len(tes)):
		# it is important to subtract later from earlier for proper time calculation
		earlier_te = tes[i]

		# The calculations for time between are broken out
		# because they require 2 Text Equivalents Simulataneously
		if i < len(tes)-1:
			later_te = tes[i+1]
			time_diff_dict = calc_time_between_text_equivalents(earlier_te,later_te)
			if earlier_te.sender == PARTICPANT_1:
				time_diffs_s1.append(time_diff_dict)
			elif earlier_te.sender == PARTICPANT_2:
				time_diffs_s2.append(time_diff_dict)


		length_dict = calc_length_text_equivalent(earlier_te)
		laugh_dict = calc_laugh(earlier_te)
		if earlier_te.sender == PARTICPANT_1:
			number_of_text_eqs_sent_s1 += 1
			avg_lengths_s1.append(length_dict)
			laughs_s1.append(laugh_dict)
		elif earlier_te.sender == PARTICPANT_2:
			number_of_text_eqs_sent_s2 += 1
			avg_lengths_s2.append(length_dict)
			laughs_s2.append(laugh_dict)


	# do the processing of data calcs aggregated
	# insert the data into the master metrics dictionary

	# number of texts sent
	master_metrics['texts_sent_s1'] = number_of_text_eqs_sent_s1
	master_metrics['texts_sent_s2'] = number_of_text_eqs_sent_s2

	# percentage of texts sent that are double texts
	if number_of_text_eqs_sent_s1 > 0:	
		# median number of seconds to reply
		master_metrics['response_rate_s1'] = np.median([td['time diff'] for td in time_diffs_s1 if not td['double text']])
		# average number of seconds to reply
		master_metrics['response_rate_mean_s1'] = np.mean([td['time diff'] for td in time_diffs_s1 if not td['double text']])
		# proportion of texts sent that are "double texts"
		master_metrics['double_text_rate_s1'] = 100.0*(sum([td['double text'] for td in time_diffs_s1])
			/float(number_of_text_eqs_sent_s1))
		# average text length in words
		master_metrics['average_length_s1'] = np.mean([ld['length_words'] for ld in avg_lengths_s1])
		# find rate of laughter
		master_metrics['laugh_rate_s1'] = 100.0*(sum([td['laugh_bool'] for td in laughs_s1])
			/float(number_of_text_eqs_sent_s1))

	if number_of_text_eqs_sent_s2 > 0:
		# median number of seconds to reply
		master_metrics['response_rate_s2'] = np.median([td['time diff'] for td in time_diffs_s2 if not td['double text']])
		# average number of seconds to reply
		master_metrics['response_rate_mean_s2'] = np.mean([td['time diff'] for td in time_diffs_s2 if not td['double text']])
		# proportion of texts sent that are "double texts"
		master_metrics['double_text_rate_s2'] = 100.0*(sum([td['double text'] for td in time_diffs_s2])
			/float(number_of_text_eqs_sent_s2))
		# average text length in words
		master_metrics['average_length_s2'] = np.mean([ld['length_words'] for ld in avg_lengths_s2])
		# find rate of laughter
		master_metrics['laugh_rate_s2'] = 100.0*(sum([td['laugh_bool'] for td in laughs_s2])
			/float(number_of_text_eqs_sent_s2))
	
	return (master_metrics)

def calc_time_between_text_equivalents(tes_1,tes_2):
	return_vals = {}
	# it is important to subtract later from earlier for proper time
	return_vals['time diff'] = (tes_2.timestamp - tes_1.timestamp).seconds
	initiator = tes_1.sender 
	return_vals['responder'] = tes_2.sender
	return_vals['sender'] = initiator
	# use the person who sent the message to calculate
	# eventually perhaps we can give advice on when the best time
	# to talk to someone is
	return_vals['day of week'] = tes_1.date_day_of_week
	return_vals['double text'] = tes_2.sender==tes_1.sender
	return_vals['hour'] = tes_1.timestamp.hour
	return return_vals

def calc_length_text_equivalent(te):
	return_vals = {}

	return_vals['day of week'] = te.date_day_of_week
	return_vals['hour'] = te.timestamp.hour
	return_vals['length_chars'] = len(te.all_text) # this counts characters
	return_vals['length_words'] = len(re.findall(r'\w+',te.all_text))

	return return_vals

def calc_laugh(te):
	return_vals = {}
	return_vals['day of week'] = te.date_day_of_week
	return_vals['hour'] = te.timestamp.hour
	# the words that count as a laugh
	# http://stackoverflow.com/questions/16453522/how-can-i-detect-laughing-words-in-a-string
	if re.search(r'\b(a*ha+h[ha]*|o?l+o+l+[ol]*|lma[o]+)\b',te.all_text.lower()):
		return_vals['laugh_bool'] = True
	else:
		return_vals['laugh_bool'] = False

	return return_vals

def calc_curse(te):
	return_vals = {}
	return_vals['day of week'] = te.date_day_of_week
	return_vals['hour'] = te.timestamp.hour
	# the words that count as a laugh
	# http://stackoverflow.com/questions/16453522/how-can-i-detect-laughing-words-in-a-string
	if re.search(r'\b([s]+[h]+[i]+[t]+|[f]+[u]+[c]+[k]+|[b]+[i]+[t]+[c]+[h]+)\b',te.all_text.lower()):
		return_vals['curse_bool'] = True
	else:
		return_vals['curse_bool'] = False

	return return_vals

