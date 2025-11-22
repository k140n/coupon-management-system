# logic.py
from datetime import datetime
from models import Coupon, UserContext, Cart

def check_eligibility(coupon: Coupon, user: UserContext, cart: Cart) -> bool:
    # 1. Date Check [cite: 82]
    # We use "replace(tzinfo=None)" to ensure we compare naive dates correctly
    now = datetime.now().replace(tzinfo=None)
    start = coupon.startDate.replace(tzinfo=None)
    end = coupon.endDate.replace(tzinfo=None)
    
    if not (start <= now <= end):
        return False

    # If the coupon has specific eligibility rules, check them
    if coupon.eligibility:
        rules = coupon.eligibility
        cart_total = cart.get_total()

        # --- User-based checks ---
        # Check User Tier [cite: 22]
        if rules.allowedUserTiers and user.userTier:
            if user.userTier not in rules.allowedUserTiers:
                return False
        
        # Check Min Lifetime Spend [cite: 24]
        if rules.minLifetimeSpend is not None and user.lifetimeSpend < rules.minLifetimeSpend:
            return False
            
        # Check Min Orders [cite: 25]
        if rules.minOrdersPlaced is not None and user.ordersPlaced < rules.minOrdersPlaced:
            return False
            
        # Check Country [cite: 27]
        if rules.allowedCountries and user.country:
            if user.country not in rules.allowedCountries:
                return False

        # --- Cart-based checks ---
        # Check Min Cart Value [cite: 30]
        if rules.minCartValue is not None and cart_total < rules.minCartValue:
            return False
        
        # Check Min Items Count [cite: 34]
        total_items = sum(item.quantity for item in cart.items)
        if rules.minItemsCount is not None and total_items < rules.minItemsCount:
            return False

        # Check Categories (Complex!)
        cart_categories = {item.category for item in cart.items}
        
        # Applicable Categories: Valid if at least one item matches [cite: 31]
        if rules.applicableCategories:
            # We use set intersection to check if they share any categories
            if not set(rules.applicableCategories).intersection(cart_categories):
                return False
        
        # Excluded Categories: Valid only if NONE match [cite: 33]
        if rules.excludedCategories:
            if set(rules.excludedCategories).intersection(cart_categories):
                return False

    return True

def calculate_discount(coupon: Coupon, cart_total: float) -> float:
    # [cite: 84-86]
    if coupon.discountType == "FLAT":
        return coupon.discountValue
    
    elif coupon.discountType == "PERCENT":
        discount = (coupon.discountValue / 100) * cart_total
        
        # Apply the cap if it exists [cite: 86]
        if coupon.maxDiscountAmount:
            discount = min(discount, coupon.maxDiscountAmount)
        
        return discount
    
    return 0.0