# -*- coding: utf-8 -*-
"""
Created on Sat Nov 22 20:54:55 2014

@author: Alvin Khong
"""
import sqlite3 as lite
import sys

con = None

        
def InsertTrends(userName, topics, rank, date, tweetId, weight):
    global con
    with con:
        cur = con.cursor()    
        #cur.execute("CREATE TABLE Cars(Id INT, Name TEXT, Price INT)")
        cur.execute("INSERT INTO TrendingTweet VALUES('"+userName+"','"+topics+"',"+str(rank)+",'"+date+"','"+tweetId+"',"+str(weight)+")")

def selectTable():
    global cur    
    cur = con.cursor()    
    cur.execute('SELECT * FROM Cars')
    data = cur.fetchall()
    return data    



def connectDB():
    global con
    try:
        con = lite.connect('TrendingTweet.db')
#         print "SQLite version: %s" % data                
        
    except lite.Error, e:
        
        print "Error %s:" % e.args[0]
        sys.exit(1)
            
    #finally:
    #    if con:
    #        con.close()
    
def canInsert(username, date):
    global cur
    tweet_list=[]    
    cur = con.cursor()    
    cur.execute('SELECT Tweets FROM TrendingTweet WHERE Username="'+username+'" AND Date="'+date+'" ORDER BY Weight DESC')
    data = cur.fetchall()
    if len(data)>0:
        return False
    else:
        return True
            
def closeDB():
    global con
    if con:
        con.close()
    
# Table Name : TrendingTweet
# Columns (Username TEXT, Topic TEXT, Rank INT, date TEXT, Tweets TEXT, Weight DOUBLE)") 
def retrieveTrendsVis(username):
    global cur    
    date_list=[]  #date.. ['2014/11/26','2014/11/24']
    topic_list=[] #list of lists.. [[1,2,3,4,5],[1,2,3,4,5]]
    t_list=[]    
    combine_list=[]
    cur = con.cursor()    
    cur.execute('SELECT DISTINCT date FROM TrendingTweet WHERE Username="'+username+'" ORDER BY date DESC LIMIT 10')
    data = cur.fetchall()
    for tup in data:
        date_list.append(tup[0])
    for d in date_list:    
        cur.execute('SELECT DISTINCT Topic FROM TrendingTweet WHERE Username="'+username+'" AND date="'+d+'" ORDER BY Rank' )
        data = cur.fetchall()
        for tup in data:
            t_list.append(tup[0].encode('utf-8'))
        topic_list.append(t_list)
        t_list=[]
    date_list = [x.encode('utf-8') for x in date_list]
    combine_list.append(date_list)
    combine_list.append(topic_list)
    print combine_list
    return combine_list  


def retrieveTopicsByDate(username, date):
    global cur
    topic_list=[]
    cur = con.cursor()    
    cur.execute('SELECT DISTINCT Topic FROM TrendingTweet WHERE Username="'+username+'" AND date="'+date+'" ORDER BY RANK')
    data = cur.fetchall()
    for tup in data:
        topic_list.append(tup[0]) 
    print topic_list
    return [x.encode('utf-8') for x in topic_list]   
        

def retrieveTweetsByTopic(username, topic, date):
    global cur
    tweet_list=[]    
    cur = con.cursor()    
    cur.execute('SELECT Tweets FROM TrendingTweet WHERE Username="'+username+'" AND Topic="'+topic+'" And date = "'+ date + '" ORDER BY Weight DESC')
    data = cur.fetchall()
    for tup in data:
        tweet_list.append(tup[0])
    return [x.encode('utf-8') for x in tweet_list]
# connectDB()
# # createTable()
# # print selectTable()
# # print retrieveTweetsByTopic("abc", 'Technology')
# print retrieveTopicsByDate('mrinalkumar23', '20141129')
# closeDB()
# connectDB()
# InsertTrends("userName", "topics", 2, "date", "tweetId", 3.0)
# closeDB()