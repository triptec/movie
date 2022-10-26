from backend import api, error, movie, movie_api_client
from backend.oauth2 import oauth2
from backend.swagger import swagger
from backend.wsgi import message_types, messages, remote


class NotFound(error.Error):
    pass


class GetRequestInvalid(error.Error):
    pass


class ListRequest(messages.Message):
    limit = messages.IntegerField(1, default=10)
    offset = messages.IntegerField(2, default=0)


class ListResult(messages.Message):
    id = messages.StringField(1)
    title = messages.StringField(2)
    imdb_id = messages.StringField(3)


class ListResponse(messages.Message):
    movies = messages.MessageField(ListResult, 1, repeated=True)


class RatingResult(messages.Message):
    source = messages.StringField(1)
    value = messages.StringField(2)


class GetRequest(messages.Message):
    id = messages.StringField(1)
    title = messages.StringField(2)


class GetResponse(messages.Message):
    id = messages.StringField(1)
    actors = messages.StringField(2)
    awards = messages.StringField(3)
    box_office = messages.StringField(4)
    country = messages.StringField(5)
    dvd = messages.StringField(6)
    director = messages.StringField(7)
    genre = messages.StringField(8)
    language = messages.StringField(9)
    metascore = messages.StringField(10)
    plot = messages.StringField(11)
    poster = messages.StringField(12)
    production = messages.StringField(13)
    rated = messages.StringField(14)
    ratings = messages.MessageField(RatingResult, 15, repeated=True)
    released = messages.StringField(16)
    response = messages.StringField(17)
    runtime = messages.StringField(18)
    title = messages.StringField(19)
    type = messages.StringField(20)
    website = messages.StringField(21)
    writer = messages.StringField(22)
    year = messages.StringField(23)
    imdb_id = messages.StringField(24)
    imdb_rating = messages.StringField(25)
    imdb_votes = messages.StringField(26)
    created = messages.StringField(27)


class AddRequest(messages.Message):
    title = messages.StringField(1, required=True)


class AddResponse(messages.Message):
    id = messages.StringField(1, required=True)


class DeleteRequest(messages.Message):
    id = messages.StringField(1, required=True)


@api.endpoint(path="movie", title="Movie API")
class Movie(remote.Service):
    @swagger("List movies")
    @remote.method(ListRequest, ListResponse)
    def list(self, request):
        result = movie.Movie.list(limit=request.limit, offset=request.offset)

        return ListResponse(
            movies=[
                ListResult(id=m.id, title=m.title, imdb_id=m.imdb_id)
                for m in result
                if m is not None
            ]
        )

    @swagger("Get movie")
    @remote.method(GetRequest, GetResponse)
    def get(self, request):
        if not request.id and not request.title:
            raise GetRequestInvalid("GetRequest requires either id or title")

        result = None
        if request.id:
            result = movie.Movie.get(id=request.id)
        elif request.title:
            result = movie.Movie.get_by_title(title=request.title)

        return GetResponse(
            id=result.id,
            actors=result.actors,
            awards=result.awards,
            box_office=result.box_office,
            country=result.country,
            dvd=result.dvd,
            director=result.director,
            genre=result.genre,
            language=result.language,
            metascore=result.metascore,
            plot=result.plot,
            poster=result.poster,
            production=result.production,
            rated=result.rated,
            ratings=[
                RatingResult(source=rating.source, value=rating.value)
                for rating in result.ratings
            ],
            released=result.released,
            response=result.response,
            runtime=result.runtime,
            title=result.title,
            type=result.type,
            website=result.website,
            writer=result.writer,
            year=result.year,
            imdb_id=result.imdb_id,
            imdb_rating=result.imdb_rating,
            imdb_votes=result.imdb_votes,
            created=result.created.isoformat(),
        )

    @swagger("Add movie")
    @remote.method(AddRequest, AddResponse)
    def add(self, request):
        query_result = movie_api_client.get_movie_by_title(request.title)
        result = movie.Movie.create_from_result(query_result)
        return AddResponse(id=result.id)

    @swagger("Delete movie")
    @oauth2.required()
    @remote.method(DeleteRequest, message_types.VoidMessage)
    def delete(self, request):
        movie.Movie.delete(request.id)
        return message_types.VoidMessage()
