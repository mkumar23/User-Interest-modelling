'''
Created on Sep 10, 2014
@author: Mrinal
'''
import oauth2 as oauth
import json
from __builtin__ import str
from classifier import getPredictions
import time

CONSUMER_KEY = ""
CONSUMER_SECRET = ""
ACCESS_KEY = ""
ACCESS_SECRET = ""
screenName = "mrinalkumar23"
consumer = oauth.Consumer(key=CONSUMER_KEY, secret=CONSUMER_SECRET)
access_token = oauth.Token(key=ACCESS_KEY, secret=ACCESS_SECRET)
client = oauth.Client(consumer, access_token)

def getAuthentication(scrName,C_key,C_sec,A_key,A_sec):
    global CONSUMER_KEY, CONSUMER_SECRET, ACCESS_KEY, ACCESS_SECRET, client, consumer, access_token, screenName 
    CONSUMER_KEY = "yWzFD3AIuvDyvVV8hN10ybrPC"
    CONSUMER_SECRET = "JxjeCgS9rnZ3Sod6kE2FgYVeBr15ghLeguECtUNwRVFISm7Y8x"
    ACCESS_KEY = "2805967592-qDxdpLy0vmuWOcrtuyaORVzdCWCzvqHHEcDTW9t"
    ACCESS_SECRET = "WrqJGINKOGYzmKrvqmIXaSMawKNofbeiJjxFdJEpRPRq7"
    consumer = oauth.Consumer(key=CONSUMER_KEY, secret=CONSUMER_SECRET)
    access_token = oauth.Token(key=ACCESS_KEY, secret=ACCESS_SECRET)
    client = oauth.Client(consumer, access_token)
    screenName = scrName
      
   
def getTweetsByID(id):
    allTweet = []
    timeline_endpoint = "https://api.twitter.com/1.1/statuses/user_timeline.json?user_id="+str(id)+"&count=10"
    response, data = client.request(timeline_endpoint)
    tweets = json.loads(data)
#     getUserDetailsByID(id)
    for tweet in tweets:
        with open("twt.txt",'a') as out:
            out.write("0\t"+tweet['text'].encode('utf-8')+'\n')
        allTweet.append([tweet['id'],tweet['text'].encode('utf-8')])
    return allTweet

def getTweetsByScrName(id):
    allTweet = []
    timeline_endpoint = "https://api.twitter.com/1.1/statuses/user_timeline.json?screen_name="+str(id)+"&count=200"
    response, data = client.request(timeline_endpoint)
    tweets = json.loads(data)
    print "Tweets:"
    for tweet in tweets:
        allTweet.append(tweet['text'])
    return allTweet

def getUserDetailsByID(id):
    timeline_endpoint = "https://api.twitter.com/1.1/users/show.json?user_id="+str(id)
    response, data = client.request(timeline_endpoint)
    info = json.loads(data)
#     if not info.has_key['error']:
    print info["name"].encode('utf8')

def getFolloweeID(scrnName):
    timeline_endpoint = "https://api.twitter.com/1.1/friends/ids.json?cursor=-1&screen_name="+scrnName+"&count=50"
    response, data = client.request(timeline_endpoint)
    userIDs = json.loads(data)
    return userIDs
def sortWithRelevance(tweet):
    tweet.sort(key = lambda x: x[2])
    return tweet

def getTweets():
    tweet = []
    userIds = getFolloweeID(screenName)
    if not userIds.has_key('ids'):
        return 'User error'
    for id in userIds['ids']:
        tweet.extend(getTweetsByID(id))
#     print tweet
    print "Here"
    prediction = getPredictions(tweet)
    return sortWithRelevance(prediction)[-10:]

def updateTrends(scrName,_):
    getAuthentication(scrName, "C_key", "C_sec", "A_key", "A_sec")
    date = time.strftime("%Y%m%d")
    print date
    import database as db
    db.connectDB()
    if not db.canInsert(scrName, date):
        return
    tweets = getTweets()
    for tweet in tweets:
        db.InsertTrends(scrName, 'Technology', 1, date, tweet[0], tweet[2])
    db.closeDB()

    
# getAuthentication("mrinalkumar23", "C_key", "C_sec", "A_key", "A_sec")
# userIds = getFolloweeID(screenName)
# for id in userIds['ids']:
#     tweet = getTweetsByID(id)


