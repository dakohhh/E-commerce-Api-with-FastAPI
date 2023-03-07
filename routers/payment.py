import os
import stripe
from fastapi import APIRouter, Request, status
from exceptions.custom_execption import ServerErrorException
from response.response import flash, customResponse
from dotenv import load_dotenv


payment  = APIRouter(
        prefix="", 
        tags=["Payments"]
)

load_dotenv()
stripe.api_key = os.getenv("STRIPE_API_KEY")


@payment.post("/create-payment-session")
async def create_payment_session(amount: float, currency:str ,order_no:str, request:Request):
    try:
        session = stripe.checkout.Session.create(
            payment_method_types=["card"],
            line_items=[
                {
                    "price_data": {
                        "currency": currency,
                        "product_data": {
                            "name": f"ORDER_NO:{order_no}",
                        },
                        "unit_amount": round(amount * 100),
                    },
                    "quantity": 1,
                },
            ],
            mode="payment",
            success_url=request.url_for("payment_successful", order_no=order_no),
            cancel_url=request.url_for("payment_error", order_no=order_no),
        )
        return customResponse(status.HTTP_200_OK, "Session ID Created", data={"session_id":session})
    except:raise ServerErrorException("Connection Problem")





@payment.get("/payment_successful/{order_no}")
async def payment_successful(request:Request, order_no:str):
    return flash("/dashboard", "success", f'ORDER_NO:{order_no}')


@payment.get("/payment_error/{order_no}")
async def payment_error(request:Request, order_no:str):
    return flash("/dashboard", "danger", f'ORDER_NO:{order_no}')