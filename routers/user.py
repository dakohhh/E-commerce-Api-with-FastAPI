import os
import datetime
from fastapi import APIRouter, Depends, status, Request
from sqlalchemy.orm import Session
from database.database import get_db
from database.crud import does_email_exist, create_user
from models.model import User, TokenData
from exceptions.custom_execption import (UserExistExecption)
from response.response import customResponse
from controller.hex import generate_hex
from controller.mail import send_email
from dotenv import load_dotenv
from authentication.oauth2 import get_current_user, get_verified_user



load_dotenv()



user = APIRouter(
    prefix="/api",
    tags=["Signup"]
)


@user.post("/signup")
async def signup(user:User, request:Request , db:Session=Depends(get_db)):

    if await does_email_exist(user.email, db):
        raise UserExistExecption("Email already exists")
    
    token = generate_hex(20)
    expire = datetime.datetime.utcnow() + datetime.timedelta(minutes=5)

    await create_user(user, db, token, expire)


    verification_link = f"{request.client.host}:{8000}/verification?email={user.email}&token={token}"
    
    # send email
    return customResponse(status.HTTP_200_OK, "Account created, verification email has been sent", data=verification_link)







@user.post("/wth")
async def wth(get_current_user:TokenData=Depends(get_verified_user)):

    return get_current_user




