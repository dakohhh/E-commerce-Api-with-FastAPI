from typing import Optional
from pydantic import BaseModel






class User(BaseModel):
    fullname:str
    email:str
    password:str




class Token(BaseModel):
    access_token:str
    token_type:str


class TokenData(BaseModel):
    email: Optional[str] =None

class Email(BaseModel):
    email:str



class Password(BaseModel):
    password:str