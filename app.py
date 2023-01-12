from fastapi import FastAPI, status
from routers.user import user
from routers.login import auth
from routers.verification import verification
from database.schema import Base
from database.database import engine
from exceptions.custom_execption import *



Base.metadata.create_all(bind=engine)






app = FastAPI()

app.include_router(user)
app.include_router(auth)
app.include_router(verification)
app.add_exception_handler(UserExistExecption, user_exist_exception_handler)
app.add_exception_handler(UnauthorizedExecption, unauthorized_exception_handler)
app.add_exception_handler(ServerErrorException, server_exception_handler)
app.add_exception_handler(NotFoundError, not_found)
app.add_exception_handler(CredentialsException, credentail_exception_handler)
app.add_exception_handler(BadRequestException, bad_request_exception_handler)



@app.route('/')
def welcome():
    from response.response import customResponse
    return customResponse(status.HTTP_200_OK, "Welcome to WizShops")