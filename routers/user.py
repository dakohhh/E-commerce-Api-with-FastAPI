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
from authentication.oauth2 import get_current_user, get_verified_user





user = APIRouter(
    prefix="/api",
    tags=["Signup"]
)


@user.post("/signup")
async def signup(user:User, request:Request , db:Session=Depends(get_db)):
    print(user.fullname, user.email, user.password)

    if await does_email_exist(user.email, db):
        raise UserExistExecption("Email already exists")

    
    verify_id = generate_hex(20)
    expire = datetime.datetime.utcnow() + datetime.timedelta(minutes=5)

    await create_user(user, db, verify_id, expire)

    # await send_email([user.email], "wisdompassword3456")
    
    return customResponse(
        status.HTTP_200_OK, 
        "Account created, verification email has been sent", 
        data=f"{request.client.host}:{request.client.port}/verification?email={user.email}&tokenid={verify_id}")



@user.post("/wth")
async def wth(get_current_user:TokenData=Depends(get_verified_user)):

    return get_current_user




