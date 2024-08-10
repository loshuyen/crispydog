from fastapi import APIRouter, Depends, Query
from fastapi.responses import JSONResponse
from database import deal as db
from .user import get_auth_user
from models import deal as model

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
        db.add_deal(user["id"], deal.products, deal.delivery_email, deal.amount)
        return JSONResponse(status_code=200, content={"ok": True})
    except IndexError:
        return JSONResponse(status_code=400, content={"error": True, "message": "product id 錯誤"})
    except Exception as e:
        print(e)
        return JSONResponse(status_code=500, content={"error": True, "message": "伺服器內部錯誤"})  
    