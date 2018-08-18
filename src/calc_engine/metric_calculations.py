#think abuot how to make this extensible for group conversations
#think about how to make it extensible for meta data
	#things like likes, hearts, dislikes in imessage

"""
things to consider when analyzing
how do emojis look in unicode or whatever string format
what about the combination of emoji codes to signify skin tone
what is the criteria for a conversation being terminated and starting anew
versus just an extended pause.
"""

#TODO
# - metrics of how interested the other person in a text conversation is.
# - laughs. 
# 	- favorite way to express humor [lmao, lol, haha, loll]
# 	- average number of ha's in a laugh
# - most terminated conversations [this is kind of just the inverse of double text?]
# - are long periods of silence followed with a "sorry"? lmao.
# - the use of punctuation to show effort score
# https://developers.google.com/edu/python/regular-expressions
# not sure what else.

import numpy as np
import calendar
import re
from src.utilities.utils import flatten_list, display_weekday
from src.utilities.utils import SKINTONES

from src.calc_engine import filter_poly as filt

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
	'top_emojis_s1':None,
	'top_emojis_s2':None,
	'curse_rate_s1':None,
	'curse_rate_s2':None,
	'laugh_rate_s1':None,
	'laugh_rate_s2':None,
	'big_words_rate_s1':None,
	'big_words_rate_s2':None,
	'longest_streak':None,
	'longest_drought':None,
	'punctuation_s1':None,
	'punctuation_s2':None,
	'link_rate_s1':None,
	'link_rate_s2':None
	}
	# will there be a new dictionary thats mostly the same, but for days of week?
	# for days of the month
	# for messages that start with sender 1 versus sender 2 ?
	
	# all of these lists will be lists of dictionaries
	time_diffs_s1 = []
	time_diffs_s2 = []
	avg_lengths_s1 = []
	avg_lengths_s2 = []
	laughs_s1 = []
	laughs_s2 = []
	curses_s1 = []
	curses_s2 = []
	links_s1 = []
	links_s2 = []
	emojis_s1 = []
	emojis_s2 = []
	streaks = []
	timestamps = []


	number_of_text_eqs_sent_s1 = 0
	number_of_text_eqs_sent_s2 = 0
	# loop through the Text Equivalent Objects
	for i in range(len(tes)):
		# it is important to subtract later from earlier for proper time calculation
		earlier_te = tes[i]

		# The calculations for time between are broken out
		# because they require 2 Text Equivalents Simulataneously
		# if you sent the text, then the time it takes the other person to respond
		# is your response rate?
		if i < len(tes)-1:
			later_te = tes[i+1]
			time_diff_dict = calc_time_between_text_equivalents(earlier_te,later_te)

			if earlier_te.sender == PARTICPANT_1:
				time_diffs_s1.append(time_diff_dict)
			elif earlier_te.sender == PARTICPANT_2:
				time_diffs_s2.append(time_diff_dict)

			if not earlier_te.sender == later_te.sender:
				# only append the day if there was an exchange between
				# 2 different participants.
				timestamps.append(earlier_te.timestamp)


		length_dict = calc_length_text_equivalent(earlier_te)
		laugh_dict = calc_laugh(earlier_te)
		curse_dict = calc_curse(earlier_te)
		link_dict = calc_link(earlier_te)
		emoji_dict = calc_emoji(earlier_te)

		if earlier_te.sender == PARTICPANT_1:
			number_of_text_eqs_sent_s1 += 1
			avg_lengths_s1.append(length_dict)
			laughs_s1.append(laugh_dict)
			curses_s1.append(curse_dict)
			links_s1.append(link_dict)
			emojis_s1.append(emoji_dict)
		elif earlier_te.sender == PARTICPANT_2:
			number_of_text_eqs_sent_s2 += 1
			avg_lengths_s2.append(length_dict)
			laughs_s2.append(laugh_dict)
			curses_s2.append(curse_dict)
			links_s2.append(link_dict)
			emojis_s2.append(emoji_dict)


	# do the processing of data calcs aggregated
	# insert the data into the master metrics dictionary
	# number of texts sent
	master_metrics['texts_sent_s1'] = number_of_text_eqs_sent_s1
	master_metrics['texts_sent_s2'] = number_of_text_eqs_sent_s2
	# the longest drought is really the greatest time difference contained in  
	# either of the two time_diffs
	# do the loops once for each time diff list because they are used multiple times.
	non_double_texts_time_diffs_s1 = [td['time diff'] for td in time_diffs_s1 if not td['double text']]
	non_double_texts_time_diffs_s2 = [td['time diff'] for td in time_diffs_s2 if not td['double text']]

	if len(non_double_texts_time_diffs_s1)>0:
		s1_longest = max(non_double_texts_time_diffs_s1) 
	else:
		s1_longest = 0
	if len(non_double_texts_time_diffs_s2)>0:
		s2_longest = max(non_double_texts_time_diffs_s2)
	else:
		s2_longest = 0

	longest_drought_seconds = max([s1_longest,s2_longest])
	# Convert seconds to days
	master_metrics['longest_drought'] = longest_drought_seconds/60.0/60.0/24.0
	master_metrics['longest_streak'] = calc_longest_streak(timestamps)



	# percentage of texts sent that are double texts
	if number_of_text_eqs_sent_s1 > 0:	
		# median number of seconds to reply
		master_metrics['response_rate_s1'] = np.median(non_double_texts_time_diffs_s1)
		# average number of seconds to reply
		master_metrics['response_rate_mean_s1'] = np.mean(non_double_texts_time_diffs_s1)
		# proportion of texts sent that are "double texts"
		master_metrics['double_text_rate_s1'] = calc_rate_of_occurrence('double text',time_diffs_s1,number_of_text_eqs_sent_s1)
		# average text length in words
		master_metrics['average_length_s1'] = np.mean([ld['length_words'] for ld in avg_lengths_s1])
		# find rate of laughter
		master_metrics['laugh_rate_s1'] = calc_rate_of_occurrence('laugh_bool',laughs_s1,number_of_text_eqs_sent_s1)
		# find rate of cursing
		master_metrics['curse_rate_s1'] =  calc_rate_of_occurrence('curse_bool',curses_s1,number_of_text_eqs_sent_s1)
		# find rate of link sharing
		master_metrics['link_rate_s1'] = calc_rate_of_occurrence('link_bool',links_s1,number_of_text_eqs_sent_s1)
		# find the rate of emoji usage
		master_metrics['emoji_rate_s1'] = calc_rate_of_occurrence('emoji_bool',emojis_s1,number_of_text_eqs_sent_s1)
		# find the top emojis
		master_metrics['top_emojis_s1'] = get_top_x_occurrences('emojis_used',emojis_s1,10)

	if number_of_text_eqs_sent_s2 > 0:
		# median number of seconds to reply
		master_metrics['response_rate_s2'] = np.median(non_double_texts_time_diffs_s2)
		# average number of seconds to reply
		master_metrics['response_rate_mean_s2'] = np.mean(non_double_texts_time_diffs_s2)
		# proportion of texts sent that are "double texts"
		master_metrics['double_text_rate_s2'] = calc_rate_of_occurrence('double text',time_diffs_s2,number_of_text_eqs_sent_s2)
		# average text length in words
		master_metrics['average_length_s2'] = np.mean([ld['length_words'] for ld in avg_lengths_s2])
		# find rate of laughter
		master_metrics['laugh_rate_s2'] = calc_rate_of_occurrence('laugh_bool',laughs_s2,number_of_text_eqs_sent_s2)
		# find rate of cursing
		master_metrics['curse_rate_s2'] =  calc_rate_of_occurrence('curse_bool',curses_s2,number_of_text_eqs_sent_s2)
		# find rate of link sharing
		master_metrics['link_rate_s2'] = calc_rate_of_occurrence('link_bool',links_s2,number_of_text_eqs_sent_s2)
		# find the rate of emoji usage
		master_metrics['emoji_rate_s2'] = calc_rate_of_occurrence('emoji_bool',emojis_s2,number_of_text_eqs_sent_s2)
		# find the top emojis
		master_metrics['top_emojis_s2'] = get_top_x_occurrences('emojis_used',emojis_s2,10)


	return (master_metrics)


def calc_most_least_active_times(tes):
	"""
	calculates most and least active times
	on the basis of number of messages sent
	and rate of response 
	"""
	master_time_metrics = {
	'most_active_day_of_week':None,
	'least_active_day_of_week':None,
	'most_active_day_of_month':None,
	'least_active_day_of_month':None,
	'most_active_month_of_year':None,
	'least_active_month_of_year':None,
	'most_active_hour_of_day':None,
	'least_active_hour_of_day':None,
	}
	response_weighting = 6000

	#days of week
	day_of_week_dict = {}
	for day_of_week in range(1,8):
		new_tes = filt.filter_by_day_of_week([day_of_week],tes)['filtered_tes']
		mets = calculate_all_metrics(new_tes)
		g = mets['texts_sent_s1'] +  mets['texts_sent_s2']
		day_of_week_dict[str(day_of_week)] = g
		# some factor that also takes into account response time.
		# reciprocal because a smaller response time means more active.
		if mets['response_rate_s1'] and mets['response_rate_s2']:
			z = response_weighting*(1/mets['response_rate_s1'] + 1/mets['response_rate_s2'])
			day_of_week_dict[str(day_of_week)] = g + z

	#month of year
	month_of_year_dict = {}
	for month in range(1,13):
		new_tes = filt.filter_by_month_of_year([month],tes)['filtered_tes']
		mets = calculate_all_metrics(new_tes)
		g = mets['texts_sent_s1'] +  mets['texts_sent_s2']
		month_of_year_dict[str(month)] = g
		# some factor that also takes into account response time.
		# reciprocal because a smaller response time means more active.

		if mets['response_rate_s1'] and mets['response_rate_s2']:
			z = response_weighting*(1/mets['response_rate_s1'] + 1/mets['response_rate_s2'])
			month_of_year_dict[str(month)] = g + z

	#days of month
	day_of_month_dict = {}
	for day_of_month in range(1,32):
		new_tes = filt.filter_by_day_of_month([day_of_month],tes)['filtered_tes']
		mets = calculate_all_metrics(new_tes)
		g = mets['texts_sent_s1'] +  mets['texts_sent_s2']
		day_of_month_dict[str(day_of_month)] = g 
		# some factor that also takes into account response time.
		# reciprocal because a smaller response time means more active.
		if mets['response_rate_s1'] and mets['response_rate_s2']:
			z = response_weighting*(1/mets['response_rate_s1'] + 1/mets['response_rate_s2'])
			day_of_month_dict[str(day_of_month)] = g + z

	#hour of day
	hour_of_day_dict = {}
	for hour in range(1,25):
		new_tes = filt.filter_by_time_of_day([hour],tes)['filtered_tes']
		mets = calculate_all_metrics(new_tes)
		g = mets['texts_sent_s1'] +  mets['texts_sent_s2']
		hour_of_day_dict[str(hour)] = g 
		# some factor that also takes into account response time.
		# reciprocal because a smaller response time means more active.
		if mets['response_rate_s1'] and mets['response_rate_s2']:
			z = response_weighting*(1/mets['response_rate_s1'] + 1/mets['response_rate_s2'])
			hour_of_day_dict[str(hour)] = g + z

	maxkey_dw = max(day_of_week_dict, key=day_of_week_dict.get)
	minkey_dw = min(day_of_week_dict, key=day_of_week_dict.get)

	maxkey_dm = max(day_of_month_dict, key=day_of_month_dict.get)
	minkey_dm = min(day_of_month_dict, key=day_of_month_dict.get)

	maxkey_my = max(month_of_year_dict, key=month_of_year_dict.get)
	minkey_my = min(month_of_year_dict, key=month_of_year_dict.get)

	maxkey_hd = max(hour_of_day_dict, key=hour_of_day_dict.get)
	minkey_hd = min(hour_of_day_dict, key=hour_of_day_dict.get)


	master_time_metrics = {
	'most_active_day_of_week':display_weekday(maxkey_dw),
	'least_active_day_of_week':display_weekday(minkey_dw),
	'most_active_day_of_month':maxkey_dm,
	'least_active_day_of_month':minkey_dm,
	'most_active_month_of_year':calendar.month_name[int(maxkey_my)],
	'least_active_month_of_year':calendar.month_name[int(minkey_my)],
	'most_active_hour_of_day':maxkey_hd,
	'least_active_hour_of_day':minkey_hd,
	}


	return (master_time_metrics)

def calc_longest_streak(timestamps):

	streaks = []
	streak = 0
	for i in range(len(timestamps)-1):
		early_t = timestamps[i]
		late_t = timestamps[i+1]
		late_t_day = late_t.isoweekday()
		early_t_day = early_t.isoweekday()

		if not early_t_day == 7:
			"""
			it is ok for it to be 1 day, because these are chat exchanges
			and the timestamp is dictated by the time the "earlier text"
			was sent. so you can have early_t be 1 am on Monday
			and late_t be 2 am on Tuesday and the streak will be extended
			even though technically more than 24 hours have passed between
			the timestamps. this is because after the 1 am on Monday the
			other text participant could have responded at 11 PM that monday
			Is this any different results then if you counted the timestamp
			as the time of the "reply" instead of the initiator? No its not.
			"""
			if (early_t_day+1 == late_t_day) and ((late_t-early_t).days in [0,1]):
				streak += 1
			elif (early_t_day == late_t_day) and ((late_t-early_t).days == 0):
				streak = streak
				# if there is a text exchange streak is 1
				if streak == 0:
					streak = 1
			else:
				streaks.append(streak)
				streak = 0
		else:
			if (late_t_day == 1) and ((late_t-early_t).days in [0,1]):
				streak += 1
			elif (early_t_day == 7) and ((late_t-early_t).days==0):
				streak = streak
				# if somebody exchange, they streak is at 1
				if streak == 0:
					streak = 1
			else:
				streaks.append(streak)
				streak = 0

	if len(streaks)==0:
		return streak
	return max(streaks)


def get_top_x_occurrences(special_key,list_of_dicts,occurrence_number):
	"""
	function to find the top occurrences of a given instance
	for instance top x emojis
	top x curse words
	top x laughing expressions
	"""
	results = []
	results_dict = {}
	for lil_d in list_of_dicts:
		if special_key in lil_d.keys():
			these_instances = lil_d[special_key]
			for this_instance in these_instances:
				z=this_instance
				if not z in results_dict.keys():
					results_dict[z] = 1
				else:
					results_dict[z] += 1


	num = len(results_dict.keys())
	#print(str(results_dict))
	#http://stackoverflow.com/questions/7197315/5-maximum-values-in-a-python-dictionary
	if num < occurrence_number:
		results = sorted(results_dict, key=results_dict.get, reverse=True)[:num]
	else:
		results = sorted(results_dict, key=results_dict.get, reverse=True)[:occurrence_number]

	return results

# method to calculate a rate as a percentage of occurrence
def calc_rate_of_occurrence(special_key,list_of_dicts,total_number):
	res = 100.0*(sum([td[special_key] for td in list_of_dicts])
			/float(total_number))
	return res

def calc_time_between_text_equivalents(tes_1,tes_2):
	return_vals = {}
	# it is important to subtract later from earlier for proper time
	tdelta = (tes_2.timestamp-tes_1.timestamp)
	# TODO: implement Pint units handler module
	return_vals['time diff'] = tdelta.seconds + tdelta.days*24.0*60.0*60.0
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
	"""
	calculates the length of each text 
	"""
	return_vals = {}

	return_vals['day of week'] = te.date_day_of_week
	return_vals['hour'] = te.timestamp.hour
	return_vals['length_chars'] = len(te.all_text) # this counts characters
	return_vals['length_words'] = len(re.findall(r'\w+',te.all_text))

	return return_vals


def calc_laugh(te):
	"""
	param: te :: TextEquivalent 
	detect if the TextEquivalent object contains laughter in it
	"""
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
	"""
	param: te :: TextEquivalent 
	detect if the TextEquivalent object contains cursing in it
	"""
	return_vals = {}
	return_vals['day of week'] = te.date_day_of_week
	return_vals['hour'] = te.timestamp.hour
	# the words that count as a curse
	if re.search(r'\b([s]+[h]+[i]+[t]+|[f]+[u]+[c]+[k]+|[b]+[i]+[t]+[c]+[h]+)\b',te.all_text.lower()):
		return_vals['curse_bool'] = True
	else:
		return_vals['curse_bool'] = False

	return return_vals

def calc_link(te):
	"""
	param: te :: TextEquivalent 
	detect if the TextEquivalent object contains a link in it
	"""
	return_vals = {}
	return_vals['day of week'] = te.date_day_of_week
	return_vals['hour'] = te.timestamp.hour
	# the words that count as a link
	# http://stackoverflow.com/questions/6883049/regex-to-find-urls-in-string-in-python
	if re.search(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+',te.all_text.lower()):
		return_vals['link_bool'] = True
	else:
		return_vals['link_bool'] = False
	return return_vals

def calc_emoji(te):
	"""
	:param te : TextEquivalent object to find
	detect if the TextEquivalent object contains an emoji in it and what the emoji(s) are
	TLDR: finds emojis in the text and does some special processing to make sure it doesnt miss skin tones used
	"""
	return_vals = {}
	return_vals['day of week'] = te.date_day_of_week
	return_vals['hour'] = te.timestamp.hour
	# the characters that count as an emoji
	# http://stackoverflow.com/questions/19149186/how-to-find-and-count-emoticons-in-a-string-using-python
	# decode the string into utf-8 to get emojis
	# because this is built in 2.7 python need to do some bs, workaround with astral plan regex
	# the normal way to do this doesnt work well so we get this convoluted workaround
	# google: python narrow build versus wide build or ES5 vs ES6 or UCS-4 vs UCS-2
	# http://stackoverflow.com/questions/31603075/how-can-i-represent-this-regex-to-not-get-a-bad-character-range-error
	# with wide build could use some regex like this -> [\U0001d300-\U0001d356]
	# http://stackoverflow.com/questions/19149186/how-to-find-and-count-emoticons-in-a-string-using-python
	txt_utf_8 = te.all_text.decode('utf-8')
	# this_match = re.findall(r'[\U0001d300-\U0001d356]',txt_utf_8)
	this_match = re.findall(ur'(\ud838[\udc50-\udfff])|([\ud839-\ud83d][\udc00-\udfff])|(\ud83e[\udc00-\udfbf])|([\udc50-\udfff]\ud838)|([\udc00-\udfff][\ud839-\ud83d])|([\udc00-\udfbf]\ud83e)',txt_utf_8)
	if re.search(ur'(\ud838[\udc50-\udfff])|([\ud839-\ud83d][\udc00-\udfff])|(\ud83e[\udc00-\udfbf])|([\udc50-\udfff]\ud838)|([\udc00-\udfff][\ud839-\ud83d])|([\udc00-\udfbf]\ud83e)',txt_utf_8):
	# if re.search(r'[\U0001d300-\U0001d356]',txt_utf_8):
		return_vals['emoji_bool'] = True
		print("Found emoji: {}".format(txt_utf_8))
		#cast it as a set so that there are no repeated unicodes
		#print('all matches ' + str(this_match))
		this_match_new = []
		# this is essentially processing the matches
		# the list comprehension is getting rid of matches 
		# that just look like u'' . empty unicode strings
		# i dont know enough about the regex expression to change it
		for i in this_match:
			this_match_temp = [unicode(z) for z in i if len(z)>0][0]
			this_match_new.append(this_match_temp)
		# cast as a set to get rid of duplicates
		first_pass = list(set(this_match_new))
		# return this to the value
		return_vals['emojis_used'] = first_pass
		"""
		If any of the emoji codes are for skin tone
		checked my looking for the intersection between
		the SKINTONES list/set
		There is another process to follow.
		That process is basically adding the skin tone
		that matches to the end of all the other emoji codes
		this is so that we can count accurately the emojis 
		that are actually 2 emoji codes. one for the standard emoji
		and another emoji code for the skin tone.
		"""
		if (list(set(this_match_new) & set(SKINTONES))):
			new_list_with_skin_appended_to_each = []
			skinlist = list(set(this_match_new) & set(SKINTONES))
			# looping through all of the skin tags
			# appending them to each value in the first pass list
			# thus we can get the combo codes together.
			# but dont combine them if the firstval is the skinval
			for skinval in skinlist:
				templist = [firstval + u' ' + skinval for firstval in first_pass 
				if not firstval==skinval]
				#print('temp list' + str(templist))
				new_list_with_skin_appended_to_each.append(templist)
			#print('new list with skin appended: ' + str(new_list_with_skin_appended_to_each))
			#print('first pass: ' + str(first_pass))
			new_list_with_skin_appended_to_each = flatten_list(new_list_with_skin_appended_to_each)
			#print('new list with skin appended AFTER: ' + str(new_list_with_skin_appended_to_each))

			# after making new lists with each skin appended to each val
			# (in all likelhood the skinlist is probably one element)
			# append this list to the original first pass list
			for combelement in new_list_with_skin_appended_to_each:
				first_pass.append(combelement)
			#first_pass.append(new_list_with_skin_appended_to_each)
			#print('last pass after combining: ' + str(first_pass))
			# now if its just skin tone alone, get rid of it
			for element in first_pass:
				if element in SKINTONES:
					first_pass.remove(element)

		else:
			first_pass = first_pass

		return_vals['emojis_used'] = first_pass
		#print('last pass: ' + str(return_vals['emojis_used']))



	else:
		return_vals['emoji_bool'] = False
	return return_vals


