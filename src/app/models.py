from dataclasses import dataclass, field
from enum import StrEnum, auto
from functools import cached_property


class ReprMode(StrEnum):
    LIST = "list"
    TABLE = "table"
    DATACLASSES = "dataclasses"
    JSON = "json"
    CSV = "csv"


class SortBy(StrEnum):
    PRICE = "price"
    PAGE = "page"


class SortOrder(StrEnum):
    ASC = "asc"
    DESC = "desc"


@dataclass(slots=True, frozen=True)
class Query:
    search_query: str
    title_query: str | None
    description_query: str | None


@dataclass(slots=True, frozen=True)
class FilterParams:
    min_price: int | None
    max_price: int | None
    include_unknown: bool
    include_sold: bool
    include_booked: bool
    include_ambiguous: bool
    include_multiple: bool


@dataclass(slots=True, frozen=True)
class SortParams:
    sort_by: SortBy
    sort_order: SortOrder


@dataclass(slots=True, frozen=True)
class Params:
    max_pages: int | None
    filter_params: FilterParams
    sort_params: SortParams
    save_to_db: bool
    template: ReprMode


@dataclass(slots=True, frozen=True)
class ProductRequest:
    query: Query
    params: Params


class ParsedStatus(StrEnum):
    OK = auto()
    NOT_FOUND = auto()
    SOLD = auto()
    BOOKED = auto()

    @cached_property
    def repr(self) -> str:
        style = {
            ParsedStatus.OK: "b green",
            ParsedStatus.NOT_FOUND: "b purple",
            ParsedStatus.SOLD: "b red",
            ParsedStatus.BOOKED: "b yellow",
        }[self]
        return f"[{style}]{self.name}[/{style}]"


class PriceStatus(StrEnum):
    OK = auto()
    MULTIPLE_FOUND = auto()
    NOT_FOUND = auto()

    @cached_property
    def repr(self) -> str:
        style = {
            PriceStatus.OK: "b green",
            PriceStatus.MULTIPLE_FOUND: "b orange",
            PriceStatus.NOT_FOUND: "b purple",
        }[self]
        return f"[{style}]{self.name}[/{style}]"


class ProductStatus(StrEnum):
    OK = auto()
    MULTIPLE_FOUND = auto()
    NOT_FOUND = auto()
    SOLD = auto()
    BOOKED = auto()
    AMBIGUOUS = auto()  # multiple statuses found

    @cached_property
    def repr(self) -> str:
        style = {
            ProductStatus.OK: "u b green",
            ProductStatus.NOT_FOUND: "u b purple",
            ProductStatus.SOLD: "u b red",
            ProductStatus.BOOKED: "u b yellow",
            ProductStatus.AMBIGUOUS: "u b blue",
            ProductStatus.MULTIPLE_FOUND: "u b orange",
        }[self]
        return f"[{style}]{self.name}[/{style}]"


class _ProductRepr:
    def __init__(self, product: "Product"):
        self.title = f"[bold]{product.title}[/bold]"
        self.description = f"[dim]{product.description}[/dim]"
        self.url = f"[u blue link={product.url}]{product.url}[/u blue link]"

        self.title_price = f"[magenta]{product.title_price or 'N/A'}[/magenta]"
        self.description_prices = ", ".join(f"[green4]{s or 'N/A'}[/green4]" for s in set(product.description_prices))
        self.price = self._construct_price_repr(product)
        self.is_query_in_title = "[b green]✔[/b green]" if product.is_query_in_title else "[b red]✘[/b red]"

        self.parsed_statuses = ", ".join(s.repr for s in set(product.parsed_statuses))
        self.status = product.status.repr

    @staticmethod
    def _construct_price_repr(product: "Product") -> str:
        if product.price_status == PriceStatus.OK:
            return f"[u b yellow]{product.price}[/u b yellow]"
        if product.price_status == PriceStatus.MULTIPLE_FOUND:
            return ", ".join(f"[b yellow]{s}[/b yellow]" for s in product.price)
        return "[b]N/A[/b]"


@dataclass(frozen=True)
class DescriptionLine:
    price: int | None
    status: ParsedStatus


@dataclass(frozen=True)
class Product:
    title: str
    description: str
    url: str
    title_price: int | None
    description_info: list[DescriptionLine]
    is_query_in_title: bool

    repr: _ProductRepr = field(init=False)

    def __post_init__(self) -> None:
        object.__setattr__(self, "repr", _ProductRepr(self))

    @cached_property
    def description_prices(self) -> list[int]:
        """List of prices found in the description."""
        return [line.price for line in self.description_info if line.price]

    @cached_property
    def parsed_statuses(self) -> list[ParsedStatus]:
        """List of statuses found in the description."""
        return [line.status for line in self.description_info if line.status]

    @cached_property
    def _parsed_statuses_set(self) -> frozenset[ParsedStatus]:
        return frozenset(self.parsed_statuses)

    @cached_property
    def _parsed_statuses_len(self) -> int:
        return len(frozenset(self.parsed_statuses))

    @cached_property
    def price(self) -> int | list[int] | None:
        price = None
        if self.is_query_in_title:
            price = self.title_price or self.description_prices
        elif self.title_price:
            price = self.title_price if self.title_price in self.description_prices else self.description_prices
        return price[0] if (isinstance(price, list) and len(price) == 1) else (price or None)

    @cached_property
    def unified_price(self) -> int:
        """Price used for filtering and sorting."""
        return self.price[0] if isinstance(self.price, list) else (self.price or 0)

    @cached_property
    def price_status(self) -> PriceStatus:
        """Returns the status of the price."""
        if self.price is None:
            return PriceStatus.NOT_FOUND
        if isinstance(self.price, list):
            return PriceStatus.MULTIPLE_FOUND
        return PriceStatus.OK

    @cached_property
    def status(self) -> ProductStatus:
        """Returns the status of the product."""
        if not self.parsed_statuses:
            return ProductStatus(self.price_status)

        if self._parsed_statuses_len > 1:
            return ProductStatus.AMBIGUOUS
        if ParsedStatus.SOLD in self._parsed_statuses_set:
            return ProductStatus.SOLD
        if ParsedStatus.BOOKED in self._parsed_statuses_set:
            return ProductStatus.BOOKED

        return ProductStatus(self.price_status)
