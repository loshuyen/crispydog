from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from routers import product, user, review, deal, cart

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")

app.include_router(product.router, tags=["Product"])
app.include_router(user.router, tags=["User"])
app.include_router(review.router, tags=["Review"])
app.include_router(deal.router, tags=["Deal"])
app.include_router(cart.router, tags=["Cart"])

@app.get("/", include_in_schema=False)
def home():
    return FileResponse("./static/index.html")

@app.get("/favicon.ico", include_in_schema=False)
def favico():
    return FileResponse("./static/images/favicon.ico")

@app.get("/product/add", include_in_schema=False)
def property():
    return FileResponse("./static/add_product.html")

@app.get("/product/{id}", include_in_schema=False)
def product():
    return FileResponse("./static/product.html")

@app.get("/checkout", include_in_schema=False)
def checkout():
    return FileResponse("./static/checkout.html")

@app.get("/library", include_in_schema=False)
def library():
    return FileResponse("./static/library.html")

@app.get("/property", include_in_schema=False)
def property():
    return FileResponse("./static/property.html")

@app.get("/store", include_in_schema=False)
def store():
    return FileResponse("./static/store.html")
