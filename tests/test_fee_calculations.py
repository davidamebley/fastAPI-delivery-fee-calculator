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

@pytest.mark.parametrize("additional_distance,expected_fee", [
    (0, 0),     # Test case for no additional distance
    (500, ADDITIONAL_DISTANCE_FEE_CENTS),
    (501, 2 * ADDITIONAL_DISTANCE_FEE_CENTS), 
    (1000, 2 * ADDITIONAL_DISTANCE_FEE_CENTS),
    (1500, 3 * ADDITIONAL_DISTANCE_FEE_CENTS) 
])
def test_additional_distance_fee(additional_distance, expected_fee):
    """Test additional distance fee for different distances."""
    actual_fee = calculate_additional_distance_fee(BASE_DISTANCE_METERS + additional_distance)
    assert actual_fee == expected_fee
