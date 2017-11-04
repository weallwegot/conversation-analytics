import datetime
import re
"""
Represents one text or batch of sequential texts from one sender
"""
class TextEquivalent:
	def __init__(self,name,timestamp_string,text):
		self.sender = name
		
		self.date_day = None
		self.date_month = None
		self.date_year = None
		self.time = None
		
		self.all_text = text
		self.timestamp = self.set_timestamp(timestamp_string)
		self.date_day_of_week = self.timestamp.isoweekday() 



	def merge_sequential_text_equiv(self,text_equivalent_to_merge):
		"""
		param: text_equivalent_to_merge :: (TextEquivalent) -> the TextEquivalent to merge with self
		merges an additional text object into the current one
		appends the text with a new line character and averages
		the timestamps
		"""
		text_to_append = text_equivalent_to_merge.all_text
		self.all_text = self.all_text + "\n" + text_to_append
		timestamp_to_merge = text_equivalent_to_merge.timestamp
		self.timestamp = self.average_timestamps(self.timestamp,timestamp_to_merge)

		if not text_equivalent_to_merge.sender == self.sender:
			error_message = "senders of merged texts must be identical \n\
				" + self.sender + " does not equal " + text_equivalent_to_merge.sender
			raise Exception(error_message)
	def average_timestamps(self,earlier,later):
		"""
		param: earlier :: (datetime) -> the earlier of the two datatime objects
		param: later :: (datetime) -> the later of the two datatime objects
		"""
		#http://stackoverflow.com/questions/25473394/finding-mid-point-date-between-two-dates-in-python
		return(earlier + (later-earlier)/2)

	def set_timestamp(self,timestamp_string):
		"""
		TODO: extend to support different formats
		parses data time string into dateime object
		format expected: YYYY-MM-DD HH:MM:SS (i think)
		"""
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