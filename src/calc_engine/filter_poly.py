import metric_calculations as mc

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
	filtered_tes = []
	dict_filtered_tes = {
	'filtered_tes':None,
	'filter_criteria':None,
	'number_returned':None
	}
	for te in tes:
		if start_date <= te.timestamp <= end_date:
			filtered_tes.append(te)

	dict_filtered_tes['filtered_tes'] = filtered_tes



	return dict_filtered_tes


