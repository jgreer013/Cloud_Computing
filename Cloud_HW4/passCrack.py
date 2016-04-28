#!/usr/bin/env python
import mincemeat
import sys
from string import digits, ascii_lowercase
from itertools import permutations
import hashlib

data = ["Humpty Dumpty sat on a wall",
        "Humpty Dumpty had a great fall",
        "All the King's horses and all the King's men",
        "Couldn't put Humpty together again",
        ]


charr = digits + ascii_lowercase
def buildData():
  ret = []
  for k in range(1,5):
    for perm in permutations(charr, r=k):
      ret.append("".join(perm))
  return ret

def chunky(l,k,ik):
  for i in xrange(0, len(l), k):
    yield (l[i:i+k], ik)

global inp
inp = sys.argv[1]

data4 = chunky(buildData(), 210, inp) # Optimized

# The data source can be any dictionary-like object
datasource = dict(enumerate(data4))

def mapfn(k, v):
  from hashlib import md5
  for pw in v[0]:
    if md5(pw).hexdigest()[:5] == v[1]:
      yield "pass", pw

def reducefn(k, vs):
  return vs

s = mincemeat.Server()
s.datasource = datasource
s.mapfn = mapfn
s.reducefn = reducefn

results = s.run_server(password="changeme")
print results
