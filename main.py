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
#module imports
from src.convo_objects.TextEquivalent import TextEquivalent
from src.calc_engine import metric_calculations as mc 
from src.read_parse import read_and_parse_text_file
from src.calc_engine import filter_poly as fil
from src.utilities import utils
from src.data_viz.visualize import create_volume_trends, create_time_trends
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

import bokeh.plotting as bkp
from bokeh.models import DatetimeTickFormatter
from bokeh.charts import Bar, output_file, show
import pandas as pd
from bokeh.sampledata.autompg import autompg as df

# print(str(df))

# p = Bar(df, label='yr', values='mpg', agg='median', group='origin',
#         title="Median MPG by YR, grouped by ORIGIN", legend='top_right')

# output_file("bar.html")

# show(p)
#########
#Read
#########
working_dir = os.getcwd()
data_folder = working_dir + os.sep + "data" 
text_file_name = "anon_convo.txt"
full_path = data_folder + os.sep + text_file_name



block_t_in_sec = 90
full_tes = read_and_parse_text_file(full_path,block_t_in_sec)
filt = fil.filter_by_day_of_week([1,2,3,4,5,6,7],full_tes)['filtered_tes']
#print(str(len(filt)))
r = mc.calculate_all_metrics(full_tes)

ub = utils.UtilityBoss()

# print('top 5 emojis S2 before converting to names: ' + str(r['top_5_emojis_s2']))
# print('top 5 emojis S1 before converting to names: ' + str(r['top_5_emojis_s1']))

s1_emojis = [ub.convert_emoji_code(code) for code in r['top_5_emojis_s1']]
s2_emojis = [ub.convert_emoji_code(code) for code in r['top_5_emojis_s2']]

r['top_5_emojis_s1'] = s1_emojis
r['top_5_emojis_s2'] = s2_emojis


#r2 = mc.calc_most_least_active_times(full_tes)
print(str(r))
#print(str(r2))


zz = create_volume_trends(full_tes)

zzz = create_time_trends(full_tes)


p_waits = Bar(zzz['hours_df'],label='hour_x',group='participant',values='hour_y',
	title='Wait Times By Participant in Conversation',legend='top_right')
bkp.show(p_waits)
# plt.bar(mdates.num2date(zz['x_ticks']),zz['y_vals'])
# plt.grid(b=True)
# plt.ylabel('Number of Texts Sent')
# plt.show()

plot = bkp.figure(plot_width=500,plot_height=500)
plot.xaxis.formatter=DatetimeTickFormatter(
        hours=["%d %B %Y"],
        days=["%d %B %Y"],
        months=["%d %B %Y"],
        years=["%d %B %Y"],
    )
plot.xaxis.major_label_orientation = pi/4
plot.vbar(x=mdates.num2date(zz['x_ticks']),top=zz['cumsum'],width=0.1)
bkp.show(plot)

# plt.bar(mdates.num2date(zz['x_ticks']),zz['cumsum'])
# plt.grid(b=True)
# plt.ylabel('Cumulative Number of Texts Sent')
# plt.show()


