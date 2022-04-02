from datetime import datetime
from pydantic import BaseModel

from movie import Movie


class MovieDto(BaseModel):
    name: str
    release_date: str
    stars: int

    @staticmethod
    def from_entity(movie: Movie):
        return MovieDto(
            name=movie.name,
            release_date=movie.release_date.isoformat(),
            stars=movie.stars,
        )