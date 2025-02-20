from os import getenv
from typing import Any


def get_env_or_secret(key: str, *, default: Any = None) -> str:
    if value := getenv(key):
        return value
    if file_path := getenv(f"{key}_FILE"):
        with open(file_path, "r") as f:
            return f.read().strip()
    return default
