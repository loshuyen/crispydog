from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from database import sale as db
from .user import get_auth_user

router = APIRouter()

@router.get("/api/sale")
def get_sales(user = Depends(get_auth_user)):
    if not user:
        return JSONResponse(status_code=403, content={"error": True, "message": "未登入系統，拒絕存取"})
    try:
        data = db.get_all_sales(user["id"])
        return JSONResponse(status_code=200, content={"data": data})
    except Exception as e:
        print(e)
        return JSONResponse(status_code=500, content={"error": True, "message": "伺服器內部錯誤"})