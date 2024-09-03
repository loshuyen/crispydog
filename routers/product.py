from fastapi import APIRouter, UploadFile, Form, Depends, Query
from fastapi.responses import JSONResponse
from pydantic import ValidationError
from typing import Annotated, Union
from models import product as model
from models.response import ResponseOK, ResponseError
from database import product as db
from utils import aws_s3
from .user import get_auth_user

router = APIRouter()

@router.get("/api/products")
def get_all_products(keyword: str | None = None, product_type: str | None = None, page: Annotated[int, Query(ge=0)] = 0) -> model.Product:
    try:
        data = db.get_published_products(keyword, product_type, page)
        return JSONResponse(status_code=200, content=data)
    except Exception as e:
        print(e)
        return JSONResponse(status_code=500, content={"error": True, "message": "伺服器內部錯誤"})

@router.get("/api/product/{id}")
def get_product_by_id(id) -> model.ProductDetail | dict:
    try:
        data = db.get_product(id)
        print(data)
        return {"data": data}
    except Exception as e:
        print(e)
        return JSONResponse(status_code=500, content={"error": True, "message": "伺服器內部錯誤"})

@router.get("/api/products/auth")
def get_products_by_owner(user = Depends(get_auth_user)) -> model.ProductOwner:
    try:
        data = db.get_owner_products(user["id"])
        return {"data": data}
    except Exception as e:
        print(e)
        return JSONResponse(status_code=500, content={"error": True, "message": "伺服器內部錯誤"})
    
@router.get("/api/products/owner")
def get_products_by_owner_name(username) -> model.ProductOwnerPublic:
    try:
        data = db.get_product_by_ownername(username)
        return {"data": data}
    except Exception as e:
        print(e)
        return JSONResponse(status_code=500, content={"error": True, "message": "伺服器內部錯誤"})

@router.post("/api/product", response_model=Union[ResponseOK, ResponseError])
async def create_product(
    image_file: UploadFile, 
    thumbnail_file: UploadFile,
    name: Annotated[str, Form()],
    price: Annotated[int, Form()],
    product_file: UploadFile | None = None,
    introduction: Annotated[str | None, Form()] = None,
    specification: Annotated[str | None, Form()] = None,
    stock: Annotated[str, Form()] = "9999",
    product_type:Annotated[int | None, Form()] = 0,
    user = Depends(get_auth_user)
):
    try:
        if not user:
            return JSONResponse(status_code=403, content={"error": True, "message": "未登入系統，拒絕存取"})
        user_id = user["id"]
        image_file_type = image_file.filename.split(".")[1]
        thumbnail_file_type = thumbnail_file.filename.split(".")[1]
        image_urls, _ = aws_s3.upload_file(image_file.file, image_file_type).values()
        thumbnail_url, _ = aws_s3.upload_file(thumbnail_file.file, thumbnail_file_type).values()
        product_file_type = None
        product_url = None
        product_size = None
        if product_type == 0 and product_file == None:
            return JSONResponse(status_code=400, content={"error": True, "message": "product_type為0時需輸入product_file"})
        if product_type == 0:
            product_file_type = product_file.filename.split(".")[1]
            product_url, product_size = aws_s3.upload_file(product_file.file, product_file_type).values()
        introduction = introduction.rstrip().replace("\n", "<br>")
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
            source_url=product_url,
            product_type=product_type
        )
        return JSONResponse(status_code=200, content={"ok": True})
    except ValidationError:
        return JSONResponse(status_code=400, content={"error": True, "message": "輸入不正確"})
    except Exception as e:
        print(e)
        return JSONResponse(status_code=500, content={"error": True, "message": "伺服器內部錯誤"})
    
@router.put("/api/product", response_model=Union[ResponseOK, ResponseError])
async def toggle_product_status(product: model.ProductId, user = Depends(get_auth_user)):
    if not user:
        return JSONResponse(status_code=403, content={"error": True, "message": "未登入系統，拒絕存取"})
    try:
        db.toggle_my_product(user["id"], product.id)
        return JSONResponse(status_code=200, content={"ok": True})
    except Exception as e:
        print(e)
        return JSONResponse(status_code=500, content={"error": True, "message": "伺服器內部錯誤"})
