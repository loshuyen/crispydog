from fastapi import APIRouter, Depends, Query
from fastapi.responses import JSONResponse
from database import deal as db
from .user import get_auth_user

router = APIRouter()

@router.get("/api/deals")
def get_deal(
        product_id: int | None = None, 
        success: int | None = Query(default=None, ge=0, le=1, description="0: 未成交的訂單、1: 已成交的訂單、Null: 所有訂單"), 
        user = Depends(get_auth_user), 
        role: int = Query(ge=0, le=1, description="0: 買家、1: 賣家")
    ):
    try:
        if not user:
            return JSONResponse(status_code=403, content={"error": True, "message": "未登入系統，拒絕存取"})
        data = db.get_all_deals(user["id"], role, product_id, success)
        return JSONResponse(status_code=200, content={"data": data})
    except Exception as e:
        print(e)
        return JSONResponse(status_code=500, content={"error": True, "message": "伺服器內部錯誤"})

@router.post("/api/deal")
def create_deal(product_id:int, delivery_email:str | None = None, user = Depends(get_auth_user)):
    try:
        if not user:
            return JSONResponse(status_code=403, content={"error": True, "message": "未登入系統，拒絕存取"})
        db.add_deal(user["id"], product_id, delivery_email)
        return JSONResponse(status_code=200, content={"ok": True})
    except Exception as e:
        print(e)
        return JSONResponse(status_code=500, content={"error": True, "message": "伺服器內部錯誤"})  
    