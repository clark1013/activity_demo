/* Getting Started:
Enter "USE {database};" before entering your SQL statements.
Type "--your question" + Enter to try out AI-generated SQL queries
Declare a parameter like "Where id = ${arg}".
*/
show databases;
use sample_data;
BEGIN;
select repo_id, sum(repo_id) from github_events group by repo_id;
rollback;
select * from test.t join sample_data.github_events on t.id=github_events.fff;
show processlist;