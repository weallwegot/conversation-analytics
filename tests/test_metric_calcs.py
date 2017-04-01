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

reload(sys)
sys.setdefaultencoding('utf-8')


"""
this test will make sure that the logic 
for recognizing courses is working correctly
on the basis of acronyms, names, numbers, cs xxxx, and csxxxx

"""


class TestMetricCalculations(unittest.TestCase):

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
		te1 = TextEquivalent("Me","2016-08-06 15:11:44","Hi")
		te2 = TextEquivalent("Me","2016-08-06 15:13:44","Wassup")
		te3 = TextEquivalent("Me","2016-08-06 16:11:44","Hi")
		te4 = TextEquivalent("Me","2016-08-06 17:13:44","Wassup")
		rd = calculate_all_metrics([te1,te2,te3,te4])

		double = rd['double_text_rate_s1']
		number = rd['texts_sent_s1']
		self.assertEquals(double,75.0,"wrong text rate")

	def test_metric_test_longest_drought(self):
		te1 = TextEquivalent("Me","2016-08-06 15:11:44","Hi")
		te2 = TextEquivalent("Me","2016-08-06 15:13:44","Wassup")
		te3 = TextEquivalent("Me","2016-08-06 16:11:44","Hi")
		te4 = TextEquivalent("Friend","2016-08-16 16:11:44","Wassup")
		rd = calculate_all_metrics([te1,te2,te3,te4])

		drought = rd['longest_drought']
		self.assertEquals(drought,10.0,"wrong drought days: " + str(drought) + 
			" DNE " + str(10.0))

	def test_metric_test_longest_streak(self):
		te1 = TextEquivalent("Me","2016-08-06 15:11:44","Hi")
		te2 = TextEquivalent("Friend","2016-08-06 15:13:44","Wassup")
		te3 = TextEquivalent("Me","2016-08-07 16:10:44","nun much, u?")
		te4 = TextEquivalent("Friend","2016-08-07 16:11:44","chillin with bae")
		te5 = TextEquivalent("Me","2016-08-08 16:10:44","word, say hi for me")
		te6 = TextEquivalent("Friend","2016-08-08 16:11:44","she dont care")
		te7 = TextEquivalent("Me","2016-08-09 16:10:44","cool, i dont like her")
		te8 = TextEquivalent("Friend","2016-08-09 16:11:44","you dont have to lol...")
		rd = calculate_all_metrics([te1,te2,te3,te4,te5,te6,te7,te8])

		streak = rd['longest_streak']
		self.assertEquals(streak,4," wrong streak days: " + str(streak) + 
			" DNE " + str(4))

	def test_metric_test_laugh_rate_50_percent(self):

		te1 = TextEquivalent("Me","2016-08-06 15:11:44","Hi,ahaha")
		te2 = TextEquivalent("Me","2016-08-06 15:13:44","Wassup")
		te3 = TextEquivalent("Me","2016-08-06 16:11:44","Hi")
		te4 = TextEquivalent("Me","2016-08-06 17:13:44","Wassup,lmaoo")
		rd = calculate_all_metrics([te1,te2,te3,te4])

		double = rd['laugh_rate_s1']
		number = rd['texts_sent_s1']
		self.assertEquals(double,50.0,"wrong laugh rate")

	def test_number_of_texts_sent(self):
		rd = calculate_all_metrics(self.tes)
		self.assertEquals(rd['texts_sent_s1'],2)
		self.assertEquals(rd['texts_sent_s2'],2)

	def test_laughing_detection_haha(self):
		te1 = TextEquivalent("Me","2016-08-06 15:11:44","Haha")
		self.assertTrue(calc_laugh(te1)['laugh_bool'],"Should contain a laugh")
		te3 = TextEquivalent("Me","2016-08-06 15:11:44","hahaha")
		self.assertTrue(calc_laugh(te3)['laugh_bool'],"Should contain a laugh")

	def test_laugh_detection_acronyms(self):
		te2 = TextEquivalent("Me","2016-08-06 15:11:44","Lol")
		self.assertTrue(calc_laugh(te2)['laugh_bool'],"Should contain a laugh")
		te4 = TextEquivalent("Me","2016-08-06 15:11:44","lolol")
		self.assertTrue(calc_laugh(te4)['laugh_bool'],"Should contain a laugh")
		te5 = TextEquivalent("Me","2016-08-06 15:11:44","lmaoo")
		self.assertTrue(calc_laugh(te5)['laugh_bool'],"Should contain a laugh")
		te6 = TextEquivalent("Me","2016-08-06 15:11:44","lmao")
		self.assertTrue(calc_laugh(te6)['laugh_bool'],"Should contain a laugh")
	def test_no_laugh_detection(self):
		te7 = TextEquivalent("Me","2016-08-06 15:11:44","hi how are you, no thats not me")
		self.assertFalse(calc_laugh(te7)['laugh_bool'],"Should not contain a laugh")

	def test_curse_detection(self):
		te7 = TextEquivalent("Me","2016-08-06 15:11:44","hi shit")
		self.assertTrue(calc_curse(te7)['curse_bool'],"Should  contain a curse")
		te7 = TextEquivalent("Me","2016-08-06 15:11:44","hi fuck")
		self.assertTrue(calc_curse(te7)['curse_bool'],"Should  contain a curse")
		te7 = TextEquivalent("Me","2016-08-06 15:11:44","hi bitch")
		self.assertTrue(calc_curse(te7)['curse_bool'],"Should  contain a curse")

	def test_curse_detection_many_letters(self):
		te7 = TextEquivalent("Me","2016-08-06 15:11:44","hi fuckkk")
		self.assertTrue(calc_curse(te7)['curse_bool'],"Should  contain a curse")
		te7 = TextEquivalent("Me","2016-08-06 15:11:44","biiitchh")
		self.assertTrue(calc_curse(te7)['curse_bool'],"Should  contain a curse")
		te7 = TextEquivalent("Me","2016-08-06 15:11:44","sshhittt")
		self.assertTrue(calc_curse(te7)['curse_bool'],"Should  contain a curse")

	def test_no_curse_detection(self):
		te7 = TextEquivalent("Me","2016-08-06 15:11:44","hi how are you, no thats not me")
		self.assertFalse(calc_curse(te7)['curse_bool'],"Should not contain a curse")

	def test_link_detection(self):
		te7 = TextEquivalent("Me","2016-08-06 15:11:44","https://github.com/weAllWeGot/conversation-analytics")
		self.assertTrue(calc_link(te7)['link_bool'],"Should contain a link")
		te7 = TextEquivalent("Me","2016-08-06 15:11:44","https://twitter.com/OluwaSumnSumn")
		self.assertTrue(calc_link(te7)['link_bool'],"Should contain a link")
		#te7 = TextEquivalent("Me","2016-08-06 15:11:44","linkedin.com")
		#self.assertTrue(calc_link(te7)['link_bool'],"Should contain a link")
		
		te7 = TextEquivalent("Me","2016-08-06 15:11:44","https://twitter.com/90spideypool/status/840747256596856832")
		self.assertTrue(calc_link(te7)['link_bool'],"Should contain a link")
		te7 = TextEquivalent("Me","2016-08-06 15:11:44","http://www.buyblack.io/")
		self.assertTrue(calc_link(te7)['link_bool'],"Should contain a link")

	def test_no_link_detection(self):
		te7 = TextEquivalent("Me","2016-08-06 15:11:44","hi how are you, no thats not me")
		self.assertFalse(calc_link(te7)['link_bool'],"Should not contain a link")


	def test_emoji_detection(self):
		
		te7 = TextEquivalent("Me","2016-08-06 15:11:44",unicode("💁🏾💁🏾💁🏾💁🏾").decode('utf-8'))
		self.assertTrue(calc_emoji(te7)['emoji_bool'],"Should contain an emoji: " + te7.all_text)
		te7 = TextEquivalent("Me","2016-08-06 15:11:44","🤗")
		self.assertTrue(calc_emoji(te7)['emoji_bool'],"Should contain an emoji: " + te7.all_text )
		te7 = TextEquivalent("Me","2016-08-06 15:11:44","🤓")
		self.assertTrue(calc_emoji(te7)['emoji_bool'],"Should contain an emoji: " + te7.all_text )
		te7 = TextEquivalent("Me","2016-08-06 15:11:44","😔")
		self.assertTrue(calc_emoji(te7)['emoji_bool'],"Should contain an emoji: " + te7.all_text )
		te7 = TextEquivalent("Me","2016-08-06 15:11:44","😂😂")
		self.assertTrue(calc_emoji(te7)['emoji_bool'],"Should contain an emoji: " + te7.all_text )
		te7 = TextEquivalent("Me","2016-08-06 15:11:44","🤔")
		self.assertTrue(calc_emoji(te7)['emoji_bool'],"Should contain an emoji: " + te7.all_text )
		te7 = TextEquivalent("Me","2016-08-06 15:11:44","👋🏿")
		self.assertTrue(calc_emoji(te7)['emoji_bool'],"Should contain an emoji: " + te7.all_text )
		te7 = TextEquivalent("Me","2016-08-06 15:11:44","💅")
		self.assertTrue(calc_emoji(te7)['emoji_bool'],"Should contain an emoji: " + te7.all_text )
		te7 = TextEquivalent("Me","2016-08-06 15:11:44","💅🏿")
		self.assertTrue(calc_emoji(te7)['emoji_bool'],"Should contain an emoji: " + te7.all_text )
		te7 = TextEquivalent("Me","2016-08-06 15:11:44","😩😩😩")
		self.assertTrue(calc_emoji(te7)['emoji_bool'],"Should contain an emoji: " + te7.all_text )
		te7 = TextEquivalent("Me","2016-08-06 15:11:44","😍")
		self.assertTrue(calc_emoji(te7)['emoji_bool'],"Should contain an emoji: " + te7.all_text )
		te7 = TextEquivalent("Me","2016-08-06 15:11:44","🙄🙄🙄")
		self.assertTrue(calc_emoji(te7)['emoji_bool'],"Should contain an emoji: " + te7.all_text )
		te7 = TextEquivalent("Me","2016-08-06 15:11:44","😱")
		self.assertTrue(calc_emoji(te7)['emoji_bool'],"Should contain an emoji: " + te7.all_text )
		te7 = TextEquivalent("Me","2016-08-06 15:11:44","😈")
		self.assertTrue(calc_emoji(te7)['emoji_bool'],"Should contain an emoji: " + te7.all_text )
		te7 = TextEquivalent("Me","2016-08-06 15:11:44","👌")
		self.assertTrue(calc_emoji(te7)['emoji_bool'],"Should contain an emoji: " + te7.all_text )
		te7 = TextEquivalent("Me","2016-08-06 15:11:44","🏾")
		self.assertTrue(calc_emoji(te7)['emoji_bool'],"Should contain an emoji: " + te7.all_text )
		te7 = TextEquivalent("Me","2016-08-06 15:11:44","👍🏿")
		self.assertTrue(calc_emoji(te7)['emoji_bool'],"Should contain an emoji: " + te7.all_text )
		te7 = TextEquivalent("Me","2016-08-06 15:11:44","🙏")
		self.assertTrue(calc_emoji(te7)['emoji_bool'],"Should contain an emoji: " + te7.all_text )
		te7 = TextEquivalent("Me","2016-08-06 15:11:44","🏃")
		self.assertTrue(calc_emoji(te7)['emoji_bool'],"Should contain an emoji: " + te7.all_text )
		te7 = TextEquivalent("Me","2016-08-06 15:11:44","💁")
		self.assertTrue(calc_emoji(te7)['emoji_bool'],"Should contain an emoji: " + te7.all_text )

	def test_no_emoji_detection(self):
		te7 = TextEquivalent("Me","2016-08-06 15:11:44","hi how are you, no thats not me")
		self.assertFalse(calc_emoji(te7)['emoji_bool'],"Should not contain an emoji")


	def test_metric_for_time_activity(self):
		te1 = TextEquivalent("Me","2016-08-11 15:11:44","Hi")
		te2 = TextEquivalent("Me","2016-08-11 15:13:44","Wassup")
		te3 = TextEquivalent("Me","2016-08-11 15:17:44","Hi")
		te4 = TextEquivalent("Friend","2016-08-16 16:11:44","Wassup")
		rd = calc_most_least_active_times([te1,te2,te3,te4])

		highhour = rd['most_active_hour_of_day']
		self.assertEquals(highhour,'15',"wrong most active hour: " + str(highhour) + 
			" DNE " + str(15))

		self.assertEquals(rd['most_active_day_of_month'],'11',"wrong most active day of month: " 
			+ str(rd['most_active_day_of_month']) + " DNE " + str(11))


		self.assertEquals(rd['most_active_day_of_week'],'Thursday',"wrong most active day of week: " 
			+ rd['most_active_day_of_week'] + " DNE " + 'Thursday')


