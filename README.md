[![Build Status](https://travis-ci.org/weAllWeGot/conversation-analytics.svg?branch=master)](https://travis-ci.org/weAllWeGot/conversation-analytics)

[![Coverage Status](https://coveralls.io/repos/github/weAllWeGot/conversation-analytics/badge.svg?branch=master)](https://coveralls.io/github/weAllWeGot/conversation-analytics?branch=master)



# conversation-analytics
understand social dynamics in a two-way conversation

# preliminary output
s1 & s2 denote different conversations participants.
```python
# response rates are in seconds
	# the first is a median, the other is an average
# double text rates are percentage of texts sent
# longest streak is consecutive days talking
# longest drought is consecutive days no talking

# average length is number of words
	master_metrics = {
	'texts_sent_s1':2453,
	'texts_sent_s2':2638,
	'response_rate_s1':22.0,
	'response_rate_s2':33.0,
	'response_rate_mean_s1':None,
	'response_rate_mean_s2':None,
	'double_text_rate_s1':7.17,
	'double_text_rate_s2':13.68,
	'emoji_rate_s1':None,
	'emoji_rate_s2':None,
	'average_length_s1':11.06,
	'average_length_s2':8.97,
	'top_5_emojis_s1':None,
	'top_5_emojis_s2':None,
	'curse_rate_s1':None,
	'curse_rate_s2':None,
	'laugh_rate_s1':19.323,
	'laugh_rate_s2':7.99,
	'big_words_rate_s1':None,
	'big_words_rate_s2':None,
	'longest_steak':None,
	'longest_drought':None,
	'punctuation_s1':None,
	'punctuation_s2':None,
	'link_rate_s1':None,
	'link_rate_s2':None
	}
```


# Future
- gather people's conversational data, with a relationship outcome
- binary classification w/ logistic regression 
- can we predict future relationship status/health ?
- MLE gradient descent
- Front end with web application to make visualization fun & pretty
