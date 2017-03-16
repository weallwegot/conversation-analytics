import datetime
import re
"""
Represents one text or batch of sequential texts
"""
class TextEquivalent:
	def __init__(self,name,timestamp_string,text):
		self.sender = name
		
		self.date_day = self.date_day_parse(timestamp_string)
		self.date_month = self.date_month_parse(timestamp_string)
		self.date_year = self.date_year_parse(timestamp_string)
		self.time = self.time_of_day_parse(timestamp_string)
		
		self.all_text = text
		self.timestamp = self.set_timestamp(timestamp_string)
		self.date_day_of_week = self.day_of_week_parse(timestamp_string)

	def append_sequential_text(self,text_to_append):
		self.all_text = self.all_text + "\n" + text_to_append
	def merge_sequential_text_equiv(self,text_equivalent_to_merge):
		text_to_append = text_equivalent_to_merge.all_text
		self.all_text = self.all_text + "\n" + text_to_append
		timestamp_to_merge = text_equivalent_to_merge.timestamp
		self.timestamp = self.average_timestamps(self.timestamp,timestamp_to_merge)

		if not text_equivalent_to_merge.sender == self.sender:
			raise NameError("no no no no no no no. \n\
			 senders of merged texts must be identical \n\
			 " + self.sender + "does not equal" + text_equivalent_to_merge.sender)
	def average_timestamps(self,earlier,later):
		return(earlier + (later-earlier)/2)
	def date_day_parse(self,timestamp_string):
		return ""
	def date_month_parse(self,timestamp_string):
		return ""		
	def date_year_parse(self,timestamp_string):
		return ""		
	def time_of_day_parse(self,timestamp_string):
		return ""	
	def day_of_week_parse(self,timestamp_string):
		return ""	
	def set_timestamp(self,timestamp_string):
		ds_ts = timestamp_string.split(' ')
		date_strings = ds_ts[0].split('-')
		time_strings = ds_ts[1].split(':')
		self.date_year = int(date_strings[0])#int(re.search(r'^\d\d\d\d',timestamp_string).group())
		self.date_month = int(date_strings[1])#int(re.search(r'\-\d\d\-',timestamp_string).group()[1:4])
		self.date_day = int(date_strings[2])#int(timestamp_string[8:10])
		hour = int(time_strings[0])#int(re.search(r'\s\d\d',timestamp_string).group()[1:])
		minute = int(time_strings[1])#int(re.search(r'^\d\d\d\d',timestamp_string).group())
		second = int(time_strings[2])#int(re.search(r'^\d\d\d\d',timestamp_string).group())
		return datetime.datetime(self.date_year,
			self.date_month,
			self.date_day,
			hour,minute,second)