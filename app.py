from fastapi import FastAPI, Request, Response
from fastapi.responses import FileResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from routers import product, user, review, deal, cart, storage, sale, notification, commission

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")

app.include_router(product.router, tags=["Product"])
app.include_router(user.router, tags=["User"])
app.include_router(review.router, tags=["Review"])
app.include_router(deal.router, tags=["Deal"])
app.include_router(cart.router, tags=["Cart"])
app.include_router(storage.router, tags=["Storage"])
app.include_router(sale.router, tags=["Sale"])
app.include_router(notification.router, tags=["Notification"])
app.include_router(commission.router, tags=["Commission"])

@app.get("/", include_in_schema=False)
def landing():
    return FileResponse("./static/landing.html")

@app.get("/index", include_in_schema=False)
def index():
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

@app.get("/checkout/commission/{id}", include_in_schema=False)
def checkout_commission():
    return FileResponse("./static/checkout_commission.html")

@app.get("/library", include_in_schema=False)
def library():
    return FileResponse("./static/library.html")

@app.get("/library/commission", include_in_schema=False)
def library_commission():
    return FileResponse("./static/commission.html")

@app.get("/property/{id}", include_in_schema=False)
def property():
    return FileResponse("./static/property.html")

@app.get("/store", include_in_schema=False)
def store():
    return FileResponse("./static/store.html")

@app.get("/sale/{product_id}", include_in_schema=False)
def sale():
    return FileResponse("./static/sale.html")

@app.get("/notification", include_in_schema=False)
def notification():
    return FileResponse("./static/notification.html")

@app.get("/profile", include_in_schema=False)
def profile():
    return FileResponse("./static/profile.html")

@app.get("/add_commission/{product_id}", include_in_schema=False)
def add_commission():
    return FileResponse("./static/add_commission.html")

@app.get("/commission", include_in_schema=False)
def commission():
    return FileResponse("./static/commission_list.html")

@app.get("/commission/{id}", include_in_schema=False)
def work_commission():
    return FileResponse("./static/work_commission.html")

@app.get("/property/commission/{id}", include_in_schema=False)
def property_commission():
    return FileResponse("./static/property_commission.html")