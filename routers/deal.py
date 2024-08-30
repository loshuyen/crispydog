from fastapi import APIRouter, Depends, Query, Body
from fastapi.responses import JSONResponse, RedirectResponse
from database import deal as db, cart, payment, notification, product, commission, user as user_db
from .user import get_auth_user
from .notification import notify_user
from models import deal as model
from datetime import datetime
from utils import pay
import json

router = APIRouter()

async def add_notification_to_db(sender_id, sender_name, product_id_list, message_type, message = None, commission_id=None):
    receiver_id_list = []
    for product_id in product_id_list:
        receiver_id_list.append(product.get_owner_by_product_id(product_id))
    await notification.add_notification(sender_id, sender_name, receiver_id_list, message_type, product_id_list, message, commission_id)

@router.get("/api/deals")
def get_deal(
        success: int | None = Query(default=None, ge=0, le=1, description="0: 未成交的訂單、1: 已成交的訂單、Null: 所有訂單"), user = Depends(get_auth_user)):
    try:
        if not user:
            return JSONResponse(status_code=403, content={"error": True, "message": "未登入系統，拒絕存取"})
        data = db.get_all_deals(user["id"], success)
        return JSONResponse(status_code=200, content={"data": data})
    except Exception as e:
        print(e)
        return JSONResponse(status_code=500, content={"error": True, "message": "伺服器內部錯誤"})

@router.post("/api/deal/credit_card")
async def create_credit_card_deal(deal: model.Deal, user = Depends(get_auth_user)):
    try:
        if not user:
            return JSONResponse(status_code=403, content={"error": True, "message": "未登入系統，拒絕存取"})
        if deal.deal.amount != db.calculate_amount(deal.deal.products):
            return JSONResponse(status_code=400, content={"error": True, "message": "輸入金額錯誤"})
        deal_id = db.add_deal(user["id"], deal.deal.products, deal.deal.delivery_email, deal.deal.amount)
        pay_result = pay.tappay_direct_pay(
            prime=deal.prime, 
            amount=deal.deal.amount, 
            order_number=datetime.now().strftime("%Y%m%d%H%M%S") + str(user["id"]), 
            phone_number=deal.contact.phone_number, 
            name=deal.contact.name, 
            email=deal.contact.email
        )
        if pay_result["payment"]["status"] != 0:
            return {"data": pay_result}
        elif pay_result["payment"]["status"] == 0:
            db.mark_as_success(deal_id)
            db.add_sale_records(deal_id, user["id"], deal.deal.products)
            cart.remove_all_product_from_cart(user["id"])
            payment.add_payment(pay_result, deal_id, user["id"])
            db.update_seller_savings(deal.deal.products)
            await add_notification_to_db(user["id"], user["username"], deal.deal.products, 0, message = None, commission_id=None)
            return {"data": pay_result}
        else:
            return JSONResponse(status_code=400, content={"error": True, "message": "訂單建立失敗，輸入不正確或其他原因"})
    except Exception as e:
        print(e)
        return JSONResponse(status_code=500, content={"error": True, "message": "伺服器內部錯誤"})  
    
@router.post("/api/deal/line")
async def create_line_deal(deal: model.Deal, user = Depends(get_auth_user)):
    try:
        if not user:
            return JSONResponse(status_code=403, content={"error": True, "message": "未登入系統，拒絕存取"})
        if deal.deal.amount != db.calculate_amount(deal.deal.products):
            return JSONResponse(status_code=400, content={"error": True, "message": "輸入金額錯誤"})
        deal_id = db.add_deal(user["id"], deal.deal.products, deal.deal.delivery_email, deal.deal.amount)
        pay_result = pay.tappay_line_pay(
            prime=deal.prime, 
            amount=deal.deal.amount, 
            order_number=datetime.now().strftime("%Y%m%d%H%M%S") + str(user["id"]), 
            phone_number=deal.contact.phone_number, 
            name=deal.contact.name, 
            email=deal.contact.email
        )
        if pay_result["status"] == 0:
            payment_body = {
                "number": pay_result["order_number"],
                "payment": {
                    "pay_method": "LINE_Pay",
                    "status": 0,
                    "message": pay_result["bank_result_msg"],
                    "rec_trade_id": pay_result["rec_trade_id"],
                    "auth_code": "no",
                    "amount": pay_result["amount"],
                    "currency": "no",
                    "transaction_time": pay_result["transaction_time_millis"],
                }
            }
            payment.add_payment(payment_body, deal_id, user["id"])
            return {"payment_url": pay_result["payment_url"]}
        return JSONResponse(status_code=400, content={"error": True, "message": "訂單建立失敗，輸入不正確或其他原因"})
    except Exception as e:
        print(e)
        return JSONResponse(status_code=500, content={"error": True, "message": "伺服器內部錯誤"})  

@router.post("/api/deal/wallet")
async def create_wallet_deal(deal: model.DealBase, user = Depends(get_auth_user)):
    if not user:
        return JSONResponse(status_code=403, content={"error": True, "message": "未登入系統，拒絕存取"})
    try:
        if deal.amount != db.calculate_amount(deal.products):
            return JSONResponse(status_code=400, content={"error": True, "message": "輸入金額錯誤"})
        savings = user_db.get_savings(user["id"])
        if savings < deal.amount:
            return JSONResponse(status_code=400, content={"error": True, "message": "錢包餘額不足"})
        deal_id = db.add_deal(user["id"], deal.products, deal.delivery_email, deal.amount, 1)
        db.add_sale_records(deal_id, user["id"], deal.products)
        cart.remove_all_product_from_cart(user["id"])
        order_number = datetime.now().strftime("%Y%m%d%H%M%S") + str(user["id"])
        payment.add_wallet_payment(order_number, deal_id, user["id"], deal.amount)
        db.update_seller_savings(deal.products)
        user_db.update_buyer_savings(user["id"], deal.amount)
        await add_notification_to_db(user["id"], user["username"], deal.products, 0, message = None, commission_id=None)
    except Exception as e:
        print(e)
        return JSONResponse(status_code=500, content={"error": True, "message": "伺服器內部錯誤"})  

@router.post("/api/deal/line/notify", include_in_schema=False)
async def get_line_callback(body = Body()):
    try:
        order_number = body["order_number"]
        label = order_number.split("-")[-2]
        commission_id = order_number.split("-")[-1]
        if body["status"] == 0:
            deal_id, user_id, username = payment.get_payment(order_number)
            db.mark_as_success(deal_id)
            products = db.get_deal_products_by_id(deal_id)
            products = json.loads(products)
            db.add_sale_records(deal_id, user_id, products)
            if label != "commission":
                cart.remove_all_product_from_cart(user_id)
                db.update_seller_savings(products)
                await add_notification_to_db(user_id, username, products, 0, message=None, commission_id=None)
            elif label == "commission":
                commission.update_commission(commission_id=commission_id, is_paid=1)
                await add_notification_to_db(user_id, username, products, 5, message=None, commission_id=int(commission_id))
    except Exception as e:
        print(e)
        return JSONResponse(status_code=500, content={"error": True, "message": "伺服器內部錯誤"})  
    
@router.get("/api/deal/line/redirect", include_in_schema=False)
def line_frontend(status:int = Query(), order_number:str = Query()):
    try:
        commission_id = int(order_number.split("-")[-1])
        label = order_number.split("-")[-2]
        if status == 0:
            if label == "commission" and commission_id:
                return RedirectResponse(f"/property/commission/{commission_id}")
            return RedirectResponse("/library")
    except Exception as e:
        print(e)