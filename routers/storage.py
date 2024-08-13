from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse, StreamingResponse
from database import storage as db
from .user import get_auth_user
import requests

router = APIRouter()

@router.get("/api/storage")
def get_all_storage(product_id: int | None = None, user = Depends(get_auth_user)):
    if not user:
        return JSONResponse(status_code=403, content={"error": True, "message": "未登入系統，拒絕存取"})
    try:
        data = db.get_all_storage(user["id"], product_id)
        return JSONResponse(status_code=200, content={"data": data})
    except Exception as e:
        print(e)
        return JSONResponse(status_code=500, content={"error": True, "message": "伺服器內部錯誤"})

@router.get("/api/storage/download/{download_endpoint}")
def download_product(download_endpoint, user = Depends(get_auth_user)):
    if not user:
         return JSONResponse(status_code=403, content={"error": True, "message": "未登入系統，拒絕存取"})
    try:
        soure_url = db.get_source_url(user["id"], download_endpoint)
        if not soure_url:
             return JSONResponse(status_code=404, content={"error": True, "message": "檔案不存在"})
        file_type = soure_url.split(".")[-1]
        response = requests.get(soure_url, stream=True)
        return StreamingResponse(
            response.raw, 
            media_type='application/octet-stream', 
            headers={"Content-Disposition": f"attachment; filename={user["username"]}.{file_type}"}
        )
    except Exception as e:
        print(e)
        return JSONResponse(status_code=500, content={"error": True, "message": "伺服器內部錯誤"})