from fastapi import APIRouter, UploadFile, Form, Depends
from fastapi.responses import JSONResponse
from pydantic import ValidationError
from typing import Annotated
from models import product as model
from database import product as db
from utils import aws_s3
from .user import get_auth_user

router = APIRouter()

@router.get("/api/products")
def get_all_products() -> model.Product:
    try:
        data = db.get_published_products()
        return JSONResponse(status_code=200, content={"data": data})
    except Exception as e:
        print(e)
        return JSONResponse(status_code=500, content={"error": True, "message": "伺服器內部錯誤"})

@router.get("/api/product/{id}")
def get_product_by_id(id):
    try:
        data = db.get_product(id)
        return {"data": data}
    except Exception as e:
        print(e)
        return JSONResponse(status_code=500, content={"error": True, "message": "伺服器內部錯誤"})
    
@router.post("/api/product")
async def create_product(
    image_file: UploadFile, 
    thumbnail_file: UploadFile,
    product_file: UploadFile,
    name: Annotated[str, Form()],
    price: Annotated[int, Form()],
    introduction: Annotated[str | None, Form()] = None,
    specification: Annotated[str | None, Form(description="{'item': '商品項目', 'description': '項目說明'}")] = None,
    stock: Annotated[int, Form()] = 9999,
    user = Depends(get_auth_user)
):
    try:
        if not user:
            return JSONResponse(status_code=403, content={"error": True, "message": "未登入系統，拒絕存取"})
        user_id = user["id"]
        image_file_type = image_file.filename.split(".")[1]
        thumbnail_file_type = thumbnail_file.filename.split(".")[1]
        product_file_type = product_file.filename.split(".")[1]
        image_file
        image_urls, _ = aws_s3.upload_file(image_file.file, image_file_type).values()
        thumbnail_url, _ = aws_s3.upload_file(thumbnail_file.file, thumbnail_file_type).values()
        product_url, product_size = aws_s3.upload_file(product_file.file, product_file_type).values()
        db.add_product(
            product_name=name, 
            user_id=user_id,
            price=price,
            image_urls=image_urls,
            thumbnail_url=thumbnail_url,
            introduction=introduction,
            specification=specification,
            file_type=product_file_type,
            file_size=product_size,
            stock=stock,
            source_url=product_url
        )
        return JSONResponse(status_code=200, content={"ok": True})
    except ValidationError:
        return JSONResponse(status_code=400, content={"error": True, "message": "輸入不正確"})
    except Exception as e:
        print(e)
        return JSONResponse(status_code=500, content={"error": True, "message": "伺服器內部錯誤"})
