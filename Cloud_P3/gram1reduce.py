#!/usr/bin/env python

import sys

prev_year = ""
year_total = 1
year_len = 0

for line in sys.stdin:
  year, total_count, total_len = line[:-1].split('\t')
  if year == prev_year:
    year_total += int(total_count)
    year_len += int(total_len)
  else:
    if prev_year != "":
      print prev_year + '\t' + str(year_total) + '\t' + str(year_len/float(year_total))
    prev_year = year
    year_total = int(total_count)
    year_len = int(total_len)
