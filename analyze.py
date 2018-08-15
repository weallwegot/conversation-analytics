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
# from src.data_viz.visualize import create_volume_trends, create_time_trends
# from src.data_viz.visualize import create_chrono_time_trends_all_calcs



block_t_in_sec = 90

def analyze_text_conversation(full_abs_path):
	full_tes = read_and_parse_text_file(full_abs_path,block_t_in_sec)
	r = mc.calculate_all_metrics(full_tes)
	###################################
	##   Convert Emoji To Readable   ##
	###################################
	ub = utils.UtilityBoss()


	s1_emojis = [ub.convert_emoji_code(code) for code in r['top_emojis_s1']]
	s2_emojis = [ub.convert_emoji_code(code) for code in r['top_emojis_s2']]

	r['top_emojis_s1'] = s1_emojis
	r['top_emojis_s2'] = s2_emojis

	return r