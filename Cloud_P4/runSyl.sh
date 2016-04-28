spark-submit --master yarn-client --num-executors 20 avgSyl.py hdfs://hadoop2-0-0/data/1gram/* > avgSyls.txt
