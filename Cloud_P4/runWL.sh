spark-submit --master yarn-client --num-executors 20 avgWordLength.py hdfs://hadoop2-0-0/data/1gram/* > avgWLs.txt
