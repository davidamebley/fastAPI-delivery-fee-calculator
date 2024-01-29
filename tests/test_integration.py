from fastapi.testclient import TestClient

from constants import *
from main import app

client = TestClient(app)

def test_small_order_surcharge():
    """
    Test case for orders with cart value less than base cart value.
    """
    # Setting up the test data
    cart_value = BASE_CART_VALUE_CENTS - 1  # Just below the base cart value
    surcharge = BASE_CART_VALUE_CENTS - cart_value

    response = client.post("/calculate-delivery-fee", json={
        "cart_value": cart_value,
        "delivery_distance": BASE_DISTANCE_METERS,
        "number_of_items": 1,
        "time": "2024-01-15T10:00:00Z"
    })
    # The expected fee is the base delivery fee plus the surcharge
    expected_fee = BASE_DELIVERY_FEE_CENTS + surcharge
    assert response.status_code == 200
    assert response.json() == {"delivery_fee": expected_fee}