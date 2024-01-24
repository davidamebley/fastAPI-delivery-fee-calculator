from datetime import datetime
from pydantic import BaseModel

# Model for incoming delivery fee calculation request.
class DeliveryFeeRequest(BaseModel):
    cart_value: int
    delivery_distance: int
    number_of_items: int
    time: datetime

# Model for outgoing delivery fee calculation response.
class DeliveryFeeResponse(BaseModel):
    delivery_fee: int