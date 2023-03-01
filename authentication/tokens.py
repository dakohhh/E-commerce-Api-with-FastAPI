import os
import jwt
import datetime
import secrets
from dotenv import load_dotenv
from models.model import TokenData
from exceptions.custom_execption import CredentialsException

load_dotenv()




def create_access_token(data):
    token = jwt.encode(
        {"user":data, 
        "exp": datetime.datetime.utcnow() + datetime.timedelta(days=30)
        }, str(os.getenv("ADMIN_SECRET_KEY")))
    
    return token




def verify_access_token(token:str):
    try:
        payload = jwt.decode(token, str(os.getenv("ADMIN_SECRET_KEY")), algorithms=["HS256"])
        return TokenData(email =payload["user"])
    except:
        raise CredentialsException("Could not validate credentials")





def verify_token(token:str):
    try:
        payload = jwt.decode(token, str(os.getenv("ADMIN_SECRET_KEY")), algorithms=["HS256"])
        return TokenData(email =payload["user"])
    except:
        return None
