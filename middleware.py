from fastapi import Depends,HTTPException, Request, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from user import User
from user_repository import UserRepository
from firebase_admin import auth

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