from backend import movie, test
from backend.setup import Seed


class TestSeed(test.TestCase):
    def test_movies(self):
        seed = Seed()

        obj = movie.Movie.create(title="test", imdb_id="tt1234567")
        self.assertEqual(movie.Movie.query().count(), 1)

        seed.movies()
        self.assertEqual(movie.Movie.query().count(), 1)

        obj.key.delete()
        self.assertEqual(movie.Movie.query().count(), 0)

        seed.movies()
        self.assertEqual(movie.Movie.query().count(), 100)
