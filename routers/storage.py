from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse, StreamingResponse
from database import storage as db, commission, deal, notification
from models import storage as model
from .user import get_auth_user
import requests

router = APIRouter()

@router.get("/api/storage")
def get_all_storage(user = Depends(get_auth_user)) -> model.StorageOut:
    if not user:
        return JSONResponse(status_code=403, content={"error": True, "message": "未登入系統，拒絕存取"})
    try:
        data = db.get_all_storage(user_id=user["id"], product_id=None, product_type=0)
        return JSONResponse(status_code=200, content={"data": data})
    except Exception as e:
        print(e)
        return JSONResponse(status_code=500, content={"error": True, "message": "伺服器內部錯誤"})

@router.get("/api/storage/commissions")
def get_all_commission_storage(user = Depends(get_auth_user)) -> model.CommissionOut:
    if not user:
        return JSONResponse(status_code=403, content={"error": True, "message": "未登入系統，拒絕存取"})
    try:
        data = commission.get_commissions_by_buyer(user["id"])
        return JSONResponse(status_code=200, content={"data": data})
    except Exception as e:
        print(e)
        return JSONResponse(status_code=500, content={"error": True, "message": "伺服器內部錯誤"})
    
@router.get("/api/storage/download/commission/{commission_id}")
async def get_commission_download_url(commission_id:int, user = Depends(get_auth_user)) -> model.CommissionUrl:
    if not user:
        return JSONResponse(status_code=403, content={"error": True, "message": "未登入系統，拒絕存取"})
    try:
        data = commission.get_commission_download_by_id_by_buyer(user["id"], commission_id)
        product = data["commission"]["product"]
        if data["commission"]["is_downloaded"] == 0:
            commission.update_commission(commission_id=commission_id, is_downloaded=1)
            deal.update_seller_savings([product["id"]])
            await notification.add_notification(user["id"], user["username"], [product["owner"]["id"]], 7, [product["id"]], None, commission_id=commission_id)
        return JSONResponse(status_code=200, content={"file_url": data["commission"]["file_url"]})
    except Exception as e:
        print(e)
        return JSONResponse(status_code=500, content={"error": True, "message": "伺服器內部錯誤"})
    
@router.get("/api/storage/download/{download_endpoint}")
def download_product(download_endpoint, user = Depends(get_auth_user)):
    if not user:
         return JSONResponse(status_code=403, content={"error": True, "message": "未登入系統，拒絕存取"})
    try:
        source_url = db.get_source_url(user["id"], download_endpoint)
        if not source_url:
             return JSONResponse(status_code=404, content={"error": True, "message": "檔案不存在"})
        response = requests.get(source_url, stream=True)
        return StreamingResponse(
            response.raw, 
            media_type='application/octet-stream', 
        )
    except Exception as e:
        print(e)
        return JSONResponse(status_code=500, content={"error": True, "message": "伺服器內部錯誤"})
    
    
@router.get("/api/storage/commission/{commission_id}")
def get_commission_storage(commission_id:int, user = Depends(get_auth_user)) -> model.CommissionOutSingle:
    if not user:
        return JSONResponse(status_code=403, content={"error": True, "message": "未登入系統，拒絕存取"})
    try:
        data = commission.get_commission_by_id_by_buyer(user["id"], commission_id)
        return JSONResponse(status_code=200, content=data)
    except Exception as e:
        print(e)
        return JSONResponse(status_code=500, content={"error": True, "message": "伺服器內部錯誤"})
    
@router.get("/api/storage/product/{product_id}")
def get_storage(product_id: int | None = None, user = Depends(get_auth_user)) -> model.Storage:
    if not user:
        return JSONResponse(status_code=403, content={"error": True, "message": "未登入系統，拒絕存取"})
    try:
        data = db.get_all_storage(user_id=user["id"], product_id=product_id, product_type=0)
        if data:
            result = data[0]
        else:
            result = None
        return JSONResponse(status_code=200, content=result)
    except Exception as e:
        print(e)
        return JSONResponse(status_code=500, content={"error": True, "message": "伺服器內部錯誤"})


