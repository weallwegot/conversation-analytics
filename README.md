[![Build Status](https://travis-ci.org/weAllWeGot/conversation-analytics.svg?branch=master)](https://travis-ci.org/weAllWeGot/conversation-analytics)

[![Coverage Status](https://coveralls.io/repos/github/weAllWeGot/conversation-analytics/badge.svg?branch=master)](https://coveralls.io/github/weAllWeGot/conversation-analytics?branch=master)



# conversation-analytics
understand social dynamics in a two-way conversation, have hard data to back up your intuition about your relationships.

For more details on the projects,  check out [the wiki pages](https://github.com/weAllWeGot/conversation-analytics/wiki).

obtain your text conversations as .txt by
running the shell script in [this project, titled Baskup](https://github.com/PeterKaminski09/baskup) .
If you want to access the visualization (you do) then you will need bokeh and its dependencies:
- NumPy
- Jinja2
- Six
- Requests
- Tornado >= 4.0
- PyYaml
- DateUtil
- Bokeh

This is best done if you have conda installed and can be done with the simple command:
`conda install bokeh`


# sample data output
s1 & s2 denote different conversations participants.
For more in depth explanations of the calculations & assumptions, see [the wiki pages](https://github.com/weAllWeGot/conversation-analytics/wiki).
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
	'top_emojis_s1':[u'thinking face', u'face with rolling eyes',
	u'person shrugging: dark skin tone', u'person shrugging',
	u'pensive face', u'weary face', u'face with tears of joy',
	u'smiling face with smiling eyes', u'hugging face', u'eyes'],
	'top_emojis_s2':[u'weary face', u'face with tears of joy',
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



   curse_rate      day_x  double_text_rate  emoji_rate  laugh_rate  link_rate  participant  wait_time 
0    2.205882     Monday          7.352941    5.147059   22.058824   1.838235           Me       65.0
1    3.341289    Tuesday          4.057279    5.250597   19.570406   0.954654           Me       20.0
2    1.861702  Wednesday          9.042553    4.521277   19.680851   0.531915           Me       37.0
3    1.219512   Thursday         11.382114    5.284553   14.634146   0.406504           Me       44.0
4    3.546099     Friday          5.673759    5.437352   19.385343   1.891253           Me       22.0
5    1.225490   Saturday          8.333333    6.127451   18.382353   0.735294           Me       38.5
6    4.207120     Sunday          7.119741    3.236246   21.035599   1.941748           Me       38.0
0    0.000000     Monday         15.719064    3.344482    7.023411   1.337793       Friend       32.5
1    0.852878    Tuesday         14.285714    5.330490    7.889126   0.213220       Friend       14.0
2    0.771208  Wednesday         11.825193    3.598972    7.712082   0.514139       Friend       20.0
3    1.127820   Thursday         17.669173    2.631579    9.398496   0.000000       Friend       30.0
4    1.098901     Friday         12.307692    3.516484    7.252747   1.318681       Friend       21.0
5    0.909091   Saturday         14.772727    2.954545    6.136364   0.454545       Friend       28.0
6    2.500000     Sunday         10.625000    2.812500   11.875000   0.000000       Friend       18.0 

```




