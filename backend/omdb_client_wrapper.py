from omdb import OMDB, OMDBNoResults

from backend import error


class NotFound(error.Error):
    pass


class OMDBClientWrapper:
    def __init__(self, apikey):
        self.omdb = OMDB(apikey)

    def search_by_title(self, title):
        return self.omdb.search(title, type="movie")

    def get_movie_by_title(self, title):
        try:
            return self.omdb.get_movie(title=title, type="movie")
        except OMDBNoResults:
            raise NotFound("No movie found with title %s" % title)

    def get_movie_by_imdb_id(self, imdb_id):
        try:
            return self.omdb.get_movie(imdbid=imdb_id, type="movie")
        except OMDBNoResults:
            raise NotFound("No movie found with imdb id %s" % imdb_id)
