from datetime import datetime
from pydantic import BaseModel


class DeliveryFeeRequest(BaseModel):
    cart_value: int
    delivery_distance: int
    number_of_items: int
    time: datetime

class DeliveryFeeResponse(BaseModel):
    delivery_fee: int