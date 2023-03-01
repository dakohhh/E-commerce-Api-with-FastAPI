from fastapi import APIRouter, Depends, Request
from authentication.dependencies import get_user
from database.crud import add_product_to_cart, remove_product_from_cart
from database.database import get_db
from sqlalchemy.orm import Session
from models.model import UserData
from response.response import redirect




shopping  = APIRouter(
        prefix="", 
        tags=["Shopping"]
)


@shopping.post("/cart")
async def add_to_cart(product_id:str, request:Request, user:UserData=Depends(get_user), db:Session=Depends(get_db)):

    await add_product_to_cart(product_id, user.user_id, db)

    return redirect("/dashboard")


@shopping.post("/cart/remove")
async def remove_item_from_cart(cart_id:str, request:Request, user:UserData=Depends(get_user), db:Session=Depends(get_db)):
    
    await remove_product_from_cart(cart_id, db)
    
    return redirect("/dashboard")
