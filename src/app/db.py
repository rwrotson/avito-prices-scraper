from datetime import datetime

from pymongo import MongoClient

from app.consts import MONGO_URL, MONGO_DB
from app.models import Product, ProductRequest

client = MongoClient(MONGO_URL)
db = client[MONGO_DB]

requests_collection = db["requests"]
products_collection = db["products"]


def save_to_db(product_request: ProductRequest, products: list[Product], *, timestamp: datetime | None = None) -> None:
    pass
