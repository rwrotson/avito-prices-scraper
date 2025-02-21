from datetime import datetime

from typer import Typer

from app.cli import defaults, opts, parsers
from app.file_loader import load_request_entries_from_file
from app.models import DatetimeRange, ProductRequest
from app.scraper.driver import mount_interface
from app.services import search_in_db as search_in_db_service_function
from app.services import search_on_avito as search_on_avito_service_function

cli_app = Typer()


@cli_app.command()
def search_on_avito(
    search_queries: opts.RequiredSearchQueries,
    *,
    title_queries: opts.TitleQueries,
    description_queries: opts.DescriptionQueries,
    max_pages: opts.MaxPages = defaults.MAX_PAGES,
    min_price: opts.MinPrice = defaults.MIN_PRICE,
    max_price: opts.MaxPrice = defaults.MAX_PRICE,
    include_unknown: opts.IncludeUnknown = defaults.INCLUDE_UNKNOWN,
    include_ambiguous: opts.IncludeAmbiguous = defaults.INCLUDE_AMBIGUOUS,
    include_multiple: opts.IncludeMultiple = defaults.INCLUDE_MULTIPLE,
    include_booked: opts.IncludeBooked = defaults.INCLUDE_BOOKED,
    include_sold: opts.IncludeSold = defaults.INCLUDE_SOLD,
    sort_by: opts.SortBy = defaults.SORT_BY,
    sort_order: opts.SortOrder = defaults.SORT_ORDER,
    template: opts.Template = defaults.TEMPLATE,
    save_to_db: opts.SaveToDb = defaults.SAVE_TO_DB,
) -> None:
    """
    Search for products on Avito by given queries.

    For 'title_queries' and 'description_queries' options:\n
      - when list of values is provided, it should be of the same length as 'search_queries',
    as each value will be used for corresponding search query
      - when None values are provided, they default to 'search_queries'
    """
    search_queries, title_queries, description_queries = parsers.parse_queries(
        search_queries=search_queries,
        title_queries=title_queries,
        description_queries=description_queries,
    )

    requests = [
        ProductRequest(
            query=parsers.parse_query(
                query_order_number=i,
                search_queries=search_queries,
                title_queries=title_queries,
                description_queries=description_queries,
            ),
            params=parsers.parse_params(
                max_pages=max_pages,
                min_price=min_price,
                max_price=max_price,
                include_unknown=include_unknown,
                include_ambiguous=include_ambiguous,
                include_multiple=include_multiple,
                include_booked=include_booked,
                include_sold=include_sold,
                sort_by=sort_by,
                sort_order=sort_order,
                template=template,
                save_to_db=save_to_db,
            ),
        )
        for i in range(len(search_queries))
    ]

    cli_call_timestamp = datetime.now().replace(second=0, microsecond=0)

    with mount_interface():
        for request in requests:
            search_on_avito_service_function(request=request, timestamp=cli_call_timestamp)


@cli_app.command()
def search_on_avito_from_file(
    file_path: opts.FilePath,
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
) -> None:
    """
    Search for products on Avito by given queries from a file.

    The file in YAML or JSON format should contain a list of dictionaries with request params,
    where each dictionary represents query and params for a single search request.

    You can find examples of this file in 'request-entries' directory.

    Other options provide fallback values for all params, when they are not provided in the file.
    """
    requests = load_request_entries_from_file(
        file_path=file_path,
        fallback_params=parsers.parse_params(
            max_pages=max_pages,
            min_price=min_price,
            max_price=max_price,
            include_unknown=include_unknown,
            include_ambiguous=include_ambiguous,
            include_multiple=include_multiple,
            include_booked=include_booked,
            include_sold=include_sold,
            sort_by=sort_by,
            sort_order=sort_order,
            template=template,
            save_to_db=save_to_db,
        ),
    )

    cli_call_timestamp = datetime.now().replace(second=0, microsecond=0)

    with mount_interface():
        for request in requests:
            search_on_avito_service_function(request=request, timestamp=cli_call_timestamp)


@cli_app.command()
def search_in_db(
    search_queries: opts.OptionalSearchQueries,
    *,
    title_queries: opts.TitleQueries,
    description_queries: opts.DescriptionQueries,
    request_ids: opts.RequestIds,
    datetime_lte: opts.DatetimeLte = defaults.DATETIME_LTE,
    datetime_gte: opts.DatetimeGte = defaults.DATETIME_GTE,
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
) -> None:
    """
    Search for product_requests and resulting products.


    """
    try:
        from app.db import get_products_from_db, get_requests_from_db
    except ImportError:
        raise ImportError("Database connection not available.")

    search_queries, title_queries, description_queries = parsers.parse_queries(
        search_queries=search_queries,
        title_queries=title_queries,
        description_queries=description_queries,
    )
    queries = [
        parsers.parse_query(
            query_order_number=i,
            search_queries=search_queries,
            title_queries=title_queries,
            description_queries=description_queries,
        )
        for i in range(len(search_queries))
    ]

    params = parsers.parse_params(
        min_price=min_price,
        max_price=max_price,
        include_unknown=include_unknown,
        include_ambiguous=include_ambiguous,
        include_multiple=include_multiple,
        include_booked=include_booked,
        include_sold=include_sold,
        sort_by=sort_by,
        sort_order=sort_order,
        template=template,
    )

    search_in_db_service_function(
        queries=queries,
        request_ids=request_ids,
        datatime_ranges=[DatetimeRange(gte=datetime_gte, lte=datetime_lte)],
        params=params,
    )
