from datetime import datetime
import os
from fastapi import FastAPI, Request
from google.cloud import ndb
from config import Settings
from movie import Movie
from movie_dto import MovieDto
from movie_repository import MovieRepository

settings = Settings()
app = FastAPI()
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = settings.service_account_path
client = ndb.Client()

@app.middleware("http")
async def ndb_context_middleware(request: Request, call_next):
    with client.context():
        response = await call_next(request)
        return response

@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/movies")
async def get_movies():
    repo = MovieRepository()
    movies = repo.get_movies()
    dtos = [MovieDto.from_entity(x) for x in movies]
    return dtos


@app.post("/movies")
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