# Imports
import json
import random
import requests
import urllib

from requests_oauthlib import OAuth1

# Constants
maxPostAttempts = 100
historySize = 600

def main():
	# Load data
	with open('/home/pyzaist/auto-tweeter/data/apothegms.json') as f:
		apothegms = json.load(f)
	
	with open('/home/pyzaist/auto-tweeter/data/upcoming.json') as f:
		upcoming = json.load(f)
	
	with open('/home/pyzaist/auto-tweeter/data/history.json') as f:
		history = json.load(f)
	
	with open('/home/pyzaist/auto-tweeter/data/auth.json') as f:
		auth = json.load(f)
	
	with open('/home/pyzaist/auto-tweeter/data/hashtags.json') as f:
		hashtagList = json.load(f)
	
	# Post random apothegm, trying until it succeeds
	for i in range(maxPostAttempts):
		status = generateStatus(apothegms, upcoming, history, hashtagList)
		if status == False:
			continue

		if postStatus(history, auth, status):
			break
	
	# Save changes to data
	with open('/home/pyzaist/auto-tweeter/data/history.json', 'w') as f:
		f.write(json.dumps(history, indent=4))
	
	with open('/home/pyzaist/auto-tweeter/data/upcoming.json', 'w') as f:
		f.write(json.dumps(upcoming, indent=4))

# Functions
def generateStatus(apothegms, upcoming, history, hashtagList):
	# If no upcoming ones with hashtags
	if len(upcoming) == 0:
		# Choose apothegm
		post = random.choice(apothegms)
		apothegm = random.choice(post['apothegms'])

		# Choose hashtags
		if isinstance(apothegm, str):
			hashtags = random.sample(hashtagList, 3)
			return {'apothegm': apothegm, 'hashtags': hashtags}
		else:
			return apothegm

		# Make sure it hasn't been posted recently
		if apothegm in history:
			print('Recently posted ' + apothegm + '. Searching again.')
			return False
	
	# If there are upcoming ones that I have added custom hashtags to
	else:
		return upcoming.pop(0)

def postStatus(history, auth, status):
	apothegm = status['apothegm']
	hashtags = status['hashtags']
	status = apothegm + '\n\n#' + hashtags[0] + '\n#' + hashtags[1] + '\n#' + hashtags[2]

	# Post apothegm
	url = 'https://api.twitter.com/1.1/statuses/update.json?' + urllib.parse.urlencode({'status': status.encode('utf-8')})

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
		print('Success.')
		return True
	else:
		print('Error! Twitter didn\'t like that. Failed with status code ' + str(res.status_code))
		print(res.text)
		print('')
		return False

main()
