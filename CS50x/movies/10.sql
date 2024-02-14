SELECT DISTINCT name FROM people, ratings, directors, movies
WHERE directors.movie_id = movies.id
AND directors.person_id = people.id
AND ratings.movie_id = movies.id
AND rating >= 9.0;