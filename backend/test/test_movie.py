import random

from backend import movie, test


class TestMovie(test.TestCase):
    def test_create(self):
        obj = movie.Movie.create(title="test", imdb_id="tt1234567")
        self.assertEqual(obj, movie.Movie.get(obj.id))
        self.assertTrue(obj.title == "test")
        self.assertTrue(obj.imdb_id == "tt1234567")
        self.assertRaises(
            movie.TitleInvalid,
            lambda: movie.Movie.create(title="", imdb_id="tt7654321"),
        )
        self.assertRaises(
            movie.IMDBIdInvalid, lambda: movie.Movie.create(title="test", imdb_id=None)
        )
        self.assertRaises(
            movie.IMDBIdExists,
            lambda: movie.Movie.create(title="test", imdb_id="tt1234567"),
        )

        movie.Movie.create(title="tast", imdb_id="tt7654321")

    def test_is_valid_imdb_id(self):
        self.assertEqual(movie.Movie.is_valid_imdb_id(""), False)
        self.assertEqual(movie.Movie.is_valid_imdb_id(None), False)
        self.assertEqual(movie.Movie.is_valid_imdb_id(1), False)
        self.assertEqual(movie.Movie.is_valid_imdb_id("abc123"), False)

        self.assertEqual(movie.Movie.is_valid_imdb_id("tt10515852"), True)

    def test_is_valid_title(self):
        self.assertEqual(movie.Movie.is_valid_title(""), False)
        self.assertEqual(movie.Movie.is_valid_title(None), False)
        self.assertEqual(movie.Movie.is_valid_title(1), False)

        self.assertEqual(movie.Movie.is_valid_title("a"), True)

    def test_title(self):
        self.assertRaises(
            movie.TitleInvalid, lambda: movie.Movie.create(title=1, imdb_id="tt1234567")
        )

        obj = movie.Movie.create(title="test", imdb_id="tt1234567")
        self.assertEqual(obj, movie.Movie.get(obj.id))

    def test_ratings(self):
        rating = movie.Rating(source="some_source", value="9.9")
        obj = movie.Movie.create(title="test", imdb_id="tt1234567", ratings=[rating])
        self.assertTrue(obj.ratings[0].source == "some_source")

    def test_create_from_result(self):
        result = {
            "actors": "Zach Callison, Michaela Dietz, Estelle",
            "awards": "2 nominations",
            "box_office": "N/A",
            "country": "United States",
            "dvd": "03 Sep 2019",
            "director": "Rebecca Sugar, Joseph D. Johnston, Kat Morris",
            "genre": "Animation, Action, Adventure",
            "language": "English",
            "metascore": "N/A",
            "plot": "Steven thinks his time defending the Earth is over, but when a new threat comes to Beach City, Steven faces his biggest challenge yet.",
            "poster": "https://m.media-amazon.com/images/M/MV5BYmVjY2U1N2UtMmZhOC00ODc5LWE1MjktODZjMmQyZmUyZWYwXkEyXkFqcGdeQXVyMTkxNjUyNQ@@._V1_SX300.jpg",
            "production": "N/A",
            "rated": "TV-PG",
            "ratings": [
                {"source": "Internet Movie Database", "value": "7.7/10"},
                {"source": "Rotten Tomatoes", "value": "100%"},
            ],
            "released": "02 Sep 2019",
            "response": "True",
            "runtime": "82 min",
            "title": "Steven Universe: The Movie",
            "type": "movie",
            "website": "N/A",
            "writer": "Ian Jones-Quartey, Chris Pianka, Matt Burnett",
            "year": "2019",
            "imdb_id": "tt10515852",
            "imdb_rating": "7.7",
            "imdb_votes": "7,357",
        }
        obj = movie.Movie.create_from_result(result)
        self.assertEqual(obj.title, result["title"])

    def test_get(self):
        obj = movie.Movie.create(title="test", imdb_id="tt1234567")
        self.assertEqual(obj, movie.Movie.get(obj.id))

        self.assertRaises(movie.IdInvalid, lambda: movie.Movie.get(id="invalid_id"))

        missing_id = obj.id
        movie.Movie.delete(missing_id)
        self.assertRaises(movie.NotFound, lambda: movie.Movie.get(id=missing_id))

    def test_delete(self):
        obj = movie.Movie.create(title="test", imdb_id="tt1234567")
        self.assertEqual(obj, movie.Movie.get(obj.id))

        id = obj.id
        self.assertEqual(movie.Movie.delete(id), None)

        self.assertRaises(movie.NotFound, lambda: movie.Movie.delete(id))

        self.assertRaises(movie.IdInvalid, lambda: movie.Movie.delete("invalid_id"))

    def test_get_by_title(self):
        obj = movie.Movie.create(title="test", imdb_id="tt1234567")
        self.assertEqual(obj, movie.Movie.get_by_title(obj.title))

        self.assertRaises(
            movie.NotFound, lambda: movie.Movie.get_by_title(title="missing_title")
        )

    def test_find_by_imdb_id(self):
        obj = movie.Movie.create(title="test", imdb_id="tt1234567")
        self.assertEqual(obj, movie.Movie.find_by_imdb_id(obj.imdb_id))

        self.assertEqual(movie.Movie.find_by_imdb_id("missing_imdb_id"), None)

    def test_list(self):
        indexes = [str(i).zfill(3) for i in [*range(1, 21)]]
        random.shuffle(indexes)
        for i in indexes:
            movie.Movie.create(title=f"test{i}", imdb_id=f"tt1234{i}")

        movies = movie.Movie.list()
        self.assertEqual(len(movies), 10)
        self.assertEqual(
            [f"test{str(i).zfill(3)}" for i in range(1, 11)],
            [m.title for m in movies],
        )
        self.assertEqual(movies[0].title, "test001")
        self.assertEqual(movies[0].imdb_id, "tt1234001")

        movies = movie.Movie.list(offset=10)
        self.assertEqual(len(movies), 10)
        self.assertEqual(
            [f"test{str(i).zfill(3)}" for i in range(11, 21)],
            [m.title for m in movies],
        )

        movies = movie.Movie.list(limit=5, offset=5)
        self.assertEqual(len(movies), 5)
        self.assertEqual(
            [f"test{str(i).zfill(3)}" for i in range(6, 11)],
            [m.title for m in movies],
        )


class TestMovieApi(test.TestCase):
    def test_list(self):
        indexes = [str(i).zfill(3) for i in [*range(1, 21)]]
        random.shuffle(indexes)
        for i in indexes:
            movie.Movie.create(title=f"test{i}", imdb_id=f"tt1234{i}")
        resp = self.api_client.post("movie.list")

        movies = resp.get("movies")
        self.assertEqual(len(movies), 10)
        self.assertEqual(
            [f"test{str(i).zfill(3)}" for i in range(1, 11)],
            [m["title"] for m in movies],
        )
        self.assertEqual(movies[0]["title"], "test001")
        self.assertEqual(movies[0]["imdb_id"], "tt1234001")

        resp = self.api_client.post("movie.list", dict(offset=10))
        movies = resp.get("movies")
        self.assertEqual(len(movies), 10)
        self.assertEqual(
            [f"test{str(i).zfill(3)}" for i in range(11, 21)],
            [m["title"] for m in movies],
        )

        resp = self.api_client.post("movie.list", dict(limit=5, offset=5))
        movies = resp.get("movies")
        self.assertEqual(len(movies), 5)
        self.assertEqual(
            [f"test{str(i).zfill(3)}" for i in range(6, 11)],
            [m["title"] for m in movies],
        )

    def test_get(self):
        obj = movie.Movie.create(title="test", imdb_id="tt1234567")
        obj1 = movie.Movie.create(title="test1", imdb_id="tt7654321")

        resp = self.api_client.post("movie.get", dict(id=obj.id))
        self.assertEqual(resp.get("id"), obj.id)

        resp = self.api_client.post("movie.get", dict(title=obj1.title))
        self.assertEqual(resp.get("title"), obj1.title)

        resp = self.api_client.post("movie.get")
        self.assertEqual(resp.get("error").get("error_name"), "GetRequestInvalid")

        resp = self.api_client.post("movie.get", dict(id="invalid_id"))
        self.assertEqual(resp.get("error").get("error_name"), "IdInvalid")

        missing_id = obj.id
        movie.Movie.delete(missing_id)
        resp = self.api_client.post("movie.get", dict(id=missing_id))
        self.assertEqual(resp.get("error").get("error_name"), "NotFound")

        resp = self.api_client.post("movie.get", dict(title="missing_title"))
        self.assertEqual(resp.get("error").get("error_name"), "NotFound")

    def test_add(self):
        resp = self.api_client.post("movie.add", dict(title="LOL"))
        self.assertEqual(resp.get("error"), None)
        obj = movie.Movie.get_by_title("LOL")
        self.assertEqual(obj.imdb_id, "tt1592873")

        resp = self.api_client.post("movie.add")
        self.assertRegex(
            resp.get("error").get("message"),
            "Message AddRequest is missing required field title",
        )

        resp = self.api_client.post("movie.add", dict(title="LOL"))
        self.assertEqual(resp.get("error").get("error_name"), "IMDBIdExists")

        resp = self.api_client.post("movie.add", dict(title="alksdlkas"))
        self.assertEqual(resp.get("error").get("error_name"), "NotFound")

        # Reporter is a common movie name.
        resp = self.api_client.post("movie.add", dict(title="Reporter"))
        obj1 = movie.Movie.get(resp["id"])
        self.assertEqual(obj1.title, "Reporter")

    def test_delete(self):
        resp = self.api_client.post(
            "user.create", dict(email="test@gmail.com", password="test", name="test")
        )
        access_token = resp.get("access_token")

        obj = movie.Movie.create(title="test", imdb_id="tt1234567")
        id = obj.id

        resp = self.api_client.post("movie.delete", dict(id=id))
        self.assertRegex(
            resp.get("error").get("message"), "Invalid or expired access token"
        )

        resp = self.api_client.post(
            "movie.delete", dict(id=id), headers=dict(authorization=access_token)
        )
        self.assertEqual(resp.get("error"), None)

        resp = self.api_client.post(
            "movie.delete", dict(id=id), headers=dict(authorization=access_token)
        )
        self.assertEqual(resp.get("error").get("error_name"), "NotFound")

        resp = self.api_client.post(
            "movie.delete",
            dict(id="invalid_id"),
            headers=dict(authorization=access_token),
        )
        self.assertEqual(resp.get("error").get("error_name"), "IdInvalid")
