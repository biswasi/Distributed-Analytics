import findspark
findspark.init()
from pyspark import SparkConf, SparkContext
from pyspark.sql import SparkSession

#conf = SparkConf().setMaster("local").setAppName("RddPractice")
sc = SparkContext.getOrCreate()


employee_data = [("1","John",28,5000),
                 ("2","Smith",30,6000),
                 ("3","Adam",35,4000),
                 ("4","Henry",40,7000)]
#spark = SparkSession.builder.appName("RddPractice").getOrCreate()
                 
#employee_rdd = sc.createDataFrame(employee_data, ["ID", "Name", "Age", "Salary"])
print("Creating DataFrame ")

employee_rdd = sc.parallelize(employee_data)
filtered_rdd = employee_rdd.filter(lambda x: x[3] > 4000)
print(filtered_rdd.collect())



