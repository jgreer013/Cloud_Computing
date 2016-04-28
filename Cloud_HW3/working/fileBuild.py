#!/usr/bin/env python

from datetime import datetime
import time

# Changes time string to seconds for Epoch
def convertTime(time):
  hour = int(time[:2])
  minute = int(time[3:])
  return 60*60*hour + 60*minute

# Shifts time by day (M-F -> 0-4)
def shiftDay(time, day):
  return int(time) + 24*60*60*int(day)

# Converts time variable to time format for ics files
def convertToICS(time_var):
  dt = time.strftime('%Y%m%dT%H%M%S', time.localtime(time_var))
  return dt

# Converts numerical days to their string values for ics files
def convertDays(dayArr):
  arr = ["MO","TU","WE","TH","FR"]
  fin = []
  for each in dayArr:
    fin.append(arr[int(each)])
  return fin

# Adds an event to the eventString (file to be downloaded)
def addEvent(name, start, end, days, eventString):
  res = ""
  res += eventString
  start_time = datetime.strftime(datetime.strptime(start, '%I:%M %p'), "%H:%M %p")[:-3]
  end_time = datetime.strftime(datetime.strptime(end, '%I:%M %p'), "%H:%M %p")[:-3]
  base_time = 1420434000
  fin_time = base_time + 5*24*60*60
  stamp = convertToICS(time.time())
  res += "BEGIN:VEVENT\n"
  st = convertToICS(shiftDay(convertTime(start_time), days[0]) + base_time)
  en = convertToICS(shiftDay(convertTime(end_time), days[0]) + base_time)
  res += "UID:" + str(days[0]) + str(st) + '\n'
  res += "DTSTAMP:" + stamp + 'Z\n'
  res += "SUMMARY:" + name + '\n'
  res += "DTSTART:" + str(st) + 'Z\n'
  res += "RRULE:FREQ=WEEKLY;UNTIL=" + str(convertToICS(fin_time)) + ";WKST=SU;BYDAY="
  dayStr = convertDays(days)
  for each in dayStr:
    res += each + ','
  res = res[:-1] + '\n'
  res += "DTEND:" + str(en) + "Z\n"
  res += "END:VEVENT\n"
  return res 

