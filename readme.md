# Auto Tweeter

Some simple Python scripts to automatically post an apogethm on my Twitter account. Feel free to reuse the code if you like.

# File overview

## scripts/

### post-apothegms.py

Posts the apothegm that is next in `upcoming.json`, or a random one from `apothegms.json` if there aren't any upcoming.

### add-hashtags.py

Selects a random apothegm from `apothegms.json` and ask for three custom hashtags to go along with it. Adds the newly hashtagged apothegm to `upcoming.json`, and replaces the tagless entry in `apothegms.json`.

### import-list.py

Asks for the URL of the original post, then reads in the apothegms line by line from a file. Injects them into `apothegms.json`.

## data/

### apothegms.json

A list of all my apothegms, separated by original post. Some of them are just strings right now, and some have hashtags associated with them. Soon they will all have hashtags.

### upcoming.json

Not included in the git repo. This file exists in the middle period between no hashtags and all hashtags. As I make progress in adding hashtags to all the apothegms, I want to post those ones I have already updated. So, this file is a staging file for that purpose.

### history.json

Not included in the git repo. The previous 600 posts. `post-apothegm.py` checks this to make sure there is significant time between repeat posts.

### hashtags.json

Standard hashtags that were previously used for posts. They are still used if `upcoming.json` runs dry and `post-apothegm.py` has to use an apothegm that hasn't been tagged yet.

### auth.json

Not included in the git repo. It is a simple JSON object that contains the authorization information needed to post to Twitter. It is used in `post-apothegm.py`.
