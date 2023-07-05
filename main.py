# main.py

from pyspark.sql import SparkSession
import os
from dotenv import load_dotenv
from transformations import my_transformation

# Load environment variables from .env file
load_dotenv()

# Set AWS credentials
AWS_ACCESS_KEY_ID = os.getenv('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = os.getenv('AWS_SECRET_ACCESS_KEY')

# Initialize Spark session
spark = SparkSession.builder \
    .appName("CSV to Parquet") \
    .config("spark.jars.packages", "org.apache.hadoop:hadoop-aws:3.3.1") \
    .getOrCreate()

# Configure S3 access
spark.conf.set("spark.hadoop.fs.s3a.access.key", AWS_ACCESS_KEY_ID)
spark.conf.set("spark.hadoop.fs.s3a.secret.key", AWS_SECRET_ACCESS_KEY)
spark.conf.set("spark.hadoop.fs.s3a.impl", "org.apache.hadoop.fs.s3a.S3AFileSystem")
spark.conf.set("spark.hadoop.fs.s3a.path.style.access", True)

# Read CSV file from S3
source_bucket = "vs-testlocal-source"
source_key = "faker_data.csv"
df = spark.read.format('csv') \
    .option('header', 'true') \
    .option('inferSchema', 'true') \
    .load(f's3a://{source_bucket}/{source_key}')

# Apply transformation
target_bucket = "vp-testlocal-target"
target_key = "faker_data"
my_transformation(df, target_bucket, target_key)
