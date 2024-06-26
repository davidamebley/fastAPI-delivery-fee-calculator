from fastapi.testclient import TestClient

from constants import *
from main import app

# Define a constant for the API endpoint
DELIVERY_FEE_ENDPOINT = "/calculate-delivery-fee"

client = TestClient(app)

def test_small_order_surcharge():
    """
    Test case for orders with cart value less than base cart value.
    """
    # Setting up the test data
    cart_value = BASE_CART_VALUE_CENTS - 1  # Just below the base cart value
    surcharge = BASE_CART_VALUE_CENTS - cart_value

    response = client.post(DELIVERY_FEE_ENDPOINT, json={
        "cart_value": cart_value,
        "delivery_distance": BASE_DISTANCE_METERS,
        "number_of_items": 1,
        "time": "2024-01-15T10:00:00Z"
    })
    # The expected fee is the base delivery fee plus the surcharge
    expected_fee = BASE_DELIVERY_FEE_CENTS + surcharge
    assert response.status_code == 200
    assert response.json() == {"delivery_fee": expected_fee}

def test_additional_distance_fee():
    """
    Test case for orders just above the base distance
    """
    response = client.post(DELIVERY_FEE_ENDPOINT, json={
        "cart_value": BASE_CART_VALUE_CENTS,
        "delivery_distance": BASE_DISTANCE_METERS + 1,   # Just over base distance
        "number_of_items": 1,
        "time": "2024-01-15T10:00:00Z"
    })
    # One unit of additonal distance fee is added
    expected_fee = BASE_DELIVERY_FEE_CENTS + ADDITIONAL_DISTANCE_FEE_CENTS
    assert response.status_code == 200
    assert response.json() == {"delivery_fee": expected_fee}
    
def test_item_count_at_threshold():
    """
    Test case for orders with items exactly at the item count threshold.
    """
    response = client.post(DELIVERY_FEE_ENDPOINT, json={
        "cart_value": BASE_CART_VALUE_CENTS,
        "delivery_distance": BASE_DISTANCE_METERS,
        "number_of_items": ITEMS_THRESHOLD_FOR_EXTRA_FEE, # Exactly at threshold
        "time": "2024-01-15T10:00:00Z"
    })
    # Additional fee for one item at threshold
    expected_fee = BASE_DELIVERY_FEE_CENTS + ADDITIONAL_ITEM_COUNT_FEE_CENTS
    assert response.status_code == 200
    assert response.json() == {"delivery_fee": expected_fee}

def test_item_count_above_threshold():
    """
    Test case for orders with one item above the item count threshold.
    """
    response = client.post(DELIVERY_FEE_ENDPOINT, json={
        "cart_value": BASE_CART_VALUE_CENTS,
        "delivery_distance": BASE_DISTANCE_METERS,
        "number_of_items": ITEMS_THRESHOLD_FOR_EXTRA_FEE + 1, # One above threshold
        "time": "2024-01-15T10:00:00Z"
    })
    # Additional fee for one extra item above threshold (2 items)
    expected_fee = BASE_DELIVERY_FEE_CENTS + (2 * ADDITIONAL_ITEM_COUNT_FEE_CENTS)
    assert response.status_code == 200
    assert response.json() == {"delivery_fee": expected_fee}

def test_rush_hour_multiplier():
    """
    Test case for orders during rush hour
    """
    response = client.post(DELIVERY_FEE_ENDPOINT, json={
        "cart_value": BASE_CART_VALUE_CENTS,
        "delivery_distance": BASE_DISTANCE_METERS + 1,   # Just over base distance
        "number_of_items": 1,
        "time": "2024-01-19T16:00:00Z"  # Friday, 4 PM, a rush hour
    })
    # Base fee including additional distance fee
    base_fee = BASE_DELIVERY_FEE_CENTS + ADDITIONAL_DISTANCE_FEE_CENTS
    # Fee with rush hour multiplier, capped at maximum fee
    expected_fee = int(min(base_fee * RUSH_HOUR_MULTIPLIER, MAX_FEE_CENTS))
    assert response.status_code == 200
    assert response.json() == {"delivery_fee": expected_fee}

def test_free_delivery():
    """
    Test case for orders with cart value reaching the free delivery threshold
    """
    response = client.post(DELIVERY_FEE_ENDPOINT, json={
        "cart_value": FREE_DELIVERY_CART_VALUE_CENTS, # Free delivery threshold
        "delivery_distance": BASE_DISTANCE_METERS * 2,
        "number_of_items": ITEMS_THRESHOLD_FOR_EXTRA_FEE,
        "time": "2024-01-15T10:00:00Z"
    })
    # No delivery fee for high cart value
    expected_fee = 0
    assert response.status_code == 200
    assert response.json() == {"delivery_fee": expected_fee}

def test_negative_cart_value():
    """
    Test case for orders with negative cart value
    """
    response = client.post(DELIVERY_FEE_ENDPOINT, json={
        "cart_value": -1, # Negative cart value
        "delivery_distance": BASE_DISTANCE_METERS,
        "number_of_items": 1,
        "time": "2024-01-15T10:00:00Z"
    })
    # Negative cart value is not allowed
    assert response.status_code == 400
    assert response.json() == {"detail": "Cart value cannot be negative. Received cart value: {}".format(-1)}

def test_negative_delivery_distance():
    """
    Test case for orders with negative delivery distance
    """
    response = client.post(DELIVERY_FEE_ENDPOINT, json={
        "cart_value": BASE_CART_VALUE_CENTS,
        "delivery_distance": -1, # Negative delivery distance
        "number_of_items": 1,
        "time": "2024-01-15T10:00:00Z"
    })
    # Negative delivery distance is not allowed
    assert response.status_code == 400
    assert response.json() == {"detail": "Delivery distance cannot be negative. Received delivery distance: {}".format(-1)}

def test_zero_number_of_items():
    """
    Test case for orders with zero number of items
    """
    response = client.post(DELIVERY_FEE_ENDPOINT, json={
        "cart_value": BASE_CART_VALUE_CENTS,
        "delivery_distance": BASE_DISTANCE_METERS,
        "number_of_items": 0, # Zero number of items
        "time": "2024-01-15T10:00:00Z"
    })
    # Zero number of items is not allowed
    assert response.status_code == 400
    assert response.json() == {"detail": "Number of items must be greater than zero. Received number of items: {}".format(0)}

def test_non_utc_time():
    """
    Test case for orders with non-UTC time
    """
    response = client.post(DELIVERY_FEE_ENDPOINT, json={
        "cart_value": BASE_CART_VALUE_CENTS,
        "delivery_distance": BASE_DISTANCE_METERS,
        "number_of_items": 1,
        "time": "2024-01-15T10:00:00+01:00" # Non-UTC time
    })
    # Non-UTC time is not allowed
    assert response.status_code == 400
    assert response.json() == {"detail": f"Order time must be in UTC. Received time: 2024-01-15 10:00:00+01:00"}