import os
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from database.database import get_db
from database.crud import does_email_exist, get_verify_token_and_expire
from response.response import customResponse
from exceptions.custom_execption import NotFoundError
from dotenv import load_dotenv
from exceptions.custom_execption import CredentialsException
load_dotenv()


verification = APIRouter(
    prefix="", 
    tags=["Verification"]
)


@verification.post("/verification")
async def verify(email:str, tokenid:str, db:Session=Depends(get_db)):

    
    if not await does_email_exist(email, db):
        raise NotFoundError("Email does not exist")

    import time
    current_time = time.time()
    verify_token, expire_time = await get_verify_token_and_expire(email, db)

    if verify_token != tokenid:
        raise CredentialsException("Token is invalid")
    
    if current_time >= expire_time.timestamp():
        raise CredentialsException("Token has expired")
    
  

    #set verified to true 
    

    # set token_ver id to null

    #set time expire to null

    return customResponse(status.HTTP_200_OK, data=[email, tokenid])


@verification.get("/verification")
def verify(email:str, tokenid:str, db:Session=Depends(get_db)):
    return "wisdom"