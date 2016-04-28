#!/usr/bin/env python
# Frazier Baker and Jeremiah Greer
# 2016 March. For CS6065 Project
######################################
from classDict import *
import re
from datetime import datetime

def getSchedInfo(callno,classDictOutput=None):
  #gets schedule info for a given callnumber
  if classDictOutput is None:
    classDictOutput = buildClassDict()
  (classes,calls) = classDictOutput
  glob = calls[callno]
  days = []
  times = []
  dates = []
  pdays = []
  ptimes = []
  for prop in glob:
    possible = (prop.isupper())
    possible = possible and (prop not in ["EAST","WEST","UCBA","CLER"])
    possible = possible and (len(prop)>3) #Always true because of spacepad
    if possible:
      m = re.search("^(M|T|W|R|F|S|U)+\s*$",prop)
      if m is None:
        continue
      m = re.findall("(M|T|W|R|F|S|U)",prop) #Trying to find days
      if len(m)>0:
        pdays = tuple(m)
    timpossible = (":" in prop and "-" in prop)
#   timpossible = timpossible or ("TBA" in prop)
    if timpossible:
      ptimes = tuple(prop.split(" - "))
    #m = re.findall("(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)",prop)
    if (re.search(" - ",prop) and not timpossible):
      (startd,endd) = prop.split(" - ")
      if startd[0] not in ['J','F','M','A','S','O','N','D']:
        startd = datetime.strftime(datetime.strptime(startd,"%m/%d/%Y"),"%b %d")
        endd = datetime.strftime(datetime.strptime(endd,"%m/%d/%Y"),"%b %d")
      if len(ptimes) is len(pdays) and len(ptimes) is 0:
        print "****"+str(ptimes)
        continue
      days.append(pdays)
      times.append(ptimes)
      dates.append((startd,endd))
      pdays = []
      ptimes= []
  retlist = []
  for i in xrange(len(dates)):
    if len(dates[i]) is 0 and len(times[i]) is 0 and len(days[i]) is 0:
      print (dates,times,days)
      return []
    if "TBA" not in times[i]:
      retlist.append((dates[i],times[i],days[i]))
  return retlist

def findSections(className):
  #Helper function for finding tough examples,
  #not necessary for main code
  dicts = buildClassDict()
  for k in dicts[0].keys():
    if re.search(className,k):
      for c in dicts[0][k]:
        print str(k)+" "+c+" "+str(dicts[1][c])

#print getSchedInfo("703319")
