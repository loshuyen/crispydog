from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
import jwt
import os
import datetime
from models import user as model
from database import user as db

router = APIRouter()
security = HTTPBearer(auto_error=False)

def get_auth_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
    try:
        token = credentials.credentials
        decode_data = jwt.decode(token, os.getenv("TOKEN_SECRET_KEY"), algorithms="HS256")
        username_from_db = db.get_username_by_id(decode_data["id"])
        if username_from_db == decode_data["username"]:
            return decode_data
        else:
            return None
    except:
        return None
	
@router.get("/api/user/auth")
def get_current_user(user = Depends(get_auth_user)) -> model.UserResponse:
    try:
        return {"data": {"id": user["id"], "username": user["username"]}}
    except:
        return {"data": None}
    
@router.put("/api/user/auth")
def login(user: model.UserIn):
    try:
        user_data = db.verify_password(user.username, user.password)
        if not user_data:
            return JSONResponse(status_code=400, content={"error": True, "message": "登入失敗，Email、密碼錯誤或尚未註冊"})
        current_utc_time = datetime.datetime.now()
        future_utc_time = current_utc_time + datetime.timedelta(days=7)
        future_unix_timestamp = int(datetime.datetime.timestamp(future_utc_time))
        user_data["exp"] = future_unix_timestamp
        token = jwt.encode(user_data, os.getenv("TOKEN_SECRET_KEY"), algorithm="HS256")
        return JSONResponse(status_code=200, content={"token": token})
    except Exception as e:
        print(e)
        return JSONResponse(status_code=500, content={"error": True, "message": "伺服器內部錯誤"})

@router.post("/api/user")
def signup(user: model.UserIn):
    try:
        exist_user = db.get_user_by_username(user.username)
        if exist_user:
            return JSONResponse(status_code=400, content={"error": True, "message": "註冊失敗，重複的帳號"})
        db.add_user(user.username, user.password)
        return JSONResponse(status_code=200, content={"ok": True})
    except:
        return JSONResponse(status_code=500, content={"error": True, "message": "伺服器內部錯誤"})