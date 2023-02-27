import datetime
from fastapi import APIRouter, Depends, Request
from fastapi.templating import Jinja2Templates
from response.response import parse_request_cookies
from sqlalchemy.orm import Session
from database.database import get_db
from database.crud import does_email_exist, create_user
from models.model import TokenData, UserForm, UserData
from response.response import flash, redirect
from controller.hex import generate_hex
from dotenv import load_dotenv
from authentication.oauth2 import get_verified_user
from authentication.dependencies import get_user

load_dotenv()



user = APIRouter(
        prefix="",
        tags=["User"]
        )

templates = Jinja2Templates(directory="templates")


@user.get("/signup")
async def signup_page(request:Request):

    get_flash_msg = parse_request_cookies(request, "msg")

    context = {"request": request, "get_flash_msg": get_flash_msg}

    return templates.TemplateResponse("signup.html", context)



@user.post("/signup")
async def signup(request:Request, user:UserForm=Depends() , db:Session=Depends(get_db)):

    if await does_email_exist(user.email, db):
        return flash("/signup", "danger", "Email already exists")
    
    token = generate_hex(20)
    expire = datetime.datetime.utcnow() + datetime.timedelta(minutes=5)

    await create_user(user, db, token, expire)
    
    verification_link = f"{request.client.host}:{8000}/verification?email={user.email}&token={token}"
    
    # send email

    return flash("/signup", "success", "Email verification link sent")






@user.get("/dashboard")
async def dashboard_page(request:Request, user:UserData=Depends(get_user)):

    if user == None:return redirect("/login")
    
    print(user)
    return templates.TemplateResponse("dashboard.html", {"request":request})



