import json
from dataclasses import asdict
from typing import Callable

from rich import print, print_json
from rich.console import Console
from rich.table import Table

from app.models import Product, ReprMode

_console = Console()


def _present_as_list(products: list[Product]) -> None:
    for i, repr_ in enumerate([pr.repr for pr in products]):
        print(f"[bold dim]{i + 1}.[/bold dim] {repr_.price} руб.: {repr_.title} ({repr_.url})")


def _present_as_table(products: list[Product]) -> None:
    table = Table(header_style="bold", show_lines=True)

    table.add_column("№", justify="right", style="bold dim")
    table.add_column("Title")
    table.add_column("Price from title", width=6)
    table.add_column("Prices from description", width=12)
    table.add_column("Price")
    table.add_column("Statuses from description")
    table.add_column("Status")

    for i, repr_ in enumerate([pr.repr for pr in products]):
        table.add_row(
            f"{i + 1}",
            f"{repr_.is_query_in_title} {repr_.title}\n{repr_.url}",
            repr_.title_price,
            repr_.description_prices,
            repr_.price,
            repr_.parsed_statuses,
            repr_.status,
        )

    _console.print(table)


def _present_as_dataclass(products: list[Product]) -> None:
    for i, product in enumerate(products):
        print(f"[bold]{i:3}.[/bold] ", end="")
        print(product)


def _present_as_json(products: list[Product]) -> None:
    json_repr = json.dumps([asdict(product) for product in products])  # noqa
    print_json(json_repr, indent=4)


def _present_as_csv(products: list[Product]) -> None:
    print("title;url;photos_number;status;price;statuses;title_price;description_prices")
    for pr in products:
        (
            pr.title.replace(";", ","),
            pr.url,
            pr.status,
            pr.price,
            str(pr.parsed_statuses),
            pr.title_price,
            str(pr.description_prices),
        )


type _PresentFunc = Callable[[list[Product]], None]

_PRESENT_STRATEGIES_MAPPING: dict[ReprMode, _PresentFunc] = {
    ReprMode.LIST: _present_as_list,
    ReprMode.TABLE: _present_as_table,
    ReprMode.DATACLASSES: _present_as_dataclass,
    ReprMode.JSON: _present_as_json,
    ReprMode.CSV: _present_as_csv,
}


def present(products: list[Product], mode: ReprMode) -> None:
    print(f"Found {len(products)} products: " + "–" * 80)

    try:
        present_func = _PRESENT_STRATEGIES_MAPPING[mode]
    except KeyError:
        raise ValueError(f"Unknown presentation mode: {mode}")

    present_func(products)
