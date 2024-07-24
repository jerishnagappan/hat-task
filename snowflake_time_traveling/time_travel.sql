use schema powerbi;
 
 
create or replace table student(
id INT AUTOINCREMENT PRIMARY KEY,
name string
 
)
data_retention_time_in_days = 1 ;
 
INSERT INTO student (NAME) VALUES
('jerry'),('happy'), ('raina'),('jadeja');
 
select * from student;
 
show tables  like 'student';
 
 
-- select * from "POWERBI"."INFORMATION_SCHEMA"."TABLES" where table_name = 'student';
 
 
 
SELECT COUNT(*) FROM STUDENT;
 
 
UPDATE STUDENT
SET NAME = 'jeni'
WHERE ID = 2;
UPDATE STUDENT
SET NAME = 'TEN'
WHERE ID = 1;
 
 
-- 01b5e228-0000-b0ac-0007-9aee00028116
 
SELECT * FROM STUDENT;
 
 
update
 
 
DELETE FROM STUDENT WHERE NAME = 'KIRAN';
 
 
SELECT COUNT(*) FROM STUDENT;
 
 
SELECT * FROM STUDENT at(statement => '01b5e223-0000-b0ad-0007-9aee00025c36');




drop table student;
 
undrop table student;
 
 
select * from student;