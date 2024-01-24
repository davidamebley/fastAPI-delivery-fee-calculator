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