import datetime
import re

from google.cloud import ndb
from google.protobuf.message import DecodeError

from backend import error


class NotFound(error.Error):
    pass


class IdInvalid(error.Error):
    pass


class TitleInvalid(error.Error):
    pass


class IMDBIdExists(error.Error):
    pass


class IMDBIdInvalid(error.Error):
    pass


class Rating(ndb.Model):
    source = ndb.TextProperty()
    value = ndb.TextProperty()


class Movie(ndb.Model):
    created = ndb.DateTimeProperty(indexed=False)
    actors = ndb.TextProperty()
    awards = ndb.TextProperty()
    box_office = ndb.TextProperty()
    country = ndb.TextProperty()
    dvd = ndb.TextProperty()
    director = ndb.TextProperty()
    genre = ndb.TextProperty()
    language = ndb.TextProperty()
    metascore = ndb.TextProperty()
    plot = ndb.TextProperty()
    poster = ndb.TextProperty()
    production = ndb.TextProperty()
    rated = ndb.TextProperty()
    ratings = ndb.StructuredProperty(Rating, repeated=True)
    released = ndb.TextProperty()
    response = ndb.TextProperty()
    runtime = ndb.TextProperty()
    title = ndb.StringProperty(indexed=True)
    type = ndb.TextProperty()
    website = ndb.TextProperty()
    writer = ndb.TextProperty()
    year = ndb.TextProperty()
    imdb_id = ndb.StringProperty(indexed=True)
    imdb_rating = ndb.TextProperty()
    imdb_votes = ndb.TextProperty()

    @classmethod
    def get(cls, id):
        key = None
        try:
            key = ndb.Key(urlsafe=id)
        except DecodeError:
            raise IdInvalid("Id is invalid: %s" % id)

        entity = key.get()

        if entity is None or not isinstance(entity, cls):
            raise NotFound("No movie found with id: %s" % id)
        return entity

    @classmethod
    def get_by_title(cls, title):
        entities = cls.query(cls.title == title).fetch(1)

        if not entities or not isinstance(entities[0], cls):
            raise NotFound("No movie found with title: %s" % title)
        return entities[0]

    @classmethod
    def find_by_imdb_id(cls, imdb_id):
        entities = cls.query(cls.imdb_id == imdb_id).fetch(1)
        return entities[0] if entities else None

    @classmethod
    def list(cls, offset=0, limit=10):
        query = cls.query()
        query = query.order(Movie.title)
        return query.fetch(offset=offset, limit=limit)

    @classmethod
    def create(
        cls,
        actors=None,
        awards=None,
        box_office=None,
        country=None,
        dvd=None,
        director=None,
        genre=None,
        language=None,
        metascore=None,
        plot=None,
        poster=None,
        production=None,
        rated=None,
        ratings=[],
        released=None,
        response=None,
        runtime=None,
        title=None,
        type=None,
        website=None,
        writer=None,
        year=None,
        imdb_id=None,
        imdb_rating=None,
        imdb_votes=None,
    ):

        if not cls.is_valid_imdb_id(imdb_id):
            raise IMDBIdInvalid("%s is invalid" % imdb_id)

        if not cls.is_valid_title(title):
            raise TitleInvalid("%s is not a valid title" % title)

        if cls.find_by_imdb_id(imdb_id) is not None:
            raise IMDBIdExists("%s already exists" % imdb_id)

        entity = cls(
            created=datetime.datetime.now(),
            actors=actors,
            awards=awards,
            box_office=box_office,
            country=country,
            dvd=dvd,
            director=director,
            genre=genre,
            language=language,
            metascore=metascore,
            plot=plot,
            poster=poster,
            production=production,
            rated=rated,
            ratings=ratings,
            released=released,
            response=response,
            runtime=runtime,
            title=title,
            type=type,
            website=website,
            writer=writer,
            year=year,
            imdb_id=imdb_id,
            imdb_rating=imdb_rating,
            imdb_votes=imdb_votes,
        )
        entity.put()

        return entity

    @classmethod
    def create_from_result(cls, result):
        ratings = []
        for rating in result["ratings"]:
            ratings.append(Rating(source=rating["source"], value=rating["value"]))
        return cls.create(
            actors=result["actors"],
            awards=result["awards"],
            box_office=result["box_office"],
            country=result["country"],
            dvd=result["dvd"],
            director=result["director"],
            genre=result["genre"],
            language=result["language"],
            metascore=result["metascore"],
            plot=result["plot"],
            poster=result["poster"],
            production=result["production"],
            rated=result["rated"],
            ratings=ratings,
            released=result["released"],
            response=result["response"],
            runtime=result["runtime"],
            title=result["title"],
            type=result["type"],
            website=result["website"],
            writer=result["writer"],
            year=result["year"],
            imdb_id=result["imdb_id"],
            imdb_rating=result["imdb_rating"],
            imdb_votes=result["imdb_votes"],
        )

    @classmethod
    def delete(cls, id):
        entity = cls.get(id)
        res = entity.key.delete()
        return res

    @classmethod
    def is_valid_title(cls, title):
        return bool(title) and isinstance(title, str) and len(title) >= 1

    @classmethod
    def is_valid_imdb_id(cls, imdb_id):
        pattern = re.compile(r"^ev\d{7}\/\d{4}(-\d)?$|^(ch|co|ev|nm|tt)\d{7,8}$")
        return (
            bool(imdb_id)
            and isinstance(imdb_id, str)
            and bool(re.match(pattern, imdb_id))
        )

    @property
    def id(self):
        return self.key.urlsafe().decode("utf-8")

    def __hash__(self):
        return hash((self.__class__.__name__, self.id))
