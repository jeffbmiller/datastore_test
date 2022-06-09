from fastapi import FastAPI, Request 
from google.cloud import ndb
from dotenv import load_dotenv
import firebase_admin
from routers import token_api, movie_api

load_dotenv()
app = FastAPI()
app.include_router(token_api.router)
app.include_router(movie_api.router)

client = ndb.Client()

default_app = firebase_admin.initialize_app()

@app.middleware("http")
async def ndb_context_middleware(request: Request, call_next):
    with client.context():
        response = await call_next(request)
        return response



