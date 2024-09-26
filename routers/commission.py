from fastapi import APIRouter, Form, Depends, UploadFile, Body
from fastapi.responses import JSONResponse
from typing import Annotated
from pydantic import ValidationError
from database import commission as db, deal, notification, product, payment, user as user_db
from models import commission as model
from models.response import ResponseOK
from models.deal import PayResultOut
from .user import get_auth_user
from utils import aws_s3, pay
from datetime import datetime
from zoneinfo import ZoneInfo

router = APIRouter()

@router.get("/api/commissions")
def get_all_commissions_by_seller(user = Depends(get_auth_user)) -> model.CommissionOutList:
    if not user:
        return JSONResponse(status_code=403, content={"error": True, "message": "未登入系統，拒絕存取"})
    try:
        data = db.get_commissions_by_seller(user["id"])
        return JSONResponse(status_code=200, content={"data": data})
    except ValidationError:
        return JSONResponse(status_code=400, content={"error": True, "message": "輸入不正確"})
    except Exception as e:
        print(e)
        return JSONResponse(status_code=500, content={"error": True, "message": "伺服器內部錯誤"})

@router.get("/api/commission/{commission_id}")
def get_commission_by_seller(commission_id:int, user = Depends(get_auth_user)) -> model.CommissionOut:
    if not user:
        return JSONResponse(status_code=403, content={"error": True, "message": "未登入系統，拒絕存取"})
    try:
        data = db.get_commission_by_id_by_seller(user["id"], commission_id)
        return JSONResponse(status_code=200, content=data[0])
    except ValidationError:
        return JSONResponse(status_code=400, content={"error": True, "message": "輸入不正確"})
    except Exception as e:
        print(e)
        return JSONResponse(status_code=500, content={"error": True, "message": "伺服器內部錯誤"})

@router.post("/api/commission")
async def create_commission(product_id: Annotated[int, Form()], photo_file: UploadFile, user = Depends(get_auth_user)) -> ResponseOK:
    if not user:
        return JSONResponse(status_code=403, content={"error": True, "message": "未登入系統，拒絕存取"})
    try:
        photo_file_type = photo_file.filename.split(".")[1]
        photo_url, _ = aws_s3.upload_file(photo_file.file, photo_file_type).values()
        print(1)
        deal_id = deal.add_deal(user["id"], [product_id], "", 0)
        print(2)
        commission_id = db.add_commission(deal_id, photo_url, product_id)
        print(3)
        owner_id = product.get_owner_by_product_id(product_id)
        print(4)
        await notification.add_notification(user["id"], user["username"], [owner_id], 3, [product_id], None, commission_id=commission_id)
        print(5)
        return JSONResponse(status_code=200, content={"ok": True})
    except ValidationError:
        return JSONResponse(status_code=400, content={"error": True, "message": "輸入不正確"})
    except Exception as e:
        print(e)
        return JSONResponse(status_code=500, content={"error": True, "message": "伺服器內部錯誤"})

@router.put("/api/commission/photo")
async def confirm_photo(commission: model.Commission, user = Depends(get_auth_user)) -> ResponseOK:
    if not user:
        return JSONResponse(status_code=403, content={"error": True, "message": "未登入系統，拒絕存取"})
    try:
        commission_info = db.get_commission(commission.id)
        if commission_info["owner"]["id"] != user["id"]:
            return JSONResponse(status_code=400, content={"error": True, "message": "無操作權限"})
        db.update_commission(commission_id=commission.id, is_accepted=1)
        await notification.add_notification(user["id"], user["username"], [commission_info["buyer"]["id"]], 4, [commission_info["product"]["id"]], None, commission_id=commission.id)
        return JSONResponse(status_code=200, content={"ok": True})
    except ValidationError:
        return JSONResponse(status_code=400, content={"error": True, "message": "輸入不正確"})
    except Exception as e:
        print(e)
        return JSONResponse(status_code=500, content={"error": True, "message": "伺服器內部錯誤"})
    
@router.put("/api/commission/pay/creditcard")
async def pay_commission_by_credit_card(commission: model.Pay, user = Depends(get_auth_user)) -> PayResultOut:
    if not user:
        return JSONResponse(status_code=403, content={"error": True, "message": "未登入系統，拒絕存取"})
    try:
        commission_info = db.get_commission(commission.commission_id)
        if commission_info["is_accepted"] != 1 or commission_info["buyer"]["id"] != user["id"]:
            return JSONResponse(status_code=400, content={"error": True, "message": "無操作權限"})
        pay_result = pay.tappay_direct_pay(
            prime=commission.prime, 
            amount=commission_info["product"]["price"], 
            order_number=datetime.now(ZoneInfo("Asia/Taipei")).strftime("%Y%m%d-%H%M%S-") + str(user["id"]),
            phone_number=commission.contact.phone_number, 
            name=commission.contact.name, 
            email=commission.contact.email
        )
        if pay_result["payment"]["status"] != 0:
            return {"data": pay_result}
        elif pay_result["payment"]["status"] == 0:
            deal.mark_as_success(commission_info["deal"]["id"])
            deal.add_sale_records(commission_info["deal"]["id"], user["id"], [commission_info["product"]["id"]])
            payment.add_payment(pay_result, commission_info["deal"]["id"], user["id"])
            db.update_commission(commission_id=commission.commission_id, is_paid=1)
            await notification.add_notification(user["id"], user["username"], [commission_info["owner"]["id"]], 5, [commission_info["product"]["id"]], None, commission_id=commission.commission_id)
            return {
                "data": {
                    "number": pay_result["number"],
                    "payment": {
                        "method": "credit_card",
                        "status": pay_result["payment"]["status"],
                        "message": pay_result["payment"]["message"],
                    }
                }
            }
    except ValidationError:
        return JSONResponse(status_code=400, content={"error": True, "message": "輸入不正確"})
    except Exception as e:
        print(e)
        return JSONResponse(status_code=500, content={"error": True, "message": "伺服器內部錯誤"})
    
@router.put("/api/commission/pay/wallet")
async def pay_commission_by_wallet(commission: model.PayWallet, user = Depends(get_auth_user)) -> PayResultOut:
    if not user:
        return JSONResponse(status_code=403, content={"error": True, "message": "未登入系統，拒絕存取"})
    try:
        commission_info = db.get_commission(commission.commission_id)
        if commission_info["is_accepted"] != 1 or commission_info["buyer"]["id"] != user["id"]:
            return JSONResponse(status_code=400, content={"error": True, "message": "無操作權限"})
        savings = user_db.get_savings(user["id"])
        order_number = datetime.now(ZoneInfo("Asia/Taipei")).strftime("%Y%m%d%H%M%S") + str(user["id"])
        
        if savings < commission_info["product"]["price"]:
            return JSONResponse(status_code=400, content={"error": True, "message": "錢包餘額不足"})
        
        user_db.update_buyer_savings(user["id"], commission_info["product"]["price"])
        deal.mark_as_success(commission_info["deal"]["id"])
        deal.add_sale_records(commission_info["deal"]["id"], user["id"], [commission_info["product"]["id"]])
        payment.add_wallet_payment(order_number, commission_info["deal"]["id"], user["id"], commission_info["product"]["price"])
        db.update_commission(commission_id=commission.commission_id, is_paid=1)
        await notification.add_notification(user["id"], user["username"], [commission_info["owner"]["id"]], 5, [commission_info["product"]["id"]], None, commission_id=commission.commission_id)        
        return {
            "data": {
                "number": order_number,
                "payment": {
                    "method": "wallet",
                    "status": 0,
                    "message": "success",
                }
            }
        }
    except Exception as e:
        print(e)
        return JSONResponse(status_code=500, content={"error": True, "message": "伺服器內部錯誤"})

@router.put("/api/commission/pay/line")
async def pay_commission_by_linepay(commission: model.Pay, user = Depends(get_auth_user)) -> model.CommissionLinePayUrl:
    if not user:
        return JSONResponse(status_code=403, content={"error": True, "message": "未登入系統，拒絕存取"})
    try:
        commission_info = db.get_commission(commission.commission_id)
        if commission_info["is_accepted"] != 1 or commission_info["buyer"]["id"] != user["id"]:
            return JSONResponse(status_code=400, content={"error": True, "message": "無操作權限"})
        pay_result = pay.tappay_line_pay(
            prime=commission.prime, 
            amount=commission_info["product"]["price"], 
            order_number=datetime.now(ZoneInfo("Asia/Taipei")).strftime("%Y%m%d%H%M%S") + str(user["id"]) + "-" + "commission" + "-" + str(commission.commission_id), 
            phone_number=commission.contact.phone_number, 
            name=commission.contact.name, 
            email=commission.contact.email
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
            payment.add_payment(payment_body, commission_info["deal"]["id"], user["id"])
            return {"payment_url": pay_result["payment_url"]}
    except ValidationError:
        return JSONResponse(status_code=400, content={"error": True, "message": "輸入不正確"})
    except Exception as e:
        print(e)
        return JSONResponse(status_code=500, content={"error": True, "message": "伺服器內部錯誤"})


@router.put("/api/commission/delivery")
async def deliver_outcome(commission_id: Annotated[int, Form()], outcome: UploadFile, user = Depends(get_auth_user)) -> ResponseOK:
    if not user:
        return JSONResponse(status_code=403, content={"error": True, "message": "未登入系統，拒絕存取"})
    try:
        commission_info = db.get_commission(commission_id)
        if commission_info["owner"]["id"] != user["id"] or commission_info["is_paid"] != 1:
            return JSONResponse(status_code=400, content={"error": True, "message": "無操作權限"})
        file_type = outcome.filename.split(".")[1]
        file_url, _ = aws_s3.upload_file(outcome.file, file_type).values()
        db.update_file_url(commission_id, file_url)
        db.update_commission(commission_id, is_delivered=1)
        await notification.add_notification(user["id"], user["username"], [commission_info["buyer"]["id"]], 6, [commission_info["product"]["id"]], None, commission_id=commission_id)
        return JSONResponse(status_code=200, content={"ok": True})
    except ValidationError:
        return JSONResponse(status_code=400, content={"error": True, "message": "輸入不正確"})
    except Exception as e:
        print(e)
        return JSONResponse(status_code=500, content={"error": True, "message": "伺服器內部錯誤"})