
#from matplotlib import dates as mdates
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import datetime
import numpy as np

def create_tuples(tes_list):
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
	bin_indices_of_time = np.digitize(all_stamps,time_axis) #index that each time belongs to
	"""
	each position in list is a tick of tine
	the value for a given index is the number of text equivalent timestamps
	that occurred in that bin
	thus it is also the count of how many texts were sent in that time tick
	so if time axis last argument is 1.0/24.0 (assuming mdates.date2num ticks)
	then the tick = 1 hour (or a 24th of a day)
	NOTE: that last argument will change if we go to UNIX timestamps 
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

	cum_sum_texts = np.cumsum(y_vals)

	return({'cumsum':cum_sum_texts,'x_ticks':x_ticks,'y_vals':y_vals})

	#plt.bar(mdates.num2date(x_ticks),y_vals)




