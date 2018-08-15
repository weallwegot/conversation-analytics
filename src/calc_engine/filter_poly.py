# used to make sure time zones are both naive or aware for comparison filtering
import pytz
import numpy as np
"""
Various functions for filtering out a list of TextEquivalent objects
into different categories
"""

def filter_by_day_of_week(list_of_days_of_week,tes):
	filtered_tes = []
	dict_filtered_tes = {
	'filtered_tes':None,
	'filter_criteria':None,
	'number_returned':None
	}
	for te in tes:
		if te.date_day_of_week in list_of_days_of_week:
			filtered_tes.append(te)
	dict_filtered_tes['filtered_tes'] = filtered_tes



	return dict_filtered_tes

def filter_by_time_of_day(list_of_hours_of_day,tes):
	filtered_tes = []
	dict_filtered_tes = {
	'filtered_tes':None,
	'filter_criteria':None,
	'number_returned':None
	}
	for te in tes:
		if te.timestamp.hour in list_of_hours_of_day:
			filtered_tes.append(te)
	dict_filtered_tes['filtered_tes'] = filtered_tes



	return dict_filtered_tes

def filter_by_month_of_year(list_of_months_of_year,tes):
	filtered_tes = []
	dict_filtered_tes = {
	'filtered_tes':None,
	'filter_criteria':None,
	'number_returned':None
	}
	for te in tes:
		if te.timestamp.month in list_of_months_of_year:
			filtered_tes.append(te)
	dict_filtered_tes['filtered_tes'] = filtered_tes


	return dict_filtered_tes

def filter_by_day_of_month(list_of_days_of_month,tes):
	filtered_tes = []
	dict_filtered_tes = {
	'filtered_tes':None,
	'filter_criteria':None,
	'number_returned':None
	}
	for te in tes:
		if te.timestamp.day in list_of_days_of_month:
			filtered_tes.append(te)
	dict_filtered_tes['filtered_tes'] = filtered_tes


	return dict_filtered_tes

def filter_by_year(list_of_years,tes):
	filtered_tes = []
	dict_filtered_tes = {
	'filtered_tes':None,
	'filter_criteria':None,
	'number_returned':None
	}
	for te in tes:
		if te.timestamp.year in list_of_years:
			filtered_tes.append(te)
	dict_filtered_tes['filtered_tes'] = filtered_tes



	return dict_filtered_tes

def filter_by_date_range(start_date,end_date,tes):
	#http://stackoverflow.com/questions/15307623/cant-compare-naive-and-aware-datetime-now-challenge-datetime-end
	utc = pytz.UTC
	filtered_tes = []
	dict_filtered_tes = {
	'filtered_tes':None,
	'filter_criteria':None,
	'number_returned':None
	}
	# if this is too slow
	# we can break out of the loop once one of the timestamps
	# is greater than the end_date
	# however this actually assumes the tes are already chronologically ordered
	for te in tes:
		try:
			if start_date.replace(tzinfo=utc) <= te.timestamp.replace(tzinfo=utc) <= end_date.replace(tzinfo=utc):
				filtered_tes.append(te)
		except AttributeError:
			# this will get hit if you pass something other than a datetime object as there is no replace functino
			if start_date <= np.datetime64(te.timestamp) <= end_date:
				filtered_tes.append(te)


	dict_filtered_tes['filtered_tes'] = filtered_tes
	dict_filtered_tes['number_returned'] = len(filtered_tes)



	return dict_filtered_tes


