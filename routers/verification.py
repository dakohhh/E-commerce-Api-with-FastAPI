from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from database.database import get_db



verification = APIRouter(
    prefix="", 
    tags=["Verification"]
)


@verification.get("/verification")
def verify(tokenid:str):
    return None