from backend import movie_api_client, test


class TestMovieClient(test.TestCase):
    def test_search_by_title(self):
        movies = movie_api_client.search_by_title("Steven")
        self.assertTrue(len(movies) > 0)

    def test_get_movie_by_imdb_id(self):
        movie = movie_api_client.get_movie_by_imdb_id("tt2407380")
        self.assertEqual(movie["imdb_id"], "tt2407380")

    def test_get_movie_by_title(self):
        movie = movie_api_client.get_movie_by_title("LOL")
        self.assertEqual(movie["imdb_id"], "tt1592873")
