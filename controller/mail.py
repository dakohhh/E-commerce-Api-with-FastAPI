import os
from fastapi_mail import FastMail, MessageSchema, ConnectionConfig
from dotenv import load_dotenv
from pydantic import BaseModel, EmailStr
from typing import List

load_dotenv()



class EmailSchema(BaseModel):
    email: List[EmailStr]



conf = ConnectionConfig(
    MAIL_USERNAME= os.getenv("MAIL_USERNAME"), 
    MAIL_PASSWORD= os.getenv("MAIL_PASSWORD"), 
    MAIL_FROM= os.getenv("MAIL_USERNAME"), 
    MAIL_PORT= int(os.getenv("MAIL_PORT")),
    MAIL_SERVER="smtp.gmail.com" , 
    USE_CREDENTIALS= True, 
    VALIDATE_CERTS = True,
    MAIL_STARTTLS = False,
    MAIL_SSL_TLS = True,

)

async def send_email(email:str, verification_link:str, name:str):

    message = MessageSchema(
        subject="VERIFY YOUR EMAIL",
        recipients= [email], 
        body= f'''
        <h1>Welcome to WIzShops {name}</h1>
        <br>
        <a href="{verification_link}" target='_blank'>Verify your email</a>
        ''' 
        ,
        subtype= "html"
    )

    fm = FastMail(conf)

    await fm.send_message(message)


