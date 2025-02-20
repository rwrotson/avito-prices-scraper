from app.models import ReprMode, SortBy, SortOrder

MAX_PAGES = 0

MIN_PRICE = 0
MAX_PRICE = 0
INCLUDE_UNKNOWN = True
INCLUDE_AMBIGUOUS = True
INCLUDE_MULTIPLE = True
INCLUDE_BOOKED = True
INCLUDE_SOLD = True

SORT_BY = SortBy.PRICE
SORT_ORDER = SortOrder.ASC

TEMPLATE = ReprMode.TABLE

SAVE_TO_DB = False

DATETIME_LTE = None
DATETIME_GTE = None
