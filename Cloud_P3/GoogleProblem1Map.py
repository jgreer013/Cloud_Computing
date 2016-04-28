#!/usr/bin/env python
import sys

mapDict = {}

for line in sys.stdin:
  cols = line[:-1].split("\t")
  year = cols[1]
  try:
    mapDict[year] += 1
  except:
    mapDict[year] = 1

for year in mapDict:
  print year + '\t' + str(mapDict[year])
