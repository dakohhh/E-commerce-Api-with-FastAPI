from fastapi import FastAPI
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from starlette.middleware.sessions import SessionMiddleware
from routers.user import user as user
from routers.authentication import auth
from routers.shopping import shopping
from routers.payment import  payment
from routers.verification import verification
from database.schema import Base
from database.database import engine
from exceptions.custom_execption import *




Base.metadata.create_all(bind=engine)



app = FastAPI()

app.include_router(user)
app.include_router(auth)
app.include_router(shopping)
app.include_router(verification)
app.include_router(payment)
app.add_exception_handler(UserExistExecption, user_exist_exception_handler)
app.add_exception_handler(UnauthorizedExecption, unauthorized_exception_handler)
app.add_exception_handler(ServerErrorException, server_exception_handler)
app.add_exception_handler(NotFoundError, not_found)
app.add_exception_handler(CredentialsException, credentail_exception_handler)
app.add_exception_handler(BadRequestException, bad_request_exception_handler)
app.add_exception_handler(RedirectException, redirect_exeception_handler)
app.add_exception_handler(FlashException, flash_exeception_handler)

app.add_middleware(SessionMiddleware, secret_key="RapemanBruh", max_age=None)



app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")



@app.get('/')
def welcome(request:Request):
    return templates.TemplateResponse("index.html", {"request":request})



