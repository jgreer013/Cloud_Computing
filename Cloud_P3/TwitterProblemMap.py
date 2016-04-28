#!/usr/bin/env python
# Frazier Baker. 2016
# To work with the twitter data set.
# Tweet length and biggest tweeter
#####################################

import sys
import json

bigtable = {}

for line in sys.stdin:
	jdict =json.loads(line)
	if jdict["user"]["screen_name"] in bigtable:
		bigtable[jdict["user"]["screen_name"]].append(len(jdict["text"]))
	else:
		bigtable[jdict["user"]["screen_name"]]=[len(jdict["text"])]
for user in bigtable:
	print user+"\t"+str(len(bigtable[user]))+","+str(sum(bigtable[user]))
