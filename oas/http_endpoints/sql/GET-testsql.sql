/* Getting Started:
Enter "USE {database};" before entering your SQL statements.
Type "--your question" + Enter to try out AI-generated SQL queries
Declare a parameter like "Where id = ${arg}".
*/
  describe test.repository;
delete from test.repository where name="ttt";
insert into test.repository (name, url) values ("ttt", "ttt");
update test.repository set url ="bbb" where name = "ttt";