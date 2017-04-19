import unittest
import os 
import datetime
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from src.convo_objects.TextEquivalent import TextEquivalent 
from src.data_viz.visualize import create_volume_trends, create_time_trends
from src.read_parse import read_and_parse_text_file
from src.calc_engine.filter_poly import (filter_by_day_of_week,
filter_by_time_of_day,
filter_by_month_of_year,
filter_by_day_of_month,
filter_by_year,
filter_by_date_range)

class TestVizCalcs(unittest.TestCase):

	def setUp(self):
		working_dir = os.path.dirname(os.path.abspath(__file__))
		data_folder = working_dir + os.sep + "test_data" 
		text_file_name = "TestData.txt"
		full_path = data_folder + os.sep + text_file_name
		self.text_eqs = read_and_parse_text_file(full_path,1) 
		self.te1 = TextEquivalent("Me","2016-08-06 15:11:44","Hi")
		self.te2 = TextEquivalent("Friend","2016-08-06 16:13:44","Wassup")
		te3 = TextEquivalent("Me","2016-08-06 18:15:44","how are you")
		te4 = TextEquivalent("Friend","2016-08-06 19:17:44","gooood")
		self.tes = [self.te1,self.te2,te3,te4]

	def test_cumulative_statistics_binning(self):
		z = create_volume_trends(self.tes)
		y=z['y_vals']
		x=z['x_ticks']
		cs=z['cumsum']

		self.assertEquals(len(cs),len(y),
			"Cumulative sums and y values need to be same length.")
		self.assertEquals(len(x),len(y),
			"X values of hours need to be equivalent to available Y values to plot.")
		self.assertEquals(6, len(x), "There are 6 bin ticks to be created between the hours of 15 and 20. " + "Not " 
			+ str(len(x)))
		self.assertEquals(4, cs[-1], "Last value whould be the total number of Text Equivalents sent.")

	"""
	this really only runs thru it to make sure there are no errors
	the functionality in time trend creations is tested
	in the test_filtering unittests & in the test_metric_calcs unittests
	"""
	def test_time_trend_creation(self):
		z = create_time_trends(self.tes)
		self.assertTrue(True,"It's not you, it's me.")


