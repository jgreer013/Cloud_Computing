from __future__ import     print_function
import sys, json
from pyspark import SparkContext

#--num-executors 20
    
def getYearSyl(line):
  def countSyls(word):
    vowels = ['a','e','i','o','u','y']
    wd = word.lower()
    return sum([1 for l in wd if l in vowels])
  sp = line.split('\t')
  return (sp[1], countSyls(sp[0]))
  
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
    
  sc = SparkContext(appName="GoogleAvgSyl")
  
  years = sc.textFile(sys.argv[1])
  yearCounts = years.map(getYearCount)
  yearSyls = years.map(getYearSyl)
  
  yearTotalSyl = yearSyls.reduceByKey(lambda a, b: a+b)
  yearTotalCount = yearCounts.reduceByKey(lambda a, b: a+b)
  
  SylCount = dict(yearTotalSyl.join(yearTotalCount).collect())
  for key in sorted(SylCount.keys()):
    syl = SylCount[key][0]
    count = float(SylCount[key][1])
    print(key + '\t' + str(syl/count))
    
