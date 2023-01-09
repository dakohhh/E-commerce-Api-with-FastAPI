from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from database.database import get_db
from database.crud import does_email_exist, auth_user, is_user_verified
from sqlalchemy.orm import Session
from exceptions.custom_execption import NotFoundError, UnauthorizedExecption
from models.model import Token




auth  = APIRouter(
        prefix="/api", 
        tags=["Authentication"]
)



@auth.post("/login")
async def login(request:OAuth2PasswordRequestForm=Depends(), db:Session=Depends(get_db)):

    if not await does_email_exist(request.username, db):
        raise NotFoundError("Invalid Credentails")
    
    if not await auth_user(request.username, request.password, db):
        raise NotFoundError("Invalid Credrntails")
    
    if not await is_user_verified(request.username, db):
        raise UnauthorizedExecption("User not verified")


    from  authentication.tokens import create_access_token

    access_token = create_access_token(request.username)

    return Token(access_token = access_token,token_type="bearer")

  