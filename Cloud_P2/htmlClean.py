#!/usr/bin/env python

import rip
from unicodedata import normalize
import re

fn = open("onestop.html",'r')
html = fn.read()
fn.close()

classLists = rip.parseUC(html)

#fn = open("unfilteredCourses.csv",'w')
for row in range(len(classLists)):
  for col in range(len(classLists[row])):
    classLists[row][col] = normalize('NFKD', classLists[row][col]).encode('ascii','ignore')
    #fn.write(classLists[row][col] + '\t')
  #fn.write("\n")
#fn.close()



# Don't be upsetti, have some spaghetti

fn = open("filteredCourses.csv","w")
count = 0
write_date = ""
prev_date = ""
for clss in classLists:
  class_head = clss[:3]
  prev_date = write_date
  for col in range(len(clss)):
    if clss[col].find("Summer S") != -1 or clss[col].find("Summer May") != -1:
      word = clss[col]
      date = word[word.find("(")+1:word.find(")")]
      if date != 'class dates vary':
        year = date[-5:]
        new_date = date[0:5] + year + date[5:]
        write_date = new_date
      else:
        write_date = ""
      continue
    if clss[col] == "" or clss[col] == " " or clss[col] == '  ':
      continue
    m = re.search("([0-9][0-9][0-9][0-9][0-9][0-9])",clss[col]) # I do want call numbers
    if m is not None and col != 6:
      fn.write(write_date + '\n')
      fn.write(class_head[0].strip() + '\t' + class_head[1] + '\t' + class_head[2] + '\t')
      fn.write(clss[col].strip() + '\t')
      continue
    m2 = re.search("(^[0-9]{3}$)",clss[col].replace(" ","")) # I don't want section numbers
    if m2 is not None:
      continue
    if col == 0:
      fn.write(clss[col].strip() + '\t')
    else:
      fn.write(clss[col] + '\t')

  if prev_date == write_date:
    fn.write(write_date + "\n")
  elif clss[0][:25] != "Summer Semester 2015-16 (":
    fn.write("\n")
fn.close()

# Maximum regretti
# HTML outletti
# Code bloodletti
# Clean format getti
