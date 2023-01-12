import datetime
from fastapi import APIRouter, Depends, Request, status
from fastapi.security import OAuth2PasswordRequestForm
from controller.hex import generate_hex
from database.database import get_db
from database.crud import does_email_exist, auth_user, is_user_verified, update_token_and_expire
from sqlalchemy.orm import Session
from exceptions.custom_execption import NotFoundError, UnauthorizedExecption
from models.model import Email, Token
from response.response import customResponse


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

  
@auth.post("/forgot_password")
async def forgot_password(user:Email,request:Request, db:Session=Depends(get_db)):

    if not await does_email_exist(user.email, db):
        raise NotFoundError("Email does not exist")
    
    
    if not await is_user_verified(user.email, db):
        raise UnauthorizedExecption("User is not verified")


    token = generate_hex(20)
    expire = datetime.datetime.utcnow() + datetime.timedelta(minutes=5)
    
    await update_token_and_expire(user.email,token, expire, db)

    link = f"{request.client.host}:{8000}/verification/reset_password?email={user.email}&token={token}"

    # send email

    return customResponse(status.HTTP_200_OK, "Reset password link sent", data=link)