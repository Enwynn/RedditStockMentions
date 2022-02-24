
# Subreddit to scrape
import requests

subUrl = 'https://oauth.reddit.com/r/empty/new'
subName = 'empty'

# CLIENT ID and SECRET TOKEN from reddit goes here.

auth = requests.auth.HTTPBasicAuth('<CLIENTID>', '<SECRET>')

# Reddit login info goes here.

data = {'grant_type': 'password',
        'username': '<>',
        'password': '<>'}

# App info goes here.

headers = {'User-Agent': '<API NAME>/0.0.1'}

#mysql connection info goes here.

password = '<>'
database = '<>'
table = '<>'

res = requests.post('https://www.reddit.com/api/v1/access_token',
                    auth=auth, data=data, headers=headers)

TOKEN = res.json()['access_token']

headers = {**headers, **{'Authorization': f"bearer {TOKEN}"}}

requests.get('https://oauth.reddit.com/api/v1/me', headers=headers)
