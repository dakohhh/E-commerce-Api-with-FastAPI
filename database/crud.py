from datetime import datetime
from controller.hex import generate_hex
from sqlalchemy.orm import Session, aliased
from models.model import User
from authentication.hashing import checkPassword, hashPassword
from .schema import (User as user_table, Products as product_table , Cart as cart_table, 
Session as session_table, SavedProducts as save_table)
from sqlalchemy import and_, exists, case, func






async def does_email_exist(email:str, db:Session):
    result = db.query(user_table).filter(user_table.email == email).first()

    if result:return True



async def create_user(user:User,db:Session, verify_id:str, expire:datetime):
   
    new_user =user_table(user_id=generate_hex(6),fullname=user.fullname,email=user.email,\
    
    password=hashPassword(user.password), token_verification=verify_id, id_expire=expire)

    db.add(new_user)

    db.commit()

    db.refresh(new_user)




async def auth_user(email:str, password:str, db:Session):
    user:user_table =  db.query(user_table).filter(user_table.email == email).first()

    if checkPassword(password, user.password):return True




async def is_user_verified(email:str, db:Session):
    user:user_table =  db.query(user_table).filter(user_table.email == email).first()

    return user.is_verified


async def get_user_data(email:str, db:Session):
    user = db.query(user_table.user_id, user_table.fullname, user_table.email, user_table.role, user_table.is_verified).filter(user_table.email == email).first()

    return user


async def get_verify_token_and_expire(email:str, db:Session):
    result = db.query(user_table.token_verification, user_table.id_expire).filter(user_table.email == email).first()

    return result[0], result[1]



async def update_token_and_expire(email:str, token, expire, db:Session):

    db.query(user_table).filter(user_table.email == email).update({user_table.token_verification: token}, synchronize_session=False)

    db.query(user_table).filter(user_table.email == email).update({user_table.id_expire: expire}, synchronize_session=False)

    db.commit()



async def update_user_verification(email, status:bool, db:Session):
    db.query(user_table).filter(user_table.email == email).update({user_table.is_verified: status}, synchronize_session=False)

    db.commit()



async def update_user_password(email, new_password, db:Session):
    db.query(user_table).filter(user_table.email == email).update({user_table.password: hashPassword(new_password)}, synchronize_session=False)
    
    db.commit()




async def add_user_sessions(session_id:str, data:str, expire:datetime,  db:Session):

    new_session = session_table(session_id=session_id, session_data=data, expiry_date=expire)

    db.add(new_session)
    
    db.commit()

    db.refresh(new_session)



async def get_session_data(session_id:str, db:Session):
    session_data = db.query(session_table.session_data, session_table.expiry_date).filter(session_table.session_id == session_id).first()

    return session_data



async def delete_session_data(session_id:str, db:Session):
    db.query(session_table).filter(session_table.session_id == session_id).delete(synchronize_session=False)

    db.commit()


async def get_all_product(db:Session):
    products = db.query(product_table).all()

    return products


async def add_product_to_cart(product_id:str, user_id:str, db:Session):
    new_item = cart_table(product_id=product_id, user_id=user_id)

    db.add(new_item)

    db.commit()

    db.refresh(new_item)


async def remove_product_from_cart(product_id:str, user_id:str, db:Session):
    db.query(cart_table).filter(cart_table.product_id == product_id and cart_table.user_id == user_id).delete(synchronize_session=False)

    db.commit()
    



async def get_cart_items(user_id:str, db:Session):
    
    cart_items = db.query(cart_table).filter(cart_table.user_id == user_id).all()

    return cart_items



async def get_saved_products(user_id:str, db:Session):
    saved_items = db.query(save_table).filter(save_table.user_id == user_id).all()

    return saved_items

    



async def add_save_product(product_id:str, user_id:str, db:Session):
    new_item = save_table(product_id=product_id, user_id=user_id)

    db.add(new_item)

    db.commit()

    db.refresh(new_item)



    
async def remove_save_product(product_id:str, user_id:str, db:Session):
    db.query(save_table).filter(save_table.product_id == product_id and save_table.user_id == user_id).delete(synchronize_session=False)

    db.commit()






async def get_save_product_by_user(user_id:str, db:Session):
    
    query = db.query(product_table, case([(cart_table.product_id.isnot(None), True)], else_=False).label('in_cart'),
                      cart_table.cart_id.label('cart_id')).\
        join(save_table).filter(save_table.user_id == user_id).\
        outerjoin(cart_table, and_(cart_table.product_id == product_table.product_id, cart_table.user_id == user_id))




    saved_and_in_cart = query.all()
    return saved_and_in_cart