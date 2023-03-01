import datetime
from fastapi import APIRouter, Depends, Request
from fastapi.templating import Jinja2Templates
from response.response import parse_request_cookies
from sqlalchemy.orm import Session
from database.database import get_db
from database.crud import does_email_exist, create_user, get_all_product, add_product_to_cart, get_cart_items, remove_product_from_cart
from models.model import UserForm, UserData
from response.response import flash, redirect
from controller.hex import generate_hex
from dotenv import load_dotenv
from authentication.dependencies import get_user

load_dotenv()



user = APIRouter(
        prefix="",
        tags=["User"]
        )

templates = Jinja2Templates(directory="templates")




@user.get("/dashboard")
async def dashboard_page(request:Request, user:UserData=Depends(get_user), db:Session=Depends(get_db)):

    products = await get_all_product(db)
    cart_items = await get_cart_items(user.user_id, db)

    cart_items = {i.cart_id : i.product_id for i in cart_items}
    
    
    context= {"request":request, "user":user, "products":products, "cart_items":cart_items}

    return templates.TemplateResponse("dashboard.html", context)







