# Imports
import json
import random
import requests
import urllib

from requests_oauthlib import OAuth1

# Load lists
with open('/home/pyzaist/twitter/data/apothegms.json') as f:
	apothegms = json.load(f)

with open('/home/pyzaist/twitter/data/hashtags.json') as f:
	hashtags = json.load(f)

with open('/home/pyzaist/twitter/data/previous.json') as f:
	previous = json.load(f)

with open('/home/pyzaist/twitter/data/auth.json') as f:
	auth = json.load(f)

# Post random apothegm, trying until it succeeds
for i in range(100):

	# Choose apothegm
	list = random.choice(apothegms)
	apothegm = random.choice(list['apothegms'])
	
	# Choose hashtags
	hashtag1 = hashtag2 = random.choice(hashtags)
	while hashtag1 == hashtag2:
		hashtag2 = random.choice(hashtags)

	status = apothegm + '\n\n' + '#' + hashtag1 + '\n#' + hashtag2

	# Make sure it hasn't been posted in the last 600 posts
	if apothegm in previous:
		print('Recently posted ' + apothegm + '. Searching again.')
		continue

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
		previous.append(apothegm)
		if len(previous) > 600:
			previous.pop(0)	
		break;
	else:
		print('Error! Twitter didn\'t like that. Failed with status code ' + str(res.status_code))
		print(res.text)
		print('')

# Save the previous posts
with open('/home/pyzaist/twitter/data/previous.json', 'w') as f:
	f.write(json.dumps(previous, indent=4))
