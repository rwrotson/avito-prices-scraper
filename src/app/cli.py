from pathlib import Path
from typing import Annotated

from typer import Argument, Option, Typer

from app.driver_interface import mount_interface
from app.file_loader import load_request_entries_from_file
from app.models import (
    FilterParams,
    Params,
    ProductRequest,
    Query,
    ReprMode,
    SortBy,
    SortOrder,
    SortParams,
)
from app.services import search_on_avito as search_on_avito_service_function

cli_app = Typer()


_NULL_SYMBOLS = {"_", "none", "null"}


_HELP_TEXTS = {
    "search_queries": "A query string(s) to search for a product with Avito search service",
    "title_query": (
        "An additional query string(s) to search for in product titles "
        "for better prices detection. "
        "If not provided, search in titles will be performed with 'search_queries' strings."
        "Use '_' to skip this option for some of queries and use 'search_queries' instead."
    ),
    "description_query": (
        "An additional query string(s) to search for in product descriptions, "
        "when there are several products in one product card at one URL. "
        "If not provided, search in descriptions will be performed with 'search_queries' strings. "
        "Use '_' to skip this option for some of queries and use 'search_queries' instead."
    ),
    "max_pages": "Maximum number of pages to search. Use '0' for full search.",
    "min_price": "Minimum price to filter by. Use '0' to not filter.",
    "max_price": "Maximum price to filter by. Use '0' to not filter.",
    "include_unknown": "Include products with unknown prices.",
    "include_ambiguous": "Include products with ambiguous prices.",
    "include_multiple": "Include products with multiple prices found in description.",
    "include_booked": "Include products marked as booked.",
    "include_sold": "Include products marked as sold.",
    "sort_by": "Sort products by price or page.",
    "sort_order": "Choose ascending or descending sort order.",
    "save_to_db": "Whether to save products to the database or not.",
    "template": "Choose a template for printing found products and prices.",
}


def _fallback_text(field_name: str) -> str:
    return f"Fallback for '{field_name}' options from file. "


@cli_app.command()
def search_on_avito(
    search_queries: Annotated[
        list[str],
        Argument(default=..., show_default=False, help=_HELP_TEXTS["search_queries"]),
    ],
    *,
    title_query: Annotated[
        list[str],
        Option(default_factory=list, show_default="_", help=_HELP_TEXTS["title_query"]),
    ],
    description_query: Annotated[
        list[str],
        Option(default_factory=list, show_default="_", help=_HELP_TEXTS["description_query"]),
    ],
    max_pages: Annotated[
        list[int],
        Option(default_factory=lambda: [0], show_default="0", min=0, help=_HELP_TEXTS["max_pages"]),
    ],
    min_price: Annotated[
        list[int],
        Option(default_factory=lambda: [0], show_default="0", min=0, help=_HELP_TEXTS["min_price"]),
    ],
    max_price: Annotated[
        list[int],
        Option(default_factory=lambda: [0], show_default="0", min=0, help=_HELP_TEXTS["max_price"]),
    ],
    include_unknown: Annotated[
        list[bool],
        Option(default_factory=lambda: [True], show_default="True", help=_HELP_TEXTS["include_unknown"]),
    ],
    include_ambiguous: Annotated[
        list[bool],
        Option(default_factory=lambda: [True], show_default="True", help=_HELP_TEXTS["include_ambiguous"]),
    ],
    include_multiple: Annotated[
        list[bool], Option(default_factory=lambda: [True], show_default="True", help=_HELP_TEXTS["include_multiple"])
    ],
    include_booked: Annotated[
        list[bool],
        Option(default_factory=lambda: [True], show_default="True", help=_HELP_TEXTS["include_booked"]),
    ],
    include_sold: Annotated[
        list[bool],
        Option(default_factory=lambda: [True], show_default="True", help=_HELP_TEXTS["include_sold"]),
    ],
    sort_by: Annotated[
        list[SortBy],
        Option(
            default_factory=lambda: [SortBy.PRICE],
            show_default="price",
            case_sensitive=False,
            help=_HELP_TEXTS["sort_by"],
        ),
    ],
    sort_order: Annotated[
        list[SortOrder],
        Option(
            default_factory=lambda: [SortOrder.ASC],
            show_default="asc",
            case_sensitive=False,
            help=_HELP_TEXTS["sort_order"],
        ),
    ],
    save_to_db: Annotated[
        list[bool],
        Option(default_factory=lambda: [False], show_default="False", help=_HELP_TEXTS["save_to_db"]),
    ],
    template: Annotated[
        list[ReprMode],
        Option(
            default_factory=lambda: [ReprMode.TABLE],
            show_default="table",
            case_sensitive=False,
            help=_HELP_TEXTS["template"],
        ),
    ],
) -> None:
    """
    Search for products on Avito by given queries.

    For options except for 'description_queries':\n
      - when single value is provided, it will be used for all search queries\n
      - when list of values is provided, it should be of the same length as 'search_queries',
    as each value will be used for corresponding search query
    """
    queries_number = len(search_queries)

    if len(description_query) not in (0, queries_number):
        raise ValueError("Length of 'description_queries' should be equal to the number of search queries.")

    title_queries = [(tq if tq.lower() not in _NULL_SYMBOLS else None) for tq in title_query]
    description_queries = [(dq if dq.lower() not in _NULL_SYMBOLS else None) for dq in description_query]
    max_pages = [(mp if mp else None) for mp in max_pages]
    min_price = [(mp if mp else None) for mp in min_price]
    max_price = [(mp if mp else None) for mp in max_price]

    kwargs = {
        "max_pages": max_pages,
        "min_price": min_price,
        "max_price": max_price,
        "include_unknown": include_unknown,
        "include_ambiguous": include_ambiguous,
        "include_multiple": include_multiple,
        "include_booked": include_booked,
        "include_sold": include_sold,
        "sort_by": sort_by,
        "sort_order": sort_order,
        "save_to_db": save_to_db,
        "template": template,
    }
    for kwarg_name, kwarg_value in kwargs.items():
        if len(kwarg_value) not in (1, queries_number):
            raise ValueError(
                f"Length of {kwarg_name} should be equal to the number of search queries or to be equal to 1."
            )

    request_entries = [
        ProductRequest(
            query=Query(
                search_query=search_queries[i],
                title_query=title_queries[i] if title_queries else None,
                description_query=description_queries[i] if description_queries else None,
            ),
            params=Params(
                max_pages=max_pages[i] if len(max_pages) > 1 else max_pages[0],
                filter_params=FilterParams(
                    min_price=min_price[i] if len(min_price) > 1 else min_price[0],
                    max_price=max_price[i] if len(max_price) > 1 else max_price[0],
                    include_unknown=include_unknown[i] if len(include_unknown) > 1 else include_unknown[0],
                    include_ambiguous=include_ambiguous[i] if len(include_ambiguous) > 1 else include_ambiguous[0],
                    include_multiple=include_multiple[i] if len(include_multiple) > 1 else include_multiple[0],
                    include_booked=include_booked[i] if len(include_booked) > 1 else include_booked[0],
                    include_sold=include_sold[i] if len(include_sold) > 1 else include_sold[0],
                ),
                sort_params=SortParams(
                    sort_by=sort_by[i] if len(sort_by) > 1 else sort_by[0],
                    sort_order=sort_order[i] if len(sort_order) > 1 else sort_order[0],
                ),
                save_to_db=save_to_db[i] if len(save_to_db) > 1 else save_to_db[0],
                template=template[i] if len(template) > 1 else template[0],
            ),
        )
        for i in range(queries_number)
    ]

    with mount_interface():
        for request_entry in request_entries:
            search_on_avito_service_function(request=request_entry)


@cli_app.command()
def search_on_avito_from_file(
    file_path: Annotated[
        Path,
        Argument(
            default=...,
            exists=True,
            readable=True,
            show_default=False,
            help="Path to a JSON or YAML text file with search queries and options.",
        ),
    ],
    *,
    max_pages: Annotated[
        int,
        Option(min=0, help=_fallback_text("max_pages") + _HELP_TEXTS["max_pages"]),
    ] = 6,
    min_price: Annotated[
        int,
        Option(min=0, help=_fallback_text("min_price") + _HELP_TEXTS["min_price"]),
    ] = 0,
    max_price: Annotated[
        int,
        Option(min=0, help=_fallback_text("max_price") + _HELP_TEXTS["max_price"]),
    ] = 0,
    include_unknown: Annotated[
        bool,
        Option(help=_fallback_text("include_unknown") + _HELP_TEXTS["include_unknown"]),
    ] = True,
    include_ambiguous: Annotated[
        bool,
        Option(help=_fallback_text("include_ambiguous") + _HELP_TEXTS["include_ambiguous"]),
    ] = True,
    include_multiple: Annotated[
        bool,
        Option(help=_fallback_text("include_multiple") + _HELP_TEXTS["include_multiple"]),
    ] = True,
    include_booked: Annotated[
        bool,
        Option(help=_fallback_text("include_booked") + _HELP_TEXTS["include_booked"]),
    ] = True,
    include_sold: Annotated[
        bool,
        Option(help=_fallback_text("include_sold") + _HELP_TEXTS["include_sold"]),
    ] = True,
    sort_by: Annotated[
        SortBy,
        Option(case_sensitive=False, help=_fallback_text("sort_by") + _HELP_TEXTS["sort_by"]),
    ] = SortBy.PRICE,
    sort_order: Annotated[
        SortOrder,
        Option(case_sensitive=False, help=_fallback_text("sort_by") + _HELP_TEXTS["sort_by"]),
    ] = SortOrder.ASC,
    save_to_db: Annotated[
        bool,
        Option(help=_fallback_text("save_to_db") + _HELP_TEXTS["save_to_db"]),
    ] = False,
    template: Annotated[
        ReprMode,
        Option(case_sensitive=False, help=_fallback_text("template") + _HELP_TEXTS["template"]),
    ] = ReprMode.TABLE,
) -> None:
    """
    Search for products on Avito by given queries from a file.

    The file in YAML or JSON format should contain a list of dictionaries with request params,
    where each dictionary represents query and params for a single search request.

    You can find examples of this file in 'request_entries' directory.

    Other options provide fallback values for all params, when they are not provided in the file.
    """
    requests = load_request_entries_from_file(
        file_path=file_path,
        fallback_params_values=Params(
            max_pages=max_pages if max_pages else None,
            filter_params=FilterParams(
                min_price=min_price if min_price else None,
                max_price=max_price if max_price else None,
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
        ),
    )

    with mount_interface():
        for request in requests:
            search_on_avito_service_function(request=request)
