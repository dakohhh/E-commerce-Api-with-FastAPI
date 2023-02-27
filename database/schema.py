from sqlalchemy import Column, Integer, String, Boolean, TIMESTAMP, text , ForeignKey, DECIMAL, SmallInteger
from .database import Base
from datetime import datetime




class User(Base):
    __tablename__ = "users"

    user_id = Column(String(12), primary_key=True, nullable=False, index=True)

    fullname = Column(String(20), nullable=False)

    email = Column(String(200), nullable=False, unique=True)

    password = Column(String(200), nullable=False)

    is_verified = Column(Boolean, default=False)

    role = Column(SmallInteger, nullable=False, default=1)

    token_verification = Column(String(40), nullable=True)

    id_expire = Column(TIMESTAMP)

    date_added = Column(TIMESTAMP, default=datetime.utcnow())

    # cart_add = relationship("Cart", back_populates="user")




class Products(Base):
    __tablename__ = "products"
    
    product_id = Column(String(100), primary_key=True, index=True)
    
    product_name = Column(String(100), nullable=False, index=True)
    
    category = Column(String(30), index=True)
    
    description = Column(String(200), index=True)

    original_price = Column(DECIMAL(7, 2), nullable=False)

    discount = Column(Integer, nullable=True, default=3)
    
    date_added =  Column(TIMESTAMP, server_default=text("NOW()"))
    

class Cart(Base):
    __tablename__ = "carts"

    cart_id = Column(Integer, primary_key=True, autoincrement=True, index=True)

    product_id =  Column(String(100),  ForeignKey("products.product_id"), nullable=False)

    user_id = Column(String(100),  ForeignKey("users.user_id"), nullable=False)

    date_added = Column(TIMESTAMP, server_default=text("NOW()"))

    # user = relationship("User", back_populates="cart_added")





class Session(Base):

    __tablename__ = "user_sessions"

    session_id = Column(String(15), primary_key=True, index=True)

    session_data = Column(String(200), nullable=False, index=True)

    expiry_date = Column(TIMESTAMP)

    

    

    