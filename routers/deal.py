from fastapi import APIRouter, Depends, Query
from fastapi.responses import JSONResponse
from database import deal as db
from .user import get_auth_user
from models import deal as model
from datetime import datetime
from utils import pay

router = APIRouter()

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

@router.post("/api/deal")
def create_deal(deal: model.Deal, user = Depends(get_auth_user)):
    try:
        if not user:
            return JSONResponse(status_code=403, content={"error": True, "message": "未登入系統，拒絕存取"})
        if deal.deal.amount != db.calculate_amount(deal.deal.products):
            return JSONResponse(status_code=400, content={"error": True, "message": "輸入金額錯誤"})
        deal_id = db.add_deal(user["id"], deal.deal.products, deal.deal.delivery_email, deal.deal.amount)
        pay_result = pay.tappay_direct_pay(
            prime=deal.prime, 
            amount=deal.deal.amount, 
            order_number=datetime.now().strftime("%Y%m%d-%H%M%S-") + str(user["id"]), 
            phone_number=deal.contact.phone_number, 
            name=deal.contact.name, 
            email=deal.contact.email
        )
        if pay_result["payment"]["status"] != 0:
            return {"data": pay_result}
        elif pay_result["payment"]["status"] == 0:
            db.mark_as_success(deal_id)
            db.add_sale_records(deal_id, user["id"], deal.deal.products)
            pay_result["payment"]["message"] = "付款成功"
            return {"data": pay_result}
        else:
            return JSONResponse(status_code=400, content={"error": True, "message": "訂單建立失敗，輸入不正確或其他原因"})
    except Exception as e:
        print(e)
        return JSONResponse(status_code=500, content={"error": True, "message": "伺服器內部錯誤"})  
    