import re
import string

from bs4 import BeautifulSoup

from app.consts import AVITO_URL, Symbols
from app.models import DescriptionLine, ParsedStatus, Product


def is_product(card_element: BeautifulSoup) -> bool:
    # try to find price block that is present only in services (not product) cards
    return not card_element.find("div", {"data-marker": "price-lists-block"})


def _normalize(s: str) -> str:
    s = s.translate(str.maketrans(string.punctuation, " " * len(string.punctuation)))  # remove punctuation
    s = re.sub(r"\s+", " ", s)  # remove extra spaces
    return s.lower().strip()


def _tokenize(s: str) -> list[str]:
    return _normalize(s).split()


def parse_product(
    product_element: BeautifulSoup,
    *,
    title_query: str,
    description_query: str,
    min_price: int | None = None,
    max_price: int | None = None,
) -> Product:
    a_element = product_element.find("a", {"itemprop": "url", "data-marker": "item-title"})

    title = a_element["title"]
    url = AVITO_URL + a_element["href"].split("?")[0]
    description = next(
        (
            p.text
            for p in product_element.find_all("p", attrs={"data-marker": False, "itemprop": False})
            if not p.text.strip().startswith(("<!-- -->", "Доставка"))
        ),
        "",
    )
    price_from_title = product_element.find("meta", {"itemprop": "price"})["content"]

    return Product(
        title=title,
        description=description,
        url=url,
        title_price=int(price_from_title) if price_from_title else None,
        description_info=parse_description(
            description=description,
            search_substr=description_query,
            min_price=min_price,
            max_price=max_price,
        ),
        is_query_in_title=all(t in _normalize(title) for t in _tokenize(title_query)),
    )


def parse_description(
    description: str,
    *,
    search_substr: str,
    min_price: int | None = None,
    max_price: int | None = None,
) -> list[DescriptionLine]:
    search_tokens = _tokenize(search_substr)

    parsed_lines = []
    for line in description.split("\n"):
        normalized_line = _normalize(line)

        if not all(token in normalized_line for token in search_tokens):
            continue

        parsed_line = parse_description_line(
            normalized_line,
            min_price=min_price,
            max_price=max_price,
        )
        parsed_lines.append(parsed_line)

    return parsed_lines


def parse_description_line(
    line: str,
    *,
    min_price: int | None = None,
    max_price: int | None = None,
) -> DescriptionLine:
    price, maybe_price, is_now_parsing_price = "", "", False

    for i, char in enumerate(line):
        if char.isdigit():
            price += char
            is_now_parsing_price = True

        elif is_now_parsing_price:
            if any(symbol == line[i : i + len(symbol)] for symbol in Symbols.NOT_RUB.values):
                price, is_now_parsing_price = "", False
                continue
            elif any(symbol == line[i : i + len(symbol)] for symbol in Symbols.RUB.values):
                break
            else:
                maybe_price = price
                price, is_now_parsing_price = "", False

        else:
            price, is_now_parsing_price = "", False

    def validate_price(v: str | int | None) -> int | None:
        v = int(v) if v else None
        if v and (not min_price or v >= min_price) and (not max_price or v <= max_price):
            return v
        return None

    price = validate_price(price) or validate_price(maybe_price)

    status = next(
        (
            status
            for status, symbols in {
                ParsedStatus.SOLD: Symbols.SOLD.values,
                ParsedStatus.BOOKED: Symbols.BOOKED.values,
            }.items()
            if any(sym in line for sym in symbols)
        ),
        ParsedStatus.OK if price else ParsedStatus.NOT_FOUND,
    )

    return DescriptionLine(price=price, status=status)
