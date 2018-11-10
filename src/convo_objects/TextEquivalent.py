#!/usr/bin/env python2
import datetime
import re
from dateutil import parser
import logging
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
		else:
			logger.warning('attempted to set timestamp w/ an incorrect type: {}'
				.format(type(tstamp)))

	def merge_sequential_text_equiv(self,text_equivalent_to_merge):
		"""
		merges an additional text object into the current one.
		appends to text the all_text attribute with a new line character
		updates the timestamp attribute by averaging the two timestamps

		:param text_equivalent_to_merge: the TextEquivalent to merge with self
		:text_equivalent_to_merge type: TextEquivalent

		"""
		text_to_append = text_equivalent_to_merge.all_text
		self.all_text = self.all_text + "\n" + text_to_append
		timestamp_to_merge = text_equivalent_to_merge.timestamp
		self.timestamp = self.average_timestamps(self.timestamp,timestamp_to_merge)

		if not text_equivalent_to_merge.sender == self.sender:
			error_msg = "Senders of merged texts must be identical\n{} does not equal {}".\
			format(self.sender,text_equivalent_to_merge.sender)
			logger.error(error_msg)
			raise Exception(error_msg)
	def average_timestamps(self,earlier,later):
		"""
		function to averages two datetime objects

		:param earlier: the earlier of the two datatime objects
		:earlier type: datetime.datetime

		:param later: the later of the two datatime objects
		:later type: datetime.datetime
		"""
		#http://stackoverflow.com/questions/25473394/finding-mid-point-date-between-two-dates-in-python
		return(earlier + (later-earlier)/2)

