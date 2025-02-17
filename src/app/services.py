from rich import print

from app.db import save_to_db
from app.filters import filter_products
from app.models import Product, ProductRequest
from app.parser import is_product, parse_product
from app.presenter import present
from app.scraper import get_card_elements_from_avito_search
from app.sorters import sort_products


def search_on_avito(request: ProductRequest) -> list[Product]:
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
    print("PARSED", len(products), "PRODUCTS", flush=True)

    products = filter_products(products, filter_params=request.params.filter_params)
    products = sort_products(products, sort_params=request.params.sort_params)

    if request.params.save_to_db:
        save_to_db(products)

    # for i, product in enumerate(products):
    #     print(i, repr(product.description), flush=True)
    present(products, mode=request.params.template)

    return products
