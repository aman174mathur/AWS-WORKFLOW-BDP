# AWS-WORKFLOW-BDP:
This project demonstrates a production-grade data pipeline that ingests semi-structured GitHub Archive data,
processes it at scale using Apache Spark on AWS EMR, 
and loads the refined data into Amazon Redshift for analytical querying and BI.

# Architecture Flow
Local System → Amazon S3 → AWS EMR (Spark) → Temporary S3 Location → Amazon Redshift

# 🏗️ Architecture :
Ingestion: GitHub Archive (JSON) files are stored in Amazon S3 (Data Lake).

Processing: AWS EMR (Spark Cluster) reads the raw data, performs transformations, and filters events.

Intermediate Storage: Transformed data is staged in a temporary S3 bucket (required for Redshift COPY command).

Data Warehousing: The final structured data is loaded into Amazon Redshift for high-performance SQL analytics.


# 🛠️ Tech Stack
Cloud: AWS (S3, EMR, Redshift, IAM)

Processing: PySpark (Apache Spark)

IDE: VS Code (Remote SSH connection to EMR Master Node)

Format: JSON (Raw), Parquet/JDBC (Processed)


# 🚀 Step-by-Step Implementation
# 1. Infrastructure Setup
AWS EMR: Launched a cluster with m5.xlarge instances. Configured Security Groups to allow inbound SSH (Port 22) and Redshift (Port 5439).

Redshift: Set up a cluster and created the target schema.

IAM Roles: Configured roles to allow EMR to read/write to S3 and allow Redshift to access S3 for the COPY operation.

<img width="1920" height="1032" alt="Screenshot 2026-01-11 193936" src="https://github.com/user-attachments/assets/9afc7c62-2180-47f3-8f7a-fec1cf0266d4" />

# 2. Development Workflow : 
To ensure a seamless development experience, I connected VS Code directly to the EMR Master Node via the Remote - SSH extension. This allowed for:

Real-time script editing on the cluster.

Direct execution of spark-submit jobs.

<img width="1920" height="1080" alt="Screenshot 2026-01-11 194216" src="https://github.com/user-attachments/assets/ab15a72e-14ff-48d8-b47a-0177476dcef8" />
<img width="1920" height="1080" alt="Screenshot 2026-01-11 194846" src="https://github.com/user-attachments/assets/349172db-9010-455e-ad01-a28b3ac7f3f5" />

# 3. Data Transformation (PySpark)
The core logic performs the following:

Filtering: Focused on PushEvent types to analyze developer activity.

Flattening: Extracted nested JSON fields (e.g., actor.login, repo.name).

Optimization: Utilized a temporary S3 directory for the Redshift Spark Connector to ensure efficient data transfer.

<img width="1920" height="1080" alt="Screenshot 2026-01-11 195050" src="https://github.com/user-attachments/assets/5c9fc0bd-fa30-42fc-b686-bbbb5a7a46f7" />
<img width="1920" height="1080" alt="Screenshot 2026-01-11 194938" src="https://github.com/user-attachments/assets/72c88bc8-8519-4c49-b1ed-1da931f75203" />

# 4 : Write Transformed Data to Temp S3
Stored the transformed data in a temporary S3 location in Parquet format for optimized loading.
<img width="1920" height="1080" alt="Screenshot 2026-01-11 194955" src="https://github.com/user-attachments/assets/9ce8df7a-176f-4ffa-88c7-6f86cb1b9030" />

# 5: Redshift Serverless Setup (Workgroup & Namespace)
Created an Amazon Redshift Serverless namespace and workgroup to manage database resources and compute independently.
<img width="1920" height="1080" alt="Screenshot 2026-01-11 195310" src="https://github.com/user-attachments/assets/48e4a04f-5916-482a-b816-c83f8c05949d" />
<img width="1920" height="1080" alt="Screenshot 2026-01-11 195301" src="https://github.com/user-attachments/assets/377145e6-c643-40ab-9de9-e51f5747d27d" />

# 6 : Redshift Table Creation and Data Validation
Created target tables in Amazon Redshift Query Editor based on the transformed schema and Validate the loaded data by running analytical queries in Amazon Redshift.
<img width="1920" height="1080" alt="Screenshot 2026-01-11 195608" src="https://github.com/user-attachments/assets/e0a2fdbc-925b-4481-bd8c-c99829e882a3" />


📊 Business Use Cases
With the data in Redshift, you can answer questions like:

Which GitHub repositories have the highest commit frequency?

What are the peak hours for developer activity globally?

Trends in programming language popularity based on repository activity.





