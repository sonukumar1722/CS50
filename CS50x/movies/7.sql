SELECT title, rating FROM movies, ratings
WHERE year = 2010
AND rating IS NOT NULL
AND ratings.movie_id = movies.id
ORDER BY rating DESC, title;