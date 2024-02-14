SELECT name FROM people WHERE
id IN (SELECT person_id FROM stars
WHERE movie_id IN (Select movie_id FROM stars
WHERE person_id IN (SELECT id from people WHERE
name like 'Kevin Bacon' AND birth = 1958)))
AND name NOT LIKE 'Kevin Bacon';