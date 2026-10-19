import os
import sys
from pyspark.sql import SparkSession

os.environ["PYSPARK_PYTHON"] = sys.executable
os.environ["PYSPARK_DRIVER_PYTHON"] = sys.executable

spark = (
    SparkSession.builder
    .master("local[*]")
    .appName("check")
    .getOrCreate()
)

print("Spark version:", spark.version)
print("Rows:", spark.range(1_000_000).count())
spark.stop()
