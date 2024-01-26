import pytest
from turtle import distance
from services.fee_calculations import *

from constants import *

def test_apply_small_order_surcharge_below_threshold():
    """
    Test small order surcharge with a cart value below the base cart value.
    """
    cart_value_below_threshold = BASE_CART_VALUE_CENTS - 100
    expected_surcharge = BASE_CART_VALUE_CENTS - cart_value_below_threshold
    assert apply_small_order_surcharge(cart_value_below_threshold) == expected_surcharge

def test_apply_small_order_surcharge_above_threshold():
    """
    Test small order surcharge with a cart value above the base cart value.
    """
    assert apply_small_order_surcharge(BASE_CART_VALUE_CENTS) == 0  # Exactly at threshold
    assert apply_small_order_surcharge(BASE_CART_VALUE_CENTS + 500) == 0    # Above threshold

def test_calculate_additional_distance_fee_within_base_distance():
    """
    Test additional distance fee within base distance.
    """
    assert calculate_additional_distance_fee(BASE_DISTANCE_METERS-1) == 0 # Just below base distance

@pytest.mark.parametrize("additional_distance,expected_fee", [
    (0, 0),     # Test case for no additional distance
    (ADDITIONAL_DISTANCE_INTERVAL_METERS - 1, ADDITIONAL_DISTANCE_FEE_CENTS),   # Right below additional threshold
    (ADDITIONAL_DISTANCE_INTERVAL_METERS, ADDITIONAL_DISTANCE_FEE_CENTS),   # Exactly at additional dist threshold
    (ADDITIONAL_DISTANCE_INTERVAL_METERS + 1, 2 * ADDITIONAL_DISTANCE_FEE_CENTS), # Just above additional dist threshold
    (2 * ADDITIONAL_DISTANCE_INTERVAL_METERS, 2 * ADDITIONAL_DISTANCE_FEE_CENTS), # 2x additional dist threshold
    (3 * ADDITIONAL_DISTANCE_INTERVAL_METERS, 3 * ADDITIONAL_DISTANCE_FEE_CENTS) # 3x additional dist threshold
])
def test_additional_distance_fee(additional_distance, expected_fee):
    """Test additional distance fee for different distances."""
    actual_fee = calculate_additional_distance_fee(BASE_DISTANCE_METERS + additional_distance)
    assert actual_fee == expected_fee
