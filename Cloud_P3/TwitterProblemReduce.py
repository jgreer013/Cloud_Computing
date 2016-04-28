#!/usr/bin/env python
# Frazier Baker. 2016
# To work with the twitter data set.
# Tweet length and biggest tweeter
#####################################

import sys

sums = {}
counts = {}

for line in sys.stdin:
	(key,val) = line.split("\t")
	if key in sums:
		sums[key]+int(val.split(",")[1])
		counts[key]+int(val.split(",")[0])
	else:
		sums[key]=int(val.split(",")[1])
		counts[key]=int(val.split(",")[0])

for key in sums:
	print key+"_av\t"+str(sums[key]/counts[key])
	print key+"_ct\t"+str(counts[key])
