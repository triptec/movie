import os

from backend.omdb_client_wrapper import OMDBClientWrapper

movie_api_client = OMDBClientWrapper(os.getenv("OMDB_APIKEY"))
