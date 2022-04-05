from datetime import datetime
from fastapi import Depends, FastAPI, HTTPException, Request, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from google.cloud import ndb
from movie import Movie
from movie_dto import MovieDto
from movie_repository import MovieRepository
from dotenv import load_dotenv
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

def get_user(req: Request, cred: HTTPAuthorizationCredentials=Depends(HTTPBearer(auto_error=False))) -> User:
        if cred is None:
            raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Bearer authentication required",
            headers={'WWW-Authenticate': 'Bearer realm="auth_required"'},
        )
        try:
            decoded_token = auth.verify_id_token(cred.credentials)
        except Exception as err:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail=f"Invalid authentication credentials. {err}",
                headers={'WWW-Authenticate': 'Bearer error="invalid_token"'},
            )

        user = UserRepository().get_by_uid(decoded_token['uid'])
        if user is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail=f"Invalid authentication credentials. {err}",
                headers={'WWW-Authenticate': 'Bearer error="User not found"'},
            )
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