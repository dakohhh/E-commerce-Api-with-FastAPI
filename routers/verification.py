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

    
    
    result = await get_verify_token_and_expire(email, db)



    if tokenid != get_token:
        raise CredentialsException("Token is invalid")

    # print(str(tokenid).encode("utf-8"))
    
    # _token = cipher.decrypt(b"rwfwfefwe")
    #check if id is in datebase


    # print(verify_email_id(email, _token, db))

    #set verified to true 

    # set token_ver id to null

    #set time expire to null

    return customResponse(status.HTTP_200_OK, data=[email, tokenid])


@verification.get("/verification")
def verify(email:str, tokenid:str, db:Session=Depends(get_db)):
    return "wisdom"