from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from .tokens import verify_access_token
from models.model import TokenData
from database.crud import is_user_verified
from database.database import get_db
from exceptions.custom_execption import UnauthorizedExecption
from sqlalchemy.orm import Session




oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")




async def get_current_user(data:str=Depends(oauth2_scheme), db:Session=Depends(get_db)):
    return verify_access_token(data)



async def get_verified_user(current_user:TokenData=Depends(get_current_user), db:Session=Depends(get_db)):
    if not await is_user_verified(current_user.email, db):
        raise UnauthorizedExecption("User not verified")

    return current_user



