# Imports
import json
import random

# Constants
path = '/home/pyzaist/auto-tweeter/'

def main():
	# Load lists
	with open(path + '/data/apothegms.json') as f:
		apothegms = json.load(f)
	
	with open(path + '/data/upcoming.json') as f:
		upcoming = json.load(f)

	response = ''
	while response != 'y':
		updateApothegm(apothegms, upcoming)
		
		# Continue?
		response = ''
		while response != 'y' and response != 'n':
			response = raw_input('Another? (y/n)')
	
	# Save changes
	with open(path + '/data/apothegms.json', 'w') as f:
		f.write(json.dumps(apothegms, indent=4))
	
	with open(path + '/data/upcoming.json', 'w') as f:
		f.write(json.dumps(upcoming, indent=4))

# Functions

def updateApothegm(apothegms, upcoming):
	# Pick random apothegm that does not have hashtags yet
	apothegm = {}
	while not isinstance(apothegm, basestring):
		post = random.choice(apothegms)
		index = random.randrange(len(post['apothegms']))
		apothegm = post['apothegms'][index]

	if isinstance(apothegm, basestring):
		
		# Get hashtags
		print('\n' + apothegm + '\n')
		hashtag1 = raw_input('hashtag1: ')
		hashtag2 = raw_input('hashtag2: ')
		hashtag3 = raw_input('hashtag3: ')

		# Update data
		apothegm_dict = {'apothegm': apothegm, 'hashtags': [hashtag1, hashtag2, hashtag3]}
		upcoming.append(apothegm_dict)
		post['apothegms'][index] = apothegm_dict

main()
