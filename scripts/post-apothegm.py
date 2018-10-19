# Imports
import json
import random
import requests
import urllib

from requests_oauthlib import OAuth1

# Constants
maxAttempts = 100
historySize = 600

# Load data
with open('/home/pyzaist/auto-tweeter/data/apothegms.json') as f:
	apothegms = json.load(f)

with open('/home/pyzaist/auto-tweeter/data/hashtags.json') as f:
	hashtagList = json.load(f)

with open('/home/pyzaist/auto-tweeter/data/history.json') as f:
	history = json.load(f)

with open('/home/pyzaist/auto-tweeter/data/auth.json') as f:
	auth = json.load(f)

with open('/home/pyzaist/auto-tweeter/data/upcoming.json') as f:
	upcoming = json.load(f)

# Post random apothegm, trying until it succeeds
for i in range(maxAttempts):

	# If no upcoming ones with hashtags
	if len(upcoming) == 0:
		# Choose apothegm
		post = random.choice(apothegms)
		apothegm = random.choice(post['apothegms'])

		# Choose hashtags
		if isinstance(apothegm, basestring):
			hashtags = random.sample(hashtagList, 3)
		else:
			hashtags = apothegm['hashtags']
			apothegm = apothegm['apothegm']

		# Make sure it hasn't been posted recently
		if apothegm in history:
			print('Recently posted ' + apothegm + '. Searching again.')
			continue
	
	# If there are upcoming ones that I have added custom hashtags to
	else:
		apothegm = upcoming.pop(0)
		hashtags = apothegm['hashtags']
		apothegm = apothegm['apothegm']

	status = apothegm + '\n\n#' + hashtags[0] + '\n#' + hashtags[1] + '\n#' + hashtags[2]

	# Post apothegm
	url = 'https://api.twitter.com/1.1/statuses/update.json?' + urllib.urlencode({'status': status.encode('utf-8')})

	authData = OAuth1(auth['client-key'],
			auth['client-secret'],
			auth['owner-key'],
			auth['owner-secret'])
	
	print('Trying to post to ' + url)
	
	res = requests.post(url=url, auth=authData)
	
	# Handle response
	if res.status_code == 200:
		history.append(apothegm)
		if len(history) > historySize:
			history.pop(0)	
		break;
	else:
		print('Error! Twitter didn\'t like that. Failed with status code ' + str(res.status_code))
		print(res.text)
		print('')

# Save changes
with open('/home/pyzaist/auto-tweeter/data/history.json', 'w') as f:
	f.write(json.dumps(history, indent=4))

with open('/home/pyzaist/auto-tweeter/data/upcoming.json', 'w') as f:
	f.write(json.dumps(upcoming, indent=4))