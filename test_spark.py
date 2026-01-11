from pyspark.sql import SparkSession
import boto3
import json

def get_secret(secret_name, region_name='ap-south-1'):
    """Retrieve secret from AWS Secrets Manager"""
    client = boto3.client('secretsmanager', region_name=region_name)
    response = client.get_secret_value(SecretId=secret_name)
    return json.loads(response['SecretString'])

def create_spark_session():
    """Create Spark session with JDBC driver only"""
    spark = SparkSession.builder \
        .appName("Redshift-JDBC-Simple") \
        .config("spark.jars.packages", "com.amazon.redshift:redshift-jdbc42:2.1.0.26") \
        .getOrCreate()
    return spark

def read_redshift_jdbc(spark, creds, table_name):
    """
    Read Redshift table using pure JDBC (NO S3 NEEDED)
    
    Pros: Simple, no S3 required
    Cons: Slower for large tables
    """
    jdbc_url = f"jdbc:redshift://{creds['host']}:{creds['port']}/{creds['dbname']}"
    
    df = spark.read \
        .format("jdbc") \
        .option("url", jdbc_url) \
        .option("dbtable", table_name) \
        .option("user", creds['username']) \
        .option("password", creds['password']) \
        .option("driver", "com.amazon.redshift.jdbc42.Driver") \
        .load()
    
    return df

# Main execution
if __name__ == "__main__":
    SECRET_NAME = "demo/resshiftwh/aman"
    REGION_NAME = "ap-south-1"
    TABLE_NAME = "public.employees"
    
    # Get credentials
    print("Retrieving credentials...")
    creds = get_secret(SECRET_NAME, REGION_NAME)
    
    if not creds:
        print("Failed to retrieve credentials")
        exit(1)
    
    print(f"✓ Credentials retrieved for: {creds['username']}")
    
    # Create Spark session
    print("Creating Spark session...")
    spark = create_spark_session()
    print("✓ Spark session created")
    
    try:
        # Read data from Redshift (NO S3 NEEDED!)
        print(f"\nReading table: {TABLE_NAME}")
        df = read_redshift_jdbc(spark, creds, TABLE_NAME)
        
        # Display schema
        print("\nTable Schema:")
        df.printSchema()
        
        # Show data
        print("\nFirst 20 rows:")
        df.show(20, truncate=False)
        
        # Get count
        print(f"\nTotal rows: {df.count()}")
        
        # Perform Spark operations
        print("\n--- Spark SQL Example ---")
        df.createOrReplaceTempView("my_redshift_table")
        
        result = spark.sql("""
            SELECT COUNT(*) as total_records
            FROM my_redshift_table
        """)
        result.show()
        
        # Filter example
        print("\n--- Filter Example ---")
        # Replace 'column_name' with actual column from your table
        # filtered_df = df.filter(df['column_name'] > 100)
        # filtered_df.show()
        
    except Exception as e:
        print(f"✗ Error: {e}")
        import traceback
        traceback.print_exc()
    
    finally:
        print("\nStopping Spark session...")
        spark.stop()
        print("✓ Done!")