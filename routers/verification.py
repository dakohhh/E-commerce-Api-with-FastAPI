import datetime
from fastapi import APIRouter, Depends, Request
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from database.database import get_db
from dotenv import load_dotenv
from database.crud import (does_email_exist, get_verify_token_and_expire, update_user_verification, is_user_verified, update_token_and_expire)

load_dotenv()


verification = APIRouter(
    prefix="", 
    tags=["Verification"]
)

templates = Jinja2Templates(directory="templates")


@verification.get("/verification")
async def verify_email(request:Request, email:str, token:str, db:Session=Depends(get_db)):

    
    if not await does_email_exist(email, db):
        return templates.TemplateResponse("verify.html", {"request": request, "__response": "User not Found"})
    

    current_time = datetime.datetime.utcnow().timestamp()
    verify_token, expire_time = await get_verify_token_and_expire(email, db)

    if verify_token != token:
        return templates.TemplateResponse("verify.html", {"request": request, "__response": "Token is invalid", "__code":1})

    
    if current_time > expire_time.timestamp():
        return templates.TemplateResponse("verify.html", {"request": request, "__response": "Token has expired", "__code":2})

    if await is_user_verified(email, db):
        return templates.TemplateResponse("verify.html", {"request": request, "__response": "User is already verified", "__code":3})


    await update_user_verification(email, True, db)

    await update_token_and_expire(email, None, None, db)

    return templates.TemplateResponse("verify.html", {"request": request,"__response": "Verified User Successfully", "__code":3})

    
