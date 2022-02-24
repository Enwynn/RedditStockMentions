from random import random

import pandas as pd
import sys
import requests
import mysql.connector
from datetime import date, datetime, time
import enviroment


# Looping through each new post in the provided url, not sure about how many posts it will go through

def redditList(url, name):
    global res
    res = requests.get(url, headers=enviroment.headers)
    df = pd.DataFrame()

    for post in res.json()['data']['children']:
        post_id = post['data']['id']
        post_url = f'https://oauth.reddit.com/r/{name}/comments/{post_id}/.json'
        post_res = requests.get(post_url, headers=enviroment.headers)
        for comment in post_res.json()[1]['data']['children']:
            if 'body' in comment['data']:
                df = df.append(pd.Series(comment['data']['body'], name=post_id), ignore_index=True)

    df_filtered = flatten(df)
    return df_filtered


def flatten(df):
    df_list = df.values.tolist()
    df_list = [item for sublist in df_list for item in sublist]

    # filters out lowercase words
    def filterDownCase(text):
        return " ".join([word for word in text.split() if word.isupper()])

    df_filtered = []
    for value in df_list:
        df_filtered.append(filterDownCase(value))
    df_filtered = [x.split() for x in df_filtered]
    df_filtered = [item for sublist in df_filtered for item in sublist]
    return df_filtered

# Prints out the result from each subreddit

def printout():
    global word
    print('Successfully inserted into database')
    print(len(sorted_word_freq))

# Stores in a local MySQL database
# (string,date,id)

def store():
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        passwd=enviroment.password,
        database=enviroment.database
    )
    mycursor = mydb.cursor()
    string_word_freq = str(sorted_word_freq)
    print(string_word_freq)
    now = datetime.now()
    formatted_date = now.strftime('%Y-%m-%d %H:%M:%S')
    id = str(int(round(1000 * (1 + random()))))
    val = (string_word_freq, formatted_date, id)
    sqlInset = "INSERT INTO crawler (stocks, crawlDate, id ) VALUES (%s, %s, %s)"
    try:
        mycursor.execute(sqlInset, val)
    except:
        print("Error: unable to insert data")
    mydb.commit()
    printout()

# Makes a map and sorts it by value (top down)

def hashList():
    global word, sorted_word_freq
    word_freq = {}
    for word in finalWords:
        if word in word_freq:
            word_freq[word] += 1
        else:
            word_freq[word] = 1

    sorted_word_freq = sorted(word_freq.items(), key=lambda x: x[1], reverse=True)
    sorted_word_freq = [x for x in sorted_word_freq if x[1] > 3]
    store()


def filtering():
    global finalWords
    finalWords = redditList(subUrl, subName)

    # Most tickers are not so long
    finalWords = [x for x in finalWords if len(x) >= 1 <= 5]

    finalWords = [''.join(c for c in s if c.isalpha()) for s in finalWords]
    # Common words that are probably not a ticker
    filter = ['A', 'I', 'AND', 'NOT','THE', 'OF', 'M', 'F', 'US', 'EU','IN', 'TO', 'IS', 'ON', 'BY', 'FOR', 'AS', 'WSB','DD']
    finalWords = [x for x in finalWords if x not in filter]

    hashList()

# subbreddits.txt is the userinput and I use the input to run this program multiple times

def start():
    global subUrl, subName
    with open('subreddits.txt', 'r') as f:
        for line in f:
            for u in line.split():
                subUrl = 'https://oauth.reddit.com/r/' + u + '/new'
                subName = u
                print(subUrl)
                filtering()


start()
