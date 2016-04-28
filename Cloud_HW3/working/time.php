<?php
  // Converts time (12:00 PM, 1:35 AM, etc) to seconds (12:00 AM converts to 0, adds up after that)
  // Seconds is required for ics files
  function validateTimeFormat($time) {
    if (gettype($time) != "string" || preg_match("/^([1-9]|1[012]):[0-5][0-9]( A| P)M/",$time) != 1) {
      return false;
    } else {
      return true;
    }
  }

  function validateTimes($start_time, $end_time) {
    if (validateTimeFormat($start_time) == false || validateTimeFormat($end_time) == false) {
      exit("Invalid Time Format. Please use h:mm A/PM to represent times.");
    }
  }

  function validateDayFormat($day) {
    if (gettype($day) != "string" || preg_match("/^[MTWRF]$/", $day) != 1) {
      return false;
    } else {
      return true;
    }
  }

  function validateDayArray($days) {
    if (gettype($days) != "array" || count($days) == 0) {
      exit("Invalid Day Format. Please use MTWRF to represent Monday-Friday.");
    } elseif (count(array_unique($days)) != count($days)) {
      exit("Array cannot contain duplicates.");
    } elseif (count($days) > 5) {
      exit("Array can only contain up to 5 values.");
    } else {
      for($i = 0; $i < count($days); $i++) {
        if (validateDayFormat($days[$i]) == false) {
          exit("Invalid Day Format. Please use MTWRF to represent Monday-Friday.");
        }
      }
    }
  }

  function validateEvent($ev) {
    if (gettype($ev) != "string") {
      exit("Invalid Event Format. Please enter a string.");
    }
  }

  function convertDays($days) {
    for ($i = 0; $i < count($days); $i++) {
      $letter = $days[$i];
      if ($letter == "M") {
        $arr[$i] = 0;
      } elseif ($letter == "T") {
        $arr[$i] = 1;
      } elseif ($letter == "W") {
        $arr[$i] = 2;
      } elseif ($letter == "R") {
        $arr[$i] = 3;
      } elseif ($letter == "F") {
        $arr[$i] = 4;
      }
    }
    return $arr;
  }

  function convertTime($hhmm) {
    $apm = substr($hhmm, -2);
    $arr = explode(':', substr($hhmm, 0, -3)); // Takes everything but the last 3 characters " AM" " PM"
    for($i = 0; $i < count($arr); $i++) {
      $nums[$i] = (int)$arr[$i];
    }
    if ($nums[0] < 12 && $apm == "PM") {
      $nums[0] = $nums[0]+12;
    } elseif ($nums[0] == 12 && $apm == "AM") {
      $nums[0] = 0;
    }
    $secs = $nums[0]*60*60 + $nums[1]*60;
    return $secs;
  }

  // $day is an int with 0 representing Monday, 1 being Tuesday, and so on
  // Shifts the time point by the day times 24 hours (in keeping with unix seconds)
  function shiftDay($secs, $day) {
    return $secs + $day*24*60*60;
  }

  // Makes the ics file use Monday, January 5, 2015 12:00 AM EST as the week for schedules
  function shiftWeek($time) {
    return $time + 1420434000;
  }

  // Function to output ics file altered from https://gist.github.com/jakebellacera/635416
  function createICS($event, $startArray, $endArray) {
    // Variables used in this script:
    //   $summary     - text title of the event
    //   $datestart   - the starting date (in seconds since unix epoch)
    //   $dateend     - the ending date (in seconds since unix epoch)
    //   $address     - the event's address
    //   $uri         - the URL of the event (add http://)
    //   $description - text description of the event
    //   $filename    - the name of this file for saving (e.g. my-event-name.ics)

    // 1. Set the correct headers for this file
    $filename = "justkidding.ics";
    header('Content-type: text/calendar; charset=utf-8');
    header('Content-Disposition: attachment; filename=' . $filename);

    // 2. Define helper functions
    function dateToCal($timestamp) {
      return date('Ymd\THis\Z', $timestamp);
    }

    // Escapes a string of characters
    function escapeString($string) {
      return preg_replace('/([\,;])/','\\\$1', $string);
    }
    
    // Print header of ics
    // Also timezone portion just in case
    echo "BEGIN:VCALENDAR\n";
    echo "VERSION:2.0\n";
    echo "PRODID:-//hacksw/handcal//NONSGML v1.0//EN\n";
    echo "CALSCALE:GREGORIAN\n";
    echo "BEGIN:VTIMEZONE\n";
    echo "TZID:America/New_York\n";
    echo "X-LIC-LOCATION:America/New_York\n";
    echo "BEGIN:DAYLIGHT\n";
    echo "TZOFFSETFROM:-0500\n";
    echo "TZOFFSETTO:-0400\n";
    echo "TZNAME:EDT\n";
    echo "DTSTART:19700308T020000\n";
    echo "RRULE:FREQ=YEARLY;BYMONTH=3;BYDAY=2SU\n";
    echo "END:DAYLIGHT\n";
    echo "BEGIN:STANDARD\n";
    echo "TZOFFSETFROM:-0400\n";
    echo "TZOFFSETTO:-0500\n";
    echo "TZNAME:EST\n";
    echo "DTSTART:19701101T020000\n";
    echo "RRULE:FREQ=YEARLY;BYMONTH=11;BYDAY=1SU\n";
    echo "END:STANDARD\n";
    echo "END:VTIMEZONE\n";

    // 3. Echo out the ics file's contents
    for ($i = 0; $i < count($startArray); $i++) {
      $datestart = $startArray[$i];
      $dateend = $endArray[$i];
      $summary = $event;
      
      echo "BEGIN:VEVENT\n";
      echo "UID:".uniqid()."\n";
      echo "DTSTAMP:".dateToCal(time())."\n";
      echo "SUMMARY:".escapeString($summary)."\n";
      echo "DTSTART:".dateToCal($datestart)."\n";
      echo "DTEND:".dateToCal($dateend)."\n";
      echo "END:VEVENT\n";
      
    }
    echo "END:VCALENDAR\n";
  }
  validateEvent($_POST["eName"]);
  validateTimes($_POST["start"], $_POST["end"]);
  validateDayArray($_POST["Days"]);
  $days = convertDays($_POST["Days"]);
  $start = convertTime($_POST["start"]);
  $end = convertTime($_POST["end"]);

  if ($start >= $end) {
    exit("Invalid Times. End time must occur after start time.");
  } else {
    for ($i = 0; $i < count($days); $i++) {
      $start_times[$i] = shiftWeek(shiftDay($start, $days[$i]));
      $end_times[$i] = shiftWeek(shiftDay($end, $days[$i]));
    }
    $event = $_POST["eName"];

    createICS($event, $start_times, $end_times);
  }
?>
