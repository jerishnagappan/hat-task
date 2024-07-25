list @powerbi.powerBI.powerbi_stg;
 
create or replace file format outputs
type='csv'
compression = 'auto'
field_delimiter =','
field_optionally_enclosed_by= '\042'
parse_header = true;
 
 
select * from table(
infer_schema(location=>'@powerbi_stg/outputs.csv',
file_format => 'outputs'));
 
 
create or replace table patent
using template(
select array_agg(object_construct(*))
from table(
infer_schema(
location=>'@powerbi_stg/outputs.csv',
file_format => 'outputs')));
 
 
copy into patent
from @powerbi_stg/outputs.csv
file_format= (format_name ='outputs')
match_by_column_name= case_insensitive;
 
select * from patent;
 
show tables;
alter table patent set enable_schema_evolution = TRUE;
show tables;
 
select * from patent;
 
 
SELECT * FROM patent;
 
 
SHOW COLUMNS IN TABLE patent;
 
DESC TABLE POWERBI.PATENT;