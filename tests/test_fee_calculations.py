import pytest
from turtle import distance
from services.fee_calculations import *

from constants import *

def test_apply_small_order_surcharge_below_threshold():
    """
    Test asmall order surcharge with a cart value below the base cart value.
    """
    assert apply_small_order_surcharge(500) == BASE_CART_VALUE_CENTS - 500

def test_apply_small_order_surcharge_above_threshold():
    """
    Test small order surcharge with a cart value above the base cart value.
    """
    assert apply_small_order_surcharge(1000) == 0
    assert apply_small_order_surcharge(1500) == 0

def test_calculate_additional_distance_fee_within_base_distance():
    """
    Test additional distance fee within base distance.
    """
    assert calculate_additional_distance_fee(BASE_DISTANCE_METERS-1) == 0

def test_calculate_additional_distance_fee_above_base_distance():
    """
    Test additional distance fee above base distance.
    """
    # Additional distance which should incur a fee
    additional_distance = 501
    additional_fee = ((additional_distance + ADDITIONAL_DISTANCE_ROUNDING) // ADDITIONAL_DISTANCE_INTERVAL_METERS) * ADDITIONAL_DISTANCE_FEE_CENTS
    assert calculate_additional_distance_fee(BASE_DISTANCE_METERS+additional_distance) == additional_fee