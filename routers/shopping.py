from fastapi import APIRouter, Depends, Request
from authentication.dependencies import get_user
from database.crud import add_product_to_cart, add_save_product, remove_product_from_cart, remove_save_product
from database.database import get_db
from sqlalchemy.orm import Session
from models.model import UserData
from response.response import redirect




shopping  = APIRouter(
        prefix="", 
        tags=["Shopping"]
)



@shopping.get("/cart")
async def cart_page(request:Request, user:UserData=Depends(get_user), db:Session=Depends(get_db)):
    pass

@shopping.post("/cart")
async def add_to_cart(id:str, request:Request, user:UserData=Depends(get_user), db:Session=Depends(get_db)):

    await add_product_to_cart(id, user.user_id, db)

    return redirect("/dashboard")


@shopping.post("/cart/remove")
async def remove_item_from_cart(id:str, request:Request, user:UserData=Depends(get_user), db:Session=Depends(get_db)):
    
    await remove_product_from_cart(id, db)
    
    return redirect("/dashboard")



@shopping.post("/save_product")
async def save_product(id:str, request:Request, user:UserData=Depends(get_user), db:Session=Depends(get_db)):


    await add_save_product(id, user.user_id, db)
    

    return redirect("/dashboard")


@shopping.post("/save_product/remove")
async def remove_from_saved(id:str, request:Request, user:UserData=Depends(get_user), db:Session=Depends(get_db)):
    
    await remove_save_product(id, db)
    return redirect("/dashboard")