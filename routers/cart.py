from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from database import cart as db, product as product_db
from models import cart as model
from models.response import ResponseOK
from .user import get_auth_user
from mysql.connector import DataError

router = APIRouter()

@router.get("/api/cart")
def get_cart_list(user = Depends(get_auth_user)) -> model.CartOut:
    if not user:
        return JSONResponse(status_code=403, content={"error": True, "message": "未登入系統，拒絕存取"})
    try:
        data = db.get_all_from_cart(user["id"])
        return JSONResponse(status_code=200, content={"data": data})
    except Exception as e:
        print(e)
        return JSONResponse(status_code=500, content={"error": True, "message": "伺服器內部錯誤"}) 

@router.post("/api/cart")
def add_product_to_cart(product: model.CartIn, user = Depends(get_auth_user)) -> ResponseOK:
    if not user:
        return JSONResponse(status_code=403, content={"error": True, "message": "未登入系統，拒絕存取"})
    try:
        existed_product = product_db.get_product(product.id)
        if not existed_product:
            return JSONResponse(status_code=400, content={"error": True, "message": "輸入格式錯誤或product_id不存在"})
        product_in_cart = db.find_product_in_card(user["id"], product.id)
        if product_in_cart:
            return JSONResponse(status_code=400, content={"error": True, "message": "商品已在購物車中"})
        db.add_product_to_cart(user["id"], product.id)
        return JSONResponse(status_code=200, content={"ok": True})
    except Exception as e:
        print(e)
        return JSONResponse(status_code=500, content={"error": True, "message": "伺服器內部錯誤"}) 

@router.delete("/api/cart")
def remove_product_from_cart(product: model.CartIn, user = Depends(get_auth_user)) -> ResponseOK:
    if not user:
        return JSONResponse(status_code=403, content={"error": True, "message": "未登入系統，拒絕存取"})
    try:
        db.remove_product_from_cart(user["id"], product.id)
        return JSONResponse(status_code=200, content={"ok": True})
    except IndexError:
        return JSONResponse(status_code=400, content={"error": True, "message": "輸入格式錯誤或product_id不存在"})
    except Exception as e:
        print(e)
        return JSONResponse(status_code=500, content={"error": True, "message": "伺服器內部錯誤"})