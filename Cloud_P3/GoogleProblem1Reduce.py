#!/usr/bin/env python

import sys

prev_year = ""
year_total = 1

for line in sys.stdin:
  year, total_count = line[:-1].split('\t')
  if year == prev_year:
    year_total += int(total_count)
  else:
    if prev_year != "":
      print prev_year + '\t' + str(year_total)
    prev_year = year
    year_total = int(total_count)
