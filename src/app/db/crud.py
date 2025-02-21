from datetime import datetime
from typing import Iterable
from uuid import uuid1

from bson.objectid import ObjectId

from app.db import serializers
from app.db.config import db
from app.models import DatetimeRange, Product, ProductRequest, Query


def save_to_db(*, product_request: ProductRequest, products: Iterable[Product], timestamp: datetime = None) -> None:
    """Save product request and products to the database."""
    timestamp = timestamp or datetime.now().replace(second=0, microsecond=0)
    request_id = uuid1().hex

    meta_params = {"timestamp": timestamp, "_id": request_id}
    request_dict = serializers.request_to_dict(product_request) | meta_params
    db["requests"].insert_one(request_dict)

    meta_params = {"timestamp": timestamp, "request_id": request_id}
    product_dicts = [serializers.product_to_dict(p) | meta_params for p in products]
    db["products"].insert_many(product_dicts)


def get_requests_from_db(
    *,
    request_ids: Iterable[str] = None,
    queries: Iterable[Query] = None,
    datetime_ranges: Iterable[DatetimeRange] = None,
) -> tuple[list[ProductRequest], list[str]]:
    """
    Get product requests from the database by one or more params.
    Logical AND -- between query, request_ids, datatime_ranges, OR -- inside each argument.
    Return tuple of requests and their IDs.
    """
    query_dict = {}
    if request_ids:
        query_dict["_id"] = {"$in": [ObjectId(id_) if ObjectId.is_valid(id_) else id_ for id_ in request_ids]}
    if queries:
        query_dict["$and"] = [{f"query.{k}": v for k, v in asdict(query).items()} for query in queries]  # noqa
    if datetime_ranges:
        timestamp_conditions = [
            {"timestamp": {k: v for k, v in [("$gte", start), ("$lte", end)] if v is not None}}
            for start, end in datetime_ranges
            if start or end
        ]
        if timestamp_conditions:
            query_dict["$or"] = query_dict.get("$or", []) + timestamp_conditions

    requests = db["requests"].find(query_dict)

    return [serializers.dict_to_request(r) for r in requests], [str(r["_id"]) for r in requests]


def get_products_from_db(request_id: str) -> list[Product]:
    """Get products from the database."""
    products = db["products"].find({"request_id": request_id})

    return [serializers.dict_to_product(p) for p in products]
