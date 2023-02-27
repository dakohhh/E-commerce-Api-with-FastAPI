from typing import Optional
from fastapi import Form
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




class UserData(BaseModel):
    fullname:str
    email: str
    is_verified: bool
    role:int





class Email(BaseModel):
    email:str



class Password(BaseModel):
    password:str



class UserForm:
    def __init__(self,
        fullname:str= Form(),
        email:str= Form(),
        password: str = Form()
        ):


        self.fullname = fullname
        self.email = email
        self.password = password

        