from fastapi import Request, Depends
from sqlalchemy.orm import Session
from .tokens import verify_token
from database.crud import get_session_data, get_user_data
from database.database import get_db
from database.schema import Session as session_table
from models.model import UserData


async def get_user(request:Request, db:Session=Depends(get_db)):

    session_id = request.session.get("SESSION_ID")

    if session_id == None:
       return None
    
    token, expire = await get_session_data(session_id, db)

    user_email = verify_token(token)

    if user_email == None:
        return None


    user_data = await get_user_data(user_email.email, db)
    
    user_data = UserData(fullname=user_data[0], email=user_data[1], is_verified=user_data[2], role=user_data[3])

    return user_data