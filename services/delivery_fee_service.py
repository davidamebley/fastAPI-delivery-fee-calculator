import re
from models.delivery_fee_models import DeliveryFeeRequest


def calculate_delivery_fee(request: DeliveryFeeRequest) -> int:
    """
    Calculates the delivery fee for a given request.
    """
    fee = 0

    # Small Order Surcharge
    if request.cart_value < 1000:   # 10€ (in cents)
        fee += 1000 - request.cart_value

    # Base Delivery Fee
    fee += 200  # 2€ (in cents)

    # Additional Distance Fee
    if request.delivery_distance > 1000:
        additional_distance = request.delivery_distance - 1000
        fee += ((additional_distance + 499) // 500) * 100
    
    # Item Count Surcharge
    if request.number_of_items >= 5:
        extra_items = request.number_of_items - 4
        fee += extra_items * 50 # 50 cents per extra item
        if request.number_of_items > 12:
            fee += 120 # Bulk fee of 1.20€

    # Free Delivery for Cart Values 200€ or more
    if request.cart_value >= 20000: # 200€ (in cents)
        return 0

    # Ensure Maximum Fee Cap
    fee = min(fee, 1500)    # 15€ (in cents)

    # Rush Hour Fee
    order_time = request.time
    if order_time.weekday() == 4 and 15 <= order_time.hour < 19:    # Fridays, 3pm to 7pm
        fee = int(min(fee * 1.2, 1500))    # total fee times 1.2, but limit to 15€ max
    
    return fee