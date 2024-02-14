SELECT title
FROM movies
    WHERE id IN
        (SELECT movie_id FROM people, stars, movies
        WHERE stars.person_id = people.id
            AND stars.movie_id = movies.id
            AND name LIKE 'Johnny Depp')
            AND id IN
                (SELECT movie_id FROM people, movies, stars
                WHERE stars.person_id = people.id
                    AND stars.movie_id = movies.id
                    AND name LIKE 'Helena Bonham Carter');