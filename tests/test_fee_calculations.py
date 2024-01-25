import dis
from turtle import distance
from services.fee_calculations import *

from constants import *

def test_apply_small_order_surcharge_below_threshold():
    """
    Test apply_small_order_surcharge() with a cart value below the base cart value.
    """
    assert apply_small_order_surcharge(500) == BASE_CART_VALUE_CENTS - 500

def test_apply_small_order_surcharge_above_threshold():
    """
    Test apply_small_order_surcharge() with a cart value above the base cart value.
    """
    assert apply_small_order_surcharge(1000) == 0
    assert apply_small_order_surcharge(1500) == 0

def test_calculate_additional_distance_fee_within_base_distance():
    """
    Test calculate_additional_distance_fee() with a distance within the base distance.
    """
    assert calculate_additional_distance_fee(BASE_DISTANCE_METERS) == 0

def test_calculate_additional_distance_fee_above_base_distance():
    """
    Test calculate_additional_distance_fee() with a distance above the base distance.
    """
    # Additional distance which should incur a fee
    additional_distance = 501
    additional_fee = ((additional_distance + ADDITIONAL_DISTANCE_ROUNDING) // ADDITIONAL_DISTANCE_INTERVAL_METERS) * ADDITIONAL_DISTANCE_FEE_CENTS
    assert calculate_additional_distance_fee(BASE_DISTANCE_METERS+additional_distance) == additional_fee
