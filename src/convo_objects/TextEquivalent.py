import datetime
import re
from dateutil import parser
"""
Represents one text or batch of sequential texts from one sender
"""
class TextEquivalent(object):
	def __init__(self,name,timestamp_string,text):
		self.sender = name
		
		self.time = None
		
		self.all_text = text
		self.timestamp = timestamp_string
		self.date_day_of_week = self.timestamp.isoweekday() 
		self.date_year = self.timestamp.year
		self.date_month = self.timestamp.month
		self.date_day = self.timestamp.day

	@property
	def timestamp(self):
		return self._timestamp

	@timestamp.setter
	def timestamp(self,tstamp):
		if isinstance(tstamp,str):
			self._timestamp = parser.parse(tstamp)
		elif isinstance(tstamp,datetime.datetime):
			self._timestamp = tstamp

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
			error_msg = "Senders of merged texts must be identical\n{} does not equal {}".\
			format(self.sender,text_equivalent_to_merge.sender)
			raise Exception(error_msg)
	def average_timestamps(self,earlier,later):
		"""
		param: earlier :: (datetime) -> the earlier of the two datatime objects
		param: later :: (datetime) -> the later of the two datatime objects
		"""
		#http://stackoverflow.com/questions/25473394/finding-mid-point-date-between-two-dates-in-python
		return(earlier + (later-earlier)/2)

