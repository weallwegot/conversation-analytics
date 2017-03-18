
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
		self.text_eqs = read_and_parse_text_file(full_path,1) 
		self.te1 = TextEquivalent("Me","2016-08-06 15:11:44","Hi")
		self.te2 = TextEquivalent("Friend","2016-08-06 15:13:44","Wassup")
		te3 = TextEquivalent("Me","2016-08-06 15:15:44","how are you")
		te4 = TextEquivalent("Friend","2016-08-06 15:17:44","gooood")
		self.tes = [self.te1,self.te2,te3,te4]



	def test_metric_test_timings(self):

		te1 = TextEquivalent("Me","2016-08-06 15:11:44","Hi")
		te2 = TextEquivalent("You","2016-08-06 15:13:44","Wassup")
		time_dict = calc_time_between_text_equivalents(te1,te2)
		time_dict['time diff'] = 120
		self.assertEquals(time_dict['time diff'],120,"time elapsed is wrong")
		self.assertEquals(time_dict['sender'],"Me","sender is wrong")
		self.assertEquals(time_dict['responder'],"You","receiver is wrong")
		self.assertEquals(time_dict['double text'],False,"double text is wrong")

	def test_metric_test_double_text(self):

		te1 = TextEquivalent("Me","2016-08-06 15:11:44","Hi")
		te2 = TextEquivalent("Me","2016-08-06 15:13:44","Wassup")
		time_dict = calc_time_between_text_equivalents(te1,te2)
		self.assertEquals(time_dict['double text'],True,"double text is wrong")

	def test_metric_test_length_of_text_message(self):

		te1 = TextEquivalent("Me","2016-08-06 15:11:44","Hi hi hi")
		te2 = TextEquivalent("Me","2016-08-06 15:13:44","Wassup")
		time_dict = calc_length_text_equivalent(te1)
		self.assertEquals(time_dict['length_chars'],8,"length is wrong")
		self.assertEquals(time_dict['length_words'],3,"length is wrong")

	def test_metric_end_to_end_response_rate(self):
		rd = calculate_all_metrics(self.tes)
		self.assertEquals(rd['response_rate_s1'],120.0,
			"response rate is wrong")
		self.assertEquals(rd['response_rate_mean_s1'],120,
			"mean response rate is wrong")

	def test_metric_end_to_end_double_text_rate_with_no_double_texts(self):
		total_dict = calculate_all_metrics(self.tes)
		self.assertEquals(total_dict['double_text_rate_s1'],0.0,
			"double text rate is wrong")

	def test_metric_test_double_text_75_percent(self):
		#the first timestamp just for reference
		#2016-08-06 15:11:44
		te1 = TextEquivalent("Me","2016-08-06 15:11:44","Hi")
		te2 = TextEquivalent("Me","2016-08-06 15:13:44","Wassup")
		te3 = TextEquivalent("Me","2016-08-06 16:11:44","Hi")
		te4 = TextEquivalent("Me","2016-08-06 17:13:44","Wassup")
		rd = calculate_all_metrics([te1,te2,te3,te4])

		double = rd['double_text_rate_s1']
		number = rd['texts_sent_s1']
		self.assertEquals(double,75.0,"wrong text rate")

	def test_number_of_texts_sent(self):
		rd = calculate_all_metrics(self.tes)
		self.assertEquals(rd['texts_sent_s1'],2)
		self.assertEquals(rd['texts_sent_s2'],2)









