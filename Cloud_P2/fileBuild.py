#!/usr/bin/env python

from datetime import datetime
import time
import calendar
from validatePermute import convertDates, convertTimes
import classDict
import schedInfo


# Shifts time by day (M-F -> 0-4)
def shiftDay(time, day): 
  return int(time) + 24*60*60*int(day)

# Converts time variable to time format for ics files
def convertToICS(time_var):
  dt = time.strftime('%Y%m%dT%H%M%S', time.localtime(time_var))
  return dt

# Converts numerical days to their string values for ics files
def convertDays(dayArr):
  arr = {"M":"MO","T":"TU","W":"WE","R":"TH","F":"FR","S":"SA","U":"SU"}
  fin = []
  for each in dayArr:
    fin.append(arr[each])
  return fin

# Adds an event to the eventString (file to be downloaded)
def addEvent(name, start, end, days, start_date, end_date):
  res = ""
  di = {"M":0,"T":1,"W":2,"R":3,"F":4,"S":5,"U":6}
  stamp = convertToICS(time.time())
  res += "BEGIN:VEVENT\n"
  base_time = start_date+(time.gmtime().tm_hour - time.localtime().tm_hour)*60*60
  fin_time = end_date+(time.gmtime().tm_hour - time.localtime().tm_hour)*60*60+(24*60*60)
  st = convertToICS(shiftDay(start, di[days[0]]) + base_time)
  en = convertToICS(shiftDay(end, di[days[0]]) + base_time)
  res += "UID:" + str(days[0]) + str(st) + '\n'
  res += "DTSTAMP:" + stamp + 'Z\n'
  res += "SUMMARY:" + name + '\n'
  res += "DTSTART:" + str(st) + '\n'
  res += "RRULE:FREQ=WEEKLY;UNTIL=" + str(convertToICS(fin_time)) + ";WKST=SU;BYDAY="
  dayStr = convertDays(days)
  for each in dayStr:
    res += each + ','
  res = res[:-1] + '\n'
  res += "DTEND:" + str(en) + "\n"
  res += "END:VEVENT\n"
  return res 

def buildFile(listOfSections, sectD):
  fill = "BEGIN:VCALENDAR\n" + "VERSION:2.0\n" + "PRODID:-//hacksw/handcal//NONSGML v1.0//EN\n" + "CALSCALE:GREGORIAN\n"
  for sect in listOfSections:
    cName = sectD[sect][0]
    timing = schedInfo.getSchedInfo(sect)
    for t in timing:
      if len(t) == 0:
        continue
      elif ('TBA',) in t:
        continue
      else:
        st, en = convertTimes(t[1])
        st_dt, en_dt = convertDates(t[0])
        dys = t[2]
        fill += addEvent(cName, st, en, dys, st_dt, en_dt)
  return fill + "END:VCALENDAR\n"
  
      
    
    
