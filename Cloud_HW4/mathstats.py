#!/usr/bin/env python
import mincemeat
import sys

my_file = open(sys.argv[1],'r')
lns = my_file.read().splitlines()

def chunky(l,k):
  if k == 0:
    k = 1
  for i in xrange(0, len(l), k):
    yield l[i:i+k]

data2 = chunky(lns, len(lns)/200) # 400 seems most optimal

# The data source can be any dictionary-like object
datasource = dict(enumerate(data2))

def mapfn(k, v):
    for w in v:
        yield "sum", int(w)

def reducefn(k, vs):
    from math import sqrt
    std = 0
    s1 = 0
    s2 = 0
    for val in vs:
      s1 += val
      s2 += val*val
    std = float(sqrt(len(vs)*s2 - s1*s1))/len(vs)
    result = sum(vs)
    return result, len(vs), std

s = mincemeat.Server()
s.datasource = datasource
s.mapfn = mapfn
s.reducefn = reducefn

results = s.run_server(password="changeme")
print "Sum: " + str(results["sum"][0])
print "Count: " + str(results["sum"][1])
print "Std: " + str(results["sum"][2])
