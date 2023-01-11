import os
from fastapi_mail import FastMail, MessageSchema, ConnectionConfig
from dotenv import load_dotenv
from pydantic import BaseModel, EmailStr
from typing import List
from .mail_template import email_verification_temp
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

async def send_email(email:EmailSchema, verification_link:str, name:str):

    message = MessageSchema(
        subject="Verify Your Email",
        recipients= email, 
        body= email_verification_temp.format(VERIFICATION_LINK=verification_link) ,
        subtype= "html"
    )

    fm = FastMail(conf)

    await fm.send_message(message)


