Cloud_P1
========

Creates an event for weekly schedule

This service takes in 4 different parameters and outputs an ics file usable by Google Calendar, iCalendar, etc.

This service is meant for creating an event which can occur multiple times per week, similar to a class. Eventually, this service can be expanded to have users generate their entire class schedule for a semester, if used in combination with UC's course selection tool. 

### Parameters: ###
  * eName (string): Event name for this event
  * start (string/time): Starting time for event (12-hour time format i.e. 1:00 AM, 11:23 PM, 6:42 AM, NOT 02:34 AM, 2:23 pm, 13:25)
  * end (string/time): Ending time for event (12-hour time format i.e. 1:00 AM, 11:23 PM, 6:42 AM)
  * Days[] (string/array): Days in the week on which the event occurs (M, T, W, R, F: must have at least one day, no more than 5, no duplicates)
  
This service is interacted through curl, with example commands listed below.

### Commandline: ###

<pre>
curl -o testcal.ics --globoff --data "Days[]=M&Days[]=W&Days[]=F&start=2:30 PM&end=3:30 PM&eName=Test Event" "localhost"
</pre>

The example listed above creates an event called Test Event which runs from 2:30 PM to 3:30 PM (EST) on Monday, Wednesday, and Friday, and returns that event in an ics file called "testcal.ics"

  * -o filename: Downloads the file as an ics file with the given name. This param is REQUIRED. Filename is up to the user, but be sure to include the .ics extension
  
  * --globoff: Allows for the parsing of the data string for square brackets. This param is REQUIRED.
  
  * --data "param1=value1&param2=value2&...": Contains the data to be sent to the web service via POST. Because Days is an array, you define the elements in the array by "array[]=value1&array[]=value2&..." This param is REQUIRED.
  
  * "hostname/filename": This is the file and path to the file that curl is POSTing the data to. For this service, since the docker image will be run on one's own machine, the host is "localhost", and the file is "time.php", thus needing a hostpath of "localhost/time.php" This param is REQUIRED.

### Future Work ###

This service will eventually be expanded such that the user will be able to:
* Request for certain courses, which will be added to the schedule
* Generate a class schedule to be imported into your Google Calendar or iCalendar
* Automatically create said schedule given a list of courses and times
* Notify the user if a schedule can't be created with the classes given

### Example Output ###
<pre>
BEGIN:VCALENDAR
VERSION:2.0
PRODID:-//hacksw/handcal//NONSGML v1.0//EN
CALSCALE:GREGORIAN
BEGIN:VTIMEZONE
TZID:America/New_York
X-LIC-LOCATION:America/New_York
BEGIN:DAYLIGHT
TZOFFSETFROM:-0500
TZOFFSETTO:-0400
TZNAME:EDT
DTSTART:19700308T020000
RRULE:FREQ=YEARLY;BYMONTH=3;BYDAY=2SU
END:DAYLIGHT
BEGIN:STANDARD
TZOFFSETFROM:-0400
TZOFFSETTO:-0500
TZNAME:EST
DTSTART:19701101T020000
RRULE:FREQ=YEARLY;BYMONTH=11;BYDAY=1SU
END:STANDARD
END:VTIMEZONE
BEGIN:VEVENT
UID:56bce28cf2028
DTSTAMP:20160211T193540Z
SUMMARY:Test Event
DTSTART:20150105T193000Z
DTEND:20150105T203000Z
END:VEVENT
BEGIN:VEVENT
UID:56bce28cf2186
DTSTAMP:20160211T193540Z
SUMMARY:Test Event
DTSTART:20150107T193000Z
DTEND:20150107T203000Z
END:VEVENT
BEGIN:VEVENT
UID:56bce28cf2401
DTSTAMP:20160211T193540Z
SUMMARY:Test Event
DTSTART:20150109T193000Z
DTEND:20150109T203000Z
END:VEVENT
END:VCALENDAR
</pre>
