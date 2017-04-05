[![Build Status](https://travis-ci.org/weAllWeGot/conversation-analytics.svg?branch=master)](https://travis-ci.org/weAllWeGot/conversation-analytics)

[![Coverage Status](https://coveralls.io/repos/github/weAllWeGot/conversation-analytics/badge.svg?branch=master)](https://coveralls.io/github/weAllWeGot/conversation-analytics?branch=master)



# conversation-analytics
understand social dynamics in a two-way conversation, have hard data to back up your intuition about your relationships.
For more details on the projects,  check out the wiki pages.
https://github.com/weAllWeGot/conversation-analytics/wiki

obtain your text conversations as .txt by
running the shell script in this repo:
https://github.com/PeterKaminski09/baskup 


# preliminary output
s1 & s2 denote different conversations participants.
```python
# response rates are in seconds
	# the first is a median, the other is an average
		# response_rate_s1: 
		# if s1 sends a text, then 22.0 seconds is the most common time 
		# that they will wait before receiving a reply from s2
# double text & laugh & curse & emoji & link rates are percentage of texts sent
# longest streak is consecutive days talking
# longest drought is consecutive days no talking

# average length is number of words
	master_metrics = {
	'texts_sent_s1':2453,
	'texts_sent_s2':2638,
	'response_rate_s1':22.0,
	'response_rate_s2':32.0,
	'response_rate_mean_s1':2439.84,
	'response_rate_mean_s2':1443.09,
	'double_text_rate_s1':7.17,
	'double_text_rate_s2':13.68,
	'emoji_rate_s1':5.055,
	'emoji_rate_s2':3.56,
	'average_length_s1':11.06,
	'average_length_s2':8.97,
	'top_10_emojis_s1':[u'thinking face', u'face with rolling eyes',
	u'person shrugging: dark skin tone', u'person shrugging',
	u'pensive face', u'weary face', u'face with tears of joy',
	u'smiling face with smiling eyes', u'hugging face', u'eyes'],
	'top_10_emojis_s2':[u'weary face', u'face with tears of joy',
	u'face with rolling eyes', u'expressionless face',
	u'thinking face', u'person tipping hand: medium-dark skin tone',
	u'skull', u'person tipping hand', u'OK hand: medium-dark skin tone',
	u'hugging face'],
	'curse_rate_s1':2.568,
	'curse_rate_s2':1.023,
	'laugh_rate_s1':19.323,
	'laugh_rate_s2':7.99,
	'big_words_rate_s1':None,
	'big_words_rate_s2':None,
	'longest_streak':17,
	'longest_drought':7.013,
	'punctuation_s1':None,
	'punctuation_s2':None,
	'link_rate_s1':1.182,
	'link_rate_s2':0.568
	}

	time_metrics = {
	'most_active_day_of_week':'Tuesday',
	'least_active_day_of_week':'Thursday',
	'most_active_month_of_year':'February',
	'least_active_month_of_year':'May',
	'most_active_hour_of_day':'14',
	'least_active_hour_of_day':'24',
	}
```




