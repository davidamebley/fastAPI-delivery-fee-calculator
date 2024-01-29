import pytest
from datetime import datetime, timezone, timedelta
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

@pytest.mark.parametrize("number_of_items, expected_fee", [
    (ITEMS_THRESHOLD_FOR_EXTRA_FEE - 1, 0), # Below threshold
    (ITEMS_THRESHOLD_FOR_EXTRA_FEE, ADDITIONAL_ITEM_COUNT_FEE_CENTS), # At threshold
    (ITEMS_THRESHOLD_FOR_EXTRA_FEE + 1, 2 * ADDITIONAL_ITEM_COUNT_FEE_CENTS), # Just above threshold
    (BULK_THRESHOLD, (BULK_THRESHOLD - (ITEMS_THRESHOLD_FOR_EXTRA_FEE - 1)) * ADDITIONAL_ITEM_COUNT_FEE_CENTS), # At the bulk threshold. No bulk fee expected
    (BULK_THRESHOLD + 1, (BULK_THRESHOLD + 1 - (ITEMS_THRESHOLD_FOR_EXTRA_FEE - 1)) * ADDITIONAL_ITEM_COUNT_FEE_CENTS + BULK_FEE_CENTS),  # Above the bulk threshold
])
def test_item_count_surcharge(number_of_items, expected_fee):
    """Test item count surcharge for various numbers of items."""""
    assert calculate_item_count_surcharge(number_of_items) == expected_fee


def create_test_time(weekday, hour):
    """Helper function to create a test time object."""
    # January 1, 2024, is a Monday (weekday 0)
    base_date = datetime(2024, 1, 1, tzinfo=timezone.utc)
    days_to_add = weekday - base_date.weekday()
    return base_date + timedelta(days=days_to_add, hours=hour)

# Calculate an initial fee below the max fee cap.
rush_hour_fee = int(MAX_FEE_CENTS / RUSH_HOUR_MULTIPLIER) -1

@pytest.mark.parametrize("weekday, hour, initial_fee, expected_fee", [
    (RUSH_HOUR_DAY, RUSH_HOUR_START - 1, MAX_FEE_CENTS, MAX_FEE_CENTS), # Just before rush hour
    (RUSH_HOUR_DAY, RUSH_HOUR_START, rush_hour_fee, int(rush_hour_fee * RUSH_HOUR_MULTIPLIER)), # At rush hour
    (RUSH_HOUR_DAY, RUSH_HOUR_START + 1, rush_hour_fee, int(rush_hour_fee * RUSH_HOUR_MULTIPLIER)), # During rush hour
    (RUSH_HOUR_DAY, RUSH_HOUR_END, rush_hour_fee, int(rush_hour_fee * RUSH_HOUR_MULTIPLIER)), # End of rush hour
    (RUSH_HOUR_DAY, RUSH_HOUR_END + 1, MAX_FEE_CENTS, MAX_FEE_CENTS), # Just after rush hour
    (RUSH_HOUR_DAY - 1, RUSH_HOUR_START + 1, MAX_FEE_CENTS, MAX_FEE_CENTS), # Different day
])
def test_apply_rush_hour_multiplier(weekday, hour, initial_fee, expected_fee):
    """Test rush hour multiplier at various times."""
    order_time = create_test_time(weekday, hour)
    assert apply_rush_hour_multiplier(initial_fee, order_time) == expected_fee