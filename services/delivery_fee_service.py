from models.delivery_fee_models import DeliveryFeeRequest

# Constants
BASE_CART_VALUE_CENTS = 1000 # Minimum cart value in cents to avoid small order surcharge.
BASE_DISTANCE_METERS = 1000 # Base distance in meters for initial delivery fee calculation.
ADDITIONAL_DISTANCE_INTERVAL_METERS = 500   #   Interval in meters for calculating additional distance fee.
ADDITIONAL_DISTANCE_ROUNDING = ADDITIONAL_DISTANCE_INTERVAL_METERS - 1  # Value used to ensure rounding up for additional distance fee calculation.
BASE_DELIVERY_FEE_CENTS = 200   # Base delivery fee in cents.
ADDITIONAL_DISTANCE_FEE_CENTS = 100 # Additional fee in cents for each extra distance interval.
ITEMS_THRESHOLD_FOR_EXTRA_FEE = 5   # Number of items threshold from which extra fee per item is applied.
BULK_THRESHOLD = 12 # Number of items threshold beyond which bulk fee is applied.
ADDITIONAL_ITEM_COUNT_FEE_CENTS = 50    # Additional fee in cents for each item beyond the ITEMS_THRESHOLD_FOR_EXTRA_FEE.
BULK_FEE_CENTS = 120    # Additional bulk fee in cents when itemcount exce BULK_THRESHOLD.
MAX_FEE_CENTS = 1500    # Maximum delivery fee cap in cents.
RUSH_HOUR_MULTIPLIER = 1.2  # Multiplier for delivery fee during rush hours.
RUSH_HOUR_DAY = 4   # (0=Monday, 1=Tuesday, ..., 6=Sunday) for rush hour calculation.
RUSH_HOUR_START = 15    # Start hour (24-hour format) for rush hour fee calculation.
RUSH_HOUR_END = 19  # End hour (24-hour format) for rush hour fee calculation.
FREE_DELIVERY_CART_VALUE_CENTS = 20000  # Cart value in cents from which delivery is free.

# Helper functions for fee calculation.
def apply_small_order_surcharge(cart_value: int) -> int:
    """
    Applies a small order surcharge to a given cart value.
    """
    if cart_value < BASE_CART_VALUE_CENTS:
        return BASE_CART_VALUE_CENTS - cart_value
    return 0

def additional_distance_fee(distance: int) -> int:
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
    if request.number_of_items > 4:
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
    if order_time.weekday() == 4 and 15 <= order_time.hour <= 19:    # Rush hour period
        fee = int(min(fee * 1.2, 1500))    # Total fee x multiplier, but limit to max fee
    
    return fee