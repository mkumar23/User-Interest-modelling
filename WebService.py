from xml.etree.ElementTree import Element, SubElement, tostring
import web
import xml.etree.ElementTree as ET
import TwitterFetcher
import database as db
import thread

#Example to read from xml file.. 
#tree = ET.parse('user_data.xml')
#root = tree.getroot()

urls = (
    '/topics/(.*)/(.*)', 'list_topics',
    '/tweets/(.*)/(.*)/(.*)', 'get_tweets',
    '/update/(.*)/(.*)/(.*)/(.*)/(.*)/(.*)', 'updateUserInfo',
    '/trends/(.*)','list_trends'
)

app = web.application(urls, globals())



#combine with calls below to sajann function. 
#sajann function decide whether to update user info, this side going to send same thing everytime..
class updateUserInfo:        
    def GET(self, notification,userID,key,secret,authkey,authsecret):
        t=(userID,"")
        print t
        thread.start_new_thread(TwitterFetcher.updateTrends, t)
        val = notification + userID +"\t" + key +"\t" + secret +"\t" + authkey +"\t" + authsecret
        print val
        return val
        
class list_trends:        
   def GET(self, user):
        output = 'trends:[';
        lst = []
          # pass userid to sajann function providing topicid
          # make calls to sajann function
        uid = "uid";
        db.connectDB()
        lst = db.retrieveTrendsVis(user)
        db.closeDB()
        d_input = lst[0]#["11/5/2014","11/3/2014","11/1/2014","10/30/2014","10/28/2014","10/26/2014","10/24/2014","10/22/2014","10/20/2014","10/18/2014"];
        rank_topic_input = lst[1]#[["Technology","topic2","topic3","Food","topic5"],["Photography","topic2","topic3","topic4","topic5"],["topic1","topic2","topic3","topic4","topic5"],["topic1","topic2","topic3","topic4","topic5"],["topic1","topic2","topic3","topic4","topic5"],["Technology","topic2","topic3","Food","topic5"],["Photography","topic2","topic3","topic4","topic5"],["topic1","topic2","topic3","topic4","topic5"],["topic1","topic2","topic3","topic4","topic5"],["topic1","topic2","topic3","topic4","topic5"]];
        root = convert_to_xml_trend(uid,d_input,rank_topic_input) 
        for child in root:
            print 'child', child.tag, child.attrib
            output += str(child.attrib) + ','
        output += ']';
        return output
                

class list_topics:        
    def GET(self, user, date):
        output = 'topics:[';
          # pass userid to sajann function providing topicid
          # make calls to sajann function
          # organise to 3 essential info below   
          # assume data organised as seen below
        uid = "uid";
        tid_input = ["tid1","tid2","tid3","tid4","tid5"];
        db.connectDB()
        topic_input = db.retrieveTopicsByDate(user, date)
        db.closeDB()
        root = convert_to_xml_topic(uid,tid_input,topic_input) 
        for child in root:
            print 'child', child.tag, child.attrib
            output += str(child.attrib) + ','
        output += ']';
        return output
          

class get_tweets:
    def GET(self, user, topic_name, date):
        output = 'tweets:[';            
        # make calls to sajann function providing topicid
        # organise messages to 3 essential info below
        # assume data organised as seen below
        tid = "topicID1";
        topic_input = "topic1"
        db.connectDB()
        mid_input = db.retrieveTweetsByTopic(user, topic_name, date)
        db.closeDB()
        root = convert_to_xml_tweet(tid,mid_input[:5],topic_input)
        for child in root:
            print 'child', child.tag, child.attrib
            output += str(child.attrib) + ','
        output += ']';
        return output


#Example Specific to Topic
#<Topics uid="userID">
#    <topic id="topicID1" name="Rocky" />
#    <topic id="topicID2" name="Steve" />
#    <topic id="topicID3" name="Melinda" />
#</Topics>


def convert_to_xml_topic(uid,tid_input,topic_input):
    top = Element('Topics',{'uid':uid})
    i=0
    for topic in topic_input:
        child = SubElement(top, 'topic',{'id':tid_input[i] ,'name':topic })
        i=i+1
    return top
  
#Example: Specific Tweets Topic 
#<Tweets tid="topicID1" name="Rocky">
#    <message id="messageID1"/>
#    <message id="messageID2"/>
#    <message id="messageID3"/>
#    <message id="messageID1"/>
#    <message id="messageID2"/>
#    <message id="messageID3"/>
#</Tweets>

def convert_to_xml_tweet(tid,mid_input,topic_input):
    top = Element('Tweets',{'tid':tid,'name':topic_input })
    i=0
    for mid in mid_input:
        child = SubElement(top, 'message',{'id':mid})
        i=i+1
    return top

#print tostring(tweet_xml)

def convert_to_xml_trend(uid,date_input,trend_input):
    top = Element('Trend',{'uid':uid});
    i=0;
    x=0;
    y=0;
    for date in date_input:
        for g in trend_input[y]:
            child = SubElement(top, 'trend',{'date':date  ,'name':g,'rank':(x+1) })
            x=x+1;
        y=y+1;
        x=0;
        
    return top;


if __name__ == "__main__":
    app.run()