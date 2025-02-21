from datetime import datetime
from typing import Iterable

from rich import print

from app.filters import filter_products
from app.models import DatetimeRange, Params, Product, ProductRequest, Query
from app.parser import is_product, parse_product
from app.presenter import present
from app.scraper.getters import get_card_elements_from_avito_search
from app.sorters import sort_products


def search_on_avito(request: ProductRequest, timestamp: datetime | None = None) -> list[Product]:
    """Search for products on Avito and return them."""
    query, params = request.query, request.params

    card_elements = get_card_elements_from_avito_search(
        search_query=query.search_query,
        max_pages=params.max_pages,
    )
    products = [
        parse_product(
            elem,
            title_query=query.title_query or query.search_query,
            description_query=query.description_query or query.search_query,
            min_price=params.filter_params.min_price,
            max_price=params.filter_params.max_price,
        )
        for elem in card_elements
        if is_product(elem)
    ]

    products = filter_products(products, filter_params=request.params.filter_params)
    products = sort_products(products, sort_params=request.params.sort_params)

    present(products, mode=request.params.template)

    if request.params.save_to_db:
        timestamp = timestamp or datetime.now().replace(second=0, microsecond=0)
        try:
            from app.db.crud import save_to_db  # noqa

            save_to_db(product_request=request, products=products, timestamp=timestamp)
            print("Saved to db!")
        except ImportError:
            print("Database connection not available. Skipping saving to db.")

    return products


def search_in_db(
    *,
    queries: Iterable[Query] = None,
    request_ids: Iterable[str] | None = None,
    datatime_ranges: Iterable[DatetimeRange] | None = None,
    params: Params,
) -> dict[ProductRequest, list[Product]]:
    """Search for product_requests and corresponding products in the database."""
    try:
        from app.db.crud import get_products_from_db, get_requests_from_db
    except ImportError:
        raise ImportError("Database connection not available.")

    request_to_products_mapping: dict[ProductRequest, list[Product]] = {}

    requests, request_ids_ = get_requests_from_db(
        queries=queries,
        request_ids=request_ids,
        datetime_ranges=datatime_ranges,
    )
    for request, request_id in zip(requests, request_ids_):
        products = get_products_from_db(request_id=request_id)
        request_to_products_mapping[request] = products

        products = filter_products(products, filter_params=params.filter_params)
        products = sort_products(products, sort_params=params.sort_params)

        present(products, mode=params.template)

    return request_to_products_mapping
