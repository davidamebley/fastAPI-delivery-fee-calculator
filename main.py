from fastapi import FastAPI
from routes.delivery_fee import router as delivery_fee_router


app = FastAPI()
app.include_router(delivery_fee_router)