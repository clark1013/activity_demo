/* Getting Started:
Enter "USE {database};" before entering your SQL statements.
Type "--your question" + Enter to try out AI-generated SQL queries
Declare a parameter like "Where id = ${arg}".
*/
use test;
select * from test.repository t1 join test.repository as t2 on t1.id=t2.id;