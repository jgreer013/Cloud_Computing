#!/usr/bin/env python

import schedInfo
import datetime
import time
import calendar
# For a section to be valid, its dates and times cannot both overlap with any other section. Checking this will require maintaining the section's id throughout the check process, 

def valTup(tup1, tup2):
  if tup1[0] <= tup2[1] and tup1[1] >=  tup2[0]:
    return False
  else:
    return True

def valDay(tup1, tup2):
  if len(set(tup1).intersection(tup2)) == 0:
    return True
  else:
    return False

# convertDates from uc format
def convertDates(date_tup):
  months = {"Jan":1,"Feb":2,"Mar":3,"Apr":4,"May":5,"Jun":6,"Jul":7,"Aug":8,"Sep":9,"Oct":10,"Nov":11,"Dec":12}
  ret = []
  for date in date_tup:
    month, day = date.strip().split(" ")
    monthInt = months[month]
    dt = str(monthInt) + "-" + str(day) + "-" + str(datetime.datetime.today().year)
    stamp = int(calendar.timegm(datetime.datetime.strptime(dt,"%m-%d-%Y").timetuple()))
    ret.append(stamp)
  return ret

# convertTimes from uc format
def convertTimes(time_tup):
  ret = []
  for time in time_tup:
    time = time + "m"
    hr, mn = datetime.datetime.strftime(datetime.datetime.strptime(time, '%I:%M%p'), "%H:%M %p")[:-3].split(":")
    ret.append(60*60*int(hr) + 60*int(mn))
  return ret
    

# We need a list of lists containing a trio of tuples containing pairs of dates and times, as well as the days it takes place [[(start_date,end_date),(start_time,end_time),(day,day,day)],[(start_date2,end_date2),(start_time2,end_time2),(day2,day2,day2)]]
# This is necessary in order to ensure that no false positives occur. Each time needs to be paired with its respective date, and both date and time need to be invalid together to be considered invalid.
# Otherwise we would have problems where both a time and date were considered invalid in their respective lists, but since they pertained to two separate classes, they actually would have been valid.
# Valid == (TimeValid) || (DateValid)
# If times overlap but dates do not, the classes are fine (session A, session B)
# If dates overlap but times do not, the classes are fine (normal case)
# If both overlap, PROBLEM

def valSect(newSect, currentSects):
  newDateTimes = schedInfo.getSchedInfo(newSect)
  curDateTimes = []
  for sect in currentSects:
    curDateTimes.extend(schedInfo.getSchedInfo(sect))
  for ndt in newDateTimes:
    date_tuple = convertDates(ndt[0])
    time_tuple = convertTimes(ndt[1])
    day_tuple = ndt[2]
    for cdt in curDateTimes:
      date_tuple2 = convertDates(cdt[0])
      time_tuple2 = convertTimes(cdt[1])
      day_tuple2 = cdt[2]
      if valTup(date_tuple, date_tuple2) == False and (valTup(time_tuple, time_tuple2)  == False and valDay(day_tuple, day_tuple2) == False):
        return False
  return True

def valTogether(allSects):
  valid = []
  for sect in allSects:
    if valSect(sect, valid) == True:
      valid.append(sect)
    else:
      return False
  return True

