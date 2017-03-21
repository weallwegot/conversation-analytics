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
import datetime
import re
#module imports
from convo_objects.TextEquivalent import TextEquivalent
from calc_engine import metric_calculations as mc 
from read_parse import read_and_parse_text_file


#########
#Read
#########
working_dir = os.getcwd()
data_folder = working_dir + os.sep + os.pardir + os.sep + "data" 
text_file_name = "anon_convo.txt"
full_path = data_folder + os.sep + text_file_name



block_t_in_sec = 90
r = mc.calculate_all_metrics(read_and_parse_text_file(full_path,block_t_in_sec))
print(str(r))


