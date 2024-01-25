from services.fee_calculations import *

from constants import *

def test_apply_small_order_surcharge_below_threshold():
    """
    Test apply_small_order_surcharge() with a cart value below the base cart value.
    """
    cart_value = 1000
    expected_fee = 0
    fee = apply_small_order_surcharge(cart_value)
    assert fee == expected_fee