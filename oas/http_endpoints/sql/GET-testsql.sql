/* Getting Started:
Enter "USE {database};" before entering your SQL statements.
Type "--your question" + Enter to try out AI-generated SQL queries
Declare a parameter like "Where id = ${arg}".
*/
with t1(a, b, c) as (select * from test.repository), t2(d, e, f) as (select * from test.repository) select * from t1 join t2 on t1.a=t2.d;