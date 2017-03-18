
import unittest

import os
import datetime
from src.convo_objects.TextEquivalent import TextEquivalent 
from src.read_parse import read_and_parse_text_file
from src.metric_calculations import calc_time_between_text_equivalents
from src.metric_calculations import calc_length_text_equivalent
from src.metric_calculations import calculate_all_metrics




"""
this test will make sure that the logic 
for recognizing courses is working correctly
on the basis of acronyms, names, numbers, cs xxxx, and csxxxx

"""


class TestMetricCalculations(unittest.TestCase):

	def setUp(self):
		#self.te = TextEquivalent()
		working_dir = os.path.dirname(os.path.abspath(__file__))
		data_folder = working_dir + os.sep + "test_data" 
		text_file_name = "TestData.txt"
		full_path = data_folder + os.sep + text_file_name
		self.text_eqs = read_and_parse_text_file(full_path,0) 
		self.te1 = TextEquivalent("Me","2016-08-06 15:11:44","Hi")
		self.te2 = TextEquivalent("Friend","2016-08-06 15:13:44","Wassup")
		te3 = TextEquivalent("Me","2016-08-06 15:15:44","how are you")
		te4 = TextEquivalent("Friend","2016-08-06 15:17:44","gooood")
		self.tes = [self.te1,self.te2,te3,te4]
		#te1.merge_sequential_text_equiv(te2)
		#self.merged_te = te1



	def test_metric_test_equivalent(self):
		#the first timestamp just for reference
		#2016-08-06 15:11:44
		te1 = TextEquivalent("Me","2016-08-06 15:11:44","Hi",)
		te2 = TextEquivalent("You","2016-08-06 15:13:44","Wassup")
		time_dict = calc_time_between_text_equivalents(te1,te2)
		time_dict['time diff'] = 120
		self.assertEquals(time_dict['time diff'],120,"time elapsed is wrong")
		self.assertEquals(time_dict['sender'],"Me","sender is wrong")
		self.assertEquals(time_dict['responder'],"You","receiver is wrong")
		self.assertEquals(time_dict['double text'],False,"double text is wrong")

	def test_metric_test_double_text(self):
		#the first timestamp just for reference
		#2016-08-06 15:11:44
		te1 = TextEquivalent("Me","2016-08-06 15:11:44","Hi",)
		te2 = TextEquivalent("Me","2016-08-06 15:13:44","Wassup")
		time_dict = calc_time_between_text_equivalents(te1,te2)
		self.assertEquals(time_dict['double text'],True,"double text is wrong")
	def test_metric_test_length(self):
		#the first timestamp just for reference
		#2016-08-06 15:11:44
		te1 = TextEquivalent("Me","2016-08-06 15:11:44","Hi",)
		te2 = TextEquivalent("Me","2016-08-06 15:13:44","Wassup")
		time_dict = calc_length_text_equivalent(te1)
		self.assertEquals(time_dict['length'],2,"length is wrong")
	def test_metric_end_to_end_response_rate(self):
		total_dict = calculate_all_metrics(self.tes)
		self.assertEquals(total_dict['response_rate_s1'],120.0,
			"response rate is wrong")
	def test_metric_end_to_end_double_text_rate(self):
		total_dict = calculate_all_metrics(self.tes)
		print(total_dict['double_text_rate_s1'])
		self.assertEquals(total_dict['double_text_rate_s1'],0.0,
			"double text rate is wrong")









