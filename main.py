from fastapi import FastAPI
from routes.delivery_fee import router as delivery_fee_router

# Create a FastAPI app instance and include the delivery fee router.
app = FastAPI()

# Include the delivery fee router to handle the delivery fee calculation endpoint.
app.include_router(delivery_fee_router)