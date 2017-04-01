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
#module imports
from src.convo_objects.TextEquivalent import TextEquivalent
from src.calc_engine import metric_calculations as mc 
from src.read_parse import read_and_parse_text_file
from src.calc_engine import filter_poly as fil
from src.utilities import utils


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

print('top 5 emojis S2 before converting to names: ' + str(r['top_5_emojis_s2']))
print('top 5 emojis S1 before converting to names: ' + str(r['top_5_emojis_s1']))

s1_emojis = [ub.convert_emoji_code(code) for code in r['top_5_emojis_s1']]
s2_emojis = [ub.convert_emoji_code(code) for code in r['top_5_emojis_s2']]

r['top_5_emojis_s1'] = s1_emojis
r['top_5_emojis_s2'] = s2_emojis


#r2 = mc.calc_most_least_active_times(full_tes)
print(str(r))
#print(str(r2))


