import logging

from backend import movie, movie_api_client

logger = logging.getLogger()


class Seed:
    def movies(self):
        count = movie.Movie.query().count(1)
        if count != 0:  # Check if movies is empty
            return
        logger.info("Seeding movies start")
        results = self.__get_hundred_movies()

        count = movie.Movie.query().count(1)
        if count != 0:  # Second check to see if movies still empty
            logger.info("Movies no longer empty, abort")
            return
        for result in results:
            movie.Movie.create_from_result(result)

        logger.info("Seeding movies done")

    def __get_hundred_movies(self):
        search_result = movie_api_client.search_by_title("Steven")
        imdb_ids = [result["imdb_id"] for result in search_result["search"]]
        movies = []
        for imdb_id in imdb_ids[:100]:
            movies.append(movie_api_client.get_movie_by_imdb_id(imdb_id))
        return movies
