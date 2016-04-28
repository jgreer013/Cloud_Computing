from __future__ import     print_function
import sys, json
from pyspark import SparkContext

#--num-executors 20
    
def getYearLength(line):
  sp = line.split('\t')
  return (sp[1], len(sp[0]))
  
def getYearCount(line):
  sp = line.split('\t')
  return (sp[1], 1)
  
def getAvgLength(a, b):
  if a > b:
    return a/float(b)
  else:
    return b/float(a)
    
if __name__ == "__main__":
  if len(sys.argv) < 2:
    print("enter a filename")
    sys.exit(1)
    
  sc = SparkContext(appName="GoogleAvgWordLength")
  
  years = sc.textFile(sys.argv[1])
  yearCounts = years.map(getYearCount)
  yearLengths = years.map(getYearLength)
  
  yearTotalLength = yearLengths.reduceByKey(lambda a, b: a+b)
  yearTotalCount = yearCounts.reduceByKey(lambda a, b: a+b)
  
  LengthCount = dict(yearTotalLength.join(yearTotalCount).collect())
  for key in sorted(LengthCount.keys()):
    length = LengthCount[key][0]
    count = float(LengthCount[key][1])
    print(key + '\t' + str(length/count))
    
