from pyspark.sql import SparkSession
from pyspark.sql import functions as F
from pyspark.sql.functions import col, explode, window
from pyspark.sql.functions import split

spark = SparkSession.builder \
            .appName("StructuredNetworkWordCount") \
            .getOrCreate()

# Create DataFrame representing the stream of input lines from connection to localhost:9999
lines = spark \
    .readStream \
    .format("socket") \
    .option("host", "host.docker.internal") \
    .option("port", 9999) \
    .option("includeTimestamp", "true") \
    .load()

words = lines.select(
    explode(split(lines.value, " ")).alias("word"),
    "timestamp"
)


# Generate running word count with a sliding window of 5 seconds and a slide duration (overlap) of 2 seconds
wordCounts = words.groupBy(
    window(col("timestamp"), "5 seconds", "2 seconds"), 
    col("word")
    ).count()

# Format window boundaries so time is visible in console output.
output_df = wordCounts.select(
    F.date_format(col("window.start"), "HH:mm:ss").alias("time"),
    col("word"),
    col("count")
)
    
 # Start running the query that prints the running counts to the console
query = output_df \
    .writeStream \
    .outputMode("update") \
    .format("console") \
    .trigger(processingTime="3 seconds") \
    .start()

query.awaitTermination()