from app.models import FilterParams, Product, ProductStatus


def filter_products[T: Product](products: list[T], *, filter_params: FilterParams) -> list[T]:
    fp = filter_params

    return [
        product
        for product in products
        if (
            (fp.min_price is None or product.unified_price >= fp.min_price)  # noqa
            and (fp.max_price is None or product.unified_price <= fp.max_price)  # noqa
            and (fp.include_unknown or product.status != ProductStatus.NOT_FOUND)
            and (fp.include_ambiguous or product.status != ProductStatus.AMBIGUOUS)
            and (fp.include_multiple or product.status != ProductStatus.MULTIPLE_FOUND)
            and (fp.include_sold or product.status != ProductStatus.SOLD)
            and (fp.include_booked or product.status != ProductStatus.BOOKED)
        )
    ]
