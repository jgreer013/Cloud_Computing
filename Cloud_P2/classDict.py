#!/usr/bin/env python

import re

# Returns a class dictionary {'name':'callNumber'} and a call number dictionary {'callNumber':[class,info,list]}
# Should be imported as a function when creating dictionaries for active use (page load?)
def buildClassDict():
  fn = open('filteredCourses.csv','r')
  courses = fn.read().splitlines()
  fn.close()

  classDict = {}
  callDict = {}
  for line in courses:
    line = line.split('\t')
    classID = line[0]
    callNum = line[3]
    m = re.search("([0-9][0-9][0-9][0-9][0-9][0-9])",callNum)
    if m is None:
      callNum = line[4]
    if classDict.get(classID) is None:
      classDict[classID] = [callNum]
    else:
      classDict[classID].append(callNum)
    callDict[callNum] = [line[2]]
    callDict[callNum].extend(line[4:])

  return classDict, callDict

