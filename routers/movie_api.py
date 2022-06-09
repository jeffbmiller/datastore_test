from datetime import datetime
from fastapi import APIRouter, Depends
from movie import Movie
from movie_dto import MovieDto
import middleware
from movie_repository import MovieRepository


router = APIRouter(
    prefix="/movie",
    tags=[],
    dependencies=[Depends(middleware.get_user)],
    responses={404: {"description": "Not found"}},
)

@router.get("/")
async def get_movies():
    repo = MovieRepository()
    movies = repo.get_movies()
    dtos = [MovieDto.from_entity(x) for x in movies]
    return dtos


@router.post("/")
async def get_movies(movie_dto: MovieDto):
    repo = MovieRepository()
    movie = Movie(
        name=movie_dto.name,
        release_date=datetime.strptime(movie_dto.release_date, "%Y-%m-%d"),
        stars=movie_dto.stars
    )
    movie = repo.save(movie)
    dto = MovieDto.from_entity(movie)
    return dto