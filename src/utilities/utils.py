

#used isoweekday & calendar module is 0 indexed
#so making simple mapping implementation
def display_weekday(string_week):
	day_d = {
	'1':'Monday',
	'2':'Tuesday',
	'3':'Wednesday',
	'4':'Thursday',
	'5':'Friday',
	'6':'Saturday',
	'7':'Sunday',
	}
	return(day_d[string_week])