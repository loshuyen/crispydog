from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/", include_in_schema=False)
def home():
    return FileResponse("./static/index.html")

@app.get("/favicon.ico", include_in_schema=False)
def favico():
    return FileResponse("favicon.ico")

@app.get("/product/{id}", include_in_schema=False)
def product():
    return FileResponse("./static/product.html")