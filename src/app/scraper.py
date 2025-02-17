from contextlib import suppress
from time import sleep
from urllib.parse import urlencode

from bs4 import BeautifulSoup
from rich import print
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.expected_conditions import element_attribute_to_include

from app.consts import AVITO_URL, XPath, SAFE_SLEEP_TIME, RICH_COLORS
from app.driver_interface import get_interface


def _get_avito_search_page(search_query: str, page_number: int) -> None:
    interface = get_interface()

    interface.get(f"{AVITO_URL}/moskva?{urlencode({'q': search_query, 'p': page_number})}")

    with suppress(TimeoutException):
        interface.wait_until(element_attribute_to_include(("xpath", XPath.PRODUCTS), "data-item-id"))
        interface.wait_until(element_attribute_to_include(("xpath", XPath.URL), "href"))

    sleep(SAFE_SLEEP_TIME)


def _get_card_elements_from_avito_search_page(search_query: str, page_number: int) -> list[BeautifulSoup]:
    interface = get_interface()

    _get_avito_search_page(search_query, page_number)

    with open(f"page_{search_query.replace(" ", "_")}_{page_number}.html", "w") as f:
        f.write(interface.page_source)

    return [
        BeautifulSoup(element.get_attribute("outerHTML"), "html.parser")
        for element in interface.find_elements_by("xpath", XPath.PRODUCTS)
    ]


def get_card_elements_from_avito_search(search_query: str, max_pages: int) -> list[BeautifulSoup]:
    print(f"Searching for [bold]<[yellow]{search_query}[/yellow]>[/bold] on Avito...")

    print("Pages: ", end="", flush=True)

    page_number = 1
    all_card_elements: list[BeautifulSoup] = []
    while True:
        color = RICH_COLORS[(page_number - 1) % len(RICH_COLORS)]
        print(f"[bold {color}]{page_number}...[/bold {color}]", end=" ", flush=True)

        if not (card_elements := _get_card_elements_from_avito_search_page(search_query, page_number)):
            number_of_chars_to_delete = len(str(page_number)) + 4
            print(f"{'\b' * number_of_chars_to_delete}[bold {color}]LAST![/bold {color}]\n")
            break

        all_card_elements.extend(card_elements)

        page_number += 1
        if max_pages and (page_number > max_pages):
            number_of_chars_to_delete = len(str(page_number)) + 4
            print(f"{'\b' * number_of_chars_to_delete}[bold {color}]MAX![/bold {color}]\n")
            break

    return all_card_elements
