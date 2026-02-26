from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, EmailStr
from typing import Optional
import asyncio
import random
from datetime import datetime

app = FastAPI(title="Performance Testing API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Models
class User(BaseModel):
    name: str
    email: EmailStr

class CartItem(BaseModel):
    productId: int
    quantity: int = 1

class Order(BaseModel):
    userId: Optional[int] = None
    productId: Optional[int] = None
    quantity: int = 1
    cartId: Optional[int] = None
    paymentMethod: str

# Database
products = [
    {
        'id': i + 1,
        'name': f'Product {i + 1}',
        'price': random.randint(10, 1000),
        'category': random.choice(['Electronics', 'Clothing', 'Books', 'Home']),
        'inStock': random.random() > 0.1
    }
    for i in range(100)
]

users = [{'id': i + 1, 'name': f'User {i + 1}', 'email': f'user{i + 1}@example.com'}
         for i in range(1000)]

orders = []
cart_counter = 1
order_counter = 1

async def simulate_delay(base: float = 0.01, variance: float = 0.05):
    await asyncio.sleep(base + random.random() * variance)

# Endpoints
@app.get("/health")
async def health_check():
    return {"status": "ok", "timestamp": datetime.now().isoformat()}

@app.get("/api/products")
async def get_products(
    search: Optional[str] = None,
    sort: Optional[str] = None,
    page: int = Query(1, ge=1),
    limit: int = Query(20, ge=1, le=100)
):
    await simulate_delay(0.02, 0.08)
    result = products.copy()
    
    if search:
        search_lower = search.lower()
        result = [p for p in result if search_lower in p['name'].lower() 
                  or search_lower in p['category'].lower()]
    
    if sort == 'price':
        result.sort(key=lambda x: x['price'])
    elif sort == 'name':
        result.sort(key=lambda x: x['name'])
    
    start = (page - 1) * limit
    end = start + limit
    
    return {
        'data': result[start:end],
        'total': len(result),
        'page': page,
        'totalPages': (len(result) + limit - 1) // limit
    }

@app.get("/api/products/flash-sale")
async def get_flash_sale():
    await simulate_delay(0.03, 0.1)
    return [
        {**p, 'originalPrice': p['price'], 'price': int(p['price'] * 0.7), 'discount': 30}
        for p in products[:5]
    ]

@app.get("/api/products/{product_id}")
async def get_product(product_id: int):
    await simulate_delay(0.015, 0.06)
    product = next((p for p in products if p['id'] == product_id), None)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product

@app.get("/api/products/{product_id}/reviews")
async def get_reviews(product_id: int):
    await simulate_delay(0.05, 0.15)
    return [
        {
            'id': i + 1,
            'rating': random.randint(1, 5),
            'comment': f'Review {i + 1} for product {product_id}',
            'author': f'User {random.randint(1, 100)}'
        }
        for i in range(5)
    ]

@app.get("/api/users")
async def get_users(page: int = Query(1, ge=1), limit: int = Query(50, ge=1, le=100)):
    await simulate_delay(0.01, 0.04)
    start = (page - 1) * limit
    end = start + limit
    return {'data': users[start:end], 'total': len(users), 'page': page}

@app.get("/api/users/{user_id}")
async def get_user(user_id: int):
    await simulate_delay(0.015, 0.05)
    user = next((u for u in users if u['id'] == user_id), None)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@app.post("/api/users", status_code=201)
async def create_user(user: User):
    await simulate_delay(0.03, 0.1)
    new_user = {'id': len(users) + 1, 'name': user.name, 'email': user.email}
    users.append(new_user)
    return new_user

@app.post("/api/cart", status_code=201)
async def create_cart(cart_item: CartItem):
    global cart_counter
    await simulate_delay(0.02, 0.08)
    product = next((p for p in products if p['id'] == cart_item.productId), None)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    if not product['inStock']:
        raise HTTPException(status_code=409, detail="Product out of stock")
    
    cart = {
        'cartId': cart_counter,
        'items': [{'product': product, 'quantity': cart_item.quantity}],
        'total': product['price'] * cart_item.quantity
    }
    cart_counter += 1
    return cart

@app.post("/api/cart/add")
async def add_to_cart(cart_item: CartItem):
    await simulate_delay(0.025, 0.09)
    return {
        'success': True,
        'message': 'Item added to cart',
        'productId': cart_item.productId,
        'quantity': cart_item.quantity
    }

@app.get("/api/cart/{cart_id}")
async def get_cart(cart_id: int):
    await simulate_delay(0.015, 0.06)
    return {'cartId': cart_id, 'items': [], 'total': 0}

@app.post("/api/orders", status_code=201)
async def create_order(order: Order):
    global order_counter
    await simulate_delay(0.1, 0.3)
    
    if random.random() < 0.05:
        raise HTTPException(status_code=402, detail="Payment processing failed")
    
    order_data = {
        'orderId': order_counter,
        'userId': order.userId,
        'productId': order.productId,
        'quantity': order.quantity,
        'cartId': order.cartId,
        'paymentMethod': order.paymentMethod,
        'status': 'confirmed',
        'createdAt': datetime.now().isoformat()
    }
    orders.append(order_data)
    order_counter += 1
    return order_data

@app.get("/api/orders/{order_id}")
async def get_order(order_id: int):
    await simulate_delay(0.02, 0.07)
    order = next((o for o in orders if o['orderId'] == order_id), None)
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    return order

@app.post("/api/logs", status_code=201)
async def create_log(log_entry: dict):
    await simulate_delay(0.005, 0.02)
    return {'logged': True}

@app.get("/api/heavy")
async def heavy_computation():
    await simulate_delay(0.2, 0.5)
    result = sum(i ** 0.5 for i in range(1000000))
    return {'result': result, 'computed': True}

@app.get("/api/slow")
async def slow_endpoint():
    await simulate_delay(2.0, 1.0)
    return {'message': 'This endpoint is intentionally slow'}

@app.get("/api/error")
async def error_endpoint():
    rand = random.random()
    if rand < 0.3:
        raise HTTPException(status_code=500, detail="Internal server error")
    elif rand < 0.5:
        raise HTTPException(status_code=503, detail="Service unavailable")
    return {'message': 'Success'}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=3000)