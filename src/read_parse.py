import re
from src.convo_objects.TextEquivalent import TextEquivalent

def read_and_parse_text_file(full_ass_path, block_text_threshold_seconds):
	"""
	:param full_ass_path: path to the file where the text data is
	:full_ass_path type: str

	:param block_text_threshold_seconds: number of seconds between sequential texts for 
	them to be considered as "one" text. they will be merged. see `merge_sequential_text_equiv()`
	:block_text_threshold_seconds type: int

	:returns: a list of TextEquivalent objects
	:rtype: list
	"""
	text_equivs = []

	with open(full_ass_path,'r') as whole_ass_convo:
		raw_data = whole_ass_convo.readlines()
		i = 0
		for line in raw_data:
			# search for a couple of letters then a colon, before 
			sender = re.search(r'^\w+\:',line)
			# search for the timestamp in YYYY-MM-DD HH:MM:SS format.
			timestamp = re.search(r'\|\d+\-\d+\-\d+\s?\d+\:\d+\:\d+',line)
			if sender and timestamp:
				# get rid of the identifying colon, last character
				sender_name = sender.group()[:-1]
				
				timestamp_string = timestamp.group()
				# slice the raw input such that sender & timestamp are gone.
				# BUG: this includes the colon and space in the text
				text_msg = line[len(sender_name):-len(timestamp_string)-1]
				# get rid of the identifier pipe, first character.
				te = TextEquivalent(sender_name,timestamp_string[1:],text_msg)
				
				if i >= 1:
					te_prev = text_equivs[i-1]
					diff = te.timestamp - te_prev.timestamp
					if (te_prev.sender==te.sender) and (abs(diff.seconds) < block_text_threshold_seconds):
						te_prev.merge_sequential_text_equiv(te)
					else:
						text_equivs.append(te)
						i += 1
				else:
					text_equivs.append(te)
					i += 1

	return text_equivs