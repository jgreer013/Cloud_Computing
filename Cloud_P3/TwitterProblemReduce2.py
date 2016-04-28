#!/usr/bin/env python
# Frazier Baker. 2016
# To work with the twitter data set.
# Tweet length and biggest tweeter
#####################################

import sys
import operator

most = 0
winner = []
bottom = []
top = []

for line in sys.stdin:
	(key,val) = line.split("\t")
	if key == "Winner":
		(worth,team) = val.split(":")
		team = eval(team)
		if worth > most:
			most = worth
			winner = []
		if worth == most:
			for member in team:
				winner.append(member)
	elif key == "Bottom5":
		val = eval(val)
		for member in val:
			bottom.append(member)
	elif key == "Top5":
		val = eval(val)
		for member in val:
			top.append(member)

sortedtop = sorted(top,key=operator.itemgetter(1))
sortedbottom = sorted(bottom,key=operator.itemgetter(1))

print "Winner\t"+str(winner)+"\t"+str(most)
print "Top5\t"+str(sortedtop[-5:])
print "Bottom5\t"+str(sortedbottom[0:5])
