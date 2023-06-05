/* Getting Started:
Enter "USE {database};" before entering your SQL statements.
Type "--your question" + Enter to try out AI-generated SQL queries
Declare a parameter like "Where id = ${arg}".
*/
use sample_data;
-- what is the most popular repo in github?
SELECT
  `repo_name`,
  COUNT(*) AS count
FROM
  sample_data.github_events
GROUP BY
  `repo_name`
ORDER BY
  count DESC
LIMIT
  1;