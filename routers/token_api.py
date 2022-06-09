import json
import os
from fastapi import APIRouter, Depends
import requests

API_KEY = os.environ.get("API_KEY")

router = APIRouter(
    prefix="/token",
    tags=[],
    dependencies=[],
    responses={404: {"description": "Not found"}},
)

@router.get("")
async def get_token(email, password):
    url = f"https://identitytoolkit.googleapis.com/v1/accounts:signInWithPassword?key={API_KEY}"
    data = {"email": email,
            "password": password,
            "returnSecureToken": True
            }
    result = requests.post(url, json=data)
    if result.ok:
            content = json.loads(result.content)
            return content['idToken']
    else:
        raise Exception("Unable to Authorize user")