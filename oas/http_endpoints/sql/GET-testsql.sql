/* Getting Started:
Enter "USE {database};" before entering your SQL statements.
Type "--your question" + Enter to try out AI-generated SQL queries
Declare a parameter like "Where id = ${arg}".
*/
with t2 as (with t1 as (select * from test.repository) select * from t1) select * from t2 ;