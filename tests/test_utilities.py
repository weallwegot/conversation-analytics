# -*- coding: utf-8 -*- 

# This Python file uses the following encoding: utf-8
import unittest

import os
import datetime
import sys
from src.convo_objects.TextEquivalent import TextEquivalent 
from src.read_parse import read_and_parse_text_file
from src.calc_engine.metric_calculations import calc_time_between_text_equivalents
from src.calc_engine.metric_calculations import calc_length_text_equivalent
from src.calc_engine.metric_calculations import calculate_all_metrics
from src.calc_engine.metric_calculations import calc_laugh,calc_curse,calc_link,calc_emoji
from src.calc_engine.metric_calculations import calc_most_least_active_times
from src.utilities import utils as u

reload(sys)
sys.setdefaultencoding('utf-8')


"""
this test will make sure that the logic 
for recognizing courses is working correctly
on the basis of acronyms, names, numbers, cs xxxx, and csxxxx

"""


class TestUtilities(unittest.TestCase):

	def setUp(self):
		working_dir = os.path.dirname(os.path.abspath(__file__))
		data_folder = working_dir + os.sep + "test_data" 


	def test_day_of_week_convert(self):
		self.assertEquals(u.display_weekday('1'),'Monday')
		self.assertEquals(u.display_weekday('2'),'Tuesday')
		self.assertEquals(u.display_weekday('3'),'Wednesday')
		self.assertEquals(u.display_weekday('4'),'Thursday')
		self.assertEquals(u.display_weekday('5'),'Friday')
		self.assertEquals(u.display_weekday('6'),'Saturday')
		self.assertEquals(u.display_weekday('7'),'Sunday')

	def test_emoji_convert(self):
		w = u.UtilityBoss()
		name = w.convert_emoji_code(u'\U0001f629')
		code = w.convert_emoji_name('weary face')
		self.assertEquals(name,'weary face')
		self.assertEquals(code,u'U+1F629')
		self.assertEquals(w.convert_emoji_name('nonsense'),'NA')
		self.assertEquals(w.convert_emoji_code('nonsense'),'NA')


