from datetime import datetime
from sqlalchemy.orm import Session
from models.model import User
from authentication.hashing import checkPassword, hashPassword
from .schema import (User as user_table, Products as product_table , Cart as cart_table)





async def does_email_exist(email:str, db:Session):
    result = db.query(user_table).filter(user_table.email == email).first()

    if result:return True



async def create_user(user:User,db:Session, verify_id:str, expire:datetime):
    from controller.hex import generate_hex
    from authentication.hashing import hashPassword

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