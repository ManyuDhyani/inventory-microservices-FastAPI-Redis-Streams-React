from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from redis_om import get_redis_connection, HashModel

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=['http://localhost:3000'],
    allow_methods=['*'],
    allow_headers=['*']
)
# Set up the Redis connection
redis = get_redis_connection(
    host="localhost",  # Change this to your Redis host if different
    port=6379,         # Default Redis port
    password=None,     # Set your Redis password if any
    decode_responses=True
)
# Define a route to test the Redis connection
@app.get("/redis")
async def test_redis():
    redis.set("test_key", "test_value")
    value = redis.get("test_key")
    return {"test_key": value}

class Product(HashModel):
    name: str
    price: float
    quantity: int

    class Meta:
        database = redis

@app.get("/products")
async def all():
    try:
        product_keys = Product.all_pks()
        return product_keys
    except Exception as e:
        return {"error": str(e)}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
