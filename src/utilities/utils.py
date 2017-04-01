
import urllib2
from bs4 import BeautifulSoup, SoupStrainer
import itertools
#used isoweekday & calendar module is 0 indexed
#so making simple mapping implementation


class UtilityBoss:
	def __init__(self):


		#this is making a url request to the official unicode page
		response = urllib2.urlopen("http://unicode.org/emoji/charts/full-emoji-list.html")
		emoji_html = response.read()
		only_names = SoupStrainer(attrs={"class": "name"})
		only_codes = SoupStrainer(attrs={"class": "code"})


		soup_names = BeautifulSoup(emoji_html,"html.parser",parse_only=only_names)
		soup_codes = BeautifulSoup(emoji_html,"html.parser",parse_only=only_codes)

		emoji_d_name = {}
		emoji_d_code = {}

		for name,code in itertools.izip(soup_names.strings,soup_codes.strings):
			emoji_d_name[name] = code
			emoji_d_code[code] = name

		self.emoji_d_name_keys = emoji_d_name
		self.emoji_d_code_keys = emoji_d_code


	def convert_emoji_code(self,unicode_raw):
		unicode_raw = unicode_raw\
		.encode('unicode_escape')\
		.upper()\
		.replace('\\','')
		real_code_key = unicode_raw.replace('000','+')
		print("code key: " + real_code_key)
		#print(self.emoji_d_code_keys.keys())
		if real_code_key in self.emoji_d_code_keys.keys():

			return(self.emoji_d_code_keys[real_code_key])
		else:
			return('NA')

	def convert_emoji_name(self,emojiname):
		if emojiname in self.emoji_d_name_keys.keys():
			return(self.emoji_d_name_keys[emoji_d_name])
		else:
			return('NA')


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


