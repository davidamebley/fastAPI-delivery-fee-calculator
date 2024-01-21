from models.delivery_fee_models import DeliveryFeeRequest


def calculate_delivery_fee(request: DeliveryFeeRequest) -> int:
    """
    Calculates the delivery fee for a given request.
    """
    fee = 0

    # Small Order Surcharge
    if request.cart_value < 1000:   # 10€ (in cents)
        fee += 1000 - request.cart_value

    # Base Delivery Fee
    fee += 200  # 2€ (in cents)

    
    return fee