from movie import Movie
from typing import List

class MovieRepository():

    def get_movies(self) -> List[Movie]:
        query = Movie.query()
        return query.fetch()

    def save(self, movie: Movie):
        movie.put()
        return movie