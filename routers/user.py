from fastapi import APIRouter, Depends, Request
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from database.database import get_db
from database.crud import get_all_product, get_cart_items, get_saved_products
from models.model import UserData
from dotenv import load_dotenv
from authentication.dependencies import get_user
from response.response import parse_request_cookies
load_dotenv()



user = APIRouter(
        prefix="",
        tags=["User"]
        )

templates = Jinja2Templates(directory="templates")




@user.get("/dashboard")
async def dashboard_page(request:Request, user:UserData=Depends(get_user), db:Session=Depends(get_db)):

	get_flash_msg = parse_request_cookies(request, "msg")
		

	products = await get_all_product(db)
	cart_items = await get_cart_items(user.user_id, db)
	saved_items = await get_saved_products(user.user_id, db)

	cart_items = {items.cart_id : items.product_id for items in cart_items}

	saved_items = {items.save_id : items.product_id for items in saved_items}



	context= {"request":request, "user":user, "products":products, "cart_items":cart_items, "saved_items":saved_items, "get_flash_msg":get_flash_msg}

	return templates.TemplateResponse("dashboard.html", context)







