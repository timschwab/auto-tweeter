# Imports
import json

# Get user input
url = raw_input('URL of list: ')
filename = 'in'

# Load list
with open('../data/apothegms.json') as f:
	data = json.load(f)

# Ensure URL hasn't been entered already
for list in data:
	if list['url'] == url:
		print('URL already exists.')
		exit()

# Create list object
apothegms = [line.strip() for line in open(filename)]
list = {'url': url, 'apothegms': apothegms}

# Add to file
data.append(list)
with open('../data/apothegms.json', 'w') as f:
	f.write(json.dumps(data, indent=4))
