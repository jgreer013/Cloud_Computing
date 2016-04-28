#!/bin/sh
spark-submit --master yarn-client --num-executors 15 Twitter6.py > twitter.txt
