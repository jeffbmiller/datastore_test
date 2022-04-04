from datetime import datetime
import re
from fastapi import Depends, FastAPI, Request
from google.cloud import ndb
from movie import Movie
from movie_dto import MovieDto
from movie_repository import MovieRepository
from dotenv import load_dotenv
from fastapi.responses import HTMLResponse
import firebase_admin
from firebase_admin import auth
from user import User

from user_repository import UserRepository

load_dotenv()
app = FastAPI()
client = ndb.Client()

default_app = firebase_admin.initialize_app()

@app.middleware("http")
async def ndb_context_middleware(request: Request, call_next):
    with client.context():
        response = await call_next(request)
        return response

def get_user(req: Request) -> User:
        token = req.headers["Authorization"]
        decoded_token = auth.verify_id_token(token)
        user = None
        if decoded_token:
            user = UserRepository().get_by_uid(decoded_token['uid'])            
        if not user:
            raise Exception("Unauthorized")
        else:
            return user


@app.get("/movies")
async def get_movies(user: User = Depends(get_user)):
    repo = MovieRepository()
    movies = repo.get_movies()
    dtos = [MovieDto.from_entity(x) for x in movies]
    return dtos


@app.post("/movies")
async def get_movies(movie_dto: MovieDto, user: User = Depends(get_user)):
    repo = MovieRepository()
    movie = Movie(
        name=movie_dto.name,
        release_date=datetime.strptime(movie_dto.release_date, "%Y-%m-%d"),
        stars=movie_dto.stars
    )
    movie = repo.save(movie)
    dto = MovieDto.from_entity(movie)
    return dto