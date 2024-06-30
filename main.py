from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from redis_om import get_redis_connection, HashModel
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

info = redis.info()
print(info['redis_version'])
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
def all():
    return [format(pk) for pk in Product.all_pks()]

def format(pk: str):
    product = Product.get(pk)

    return {
        'id': product.pk,
        'name': product.name,
        'price': product.price,
        'quantity': product.quantity
    }

@app.post('/products')
def create(product: Product):
    return product.save()


@app.get('/products/{pk}')
def get(pk: str):
    return Product.get(pk)

@app.delete('/products/{pk}')
def delete(pk: str):
    return Product.delete(pk)