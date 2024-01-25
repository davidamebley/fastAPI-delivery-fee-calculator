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