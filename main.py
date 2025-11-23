from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from typing import List, Optional

from models import Coupon, UserContext, Cart
from logic import check_eligibility, calculate_discount

app = FastAPI()
templates = Jinja2Templates(directory="templates")

# --- DATABASE (In-Memory) ---
coupons_db = []

# [cite: 126-127] Initialize with the mandatory hardcoded admin
users_db = {
    "hire-me@anshumat.org": {
        "email": "hire-me@anshumat.org",
        "password": "HireMe@2025!",
        "userId": "u123",
        "tier": "GOLD",
        "role": "ADMIN"  # Special role for the demo user
    }
}

# --- MODELS ---
class LoginRequest(BaseModel):
    email: str
    password: str

class SignupRequest(BaseModel):
    email: str
    password: str

class ApplicableCouponsRequest(BaseModel):
    user: UserContext
    cart: Cart

class ApplicableCouponResponse(BaseModel):
    couponCode: str
    discountAmount: float
    message: str

# --- AUTH ENDPOINTS ---

@app.post("/signup")
def signup(request: SignupRequest):
    if request.email in users_db:
        raise HTTPException(status_code=400, detail="User already exists")
    
    # Create new customer user
    new_user = {
        "email": request.email,
        "password": request.password,
        "userId": f"user_{len(users_db) + 1}",
        "tier": "REGULAR",  # Default tier for new signups
        "role": "CUSTOMER"  # Default role
    }
    users_db[request.email] = new_user
    return {"message": "Account created successfully"}

@app.post("/login")
def login(request: LoginRequest):
    user = users_db.get(request.email)
    
    # Strict credential check
    if not user or user["password"] != request.password:
        raise HTTPException(status_code=401, detail="Invalid email or password")
    
    return {
        "token": "fake-jwt-token",
        "userId": user["userId"],
        "userTier": user["tier"],
        "role": user["role"],
        "message": "Login successful"
    }

# --- COUPON ENDPOINTS ---

@app.post("/coupons")
def create_coupon(coupon: Coupon):
    coupons_db.append(coupon)
    return {"message": "Coupon created", "code": coupon.code}

@app.get("/coupons")
def list_coupons():
    return coupons_db

@app.post("/applicable-coupons")
def get_best_coupon(request: ApplicableCouponsRequest):
    eligible_coupons = []
    for coupon in coupons_db:
        if check_eligibility(coupon, request.user, request.cart):
            discount = calculate_discount(coupon, request.cart.get_total())
            eligible_coupons.append((coupon, discount))

    if not eligible_coupons:
        return {"message": "No applicable coupons found"}

    eligible_coupons.sort(key=lambda x: (-x[1], x[0].endDate))
    best_coupon, best_discount = eligible_coupons[0]

    return ApplicableCouponResponse(
        couponCode=best_coupon.code,
        discountAmount=best_discount,
        message=f"Best coupon found: {best_coupon.code}"
    )

# --- UI ROUTES ---

@app.get("/", response_class=HTMLResponse)
def show_login(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

@app.get("/admin", response_class=HTMLResponse)
def show_admin(request: Request):
    return templates.TemplateResponse("admin.html", {"request": request})

@app.get("/shop", response_class=HTMLResponse)
def show_shop(request: Request):
    return templates.TemplateResponse("shop.html", {"request": request})