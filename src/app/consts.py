from enum import Enum, StrEnum
from os import getenv

from app.utils import get_env_or_secret

AVITO_URL = "https://www.avito.ru"

RICH_COLORS = ("blue", "magenta", "cyan")

SAFE_SLEEP_TIME = float(getenv("AVITO_PARSER_SAFE_SLEEP_TIME", default=1.0))

MONGO_USERNAME = get_env_or_secret("MONGO_USERNAME")
MONGO_PASSWORD = get_env_or_secret("MONGO_PASSWORD")
MONGO_HOST = get_env_or_secret("MONGO_HOST")
MONGO_PORT = int(get_env_or_secret("MONGO_PORT", default=27017))
MONGO_DBNAME = get_env_or_secret("MONGO_DBNAME")
MONGO_URL = f"mongodb://{MONGO_USERNAME}:{MONGO_PASSWORD}@{MONGO_HOST}:{MONGO_PORT}"


class XPath(StrEnum):
    PRODUCTS = '//div[@itemtype="http://schema.org/Product" and @data-marker="item"]'
    SERVICES = '//div[@data-marker="price-lists-block"]'
    URL = '//a[@itemprop="url" and @data-marker="item-title"]'


class Symbols(Enum):
    RUB = (
        "₽",
        "рублей",
        "рубля",
        "рубль",
        "р",
        "руб",
        "rub",
    )
    NOT_RUB = (
        "г",
        "гр",
        "кг",
        "ш",
        "c",
    )
    SOLD = (
        "продано",
        "продан",
        "продана",
        "проданы",
        "продана",
        "🔴",
        "🚫",
        "❌",
        "✖️",
    )
    BOOKED = (
        "бронь",
        "забронировано",
        "забронирован",
        "забронирована",
        "забронированы",
        "забронирована",
    )

    @property
    def values(self) -> frozenset[str]:
        return frozenset(self.value) | frozenset({f" {symbol}" for symbol in self.value})


RUB_SYMBOLS = Symbols.RUB.values
NOT_RUB_SYMBOLS = Symbols.NOT_RUB.values
SOLD_SYMBOLS = Symbols.SOLD.values
BOOKED_SYMBOLS = Symbols.BOOKED.values
