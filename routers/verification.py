from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from database.database import get_db
from response.response import customResponse



verification = APIRouter(
    prefix="", 
    tags=["Verification"]
)


@verification.post("/verification")
def verify(email:str, tokenid:str):
    
    #check if email is in database

    #decrypt token

    #check if token is in datebase 

    #set verified to true 

    # set token_ver id to null

    #set time expire to null

    return customResponse(status.HTTP_200_OK, data=[email, tokenid])
