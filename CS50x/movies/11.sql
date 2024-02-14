SELECT title FROM movies, ratings, stars, people
WHERE ratings.movie_id = movies.id
AND stars.movie_id = movies.id
AND stars.person_id = people.id
AND name like 'Chadwick Boseman'
ORDER BY rating DESC limit 5;