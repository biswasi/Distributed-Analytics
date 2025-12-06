from pyspark.sql import SparkSession

from datetime import datetime, date 
import pandas as pd 
from pyspark.sql import Row 
from pyspark.sql import SparkSession 

spark = SparkSession.builder.getOrCreate()

df = spark.createDataFrame([ 
    Row(a=1, b=4., c='GFG1', d=date(2000, 8, 1), 
        e=datetime(2000, 8, 1, 12, 0)), 
    
    Row(a=2, b=8., c='GFG2', d=date(2000, 6, 2),  
        e=datetime(2000, 6, 2, 12, 0)), 
    
    Row(a=4, b=5., c='GFG3', d=date(2000, 5, 3), 
        e=datetime(2000, 5, 3, 12, 0)) 
]) 

df.show() 
df.printSchema() 

employee_data = [("1","John",28,5000),
                 ("2","Smith",30,6000),
                 ("3","Adam",35,4000),
                 ("4","Henry",40,7000)]

employee_rdd = spark.createDataFrame(employee_data, ["ID", "Name", "Age", "Salary"])
print("Creating Employee DataFrame ")

#filtered_rdd = employee_rdd.filter(lambda x: x[3] > 4000)
filtered_rdd = employee_rdd.filter(employee_rdd.Salary > 3000)
print(filtered_rdd.collect())

dataRDD = [("Assignment", 1),	

  ("Ruderford", 1),	

  ("Manik", 1),	

  ("Travelling", 1)]

rdd1 = spark.sparkContext.parallelize(dataRDD)	
rdd2 = rdd1.reduceByKey(lambda a,b :a+b)
for element in rdd2.collect():
   print(element)
