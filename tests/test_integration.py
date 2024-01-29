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
    