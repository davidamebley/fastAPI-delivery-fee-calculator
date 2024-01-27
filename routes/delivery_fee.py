from fastapi import APIRouter, HTTPException
from datetime import timezone

from models.delivery_fee_models import DeliveryFeeRequest, DeliveryFeeResponse
from services.delivery_fee_service import calculate_delivery_fee


router = APIRouter()

@router.post("/calculate-delivery-fee", response_model=DeliveryFeeResponse)
async def calculate_delivery_fee_api(request: DeliveryFeeRequest) -> DeliveryFeeResponse:
    # Custom Validations
    if request.cart_value < 0:
        raise HTTPException(
            status_code=400, detail="Cart value cannot be negative."
        )
    if request.delivery_distance < 0:
        raise HTTPException(
            status_code=400, detail="Delivery distance cannot be negative."
        )
    if request.number_of_items <= 0:    # Ensuring there's a least one item
        raise HTTPException(
            status_code=400, detail="Number of items must be greater than zero."
        )
    # Check if time is in UTC
    if request.time.tzinfo != timezone.utc:
        raise HTTPException(
            status_code=400, detail="Order time must be in UTC."
        )

    fee = calculate_delivery_fee(request)
    return DeliveryFeeResponse(delivery_fee=fee)