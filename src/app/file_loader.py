import json
from dataclasses import asdict, fields
from functools import partial
from pathlib import Path
from typing import Callable, TextIO, TypedDict
from warnings import warn

import yaml

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

warn = partial(warn, stacklevel=2)


class LoaderMapping(TypedDict):
    loader_func: Callable[[TextIO], list | dict]
    decode_error: type[Exception]


__LOADERS: list[LoaderMapping] = [
    {"loader_func": json.load, "decode_error": json.JSONDecodeError},
    {"loader_func": yaml.safe_load, "decode_error": yaml.YAMLError},
]

__QUERY_KEYS = {field.name for field in fields(Query)}  # noqa
__QUERY_KEYS_NUMBER = len(__QUERY_KEYS)

__params_fields = fields(Params) + fields(FilterParams) + fields(SortParams)  # noqa
__PARAMS_KEYS = {f.name for f in __params_fields} - {"sort_by", "sort_order"}
__PARAMS_KEYS_NUMBER = len(__PARAMS_KEYS)

__QUERY_AND_PARAMS_KEYS = __QUERY_KEYS | __PARAMS_KEYS
__ALL_KEYS = __QUERY_AND_PARAMS_KEYS | {"query", "params"}

__ENUM_FIELDS_MAPPING = {
    "sort_by": SortBy,
    "sort_order": SortOrder,
    "template": ReprMode,
}


def load_data_from_file(file_path: Path) -> list | dict:
    """Loads data from a file in supported formats."""
    if not file_path.exists():
        raise FileNotFoundError(f"File not found: {file_path}")

    for loader in __LOADERS:
        try:
            with file_path.open("r") as file:
                return loader["loader_func"](file)
        except loader["decode_error"]:  # noqa
            continue
    else:
        raise ValueError(f"Unsupported file format: {file_path}")


def _parse_query_from_entry(request_entry: dict, entry_index: int) -> Query:
    if not isinstance(request_entry, dict):
        raise ValueError(f"Expected a dict, got: {type(request_entry)} on query #{entry_index}")

    if query_section := request_entry.get("query"):
        if len(query_section) > __QUERY_KEYS_NUMBER:
            warn(f"Unexpected keys in entry #{entry_index}: {set(query_section) - __QUERY_KEYS}")
        for key in __QUERY_KEYS:
            if key in request_entry:
                warn(f"Ignoring key '{key}' in request entry root #{entry_index}, because 'query' provided")
    else:
        query_section = request_entry

    if not isinstance(query_section, dict):
        raise ValueError(f"Expected a dict, got: {type(query_section)} in query on query #{entry_index}")

    query = {k: v for k, v in query_section.items() if k in __QUERY_KEYS}

    if not (search_query := query.get("search_query")):
        raise ValueError(f"Missing 'search_query' key in: {query} on query #{entry_index}")

    return Query(
        search_query=search_query,
        title_query=query.get("title_query", None),
        description_query=query_section.get("description_query", None),
    )


def _parse_params_from_entry(request_entry: dict, entry_index: int, fallback_params_values: Params) -> Params:
    params_fb = asdict(fallback_params_values)  # noqa
    filter_params_fb = params_fb["filter_params"]
    sort_params_fb = params_fb["sort_params"]

    if params_section := request_entry.get("params"):
        if len(params_section) > len(__PARAMS_KEYS):
            warn(f"Unexpected keys in entry #{entry_index}: {set(params_section) - __PARAMS_KEYS}")
        for key in __PARAMS_KEYS:
            if key in request_entry:
                warn(f"Ignoring key '{key}' in request entry root #{entry_index}, because 'params' provided")
    else:
        params_section = request_entry

    if not isinstance(params_section, dict):
        raise ValueError(f"Expected a dict, got: {type(params_section)} in params on query #{entry_index}")

    parsed_params_dict = {k: v for k, v in params_section.items() if k in __PARAMS_KEYS}

    for key, enum_cls in __ENUM_FIELDS_MAPPING.items():
        if parsed_params_dict.get(key):
            parsed_params_dict[key] = enum_cls(parsed_params_dict[key].lower())

    return Params(
        max_pages=parsed_params_dict.get("max_pages", params_fb["max_pages"]),
        filter_params=FilterParams(
            min_price=parsed_params_dict.get("min_price", filter_params_fb["min_price"]),
            max_price=parsed_params_dict.get("max_price", filter_params_fb["max_price"]),
            include_unknown=parsed_params_dict.get("include_unknown", filter_params_fb["include_unknown"]),
            include_ambiguous=parsed_params_dict.get("include_ambiguous", filter_params_fb["include_ambiguous"]),
            include_multiple=parsed_params_dict.get("include_multiple", filter_params_fb["include_multiple"]),
            include_sold=parsed_params_dict.get("include_sold", filter_params_fb["include_sold"]),
            include_booked=parsed_params_dict.get("include_booked", filter_params_fb["include_booked"]),
        ),
        sort_params=SortParams(
            sort_by=parsed_params_dict.get("sort_by", sort_params_fb["sort_by"]),
            sort_order=parsed_params_dict.get("sort_order", sort_params_fb["sort_order"]),
        ),
        save_to_db=parsed_params_dict.get("save_to_db", params_fb["save_to_db"]),
        template=parsed_params_dict.get("template", params_fb["template"]),
    )


def load_request_entries_from_file(file_path: Path, fallback_params_values: Params) -> list[ProductRequest]:
    """Parses a YAML or JSON file with a list of product requests. Example files in 'request-entries' directory."""
    if not (loaded_data := load_data_from_file(file_path)):
        raise ValueError(f"File is empty: {file_path}")

    if not isinstance(loaded_data, list):
        raise ValueError(f"Expected a list, got: {type(loaded_data)} in {file_path}")

    product_requests: list[ProductRequest] = []
    for i, entry in enumerate(loaded_data, start=1):
        if not isinstance(entry, dict):
            raise ValueError(f"Expected a dict, got: {type(entry)} in {file_path}")

        for key in entry:
            if key not in __ALL_KEYS:
                warn(f"Unexpected key '{key}' in request entry root #{i}")

        product_requests.append(
            ProductRequest(
                query=_parse_query_from_entry(
                    request_entry=entry,
                    entry_index=i,
                ),
                params=_parse_params_from_entry(
                    request_entry=entry,
                    entry_index=i,
                    fallback_params_values=fallback_params_values,
                ),
            )
        )

    return product_requests
