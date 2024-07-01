from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from redis_om import get_redis_connection, HashModel
from starlette.requests import Request
import json

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=['http://localhost:3000'],
    allow_methods=['*'],
    allow_headers=['*']
)

# Load configuration from a JSON file
with open('config.json', 'r') as f:
    config = json.load(f)


# Set up the Redis connection
redis = get_redis_connection(
    host=config['redis']['host'],
    port=config['redis']['port'],
    password=config['redis']['password'],
    decode_responses=True
)

class Order(HashModel):
    product_id: str
    price: float
    fee: float
    total: float
    quantity: int
    status: str #pending, completed, refunded

    class Meta:
        database = redis

@app.post('/orders')
async def create(request: Request):
    body = await request.json()