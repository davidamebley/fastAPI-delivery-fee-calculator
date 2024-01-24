from datetime import datetime
from models.delivery_fee_models import DeliveryFeeRequest

# Helper functions for fee calculation.
def apply_small_order_surcharge(cart_value: int) -> int:
    """
    Applies a small order surcharge to a given cart value.
    """
    if cart_value < BASE_CART_VALUE_CENTS:
        return BASE_CART_VALUE_CENTS - cart_value
    return 0

def calculate_additional_distance_fee(distance: int) -> int:
    """
    Calculates the additional distance fee for a given distance.
    """
    if distance > BASE_DISTANCE_METERS:
        additional_distance = distance - BASE_DISTANCE_METERS
        return ((additional_distance + ADDITIONAL_DISTANCE_ROUNDING) // ADDITIONAL_DISTANCE_INTERVAL_METERS) * ADDITIONAL_DISTANCE_FEE_CENTS
    return 0

def calculate_item_count_surcharge(number_of_items: int) -> int:
    """
    Calculates the item count surcharge for a given number of items.
    """
    if number_of_items >= ITEMS_THRESHOLD_FOR_EXTRA_FEE:
        extra_items = number_of_items - ITEMS_THRESHOLD_FOR_EXTRA_FEE
        item_surchage = extra_items * ADDITIONAL_ITEM_COUNT_FEE_CENTS
        if number_of_items > BULK_THRESHOLD:
            item_surchage += BULK_FEE_CENTS # Apply bulk fee
            return item_surchage
    return 0

def apply_rush_hour_multiplier(fee: int, order_time: datetime) -> int:
    """
    Applies the rush hour fee multiplier to cart value
    """
    if order_time.weekday() == RUSH_HOUR_DAY and RUSH_HOUR_START <= order_time.hour <= RUSH_HOUR_END:
        return int(min(fee * RUSH_HOUR_MULTIPLIER, MAX_FEE_CENTS))
    return fee

# Main function for fee calculation.
def calculate_delivery_fee(request: DeliveryFeeRequest) -> int:
    """
    Calculates the delivery fee for a given request.
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