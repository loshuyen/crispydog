from fastapi import APIRouter, Query, Depends
from fastapi.responses import JSONResponse
from typing import Annotated
from database import review as db, deal
from models import review as model
from .user import get_auth_user

router = APIRouter()

@router.get("/api/review/{product_id}")
def get_reviews(product_id: int, page: Annotated[int, Query(ge=0)]):
    try:
        result = db.get_reviews(product_id, page)
        return JSONResponse(status_code=200, content=result)
    except:
        return JSONResponse(status_code=500, content={"error": True, "message": "伺服器內部錯誤"})

@router.post("/api/review")
def create_review(review: model.ReviewIn, user = Depends(get_auth_user)):
    try:
        if not user:
            return JSONResponse(status_code=403, content={"error": True, "message": "未登入系統，拒絕存取"})
        product_bought = deal.get_all_deals(user_id=user["id"], role=0, product_id=review.product_id, success=1)
        review_existed = db.get_review(product_id=review.product_id, user_id=user["id"])
        if product_bought and not review_existed:
            review = review.model_dump()
            db.add_review(**review, reviewer_id=user["id"])
            return JSONResponse(status_code=200, content={"ok": True})
        else:
            return JSONResponse(status_code=400, content={"error": True, "message": "重複評論或未購買該商品"})
    except:
        return JSONResponse(status_code=500, content={"error": True, "message": "伺服器內部錯誤"})

@router.put("/api/review")
def update_review(review: model.ReviewIn, user = Depends(get_auth_user)):
    try:
        if not user:
            return JSONResponse(status_code=403, content={"error": True, "message": "未登入系統，拒絕存取"})
        review_existed_id = db.get_review(product_id=review.product_id, user_id=user["id"])
        if review_existed_id:
            review = review.model_dump()
            db.update_review(**review, review_id=review_existed_id)
            return JSONResponse(status_code=200, content={"ok": True})
        else:
            return JSONResponse(status_code=400, content={"error": True, "message": "評論不存在"})
    except:
        return JSONResponse(status_code=500, content={"error": True, "message": "伺服器內部錯誤"})