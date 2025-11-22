# main.py (Updated)
from fastapi import FastAPI
from pydantic import BaseModel
from typing import List, Optional

# Import our custom modules
from models import Coupon, UserContext, Cart
from logic import check_eligibility, calculate_discount

app = FastAPI()

# In-memory database
coupons_db = []

# --- Helper Models for the Request/Response ---
class ApplicableCouponsRequest(BaseModel):
    user: UserContext
    cart: Cart

class ApplicableCouponResponse(BaseModel):
    couponCode: str
    discountAmount: float
    message: str

# --- Add this to main.py ---

class LoginRequest(BaseModel):
    email: str
    password: str

@app.post("/login")
def login(request: LoginRequest):
    # Hardcoded credentials as required by assignment [cite: 126]
    if request.email == "hire-me@anshumat.org" and request.password == "HireMe@2025!":
        return {
            "token": "fake-jwt-token-for-demo", 
            "userId": "u123", 
            "message": "Login successful"
        }
    return {"message": "Invalid credentials"}, 401

@app.get("/")
def read_root():
    return {"message": "Coupon System is running!"}

@app.post("/coupons")
def create_coupon(coupon: Coupon):
    coupons_db.append(coupon)
    return {"message": "Coupon created", "code": coupon.code}

@app.get("/coupons")
def list_coupons():
    return coupons_db

# This is the Main Assignment API: 4.2 Best Coupon 
@app.post("/applicable-coupons")
def get_best_coupon(request: ApplicableCouponsRequest):
    eligible_coupons = []

    # 1. Filter coupons based on rules [cite: 81-83]
    for coupon in coupons_db:
        if check_eligibility(coupon, request.user, request.cart):
            discount = calculate_discount(coupon, request.cart.get_total())
            eligible_coupons.append((coupon, discount))

    # 2. If no coupons apply, return empty message [cite: 91]
    if not eligible_coupons:
        return {"message": "No applicable coupons found"}

    # 3. Select the "Best" coupon [cite: 87-90]
    # Sort rules:
    # Priority 1: Highest Discount (descending)
    # Priority 2: Earliest End Date (ascending)
    eligible_coupons.sort(key=lambda x: (-x[1], x[0].endDate))

    best_coupon, best_discount = eligible_coupons[0]

    return ApplicableCouponResponse(
        couponCode=best_coupon.code,
        discountAmount=best_discount,
        message=f"Best coupon found: {best_coupon.code}"
    )