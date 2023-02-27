from fastapi import Request, Depends
from sqlalchemy.orm import Session
from .tokens import verify_token
from database.crud import get_session_data, get_user_data
from database.database import get_db
from database.schema import Session as session_table


async def get_user(request:Request, db:Session=Depends(get_db)):

    session_id = request.session.get("SESSION_ID")

    if session_id == None:
       return None
    
    token, expire = await get_session_data(session_id, db)

    user = verify_token(token)

    if user == None:
        return None


    user = await get_user_data(user.email, db)

    return user