#!/usr/bin/env python
# Frazier Baker								      #
# Attempting to scrape a UC page with BeautifulSoup because screenscraping    #
#  poorly written websites isn't fun.					      #
###############################################################################

import codecs
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.support.ui import Select
from time import sleep
import re

def scrapeUC():
  #extracts raw html from onestop
  browser = webdriver.Firefox()
  browser.get("http://webapps2.uc.edu/scheduleofclasses/")
  Select(browser.find_element_by_id("MainContent_Term")).select_by_index(0)
  Select(browser.find_element_by_id("MainContent_TermSession")).select_by_index(1)
  browser.find_element_by_id("MainContent_Keyword").send_keys(".")
  browser.find_element_by_id("MainContent_Submit").click()
  sleep(10)
  Src = browser.page_source
  browser.close()
  return Src
#end

def parseUC(html=None):
  #constructs groups of related fields for classes
  if html is None:
    html = scrapeUC()
  soup = BeautifulSoup(html,'html.parser')
  cells = soup.find_all('td')
  groups = []
  thisGroup = []
  for c in cells:
    if("Availability" in str(c)):
      groups.append(thisGroup)
      thisGroup = [c.get_text()]
    else:
      thisGroup.append(c.get_text())
  return groups
#end

def sectionize(classID,groups=None):
  #Breaks class into sections with unique Call Numbers
  if groups is None:
    groups = parseUC()
  sections = {}
  for g in groups:
    if classID not in g:
      continue
    else:
      sid=None
      for portion in g:
        if len(portion) is 0:
          continue
        m = re.search("(\d\d\d\d\d\d)",portion)
        if m is not None:
          sid = m.group(0)
          sections[sid] = [sid]
        elif sid is not None:
          sections[sid].append(portion)
  return sections

def permuteAll(classList,groups=None):
  #Creates permutations of sections for a given classlist
  #Some permutations may be invalid
  if groups is None:
    groups = parseUC()
  classes = {}
  perms = []
  permct = 1
  for c in classList:
    classes[c] = sectionize(c,groups)
    permct*=len(classes[c])
  for p in range(permct):
    temp = []
    for c in classList:
      temp.append(classes[c][classes[c].keys()[p/(permct/len(classes[c]))]])
    perms.append(temp)
  return perms

def convertToDaysTimes(perms):
  days = []
  times= []
  for p in perms:
    pdays = []
    ptimes = []
    for c in p:
      for prop in c:
        possible = (prop is prop.upper())
        possible = possible and (prop not in ["EAST","WEST","UCBA","CLER"])
        possible = possible and (len(prop)>3) #Always true because of spacepad
        if possible:
          m = re.findall("(M|T|W|R|F|S|U)",prop) #Trying to find days
          if len(m)>0:
            pdays.append(tuple(m))
        timpossible = (":" in prop and "-" in prop)
        timpossible = timpossible or ("TBA" in prop)
        if timpossible:
          ptimes.append(tuple(prop.split(" - ")))
    days.append(pdays)
    times.append(ptimes)
  return (days,times)
#end

def createStatic():
  #Creates a static HTML Document for reference on selenium-less systems
  f=codecs.open("onestop.html","w","utf-8")
  f.write(scrapeUC())
  f.close()


def TEST(classes):
  html = None
  with codecs.open("onestop.html","r","utf-8") as f:
    html = f.read()
  groups = parseUC(html)
  perms = permuteAll(classes,groups)
  f = codecs.open("testout.txt","w","utf-8")
  f.write(str(convertToDaysTimes(perms)))
  f.close()
  
TEST(["CS2011","COMM1071","ANNP8020"])
### OLD TEST ###
#print permuteAll(["CS2011","COMM1071","ENGL4092"])
