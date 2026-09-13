from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from database import get_product
from database import get_products
from database import get_price_history
from datetime import datetime
from analytics import calculate_price_change

app = FastAPI()


class Product(BaseModel):
    id: int
    external_id: str
    name: str


class PriceHistory(BaseModel):
    product_id: int
    price: float
    recorded_at: datetime


@app.get("/products", response_model=list[Product])
def read_products():
    return get_products()


@app.get("/products/{product_id}/prices", response_model=list[PriceHistory])
def read_prices(product_id: int):
    product = get_product(product_id)

    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    return get_price_history(product_id)


@app.get("/products/{product_id}/change")
def read_price_change(product_id: int):
    product = get_product(product_id)

    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    history = get_price_history(product_id)
    calculation = calculate_price_change(history)

    if not calculation:
        return {"message": "Not enough price history"}
    return calculation
