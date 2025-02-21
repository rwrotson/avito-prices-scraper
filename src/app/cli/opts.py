from datetime import datetime
from pathlib import Path
from typing import Annotated

from typer import Argument, Option

from app.models import ReprMode, SortBy, SortOrder

_SEARCH_QUERIES_HELP = "A query string(s) to search for a product with Avito search service"

# Queries options --------------------------------------------------------------
RequiredSearchQueries = Annotated[
    list[str],
    Argument(
        default=...,
        show_default=False,
        help=_SEARCH_QUERIES_HELP,
    ),
]
OptionalSearchQueries = Annotated[
    list[str],
    Option(
        default_factory=list,
        help=_SEARCH_QUERIES_HELP,
    ),
]
TitleQueries = Annotated[
    list[str],
    Option(
        default_factory=list,
        help=(
            "An additional query string(s) to search for in product titles for better prices detection. "
            "If not provided, search in titles will be performed with 'search_queries' strings."
            "Use '_' to skip this option for some of queries and use 'search_queries' instead."
        ),
    ),
]
DescriptionQueries = Annotated[
    list[str],
    Option(
        default_factory=list,
        help=(
            "An additional query string(s) to search for in product descriptions, "
            "when there are several products in one product card at one URL. "
            "If not provided, search in descriptions will be performed with 'search_queries' strings. "
            "Use '_' to skip this option for some of queries and use 'search_queries' instead."
        ),
    ),
]

# Scraper options --------------------------------------------------------------
MaxPages = Annotated[
    int,
    Option(
        min=0,
        help="Maximum number of pages to scrape. Use '0' to scrape all pages.",
    ),
]

# Filter options ---------------------------------------------------------------
MinPrice = Annotated[
    int,
    Option(
        min=0,
        help="Minimum price to filter by. Use '0' to not filter.",
    ),
]
MaxPrice = Annotated[
    int,
    Option(
        min=0,
        help="Maximum price to filter by. Use '0' to not filter.",
    ),
]
IncludeUnknown = Annotated[
    bool,
    Option(
        help="Include products with unknown prices.",
    ),
]
IncludeAmbiguous = Annotated[
    bool,
    Option(
        help="Include products with ambiguous prices.",
    ),
]
IncludeMultiple = Annotated[
    bool,
    Option(
        help="Include products with multiple prices found in description.",
    ),
]
IncludeBooked = Annotated[
    bool,
    Option(
        help="Include products marked as booked.",
    ),
]
IncludeSold = Annotated[
    bool,
    Option(
        help="Include products marked as sold.",
    ),
]

# Sort options -----------------------------------------------------------------
SortBy = Annotated[
    SortBy,
    Option(
        case_sensitive=False,
        help="Sort products by price or page.",
    ),
]
SortOrder = Annotated[
    SortOrder,
    Option(
        # show_default="asc",
        case_sensitive=False,
        help="Sort products in ascending or descending order.",
    ),
]

# Representation options -------------------------------------------------------
Template = Annotated[
    ReprMode,
    Option(
        case_sensitive=False,
        help="Choose a template for printing found products and prices.",
    ),
]

# Other options ----------------------------------------------------------------
SaveToDb = Annotated[
    bool,
    Option(
        help="Whether to save products to the database or not.",
    ),
]

FilePath = Annotated[
    Path,
    Argument(
        default=...,
        exists=True,
        readable=True,
        show_default=False,
        help="Path to a JSON or YAML text file with search queries and options.",
    ),
]

RequestIds = Annotated[
    list[str],
    Option(
        default_factory=list,
        # show_default="None",
        help="Filter by request ID.",
    ),
]

DatetimeLte = Annotated[
    datetime | None,
    Option(
        parser=datetime.fromisoformat,
        help="Filter by max timestamp.",
    ),
]
DatetimeGte = Annotated[
    datetime | None,
    Option(
        parser=datetime.fromisoformat,
        help="Filter by min timestamp.",
    ),
]
