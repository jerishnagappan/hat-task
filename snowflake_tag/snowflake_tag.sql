CREATE OR REPLACE TAG sensitive_data;
CREATE OR REPLACE TAG project_alpha;
 
 
CREATE OR REPLACE TABLE sales_data (
    sale_id INT,
    customer_name STRING,
    amount DECIMAL(10, 2),
    sale_date DATE
);
 
CREATE OR REPLACE TABLE customer_info (
    customer_id INT,
    customer_name STRING,
    email STRING,
    phone STRING
);
 
-- Apply Tags to Tables
ALTER TABLE sales_data SET TAG sensitive_data = 'confidential';
ALTER TABLE sales_data SET TAG project_alpha = 'sales_project';
 
ALTER TABLE customer_info SET TAG sensitive_data = 'customer_info';
 
-- Create a Virtual Warehouse
CREATE OR REPLACE WAREHOUSE demo_warehou
    WAREHOUSE_SIZE = 'SMALL'
    AUTO_SUSPEND = 60
    AUTO_RESUME = TRUE;
 
-- Apply Tags to Warehouse
ALTER WAREHOUSE demo_warehou SET TAG project_alpha = 'warehouse_for_project';
ALTER WAREHOUSE demo_warehou SET TAG sensitive_data = 'confidential';
 
 
-- List All Tags
SHOW TAGS;
 
 
-- Remove Tags from Tables
ALTER TABLE sales_data UNSET TAG sensitive_data;
ALTER TABLE sales_data UNSET TAG project_alpha;
 
ALTER TABLE customer_info UNSET TAG sensitive_data;
 
-- Remove Tags from Warehouse
ALTER WAREHOUSE demo_warehouse UNSET TAG project_alpha;
ALTER WAREHOUSE demo_warehouse UNSET TAG sensitive_data;
 
 
 
 
 
-- List All Tags
SHOW TAGS;
 
-- Check Tags on Specific Object
SELECT *
FROM INFORMATION_SCHEMA.TAG_REFERENCES
WHERE OBJECT_NAME = 'SALES_DATA';
 
-- Check Tags on All Tables
SELECT *
FROM INFORMATION_SCHEMA.TAG_REFERENCES
WHERE OBJECT_TYPE = 'TABLE';
 