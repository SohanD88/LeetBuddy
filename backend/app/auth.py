from fastapi import Depends, HTTPException, Header
import jwt
from jwt import InvalidTokenError
from app.settings import get_settings

def get_current_user(authorization: str = Header(None)) -> str:
    """
    Gets and verifies Supabase JWT
    returns the users id if the user is authenticated
    """

    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Invalid authorization header")
    
    token = authorization.split(" ", 1)[1]
    settings = get_settings()


    try: 
        payload = jwt.decode(token, settings.supabase_jwt_secret, algorithms=["HS256"], options ={"verify_aud": False})
    except InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token")
    
    user_id = payload.get("sub")
    if not user_id:
        raise HTTPException(status_code=401, detail="Invalid token payload")
    
    return user_id