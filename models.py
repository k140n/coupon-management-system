# models.py
from pydantic import BaseModel
from typing import List, Optional, Literal
from datetime import datetime

# 1. Define the Eligibility Rules [cite: 19-34]
class Eligibility(BaseModel):
    allowedUserTiers: Optional[List[str]] = None  # e.g. ["GOLD", "PLATINUM"]
    minLifetimeSpend: Optional[float] = None
    minOrdersPlaced: Optional[int] = None
    firstOrderOnly: Optional[bool] = False
    allowedCountries: Optional[List[str]] = None
    minCartValue: Optional[float] = None
    applicableCategories: Optional[List[str]] = None
    excludedCategories: Optional[List[str]] = None
    minItemsCount: Optional[int] = None

# 2. Define the Coupon Structure [cite: 14-17]
class Coupon(BaseModel):
    code: str
    description: Optional[str] = None
    discountType: Literal["FLAT", "PERCENT"]  # Must be one of these two
    discountValue: float
    maxDiscountAmount: Optional[float] = None
    startDate: datetime
    endDate: datetime
    usageLimitPerUser: Optional[int] = None
    eligibility: Optional[Eligibility] = None  # Nesting the rules inside

# 3. Define the Inputs (User & Cart) 
class CartItem(BaseModel):
    productId: str
    category: str
    unitPrice: float
    quantity: int

class Cart(BaseModel):
    items: List[CartItem]
    
    # Helper to get total price easily
    def get_total(self):
        return sum(item.unitPrice * item.quantity for item in self.items)

class UserContext(BaseModel):
    userId: str
    userTier: Optional[str] = None
    country: Optional[str] = None
    lifetimeSpend: Optional[float] = 0
    ordersPlaced: Optional[int] = 0