from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse, RedirectResponse
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
import jwt
import os
import datetime
from models import user as model
from database import user as db
from utils import google_auth
import requests

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
	
def generate_token(user_data):
    current_utc_time = datetime.datetime.now()
    future_utc_time = current_utc_time + datetime.timedelta(days=7)
    future_unix_timestamp = int(datetime.datetime.timestamp(future_utc_time))
    user_data["exp"] = future_unix_timestamp
    token = jwt.encode(user_data, os.getenv("TOKEN_SECRET_KEY"), algorithm="HS256")
    return token
    
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
        token = generate_token(user_data)
        return JSONResponse(status_code=200, content={"token": token})
    except Exception as e:
        print(e)
        return JSONResponse(status_code=500, content={"error": True, "message": "伺服器內部錯誤"})

@router.get("/api/user")
def get_user_profile(user = Depends(get_auth_user)):
    if not user:
        return JSONResponse(status_code=403, content={"error": True, "message": "未登入系統，拒絕存取"})
    try:
        result = db.get_user_profile_by_id(user["id"])
        return JSONResponse(status_code=200, content=result)
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

@router.get("/api/user/auth/google")
def request_google_auth_token():
    authorization_url = google_auth.fetch_auth()
    return {"url": authorization_url}

@router.get("/api/user/auth/google/callback", include_in_schema=False)
def get_google_auth_token(code: str):
    credentials = google_auth.get_credential(code)
    client_id = credentials.client_id
    user_info_url = "https://www.googleapis.com/oauth2/v3/userinfo"
    headers = {"Authorization": f"Bearer {credentials.token}"}
    response = requests.get(user_info_url, headers=headers)
    user_name = None
    user_id = None
    user_email = None
    if response.status_code == 200:
        user_info = response.json()
        user_name = user_info.get("name")
        user_id = user_info.get("sub")
        user_email = user_info.get("email")
    user_id = int(user_id) % 100000000
    user = db.get_username_by_id(user_id)
    if not user:
        db.add_google_user(user_id, user_name)
    token = generate_token({"id": user_id, "username": user_name})
    return RedirectResponse(f"/index?token={token}")