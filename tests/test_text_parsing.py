
import unittest

import os
import datetime
from src.convo_objects.TextEquivalent import TextEquivalent 
from src.read_parse import read_and_parse_text_file




"""
this test will make sure that the logic 
for recognizing courses is working correctly
on the basis of acronyms, names, numbers, cs xxxx, and csxxxx

"""


class TestTextParsing(unittest.TestCase):

	def setUp(self):
		#self.te = TextEquivalent()
		working_dir = os.path.dirname(os.path.abspath(__file__))
		data_folder = working_dir + os.sep + "test_data" 
		text_file_name = "TestData.txt"
		full_path = data_folder + os.sep + text_file_name
		self.text_eqs = read_and_parse_text_file(full_path,3) 
		te1 = TextEquivalent("Me","2016-08-06 15:11:44","Hi",)
		te2 = TextEquivalent("Me","2016-08-06 15:13:44","Wassup")
		te1 = TextEquivalent("Me","2016-08-06 15:11:44","Hi")
		te2 = TextEquivalent("Me","2016-08-06 15:13:44","Wassup")
		te1.merge_sequential_text_equiv(te2)
		self.merged_te = te1



	def test_timestamp_date_parse(self):
		#the first timestamp just for reference
		#2016-08-06 15:11:44
		self.assertTrue(self.text_eqs[0].date_day==6,
			"Timestamp day not correct")
		self.assertTrue(self.text_eqs[0].date_month==8,
			"Timestamp month not correct")
		self.assertTrue(self.text_eqs[0].date_year==2016,
			"Timestamp year not correct")
		self.assertTrue(self.text_eqs[0].timestamp.hour==15,
			"Timestamp hour not correct")
		self.assertTrue(self.text_eqs[0].timestamp.minute==11,
			"Timestamp minute not correct")
		self.assertTrue(self.text_eqs[0].timestamp.second==44,
			"Timestamp second not correct")


	def test_timestamp_day_of_week_parse(self):
		day_of_week = datetime.datetime(2016,8,6).isoweekday()
		self.assertTrue(self.text_eqs[0].date_day_of_week==day_of_week,
			"Timestamp day of week not correct")

	def test_name_sender(self):
		self.assertEquals(self.text_eqs[0].sender,"Friend",
			"Incorrect parsing of sender")

	def test_text_merging_time(self):
		my_te = self.merged_te 
		self.assertEquals(my_te.timestamp.minute,12,
			"Timestamp merging minutes of week not correct")
		self.assertEquals(my_te.timestamp.hour,15,
			"Timestamp hours merge incorrect")
		self.assertEquals(my_te.timestamp.second,44,
			"Timestamp seconds merge incorrect")

	def test_text_merging_text(self):
		my_te = self.merged_te 
		self.assertTrue("Wassup" in my_te.all_text,
			"Text merging not correct")

	def test_merge_incorrect_senders(self):

		te1 = TextEquivalent("Me","2016-08-06 15:11:44","Hi",)
		te2 = TextEquivalent("You","2016-08-06 15:13:44","Wassup")
		error_message = "senders of merged texts must be identical \n\
			" + "Me" + " does not equal " + "You"
		with self.assertRaises(Exception) as context:
			te1.merge_sequential_text_equiv(te2)

		self.assertTrue(error_message==error_message,"error")





