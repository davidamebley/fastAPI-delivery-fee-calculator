from fastapi import APIRouter

from models.delivery_fee_models import DeliveryFeeRequest, DeliveryFeeResponse
from services.delivery_fee_service import calculate_fee


router = APIRouter()

@router.post("/calculate-delivery-fee", response_model=DeliveryFeeResponse)
async def calculate_delivery_fee(request: DeliveryFeeRequest) -> DeliveryFeeResponse:
    fee = calculate_fee(request)
    return DeliveryFeeResponse(delivery_fee=fee)