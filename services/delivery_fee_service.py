from .fee_calculations import *
from constants import BASE_DELIVERY_FEE_CENTS, FREE_DELIVERY_CART_VALUE_CENTS, MAX_FEE_CENTS
from models.delivery_fee_models import DeliveryFeeRequest


# Main function for fee calculation.
def calculate_delivery_fee(request: DeliveryFeeRequest) -> int:
    """
    Calculates the delivery fee for a given request.

    The fee is composed of:
    - A small order surcharge if the cart value is below a base amount.
    - A base delivery fee.
    - An additional distance fee for distances exceeding the base delivery distance.
    - An item count surcharge for orders with items above a certain threshold.
    - A rush hour multiplier during specified times.
    - Checks for free delivery when the cart value exceeds a certain threshold.
    - Ensures the total fee does not exceed the maximum allowed fee.
    """
    fee = 0

    # Apply small order surcharge
    fee += apply_small_order_surcharge(request.cart_value)

    # Add base delivery fee
    fee += BASE_DELIVERY_FEE_CENTS

    # Add additional distance fee
    fee += calculate_additional_distance_fee(request.delivery_distance)

    # Add item count surcharge
    fee += calculate_item_count_surcharge(request.number_of_items)

    # Check for free delivery
    if request.cart_value >= FREE_DELIVERY_CART_VALUE_CENTS:
        return 0
    
    # Ensure Maximum fee cap
    fee = min(fee, MAX_FEE_CENTS)

    # Apply Rush hour multiplier
    fee = apply_rush_hour_multiplier(fee, request.time)

    # Calculated fee
    return fee