#!/usr/bin/env python
# Frazier Baker. 2016
# To work with the twitter data set.
# Tweet length and biggest tweeter
#####################################

import sys
import operator

averages = {}
winner = "@nobody"
most = 0
for line in sys.stdin:
	(key,val) = line.split("\t")
	key = key[0:-3]
	if "_ct\t" in line:
		if int(val)>most:
			winner = [key]
			most = int(val)
		elif int(val)==most:
			winner.append(key)
	elif "_av\t" in line:
		averages[key] = int(val)
print "Winner\t"+str(most)+":"+str(winner)
averagesort = sorted(averages.items(),key=operator.itemgetter(1))
print "Bottom5\t"+str(averagesort[0:5])
print "Top5\t"+str(averagesort[-5:])
