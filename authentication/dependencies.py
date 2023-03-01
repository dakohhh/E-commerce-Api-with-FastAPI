import datetime
from fastapi import Request, Depends
from sqlalchemy.orm import Session
from exceptions.custom_execption import RedirectException, FlashException
from .tokens import verify_token
from database.crud import get_session_data, get_user_data, delete_session_data
from database.database import get_db
from models.model import UserData




async def get_user(request:Request, db:Session=Depends(get_db)):
    session_id = request.session.get("SESSION_ID")
    if session_id == None:raise RedirectException("/login")

    session_data =  await get_session_data(session_id, db)
    if session_data == None:
        request.session.pop("SESSION_ID")
        raise RedirectException("/login")

    token, expire = session_data

    current_time = datetime.datetime.utcnow().timestamp()

    if current_time > expire.timestamp():
        request.session.pop("SESSION_ID")
        await delete_session_data(session_id, db)
        raise FlashException("/login", "danger", "The session has expired")

    user_email = verify_token(token)        

    user_data = await get_user_data(user_email.email, db)

    user = UserData(
        user_id= user_data[0], 
        fullname=user_data[1], 
        email=user_data[2], 
        is_verified=user_data[3], 
        role=user_data[4])

    return user
    