#transformations.py

def my_transformation(df, target_bucket, target_key):
    # Write DataFrame to Parquet on S3
    #df.write.parquet(f's3a://{target_bucket}/{target_key}')
    df = df.drop('product_name')
    df.coalesce(1).write.parquet(f's3a://{target_bucket}/{target_key}')

