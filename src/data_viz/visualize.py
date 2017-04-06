
import pandas.DataFrame 
from src.calc_engine import metric_calculations,filter_poly
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import datetime
import numpy as np
from src.utilities.utils import display_weekday


def create_volume_trends(tes_list):
	#find integer of first day and last day (can use mdates in matplotlib)
	#or timestamp in UNIX time
	#partition into bins on a per hour basis
	#if TextEquivalent is between the bins add to count
	#similar approach can be used for response time trending
	#or to do the full metric calculation on all of the TextEqu. that fall in the bin
	#checkout numpy and cumsum()
	"""
	http://stackoverflow.com/questions/3034162/plotting-a-cumulative-graph-of-python-datetimes
	http://stackoverflow.com/questions/37293014/draw-a-cumulative-chart-from-a-pandas-dataframe
	https://docs.scipy.org/doc/numpy/reference/generated/numpy.cumsum.html
	"""
	daily_text_eqs = {}
	start_num = mdates.date2num(tes_list[0].timestamp)
	end_num = mdates.date2num(tes_list[-1].timestamp)
	"""
	how long is a tick (in mdates date2num units)
	1 hour bins (float division)
	"""
	tick_quant = (1.0/24.0) 
	time_axis = np.arange(start_num,end_num,tick_quant) 
	all_stamps = [mdates.date2num(te.timestamp) for te in tes_list]
	"""
	#time_axis are the bins.
	#qll_stamps are the timestamps for ever Text Equivalent
	#np.digitize will place each timestamp into a bin the value of each elemnt
	"""
	bin_indices_of_time = np.digitize(all_stamps,time_axis) 

	"""
	each position in list is a tick of tine
	the value for a given index is the number of text equivalent timestamps
	that occurred in that bin
	thus it is also the count of how many texts were sent in that time tick
	so if time axis last argument is 1.0/24.0 (assuming mdates.date2num ticks)
	then the tick = 1 hour (or a 24th of a day)
	NOTE: that last argument will change if we go to UNIX timestamps 
	np.bincount() will return a list that
	corresponds to the number of timestamps that fell into that bin.
	[33, 2, 21] means 33 timestamps in first bin. 2 timestamps in 2nd bin. 21 timestamps in 3rd bin
	"""
	bincounts = np.bincount(bin_indices_of_time) 
	# initialize list to hold (x,y) pairs (date_as_number,number_of_texts_sent)
	# makes this cumsummable easily np.cumsum()
	tuples_list = []
	x_ticks = []
	y_vals = []
	# convert the indices of the bincounts array to datetimes.
	for index in range(0,len(bincounts)):
		number_of_texts_sent_this_tick = bincounts[index]
		index_2_num = index*tick_quant+start_num
		#store as tuples
		tuples_list.append((index_2_num,number_of_texts_sent_this_tick))
		#store just the x values
		x_ticks.append(index_2_num)
		#store just the y values
		y_vals.append(number_of_texts_sent_this_tick)
	#cumulative summation
	cum_sum_texts = np.cumsum(y_vals)

	return({'cumsum':cum_sum_texts,'x_ticks':x_ticks,'y_vals':y_vals})

	#plt.bar(mdates.num2date(x_ticks),y_vals)

def give_me_everything(tes_list):
	a=tes_list
	# this is inefficient because its doing the same processing 
	# for each function call. refactor.
	return({'volume':create_volume_trends(a),
		    'response':create_response_time_trends(a),
		    'emoji':create_emoji_trends(a),
		    'laugh':create_laugh_trends(a),
		    'curse':create_curse_trends(a),
		    'link':create_link_trends(a),
		    'double text':create_double_text_trends(a)
		   })
"""
go through the calculation after dividing Text Equivalents into days of week
then again after dividing Text Equivalents into hours of day
create one dataframe with each variable as a column
"""
def create_time_trends(tes_list):
	# Do the days of the week
	days_of_week = range(1,8)
	wait_day_time_s1 = []
	wait_day_time_s2 = []
	emoji_day_s1 = []
	emoji_day_s2 = []
	laugh_day_s1 = []
	laugh_day_s2 = []
	curse_day_s1 = []
	curse_day_s2 = []
	link_day_s1 = []
	link_day_s2 = []
	double_day_s1 = []
	double_day_s2 = []
	for curr_day in days_of_week:
		day_tes = filter_poly.filter_by_day_of_week([curr_day],tes_list)['filtered_tes']
		day_calcs = metric_calculations.calculate_all_metrics(day_tes)
		wait_day_time_s1.append(day_calcs['response_rate_s1'])
		wait_day_time_s2.append(day_calcs['response_rate_s2'])
		emoji_day_s1.append(day_calcs['emoji_rate_s1'])
		emoji_day_s2.append(day_calcs['emoji_rate_s2'])
		laugh_day_s1.append(day_calcs['laugh_rate_s1'])
		laugh_day_s2.append(day_calcs['laugh_rate_s2'])
		curse_day_s1.append(day_calcs['curse_rate_s1'])
		curse_day_s2.append(day_calcs['curse_rate_s2'])
		link_day_s1.append(day_calcs['link_rate_s1'])
		link_day_s2.append(day_calcs['link_rate_s2'])
		double_day_s1.append(day_calcs['double_text_rate_s1'])
		double_day_s2.append(day_calcs['double_text_rate_s2'])

	day_of_week_words = [display_weekday(g) for g in days_of_week]



	# Do the hours of the day
	hours_of_day = range(1,25)
	wait_hr_time_s1 = []
	wait_hr_time_s2 = []
	emoji_hr_s1 = []
	emoji_hr_s2 = []
	laugh_hr_s1 = []
	laugh_hr_s2 = []
	curse_hr_s1 = []
	curse_hr_s2 = []
	link_hr_s1 = []
	link_hr_s2 = []
	double_hr_s1 = []
	double_hr_s2 = []
	for curr_hour in hours_of_day:
		hour_tes = filter_poly.filter_by_time_of_day([curr_hour],tes_list)['filtered_tes']
		hour_calcs = metric_calculations.calculate_all_metrics(hour_tes)
		wait_hr_time_s1.append(hour_calcs['response_rate_s1'])
		wait_hr_time_s2.append(hour_calcs['response_rate_s2'])
		emoji_hr_s1.append(hour_calcs['emoji_rate_s1'])
		emoji_hr_s2.append(hour_calcs['emoji_rate_s2'])
		laugh_hr_s1.append(hour_calcs['laugh_rate_s1'])
		laugh_hr_s2.append(hour_calcs['laugh_rate_s2'])
		curse_hr_s1.append(hour_calcs['curse_rate_s1'])
		curse_hr_s2.append(hour_calcs['curse_rate_s2'])
		link_hr_s1.append(hour_calcs['link_rate_s1'])
		link_hr_s2.append(hour_calcs['link_rate_s2'])
		double_hr_s1.append(hour_calcs['double_text_rate_s1'])
		double_hr_s2.append(hour_calcs['double_text_rate_s2'])



	hour_d_1 = {'hour_x':hours_of_day,
		'wait_time': wait_hr_time_s1,
		'emoji_rate':emoji_hr_s1,
		'laugh_rate':laugh_hr_s1,
		'curse_rate':curse_hr_s1,
		'link_rate':link_hr_s1,
		'double_text_rate':double_hr_s1,
		'participant': ['Me']*len(hours_of_day) }

	hour_d_2 = {'hour_x':hours_of_day,
		'wait_time': wait_hr_time_s2,
		'emoji_rate':emoji_hr_s2,
		'laugh_rate':laugh_hr_s2,
		'curse_rate':curse_hr_s2,
		'link_rate':link_hr_s2,
		'double_text_rate':double_hr_s2,
		'participant': ['Friend']*len(hours_of_day) 
		}

	df_hour = pd.DataFrame(hour_d_1)
	df_hour = df_hour.append(pd.DataFrame(hour_d_2))

	print(str(df_hour))

	day_d_1 =	{
		'day_x':day_of_week_words,
		'wait_time': wait_day_time_s1,
		'emoji_rate':emoji_day_s1,
		'laugh_rate':laugh_day_s1,
		'curse_rate':curse_day_s1,
		'link_rate':link_day_s1,
		'double_text_rate':double_day_s1,
		'participant':['Me']*len(day_of_week_words)
		}

	day_d_2 = {
		'day_x':day_of_week_words,
		'wait_time': wait_day_time_s2,
		'emoji_rate':emoji_day_s2,
		'laugh_rate':laugh_day_s2,
		'curse_rate':curse_day_s2,
		'link_rate':link_day_s2,
		'double_text_rate':double_day_s2,
		'participant':['Friend']*len(day_of_week_words)
		}

	df_day = pd.DataFrame(day_d_1)
	df_day = df_day.append(pd.DataFrame(day_d_2))
	print(str(df_day))


	return({'hours_df':df_hour,
			'days_df': df_day
			})

def create_emoji_trends(tes_list):



	return({})

def create_laugh_trends(tes_list):



	return({})

def create_curse_trends(tes_list):



	return({})

def create_link_trends(tes_list):



	return({})

def create_double_text_trends(tes_list):



	return({})




