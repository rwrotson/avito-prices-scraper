from typing import Literal

from pymongo import ASCENDING, HASHED, MongoClient
from pymongo.collection import Collection

from app.consts import MONGO_DBNAME, MONGO_URL

type CollectionNames = Literal[
    "requests",
    "products",
]
type Db = dict[CollectionNames, Collection]
type FieldName = str
type IndexType = int | str
type IndexesConfig = dict[CollectionNames, list[tuple[FieldName, IndexType]]]


def _initialize_db() -> Db:
    client = MongoClient(MONGO_URL)
    db = client[MONGO_DBNAME]

    return {
        "requests": db["requests"],
        "products": db["products"],
    }


def _create_indexes_if_not_exist(db: Db, indexes: IndexesConfig) -> None:
    """Create indexes for the collections if they do not exist"""
    for collection_name, index_entry in indexes.items():
        collection = db[collection_name]
        existing_indexes = {index["name"] for index in collection.list_indexes()}

        for field_name, index_type in index_entry:
            index_name = f"{field_name}_index"
            if index_name not in existing_indexes:
                collection.create_index([(field_name, index_type)], name=index_name)


_INDEXES_CONFIG: IndexesConfig = {
    "requests": [
        ("timestamp", ASCENDING),
        ("request_id", HASHED),
        ("query.search_query", ASCENDING),
        ("query.title_query", ASCENDING),
        ("query.description_query", ASCENDING),
    ],
    "products": [
        ("timestamp", ASCENDING),
        ("request_id", HASHED),
        ("title", ASCENDING),
        ("url", ASCENDING),
        ("price", ASCENDING),
        ("status", ASCENDING),
    ],
}

db = _initialize_db()
_create_indexes_if_not_exist(indexes=_INDEXES_CONFIG, db=db)
