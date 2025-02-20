from app.cli import defaults, opts
from app.models import FilterParams, Params, Query, SortParams

_NULL_SYMBOLS = {"_", "none", "null"}


def parse_params(
    *,
    max_pages: opts.MaxPages = defaults.MAX_PAGES,
    min_price: opts.MinPrice = defaults.MIN_PRICE,
    max_price: opts.MaxPrice = defaults.MAX_PRICE,
    include_unknown: opts.IncludeUnknown = defaults.INCLUDE_UNKNOWN,
    include_ambiguous: opts.IncludeAmbiguous = defaults.INCLUDE_AMBIGUOUS,
    include_multiple: opts.IncludeMultiple = defaults.INCLUDE_MULTIPLE,
    include_booked: opts.IncludeBooked = defaults.INCLUDE_BOOKED,
    include_sold: opts.IncludeSold = defaults.INCLUDE_BOOKED,
    sort_by: opts.SortBy = defaults.SORT_BY,
    sort_order: opts.SortOrder = defaults.SORT_ORDER,
    template: opts.Template = defaults.TEMPLATE,
    save_to_db: opts.SaveToDb = defaults.SAVE_TO_DB,
) -> Params:
    return Params(
        max_pages=max_pages or None,
        filter_params=FilterParams(
            min_price=min_price or None,
            max_price=max_price or None,
            include_unknown=include_unknown,
            include_ambiguous=include_ambiguous,
            include_multiple=include_multiple,
            include_booked=include_booked,
            include_sold=include_sold,
        ),
        sort_params=SortParams(
            sort_by=sort_by,
            sort_order=sort_order,
        ),
        save_to_db=save_to_db,
        template=template,
    )


def parse_query(
    query_order_number: int,
    *,
    search_queries: opts.OptionalSearchQueries,
    title_queries: opts.TitleQueries,
    description_queries: opts.DescriptionQueries,
) -> Query:
    return Query(
        search_query=search_queries[query_order_number],
        title_query=title_queries[query_order_number] if title_queries else None,
        description_query=description_queries[query_order_number] if description_queries else None,
    )


def parse_queries(
    *,
    search_queries: opts.OptionalSearchQueries,
    title_queries: opts.TitleQueries,
    description_queries: opts.DescriptionQueries,
) -> tuple[list[str], list[str | None], list[str | None]]:
    queries_number = len(search_queries)

    for queries_type in (title_queries, description_queries):
        if len(queries_type) not in (0, queries_number):
            raise ValueError(f"Length of '{queries_type}' should be equal to the number of search queries.")

    title_queries = [(tq if tq.lower() not in _NULL_SYMBOLS else None) for tq in title_queries]
    description_queries = [(dq if dq.lower() not in _NULL_SYMBOLS else None) for dq in description_queries]

    return search_queries, title_queries, description_queries
