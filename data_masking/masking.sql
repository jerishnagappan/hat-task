CREATE TABLE customer_info (
    customer_id INTEGER,
    customer_name VARCHAR(100),
    email VARCHAR(100)
);
 
INSERT INTO customer_info (customer_id, customer_name, email)
VALUES
    (1, 'John Doe', 'john.doe@example.com'),
    (2, 'Jane Smith', 'jane.smith@example.com');
 
    
select * from customer_info;
 
 
CREATE VIEW masked_customers_info AS
SELECT
    customer_id,customer_name,
    CASE
        WHEN CURRENT_ROLE() IN ('ROLE_WITH_ACCESS_TO_SENSITIVE_DATA') THEN email
        ELSE '***@*****.com' 
    END AS email_masked
FROM
    customer_info;