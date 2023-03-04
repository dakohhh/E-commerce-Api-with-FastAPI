from fastapi import APIRouter, Depends, Request
from fastapi.templating import Jinja2Templates
from authentication.dependencies import get_user
from database.database import get_db
from sqlalchemy.orm import Session
from models.model import UserData
from response.response import redirect
from database.crud import (add_product_to_cart, add_save_product, get_save_product_by_user, 
remove_product_from_cart, remove_save_product, get_cart_items)




shopping  = APIRouter(
        prefix="", 
        tags=["Shopping"]
)

templates = Jinja2Templates(directory="templates")


@shopping.get("/cart")
async def cart_page(request:Request, user:UserData=Depends(get_user), db:Session=Depends(get_db)):
    pass



@shopping.post("/cart")
async def add_to_cart(id:str, request:Request, user:UserData=Depends(get_user), db:Session=Depends(get_db)):

    await add_product_to_cart(id, user.user_id, db)
    


@shopping.delete("/cart")
async def remove_item_from_cart(id:str, request:Request, user:UserData=Depends(get_user), db:Session=Depends(get_db)):
    
    await remove_product_from_cart(id, user.user_id, db)
    
    



@shopping.get("/save_products")
async def saved_product_page(request:Request, user:UserData=Depends(get_user), db:Session=Depends(get_db)):

    saved_products =  await get_save_product_by_user(user.user_id, db)

    cart_items = await get_cart_items(user.user_id, db)


    context= {"request":request, "user":user, "saved_products":saved_products, "cart_items":cart_items}

    return templates.TemplateResponse("saved_items.html", context)
    

@shopping.post("/save_products")
async def save_products(id:str, request:Request, user:UserData=Depends(get_user), db:Session=Depends(get_db)):


    await add_save_product(id, user.user_id, db)
    


@shopping.delete("/save_products")
async def remove_from_saved(id:str, request:Request, user:UserData=Depends(get_user), db:Session=Depends(get_db)):
    
    await remove_save_product(id, user.user_id, db)
