import pandas as pd
import requests

# Subreddit to scrape

wsbUrl = 'https://oauth.reddit.com/r/wallstreetbets/new'
namewsb = 'wallstreetbets'

# CLIENT ID and SECRET TOKEN from reddit goes here.

auth = requests.auth.HTTPBasicAuth('CLIENT ID', 'SECRET TOKEN')

# Reddit login info goes here.

data = {'grant_type': 'password',
        'username': '<Username>',
        'password': '<Password>'}

# App info goes here.

headers = {'User-Agent': '<APP-info>/0.0.1'}

res = requests.post('https://www.reddit.com/api/v1/access_token',
                    auth=auth, data=data, headers=headers)

TOKEN = res.json()['access_token']

headers = {**headers, **{'Authorization': f"bearer {TOKEN}"}}

requests.get('https://oauth.reddit.com/api/v1/me', headers=headers)


# Looping through each post in the provided url

def redditList(url, name):
    global res
    res = requests.get(url, headers=headers)
    df = pd.DataFrame()  # initialize dataframe

    for post in res.json()['data']['children']:
        post_id = post['data']['id']
        post_url = f'https://oauth.reddit.com/r/{name}/comments/{post_id}/.json'
        post_res = requests.get(post_url, headers=headers)
        for comment in post_res.json()[1]['data']['children']:
            if 'body' in comment['data']:
                df = df.append(pd.Series(comment['data']['body'], name=post_id), ignore_index=True)

    df_list = df.values.tolist()

    df_list = [item for sublist in df_list for item in sublist]

    # filters out lowercase words

    df_filtered = []
    for value in df_list:
        df_filtered.append(filterDownCase(value))

    # Make every element in a string its own element in a list

    df_filtered = [x.split() for x in df_filtered]

    # Flatten the list

    df_filtered = [item for sublist in df_filtered for item in sublist]
    return df_filtered


def filterDownCase(text):
    return " ".join([word for word in text.split() if word.isupper()])


finalWords = redditList(wsbUrl, namewsb)

# Filter out 'I', or other common capitalized words

finalWords = [x for x in finalWords if x != 'I']


# Makes a hashmap of words and their frequencies

word_freq = {}
for word in finalWords:
    if word in word_freq:
        word_freq[word] += 1
    else:
        word_freq[word] = 1

# Sort the hashmap by frequency

sorted_word_freq = sorted(word_freq.items(), key=lambda x: x[1], reverse=True)

# Store the hashmap in a text file

with open('word_freq.txt', 'w') as f:
    for word, freq in sorted_word_freq:
        f.write(f'{word} {freq}\n')
