import datetime
from fastapi import APIRouter, Depends, Request, status
from sqlalchemy.orm import Session
from controller.hex import generate_hex
from database.database import get_db
from response.response import customResponse
from exceptions.custom_execption import NotFoundError, CredentialsException, UnauthorizedExecption
from dotenv import load_dotenv
from models.model import Email, Password
from database.crud import (
does_email_exist, get_verify_token_and_expire, update_user_verification, 
is_user_verified, update_token_and_expire, update_user_password)

load_dotenv()


verification = APIRouter(
    prefix="", 
    tags=["Verification"]
)


@verification.post("/verification")
async def verify_email(email:str, token:str, db:Session=Depends(get_db)):

    
    if not await does_email_exist(email, db):
        raise NotFoundError("Email does not exist")
    

    current_time = datetime.datetime.utcnow().timestamp()
    verify_token, expire_time = await get_verify_token_and_expire(email, db)

    if verify_token != token:
        raise CredentialsException("Token is invalid")

    
    if current_time > expire_time.timestamp():
        raise CredentialsException("Token has expired")

    if await is_user_verified(email, db):
        return customResponse(status.HTTP_200_OK, "User is already verified")

    await update_user_verification(email, True, db)

    await update_token_and_expire(email, None, None, db)

    return customResponse(status.HTTP_200_OK, "Account successfully verified")



@verification.post("/request_verification_email")
async def request_user_verification_email(user:Email, request:Request, db:Session=Depends(get_db)):
    
    if not await does_email_exist(user.email, db):
        raise NotFoundError("Email does not exist")
    
    if await is_user_verified(user.email, db):
        return customResponse(status.HTTP_200_OK, "User is already verified")
    
    token = generate_hex(20)

    expire = datetime.datetime.utcnow() + datetime.timedelta(minutes=5)

    verification_link = f"{request.client.host}:{8000}/verification?email={user.email}&token={token}"


    await update_token_and_expire(user.email, token, expire, db)
    
    #send email

    return customResponse(status.HTTP_200_OK, "Verification email has been sent", data=verification_link)



# Do a get for this with query(email, token)
@verification.put("/verification/reset_password")
async def reset_password(new_password:Password, email:str, token:str, db:Session=Depends(get_db)):

    if not await does_email_exist(email, db):
        raise NotFoundError("Email does not exist")
    
    if not await is_user_verified(email, db):
        raise UnauthorizedExecption("User is not verified")
    
    current_time = datetime.datetime.utcnow().timestamp()
    verify_token, expire_time = await get_verify_token_and_expire(email, db)

    if verify_token != token:
        raise CredentialsException("Token is invalid")

    
    if current_time > expire_time.timestamp():
        raise CredentialsException("Token has expired")

    
    await update_user_password(email, new_password.password, db)

    await update_token_and_expire(email, None, None, db)

    return customResponse(status.HTTP_200_OK, "Password reset successfull")