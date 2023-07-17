USE test;
UPDATE `repository` SET `name` = IF(length(${name})>0,${name},`name`),
`url` = IF(length(${url})>0,${url},`url`) 
 WHERE `id` = ${id} ;