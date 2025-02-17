from enum import Enum, StrEnum
from os import getenv
from typing import Any


def _get_env_or_secret(key: str, *, default: Any = None) -> str:
    if value := getenv(key):
        return value
    if file_path := getenv(f"{key}_FILE"):
        with open(file_path, "r") as f:
            return f.read().strip()
    return default


SAFE_SLEEP_TIME = float(getenv("AVITO_PARSER_SAFE_SLEEP_TIME", default=1.0))
RICH_COLORS = ("blue", "magenta", "cyan")

AVITO_URL = "https://www.avito.ru"


MONGO_USERNAME = _get_env_or_secret("MONGODB_USERNAME")
MONGO_PASSWORD = _get_env_or_secret("MONGODB_PASSWORD")
MONGO_HOST = _get_env_or_secret("MONGODB_HOST")
MONGO_PORT = int(_get_env_or_secret("MONGODB_PORT", default=27017))
MONGO_DB = _get_env_or_secret("MONGODB_DB")
MONGO_URL = f"mongodb://{MONGO_USERNAME}:{MONGO_PASSWORD}@{MONGO_HOST}:{MONGO_PORT}/{MONGO_DB}"


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
