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

async def send_email(email:EmailSchema, verificationLink:str):

    message = MessageSchema(
        subject="Testing Yeah",
        recipients= email, 
        body= f"<p> Pussy yeah {verificationLink}</p>",
        subtype= "html"
    )

    fm = FastMail(conf)

    await fm.send_message(message)


