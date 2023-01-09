from typing import Optional
from pydantic import BaseModel
from fastapi import Form





class User(BaseModel):
    fullname:str
    email:str
    password:str



class Token(BaseModel):
    access_token:str
    token_type:str


class TokenData(BaseModel):
    email: Optional[str] =None