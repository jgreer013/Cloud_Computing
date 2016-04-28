#!/usr/bin/env python
import mincemeat

data2 = range(2,10000000)
def chunky(l,k):
  for i in xrange(0, len(l), k):
    yield l[i:i+k]

data3 = chunky(data2, 400) # 400 seems most optimal

# The data source can be any dictionary-like object
datasource = dict(enumerate(data3))

def mapfn(k, v):
  from math import sqrt
  for num in v:
    if str(num) == str(num)[::-1] and num%2 == 1:
      def isPrime(n):
        for k in xrange(2,int(sqrt(n))):
          if n % k == 0:
            return False
        return True
      if isPrime(num) == True:
        yield "pal", int(num)

def reducefn(k, vs):
    result = sum(vs) # Mine runs 0.2s faster with this here than with it not
    return vs

s = mincemeat.Server()
s.datasource = datasource
s.mapfn = mapfn
s.reducefn = reducefn

results = s.run_server(password="changeme")
print results["pal"]
