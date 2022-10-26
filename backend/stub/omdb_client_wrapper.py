import backend
from backend.omdb_client_wrapper import NotFound

SEARCH_DATA = [
    {
        "poster": "N/A",
        "title": "Steven Universe: The Movie",
        "type": "movie",
        "year": "2019",
        "imdb_id": "tt10515852",
    }
] + [
    {
        "poster": "test",
        "title": f"Steven{str(i).zfill(3)}",
        "type": "movie",
        "year": "test",
        "imdb_id": f"tt10515{str(i).zfill(3)}",
    }
    for i in [*range(1, 111)]
]

DATA = [
    {
        "actors": "Scott Marlowe, Matthew Risch, Evan Boomer",
        "awards": "3 wins & 3 nominations",
        "box_office": "$18,823",
        "country": "United States",
        "dvd": "06 Jun 2014",
        "director": "Chris Mason Johnson",
        "genre": "Drama, History, Romance",
        "language": "English, Portuguese, French",
        "metascore": "70",
        "plot": "In 1985, a gay dance understudy hopes for his on-stage chance while fearing the growing AIDS epidemic.",
        "poster": "https://m.media-amazon.com/images/M/MV5BMTQwMDU5NDkxNF5BMl5BanBnXkFtZTcwMjk5OTk4OQ@@._V1_SX300.jpg",
        "production": "N/A",
        "rated": "TV-MA",
        "ratings": [
            {"source": "Internet Movie Database", "value": "6.4/10"},
            {"source": "Rotten Tomatoes", "value": "82%"},
            {"source": "Metacritic", "value": "70/100"},
        ],
        "released": "04 Apr 2014",
        "response": "True",
        "runtime": "89 min",
        "title": "Test",
        "type": "movie",
        "website": "N/A",
        "writer": "Chris Mason Johnson",
        "year": "2013",
        "imdb_id": "tt2407380",
        "imdb_rating": "6.4",
        "imdb_votes": "1,642",
    },
    {
        "actors": "Miley Cyrus, Douglas Booth, Ashley Greene",
        "awards": "1 nomination",
        "box_office": "N/A",
        "country": "United States",
        "dvd": "31 Jul 2012",
        "director": "Lisa Azuelos",
        "genre": "Comedy, Drama, Romance",
        "language": "English, French, Ukrainian",
        "metascore": "N/A",
        "plot": "As a new year at school begins, Lola's heart is broken by her boyfriend, though soon she's surprised by her best friend, promising musician Kyle, who reveals his feelings for her.",
        "poster": "https://m.media-amazon.com/images/M/MV5BMTA0MjI5ODA3MjReQTJeQWpwZ15BbWU3MDI1NTE3Njc@._V1_SX300.jpg",
        "production": "N/A",
        "rated": "PG-13",
        "ratings": [
            {"source": "Internet Movie Database", "value": "4.3/10"},
            {"source": "Rotten Tomatoes", "value": "14%"},
        ],
        "released": "01 Mar 2012",
        "response": "True",
        "runtime": "97 min",
        "title": "LOL",
        "type": "movie",
        "website": "N/A",
        "writer": "Lisa Azuelos, Kamir Aïnouz, Nans Delgado",
        "year": "2012",
        "imdb_id": "tt1592873",
        "imdb_rating": "4.3",
        "imdb_votes": "56,442",
    },
    {
        "actors": "Eric Daniel Metzgar, Nicholas Kristof, Samantha Power",
        "awards": "3 nominations",
        "box_office": "N/A",
        "country": "United States",
        "dvd": "14 Jan 2014",
        "director": "Eric Daniel Metzgar",
        "genre": "Documentary",
        "language": "English",
        "metascore": "N/A",
        "plot": "Journalist Nicholas Kristof travels to the Democratic Republic of Congo to investigate the growing humanitarian crisis.",
        "poster": "https://m.media-amazon.com/images/M/MV5BMTc5MDA4NTQzNV5BMl5BanBnXkFtZTgwMTI3NjM4MDE@._V1_SX300.jpg",
        "production": "N/A",
        "rated": "Not Rated",
        "ratings": [{"source": "Internet Movie Database", "value": "7.3/10"}],
        "released": "16 Jan 2009",
        "response": "True",
        "runtime": "90 min",
        "title": "Reporter",
        "type": "movie",
        "website": "N/A",
        "writer": "N/A",
        "year": "2009",
        "imdb_id": "tt1331024",
        "imdb_rating": "7.3",
        "imdb_votes": "109",
    },
    {
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
    },
] + [
    {
        "actors": "test",
        "awards": "test",
        "box_office": "test",
        "country": "test",
        "dvd": "test",
        "director": "test",
        "genre": "test",
        "language": "test",
        "metascore": "test",
        "plot": "test",
        "poster": "test",
        "production": "test",
        "rated": "test",
        "ratings": [{"source": "source1", "value": "value1"}],
        "released": "test",
        "response": "test",
        "runtime": "test",
        "title": f"Steven{str(i).zfill(3)}",
        "type": "movie",
        "website": "test",
        "writer": "test",
        "year": "test",
        "imdb_id": f"tt10515{str(i).zfill(3)}",
        "imdb_rating": "test",
        "imdb_votes": "test",
    }
    for i in [*range(1, 111)]
]


class OMDBClientWrapper:
    def search_by_title(self, title):
        return {
            "search": [record for record in SEARCH_DATA if title in record["title"]]
        }

    def get_movie_by_title(self, title):
        movie = next((record for record in DATA if record["title"] == title), None)
        if not movie:
            raise NotFound("No movie found with title %s" % title)
        return movie

    def get_movie_by_imdb_id(self, imdb_id):
        movie = next((record for record in DATA if record["imdb_id"] == imdb_id), None)
        if not movie:
            raise NotFound("No movie found with imdb id %s" % imdb_id)
        return movie


backend.movie_api_client = OMDBClientWrapper()
