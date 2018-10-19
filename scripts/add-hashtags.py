# Imports
import json
import random

# Load lists
with open('../data/apothegms.json') as f:
	apothegms = json.load(f)

with open('../data/upcoming.json') as f:
	upcoming = json.load(f)

while True:
	# Pick random apothegm that does not have hashtags yet
	post = random.choice(apothegms)
	apothegm = random.choice(post['apothegms'])

	if isinstance(apothegm, basestring):
		
		# Get hashtags
		print('\n' + apothegm + '\n')
		hashtag1 = raw_input('hashtag1: ')
		hashtag2 = raw_input('hashtag2: ')
		hashtag3 = raw_input('hashtag3: ')

		# Update data
		apothegm_dict = {'apothegm': apothegm, 'hashtags': [hashtag1, hashtag2, hashtag3]}
		upcoming.append(apothegm_dict)
	
	# Continue?
	response = ''
	while response != 'y' and response != 'n':
		response = raw_input('Another? (y/n)')
	
	if response != 'y':
		break

# Save changes
with open('../data/apothegms.json', 'w') as f:
	f.write(json.dumps(apothegms, indent=4))

with open('../data/upcoming.json', 'w') as f:
	f.write(json.dumps(upcoming, indent=4))


