import unittest
import os 
import datetime
from src.convo_objects.TextEquivalent import TextEquivalent 
from src.read_parse import read_and_parse_text_file
from src.calc_engine.filter_poly import (filter_by_day_of_week,
filter_by_time_of_day,
filter_by_month_of_year,
filter_by_day_of_month,
filter_by_year,
filter_by_date_range)

class TestFilters(unittest.TestCase):

	def setUp(self):
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

	def test_sanity_check_filter_days_of_week(self):
		tes_dict=filter_by_day_of_week([1,2,3,4,5,6,7],self.text_eqs)
		test_res = tes_dict['filtered_tes']
		self.assertEquals(len(test_res),len(self.text_eqs),
			"Filtering every day of the week should be same as no filter")


	def test_filter_by_year(self):
		tes_dict=filter_by_year([2017],self.text_eqs)
		test_res = tes_dict['filtered_tes']
		self.assertTrue(len(test_res)>0,"No messages captured in filter")
		for te in test_res:

			self.assertEquals(te.timestamp.year,2017,"Year should be 2017 " +
				"but it is " + str(te.timestamp.year))

	def test_filter_by_year_multiple(self):
		tes_dict=filter_by_year([2017,2016],self.text_eqs)
		test_res = tes_dict['filtered_tes']
		self.assertTrue(len(test_res)>0,"No messages captured in filter")
		for te in test_res:

			self.assertIn(te.timestamp.year,[2017,2016],"Year should be 2017 or 2016" +
				"but it is " + str(te.timestamp.year))

	def test_filter_by_month(self):
		tes_dict=filter_by_month_of_year([9],self.text_eqs)
		test_res = tes_dict['filtered_tes']
		self.assertTrue(len(test_res)>0,"No messages captured in filter")
		for te in test_res:
			self.assertEquals(te.timestamp.month,9,"Month should be 9 " +
				"but it is " + str(te.timestamp.month))

	def test_filter_by_month_multiple(self):
		tes_dict=filter_by_month_of_year([9,1],self.text_eqs)
		test_res = tes_dict['filtered_tes']
		self.assertTrue(len(test_res)>0,"No messages captured in filter")
		for te in test_res:
			self.assertIn(te.timestamp.month,[9,1],"Month should be 9 or 1 " +
				"but it is " + str(te.timestamp.month))

	def test_filter_by_day_of_month(self):
		tes_dict=filter_by_day_of_month([6],self.text_eqs)
		test_res = tes_dict['filtered_tes']
		self.assertTrue(len(test_res)>0,"No messages captured in filter")
		for te in test_res:
			self.assertEquals(te.timestamp.day,6,"Day should be 6 " +
				"but it is " + str(te.timestamp.day))

	def test_filter_by_day_of_month_multiple(self):
		tes_dict=filter_by_day_of_month([8,11],self.text_eqs)
		test_res = tes_dict['filtered_tes']
		self.assertTrue(len(test_res)>0,"No messages captured in filter")
		for te in test_res:
			self.assertIn(te.timestamp.day,[8,11],"Day should be 6 or 11 " +
				"but it is " + str(te.timestamp.day))


	def test_filter_by_day_of_week(self):
		tes_dict=filter_by_day_of_week([1],self.text_eqs)
		test_res = tes_dict['filtered_tes']
		self.assertTrue(len(test_res)>0,"No messages captured in filter")
		for te in test_res:
			self.assertEquals(te.date_day_of_week,1,"Day of week should be 1 " +
				"but it is " + str(te.date_day_of_week))

	def test_filter_by_day_of_week_multiple(self):
		tes_dict=filter_by_day_of_week([3,1],self.text_eqs)
		test_res = tes_dict['filtered_tes']
		self.assertTrue(len(test_res)>0,"No messages captured in filter")
		for te in test_res:
			self.assertIn(te.date_day_of_week,[3,1],"Day of week should \
				be 3 or 1 " +
				"but it is " + str(te.date_day_of_week))


	def test_filter_by_time_of_day(self):
		tes_dict=filter_by_time_of_day([20],self.text_eqs)
		test_res = tes_dict['filtered_tes']
		self.assertTrue(len(test_res)>0,"No messages captured in filter")
		for te in test_res:
			self.assertEquals(te.timestamp.hour,20,"Time (hour) of day should be 20 " +
				"but it is " + str(te.timestamp.hour))

	def test_filter_by_time_of_day_multiple(self):
		tes_dict=filter_by_time_of_day([15,3,1,10,8,22],self.text_eqs)
		test_res = tes_dict['filtered_tes']
		self.assertTrue(len(test_res)>0,"No messages captured in filter")

		for te in test_res:
			
			self.assertIn(te.timestamp.hour,[15,3,1,10,8,22],"Time (hour) of day should \
				be 3, 15, 1, 10, 8, or 22 " +
				"but it is " + str(te.timestamp.hour))

	def test_filter_by_date_range(self):
		begin = datetime.datetime(2016,8,3)
		end = datetime.datetime(2017,2,1)
		tes_dict=filter_by_date_range(begin,end,self.text_eqs)
		test_res = tes_dict['filtered_tes']
		self.assertTrue(len(test_res)>0,"No messages captured in filter")
		for te in test_res:
			self.assertTrue(begin <= te.timestamp <= end, "Date is not between specified dates")





