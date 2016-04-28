#!/usr/bin/env python
import sys

mapDict = {}

for line in sys.stdin:
  cols = line[:-1].split("\t")
  year = cols[1]
  word = cols[0]
  try:
    mapDict[year][0] += 1
    mapDict[year][1] += len(word)
  except:
    mapDict[year] = [1, len(word)]

for year in mapDict:
  print year + '\t' + str(mapDict[year][0]) + '\t' + str(mapDict[year][1])
