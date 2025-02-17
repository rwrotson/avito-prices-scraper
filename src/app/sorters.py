from typing import Callable

from app.models import Product, SortBy, SortOrder, SortParams


def _sort_by_page[T: Product](products: list[T], sort_order: SortOrder) -> list[T]:
    return products if (sort_order == SortOrder.ASC) else products[::-1]


def _sort_by_price[T: Product](products: list[T], sort_order: SortOrder) -> list[T]:
    return sorted(
        products,
        key=lambda p: p.unified_price,
        reverse=(sort_order == SortOrder.DESC),
    )


type _SorterFunc = Callable[[list[Product], SortOrder], list[Product]]

_SORT_STRATEGIES_MAPPING: dict[SortBy, _SorterFunc] = {
    SortBy.PAGE: _sort_by_page,
    SortBy.PRICE: _sort_by_price,
}


def sort_products[T: Product](products: list[T], *, sort_params: SortParams) -> list[T]:
    try:
        sort_func = _SORT_STRATEGIES_MAPPING[sort_params.sort_by]
    except KeyError:
        raise ValueError(f"Unknown sorting_option {sort_params.sort_by}")

    return sort_func(products, sort_params.sort_order)
