
import pandas as pd
from src.calc_engine import metric_calculations,filter_poly
import matplotlib.dates as mdates
import datetime
import numpy as np
from src.utilities.utils import display_weekday, UtilityBoss
# used to make sure time zones are both naive or aware for comparison filtering
import pytz



"""
go through the calculation for wait time but binned in successive time buckets
so we can see how the trend is over the life of the texting relationship
"""
def create_chrono_time_trends_all_calcs(tes_list,tickquant_days):
	#http://stackoverflow.com/questions/15307623/cant-compare-naive-and-aware-datetime-now-challenge-datetime-end
	utc = pytz.UTC
	# needed to convert emoji codes to names
	ub = UtilityBoss()
	start_num = (tes_list[0].timestamp.replace(tzinfo=utc))
	end_num = (tes_list[-1].timestamp.replace(tzinfo=utc))
	"""
	ticks of time are defined here
	"""	
	tick_quant = datetime.timedelta(days=tickquant_days)
	time_axis = np.arange(start_num,end_num,tick_quant) 
	# all_stamps = [te.timestamp for te in tes_list]

	"""
	#time_axis are the bins.
	#all_stamps are the timestamps for every Text Equivalent
	#np.digitize will place each timestamp into a bin the value of each elemnt
	"""
	# bin_indices_of_time = np.digitize(all_stamps,time_axis) 
	# i actually dont think this is what you want... 

	# might have to loop thru. :weary-face: 
	wait_ticks_time_s1 = []
	wait_ticks_time_s2 = []
	emoji_ticks_s1 = []
	emoji_ticks_s2 = []
	laugh_ticks_s1 = []
	laugh_ticks_s2 = []
	curse_ticks_s1 = []
	curse_ticks_s2 = []
	link_ticks_s1 = []
	link_ticks_s2 = []
	double_ticks_s1 = []
	double_ticks_s2 = []
	top_ems_ticks_s1 = []
	top_ems_ticks_s2 = []
	volume_ticks_s1 = []
	volume_ticks_s2 = []
	ticks_as_dates = []
	for i in range(0,len(time_axis)-1):
		# filter on "between time_axis[i] and time_axis[i+1]"
		# issue here is that the function for fitlereing timestamps as "in between"
		# takes as an input the times as datetime.datetime objects.
		early = (time_axis[i])
		late = (time_axis[i+1])
		tes_for_current_time_block = filter_poly.filter_by_date_range(early,late,tes_list)['filtered_tes']
		ticks_calcs = metric_calculations.calculate_all_metrics(tes_for_current_time_block)
		wait_ticks_time_s1.append(ticks_calcs['response_rate_s1'])
		wait_ticks_time_s2.append(ticks_calcs['response_rate_s2'])
		emoji_ticks_s1.append(ticks_calcs['emoji_rate_s1'])
		emoji_ticks_s2.append(ticks_calcs['emoji_rate_s2'])
		laugh_ticks_s1.append(ticks_calcs['laugh_rate_s1'])
		laugh_ticks_s2.append(ticks_calcs['laugh_rate_s2'])
		curse_ticks_s1.append(ticks_calcs['curse_rate_s1'])
		curse_ticks_s2.append(ticks_calcs['curse_rate_s2'])
		link_ticks_s1.append(ticks_calcs['link_rate_s1'])
		link_ticks_s2.append(ticks_calcs['link_rate_s2'])
		double_ticks_s1.append(ticks_calcs['double_text_rate_s1'])
		double_ticks_s2.append(ticks_calcs['double_text_rate_s2'])
		volume_ticks_s1.append(ticks_calcs['texts_sent_s1'])
		volume_ticks_s2.append(ticks_calcs['texts_sent_s2'])
		if ticks_calcs['top_emojis_s1']:
			ticks_s1_emojis = [ub.convert_emoji_code(code) for code in ticks_calcs['top_emojis_s1']]
			top_ems_ticks_s1.append(ticks_s1_emojis)
		else:
			top_ems_ticks_s1.append([])
		if ticks_calcs['top_emojis_s2']:
			ticks_s2_emojis = [ub.convert_emoji_code(code) for code in ticks_calcs['top_emojis_s2']]
			top_ems_ticks_s2.append(ticks_s2_emojis)
		else:
			top_ems_ticks_s2.append([])
		try:
			ticks_as_dates.append(early.replace(tzinfo=utc))
		except AttributeError:
			# this is for the case where np datetime 64 is used instead of datetime
			ticks_as_dates.append(early)
		#ticks_as_dates.append(late)

	#cumulative totals for participant 1
	dict_cum_1 =	{'x_ticks':time_axis[:-1],
		'date_ticks':ticks_as_dates,
		'wait_time': wait_ticks_time_s1,
		'emoji_rate':emoji_ticks_s1,
		'laugh_rate':laugh_ticks_s1,
		'curse_rate':curse_ticks_s1,
		'link_rate':link_ticks_s1,
		'double_text_rate':double_ticks_s1,
		'top_emojis':top_ems_ticks_s1,
		'texts_sent':volume_ticks_s1,
		'participant':['Me']*(len(time_axis)-1)
		}
	#cumulative totals for participant 2
	dict_cum_2 = {'x_ticks':time_axis[:-1],
		'date_ticks':ticks_as_dates,
		'wait_time': wait_ticks_time_s2,
		'emoji_rate':emoji_ticks_s2,
		'laugh_rate':laugh_ticks_s2,
		'curse_rate':curse_ticks_s2,
		'link_rate':link_ticks_s2,
		'double_text_rate':double_ticks_s2,
		'top_emojis':top_ems_ticks_s2,
		'texts_sent':volume_ticks_s2,
		'participant':['Friend']*(len(time_axis)-1)
		}
	#append the data frames for both participants
	df_cum = pd.DataFrame(dict_cum_1)
	df_cum = df_cum.append(pd.DataFrame(dict_cum_2))
	return(df_cum)


def create_volume_trends(tes_list,tickquant_days):
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

	def _convert_to_unix_time(tstamp):
		unix_epoch = np.datetime64(0,'s')
		one_second = np.timedelta64(1,'s')
		unix_time = (np.datetime64(tstamp) - unix_epoch)/one_second
		return unix_time

	daily_text_eqs = {}
	start_num = np.datetime64(tes_list[0].timestamp)
	end_num = np.datetime64(tes_list[-1].timestamp)
	"""
	how long is a tick (in mdates date2num units)
	1 hour bins (float division) -> this is too short
	5 day long bins
	"""
	tick_quant = datetime.timedelta(days=tickquant_days) 
	time_axis = np.arange(start_num,end_num,tick_quant) 
	all_stamps = [_convert_to_unix_time(te.timestamp) for te in tes_list]
	time_axis = [_convert_to_unix_time(tick) for tick in time_axis]
	"""
	#time_axis are the bins.
	#all_stamps are the timestamps for every Text Equivalent
	#np.digitize will place each timestamp into a bin the value of each elemnt
	"""
	bin_indices_of_time = np.digitize(all_stamps,time_axis) 

	"""
	each position in list is a tick of time
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
		#convert the index into an equivalent time
		try:
			index_2_num = index*tick_quant+start_num
		except TypeError:
			# catch inconsistent datetimes np.datetime64 vs datetime.datetime vs timedelta vs np.timedelta64
			index_2_num = np.timedelta64(index*tick_quant) + np.datetime64(start_num)

		#store as tuples
		tuples_list.append((index_2_num,number_of_texts_sent_this_tick))
		#store just the x values
		x_ticks.append(index_2_num)
		#store just the y values
		y_vals.append(number_of_texts_sent_this_tick)
	#cumulative summation
	cum_sum_texts = np.cumsum(y_vals)

	return({'cumsum':cum_sum_texts,'x_ticks':x_ticks,'y_vals':y_vals})

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
	top_ems_day_s1 = []
	top_ems_day_s2 = []
	volume_day_s1 = []
	volume_day_s2 = []
	# needed to convert emoji codes to names
	ub = UtilityBoss()
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
		volume_day_s1.append(day_calcs['texts_sent_s1'])
		volume_day_s2.append(day_calcs['texts_sent_s2'])
		if day_calcs['top_emojis_s1']:
			day_s1_emojis = [ub.convert_emoji_code(code) for code in day_calcs['top_emojis_s1']]
			top_ems_day_s1.append(day_s1_emojis)
		else:
			top_ems_day_s1.append([])
		if day_calcs['top_emojis_s2']:
			day_s2_emojis = [ub.convert_emoji_code(code) for code in day_calcs['top_emojis_s2']]
			top_ems_day_s2.append(day_s2_emojis)
		else:
			top_ems_day_s2.append([])




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
	top_ems_hr_s1 = []
	top_ems_hr_s2 = []
	volume_hr_s1 = []
	volume_hr_s2 = []
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
		volume_hr_s1.append(hour_calcs['texts_sent_s1'])
		volume_hr_s2.append(hour_calcs['texts_sent_s2'])
		if hour_calcs['top_emojis_s1']:	
			hr_s1_emojis = [ub.convert_emoji_code(code) for code in hour_calcs['top_emojis_s1']]
			top_ems_hr_s1.append(hr_s1_emojis)
		else:
			top_ems_hr_s1.append([])
		if hour_calcs['top_emojis_s2']:
			hr_s2_emojis = [ub.convert_emoji_code(code) for code in hour_calcs['top_emojis_s2']]
			top_ems_hr_s2.append(hr_s2_emojis)
		else:
			top_ems_hr_s2.append([])

	# do some conversions using utilities functions for visualizations



	day_of_week_words = [display_weekday(g) for g in days_of_week]


	hour_d_1 = {'hour_x':hours_of_day,
		'wait_time': wait_hr_time_s1,
		'emoji_rate':emoji_hr_s1,
		'laugh_rate':laugh_hr_s1,
		'curse_rate':curse_hr_s1,
		'link_rate':link_hr_s1,
		'double_text_rate':double_hr_s1,
		'top_emojis':top_ems_hr_s1,
		'texts_sent':volume_hr_s1,
		'participant': ['Me']*len(hours_of_day) }

	hour_d_2 = {'hour_x':hours_of_day,
		'wait_time': wait_hr_time_s2,
		'emoji_rate':emoji_hr_s2,
		'laugh_rate':laugh_hr_s2,
		'curse_rate':curse_hr_s2,
		'link_rate':link_hr_s2,
		'double_text_rate':double_hr_s2,
		'top_emojis':top_ems_hr_s2,
		'texts_sent':volume_hr_s2,
		'participant': ['Friend']*len(hours_of_day) 
		}
	#append the data frames for both participants
	df_hour = pd.DataFrame(hour_d_1)
	df_hour = df_hour.append(pd.DataFrame(hour_d_2))

	day_d_1 =	{
		'day_x':day_of_week_words,
		'wait_time': wait_day_time_s1,
		'emoji_rate':emoji_day_s1,
		'laugh_rate':laugh_day_s1,
		'curse_rate':curse_day_s1,
		'link_rate':link_day_s1,
		'double_text_rate':double_day_s1,
		'top_emojis':top_ems_day_s1,
		'texts_sent':volume_day_s1,
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
		'top_emojis':top_ems_day_s2,
		'texts_sent':volume_day_s2,
		'participant':['Friend']*len(day_of_week_words)
		}
	#append the data frames for both participants
	df_day = pd.DataFrame(day_d_1)
	df_day = df_day.append(pd.DataFrame(day_d_2))


	return({'hours_df':df_hour,
			'days_df': df_day
			})






