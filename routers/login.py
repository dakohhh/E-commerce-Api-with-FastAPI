import datetime
from fastapi import APIRouter, Depends, Request, status
from fastapi.templating import Jinja2Templates
from fastapi.security import OAuth2PasswordRequestForm
from controller.hex import generate_hex
from database.database import get_db
from database.crud import does_email_exist, auth_user, is_user_verified, update_token_and_expire, add_user_sessions
from sqlalchemy.orm import Session
from exceptions.custom_execption import NotFoundError, UnauthorizedExecption
from models.model import Email, Token
from response.response import customResponse, flash, parse_request_cookies, redirect


auth  = APIRouter(
        prefix="", 
        tags=["Authentication"]
)

templates = Jinja2Templates(directory="templates")


@auth.get("/login")
async def login_page(request:Request):

    get_flash_msg = parse_request_cookies(request, "msg")
    context = {"request": request, "get_flash_msg":get_flash_msg}
    return templates.TemplateResponse("login.html", context)


@auth.post("/login")
async def login(request:Request, request_form:OAuth2PasswordRequestForm=Depends(), db:Session=Depends(get_db)):

    if not await does_email_exist(request_form.username, db):
        
        return flash("/login", "danger", "Email or password is incorrect")
    
    if not await auth_user(request_form.username, request_form.password, db):
        
        return flash("/login", "danger", "Email or password is incorrect")
    
    if not await is_user_verified(request_form.username, db):

        return flash("/login", "warning", "Email not verified")


    from  authentication.tokens import create_access_token

    access_token = create_access_token(request_form.username)

    session_id = generate_hex(6)

    session_expire = datetime.datetime.utcnow() + datetime.timedelta(minutes=5)

    await add_user_sessions(session_id, access_token, session_expire, db)
    
    request.session["SESSION_ID"] = session_id

    return redirect("/dashboard")



@auth.get("/logout")
def logout(request:Request):
    if request.session["SESSION_ID"]:
        request.session.pop("SESSION_ID")
        redirect("/login")
    else:
        redirect("/logout")




@auth.post("/forgot_password")
async def forgot_password(user:Email,request:Request, db:Session=Depends(get_db)):

    if not await does_email_exist(user.email, db):
        raise NotFoundError("Email does not exist")
    
    
    if not await is_user_verified(user.email, db):
        raise UnauthorizedExecption("User is not verified")


    token = generate_hex(20)
    expire = datetime.datetime.utcnow() + datetime.timedelta(minutes=5)
    
    await update_token_and_expire(user.email,token, expire, db)

    link = f"{request.client.host}:{8000}/verification/reset_password?email={user.email}&token={token}"

    # send email

    return customResponse(status.HTTP_200_OK, "Reset password link sent", data=link)