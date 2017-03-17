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

#one method for all metrics so the loop only happens once
def calculate_all_metrics(tes):
	list_of_dicts_time_diff = []
	for i in range(len(tes)-1):
		#
		earlier_te = tes[i]
		later_te = tes[i+1]
		time_diff = calc_time_between_text_equivalents(earlier_te,later_te)


def calc_time_between_text_equivalents(tes_1,tes_2):
	return_vals = {}
	time_diff = tes_2.timestamp - tes_1.timestamp
	initiater = tes_1.sender 
	return_vals['responder'] = tes_2.sender
	return_vals['sender'] = tes_1.sender
	return_vals['day of week'] = tes_1.date_day_of_week


