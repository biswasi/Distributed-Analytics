# importing window from pyspark.sql.window
from pyspark.sql.window import Window

# importing aggregate functions
# from pyspark.sql.functions
from pyspark.sql.functions import col,avg,sum,min,max,row_number 
spark = SparkSession.builder.appName("pyspark_window").getOrCreate()

# sample data for dataframe
sampleData = (("Ram", 28, "Sales", 3000),
              ("Meena", 33, "Sales", 4600),
              ("Robin", 40, "Sales", 4100),
              ("Kunal", 25, "Finance", 3000),
              ("Ram", 28, "Sales", 3000),
              ("Srishti", 46, "Management", 3300),
              ("Jeny", 26, "Finance", 3900),
              ("Hitesh", 30, "Marketing", 3000),
              ("Kailash", 29, "Marketing", 2000),
              ("Sharad", 39, "Sales", 4100)
              )

# column names for dataframe
columns = ["Employee_Name", "Age",
           "Department", "Salary"]
# creating the dataframe df
df = spark.createDataFrame(data=sampleData,
                           schema=columns)

# creating a window partition of dataframe
windowPartitionAgg = Window.partitionBy("Department").orderBy("Age")
# print schema
df.printSchema()
# show df
df.show()

# applying window aggregate function
# to df3 with the help of withColumn

# this is average()
df3.withColumn("Avg", 
               avg(col("salary")).over(windowPartitionAgg))
    #this is sum()
  .withColumn("Sum",
              sum(col("salary")).over(windowPartitionAgg))
    #this is min()
  .withColumn("Min",
              min(col("salary")).over(windowPartitionAgg))
    #this is max()
  .withColumn("Max", 
              max(col("salary")).over(windowPartitionAgg)).show()
