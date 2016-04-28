#!/usr/bin/env python
# Python Spark Code for Twitter Problem #6

from __future__ import print_function
import json
from pyspark import SparkContext
from datetime import datetime

sc = SparkContext(appName="bakerTwitter6Py")
twitter = sc.textFile("hdfs:///data/twitter/*")

def weekday(timetag):
   dt = datetime.strptime(timetag[0],"%a %b %d %H:%M:%S +0000 %Y")
   wday = dt.strftime("%a")
   taglist = []
   for tag in timetag[1]:
     taglist.append((tag["text"],wday))
   return taglist

def hour(timetag):
   dt = datetime.strptime(timetag[0],"%a %b %d %H:%M:%S +0000 %Y")
   hr = dt.strftime("%H")
   taglist = []
   for tag in timetag[1]:
     taglist.append((tag["text"],hr))
   return taglist

def mode(taglist):
   tcount = {}
   for t in taglist:
      if t not in tcount:
        tcount[t] = 1
      else:
        tcount[t]+= 1
   return max(tcount,key=lambda k: tcount[k])

def prp_max(pair):
   prp = pair[1]
   pd = dict()
   for p in prp:
     if p not in pd:
       pd[p]=1
     else:
       pd[p]+=1
   return (pair[0],max(pd,key=lambda k: pd[k]))


weekdayTaginfo = twitter.flatMap(lambda tweet: weekday((json.loads(tweet)["created_at"],tuple(json.loads(tweet)["entities"]["hashtags"]))))
hourTaginfo = twitter.flatMap(lambda tweet: hour((json.loads(tweet)["created_at"],tuple(json.loads(tweet)["entities"]["hashtags"]))))

hres = hourTaginfo.groupBy(lambda x: x[1]).map(prp_max)
wres = weekdayTaginfo.groupBy(lambda x: x[1]).map(prp_max)

print "Most commoon hashtag for each hour of the day:"
print hres.collect()
print "\nMost common hashtag for each day of the week:"
print wres.collect()
