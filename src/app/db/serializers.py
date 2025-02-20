from dataclasses import asdict
from typing import Any

from app.models import (
    DescriptionLine,
    FilterParams,
    Params,
    Product,
    ProductRequest,
    Query,
    SortParams,
)


def request_to_dict(request: ProductRequest) -> dict[str, Any]:
    data = asdict(request)  # noqa
    filter_params = data["params"].pop("filter_params")
    sort_params = data["params"].pop("sort_params")

    return {
        "query": data["query"],
        "params": {**data["params"], **filter_params, **sort_params},
    }


def dict_to_request(request_dict: dict[str, Any]) -> ProductRequest:
    d = request_dict.copy()

    def split_dict(original: dict, *key_sets) -> tuple[dict, ...]:
        return tuple({k: original[k] for k in key_set if k in original} for key_set in key_sets)

    common_params, sort_params, filter_params = split_dict(
        d["params"],
        Params.__annotations__.keys(),
        SortParams.__annotations__.keys(),
        FilterParams.__annotations__.keys(),
    )

    return ProductRequest(
        query=Query(**d["query"]),
        params=Params(
            filter_params=FilterParams(**filter_params),
            sort_params=SortParams(**sort_params),
            **common_params,
        ),
    )


def dict_to_product(product_dict: dict[str, Any]) -> Product:
    d = product_dict.copy()
    for key in ("price", "price_status", "status"):
        d.pop(key)

    price_statuses_zip = zip(d.pop("description_prices"), d.pop("parsed_statuses"))
    d |= {"description_info": [DescriptionLine(price=price, status=status) for price, status in price_statuses_zip]}

    return Product(**d)


def product_to_dict(product: Product) -> dict[str, Any]:
    data = asdict(product)  # noqa
    data |= {
        "price": product.price,
        "price_status": product.price_status,
        "status": product.status,
        "description_prices": [line.price for line in product.description_info],
        "parsed_statuses": [line.status for line in product.description_info],
    }
    for key in ("price", "price_status", "status"):
        data.pop(key)
    return data
