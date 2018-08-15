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
from math import pi
import uuid
#module imports
from src.convo_objects.TextEquivalent import TextEquivalent
from src.calc_engine import metric_calculations as mc 
from src.read_parse import read_and_parse_text_file
from src.calc_engine import filter_poly as fil
from src.utilities import utils
from src.data_viz.visualize import create_volume_trends, create_time_trends
from src.data_viz.visualize import create_chrono_time_trends_all_calcs
#plotting tings
import plotly.offline as py
import plotly.graph_objs as go

import pandas as pd

##############################
## Assign UUID to Analysis  ##
##############################

analysis_id = str(uuid.uuid4())

###########################
## Read Data From File   ##
###########################
working_dir = os.getcwd()
data_folder = working_dir + os.sep + "data" 
text_file_name = "anon_convo.txt"
text_file_name = "ebunoluwa.txt"
full_path = data_folder + os.sep + text_file_name

###########################
## Parse Data From File  ##
###########################

block_t_in_sec = 25
full_tes = read_and_parse_text_file(full_path,block_t_in_sec)
filt = fil.filter_by_day_of_week([1,2,3,4,5,6,7],full_tes)['filtered_tes']

###########################
## Calc Data From File  ##
###########################


r = mc.calculate_all_metrics(full_tes)

###################################
##   Convert Emoji To Readable   ##
###################################
ub = utils.UtilityBoss()


s1_emojis = [ub.convert_emoji_code(code) for code in r['top_emojis_s1']]
s2_emojis = [ub.convert_emoji_code(code) for code in r['top_emojis_s2']]

r['top_emojis_s1'] = s1_emojis
r['top_emojis_s2'] = s2_emojis


#r2 = mc.calc_most_least_active_times(full_tes)
print(str(r))

#convert r to dataframe
#write dataframe to csv

# the 2nd argument is for the length of the bins in the plot (in days)
# calculates how many texts were sent over time. cumulatively
CUMULATIVE_TEXT_DAY_BIN = 1.0
zz = create_volume_trends(full_tes,CUMULATIVE_TEXT_DAY_BIN)

# calculates data on the basis of hours and days of the week
zzz = create_time_trends(full_tes)

# the 2nd argument is for the length of the bins in the plot (in days).
# creates long term trends for all the metrics.
noice = create_chrono_time_trends_all_calcs(full_tes,2.0)

# output_file("main.html")

print(str(zzz['hours_df']))

print(str(zzz['days_df']))

# write id to text file
target = open('my_info.txt','w')
target.write("Your unique ID is: " + analysis_id)
target.close()

# write resulting data to csvs
noice.to_csv('time_trends_.csv')

pd.DataFrame.from_dict(r).to_csv('metric_calc_.csv')

zzz['hours_df'].to_csv('hours_df_.csv')

zzz['days_df'].to_csv('days_df_.csv')




"""
All the plots below are the metrics as they
are calculated over time in chronological order
they display how your texting behavior and that of your partner
change over the life of your texting conversations
"""


def newvbar(data,label,group,values,title,legend,ylabel,width=0.05):
	return
	plc = figure()

	data1 = data[data["participant"] == "Me"]
	data2 = data[data["participant"] == "Friend"]

	trace1 = go.Bar(x=data1[label],y=data1[values],name="Me")
	trace2 = go.Bar(x=data2[label],y=data2[values],name="Friend")
	bardata = [trace1,trace2]
	
	layout = go.Layout(
		barmode='group',
		title=title,
		yaxis=dict(
			title=ylabel
		)
	)

	fig = go.Figure(data=bardata,layout=layout)
	py.plot(fig)

	# fig = plc.vbar(x=data[label],width=width,top=data[values],group=group,legend=legend,ylabel=ylabel,title=title)

	# return fig

def non_comparative_bar(dataframe,xlabel,ylabel,title,width=0.05):
	plc = figure()

	data = [go.Bar(
	            x=dataframe[xlabel],
	            y=dataframe[ylabel]
	    )]

	layout = go.Layout(title=title,
					   yaxis=dict(
					   	title=ylabel)
					   )

	fig = go.Figure(data=data,layout = layout)
	py.plot(fig)


p_waits_cumulative = newvbar(data=noice,label='x_ticks',group='participant',values='wait_time',
	title='Wait Times Over Time',legend='top_right',ylabel='Wait Time (sec)')

p_emoji_cumulative = newvbar(data=noice,label='x_ticks',group='participant',values='emoji_rate',
	title='Emoji Rate Over Time',legend='top_right',ylabel='Emoji Rate (%)')


p_laugh_cumulative = newvbar(data=noice,label='x_ticks',group='participant',values='laugh_rate',
	title='Laugh Rate (%) Over Time',legend='top_right',ylabel='Laugh Rate (%)')


p_dt_cumulative = newvbar(data=noice,label='x_ticks',group='participant',values='double_text_rate',
	title='Double Text Rate (%) Over Time',legend='top_right',ylabel='Double Text Rate (%)')


p_link_cumulative = newvbar(data=noice,label='x_ticks',group='participant',values='link_rate',
	title='Link Rate (%) Over Time',legend='top_right',ylabel='Link Rate (%)')



p_curse_cumulative = newvbar(data=noice,label='x_ticks',group='participant',values='curse_rate',
	title='Curse Rate (%) Over Time',legend='top_right',ylabel='Curse Rate (%)')


"""
All the plots below are the ones that are broken down by day of week
and by the hour of the day
"""


p_vol_hr = newvbar(data=zzz['hours_df'],label='hour_x',group='participant',values='texts_sent',
	title='Number of Texts Sent By Time of Day',legend='top_right',ylabel='Number of Texts Sent')


p_vol_day = newvbar(data=zzz['days_df'],label='day_x',group='participant',values='texts_sent',
	title='Number of Texts Sent By Day of Week',legend='top_right',ylabel='Number of Texts Sent')


p_waits_hr = newvbar(data=zzz['hours_df'],label='hour_x',group='participant',values='wait_time',
	title='Wait Times By Time of Day',legend='top_right',ylabel='Wait Time (sec)')


p_waits_day = newvbar(data=zzz['days_df'],label='day_x',group='participant',values='wait_time',
	title='Wait Times By Day of Week',legend='top_right',ylabel='Wait Time (sec)')


p_emoji_hr = newvbar(data=zzz['hours_df'],label='hour_x',group='participant',values='emoji_rate',
	title='Emoji Rate By Time of Day',legend='top_right',ylabel='Emoji Rate (%)')


p_emoji_day = newvbar(data=zzz['days_df'],label='day_x',group='participant',values='emoji_rate',
	title='Emoji Rate By Day of Week',legend='top_right',ylabel='Emoji Rate (%)')


p_laugh_hr = newvbar(data=zzz['hours_df'],label='hour_x',group='participant',values='laugh_rate',
	title='Laugh Rate (%) By Time of Day',legend='top_right',ylabel='Laugh Rate (%)')


p_laugh_day = newvbar(data=zzz['days_df'],label='day_x',group='participant',values='laugh_rate',
	title='Laugh Rate (%) By Day of Week',legend='top_right',ylabel='Laugh Rate (%)')


p_dt_hr = newvbar(data=zzz['hours_df'],label='hour_x',group='participant',values='double_text_rate',
	title='Double Text Rate (%) By Time of Day',legend='top_right',ylabel='Double Text Rate (%)')



p_dt_day = newvbar(data=zzz['days_df'],label='day_x',group='participant',values='double_text_rate',
	title='Double Text Rate (%) By Day of Week',legend='top_right',ylabel='Double Text Rate (%)')



p_link_hr = newvbar(data=zzz['hours_df'],label='hour_x',group='participant',values='link_rate',
	title='Link Rate (%) By Time of Day',legend='top_right',ylabel='Link Rate (%)')



p_link_day = newvbar(data=zzz['days_df'],label='day_x',group='participant',values='link_rate',
	title='Link Rate (%) By Day of Week',legend='top_right',ylabel='Link Rate (%)')



p_curse_hr = newvbar(data=zzz['hours_df'],label='hour_x',group='participant',values='curse_rate',
	title='Curse Rate (%) By Time of Day',legend='top_right',ylabel='Curse Rate (%)')



p_curse_day = newvbar(data=zzz['days_df'],label='day_x',group='participant',values='curse_rate',
	title='Curse Rate (%) By Day of Week',legend='top_right',ylabel='Curse Rate (%)')

"""
The two plots below are cumulatives as well for number of texts sent
they are separate because the algorithm for calculating them is different
"""

p_cumulative_texts_sent = non_comparative_bar(dataframe=zz,xlabel='x_ticks',ylabel='cumsum',
	title='Number of Text Equivalents Over Time',width=0.025)

p_texts_per_day_bin = non_comparative_bar(dataframe=zz,xlabel='x_ticks',ylabel='y_vals',
	title='Number of Texts Per {} Day Period'.format(CUMULATIVE_TEXT_DAY_BIN), width=0.025)
