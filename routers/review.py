from fastapi import APIRouter, Query, Depends
from fastapi.responses import JSONResponse
from typing import Annotated
from database import review as db, deal, product, notification
from models import review as model
from .user import get_auth_user
import json

router = APIRouter()

@router.get("/api/review/{product_id}")
def get_reviews(product_id: int, page: Annotated[int, Query(ge=0)]):
    try:
        result = db.get_reviews(product_id, page)
        return JSONResponse(status_code=200, content=result)
    except:
        return JSONResponse(status_code=500, content={"error": True, "message": "伺服器內部錯誤"})
    
@router.get("/api/review")
def get_my_reviews(product_id: int | None = None, user = Depends(get_auth_user)):
    try:
        result = db.get_review(product_id, user["id"])
        return JSONResponse(status_code=200, content= {"data": result})
    except:
        return JSONResponse(status_code=500, content={"error": True, "message": "伺服器內部錯誤"})

@router.post("/api/review")
async def create_review(review: model.ReviewIn, user = Depends(get_auth_user)):
    try:
        if not user:
            return JSONResponse(status_code=403, content={"error": True, "message": "未登入系統，拒絕存取"})
        product_bought = deal.get_all_deals(user_id=user["id"], success=1)
        review_existed = db.get_review(product_id=review.product_id, user_id=user["id"])
        if product_bought and not review_existed:
            review = review.model_dump()
            db.add_review(**review, reviewer_id=user["id"])
            owner_id = product.get_owner_by_product_id(review["product_id"])
            await notification.add_single_notification(user["id"], user["username"], owner_id, 1, review["product_id"])
            return JSONResponse(status_code=200, content={"ok": True})
        else:
            return JSONResponse(status_code=400, content={"error": True, "message": "重複評論或未購買該商品"})
    except Exception as e:
        print(e)
        return JSONResponse(status_code=500, content={"error": True, "message": "伺服器內部錯誤"})

@router.put("/api/review")
async def update_review(review: model.ReviewIn, user = Depends(get_auth_user)):
    try:
        if not user:
            return JSONResponse(status_code=403, content={"error": True, "message": "未登入系統，拒絕存取"})
        review_list = db.get_review(product_id=review.product_id, user_id=user["id"])
        if review_list:
            review = review.model_dump()
            db.update_review(**review, review_id=review_list[0]["review"]["id"])
            owner_id = product.get_owner_by_product_id(review["product_id"])
            await notification.add_single_notification(user["id"], user["username"], owner_id, 2, review["product_id"])
            return JSONResponse(status_code=200, content={"ok": True})
        else:
            return JSONResponse(status_code=400, content={"error": True, "message": "評論不存在"})
    except Exception as e:
        print(e)
        return JSONResponse(status_code=500, content={"error": True, "message": "伺服器內部錯誤"})