import datetime as dt
from models.day import Day, handle_weekends, get_next_tuesday
import pandas as pd


class Treatment:
    _ORDER_ID: int
    _EXPECTED_DATE: dt.date
    _ACTUAL_DATE: dt.date | None
    _NAME: str
    display_name: str
    _REST_DAYS: int

    @property
    def order_id(self) -> int:
        return self._ORDER_ID

    @property
    def name(self) -> str:
        return self._NAME

    @property
    def rest_days(self) -> int:
        return self._REST_DAYS

    @property
    def expected_date(self) -> dt.date:
        return self._EXPECTED_DATE

    @property
    def actual_date(self) -> dt.date | None:
        return self._ACTUAL_DATE

    def __str__(self):
        return f"{self.display_name.ljust(9)}: {self.expected_date}"

    def __lt__(self, other):
        # If they are from the same class, compare by date
        if isinstance(other, type(self)):
            if self._ACTUAL_DATE and other._ACTUAL_DATE:
                return self._ACTUAL_DATE < other._ACTUAL_DATE
            elif self._ACTUAL_DATE and not other._ACTUAL_DATE:
                return self._ACTUAL_DATE < other.expected_date
            elif not self._ACTUAL_DATE and other._ACTUAL_DATE:
                return self.expected_date < other._ACTUAL_DATE
            else:
                return self.expected_date < other.expected_date

        # If they are from different classes, compare by order_id
        return self.order_id < other.order_id

    def __gt__(self, other):
        # If they are from the same class, compare by date
        if isinstance(other, type(self)):
            if self._ACTUAL_DATE and other._ACTUAL_DATE:
                return self._ACTUAL_DATE > other._ACTUAL_DATE
            elif self._ACTUAL_DATE and not other._ACTUAL_DATE:
                return self._ACTUAL_DATE > other.expected_date
            elif not self._ACTUAL_DATE and other._ACTUAL_DATE:
                return self.expected_date > other._ACTUAL_DATE
            else:
                return self.expected_date > other.expected_date

        # If they are from different classes, compare by order_id
        return self.order_id > other.order_id

    def __eq__(self, other):
        # If they are from the same class, compare by date
        if isinstance(other, type(self)):
            if self._ACTUAL_DATE and other._ACTUAL_DATE:
                return self._ACTUAL_DATE == other._ACTUAL_DATE
            elif self._ACTUAL_DATE and not other._ACTUAL_DATE:
                return self._ACTUAL_DATE == other.expected_date
            elif not self._ACTUAL_DATE and other._ACTUAL_DATE:
                return self.expected_date == other._ACTUAL_DATE
            else:
                return self.expected_date == other.expected_date

        # If they are from different classes, compare by order_id
        return self.order_id == other.order_id

    def __le__(self, other):
        # If they are from the same class, compare by date
        if isinstance(other, type(self)):
            if self._ACTUAL_DATE and other._ACTUAL_DATE:
                return self._ACTUAL_DATE <= other._ACTUAL_DATE
            elif self._ACTUAL_DATE and not other._ACTUAL_DATE:
                return self._ACTUAL_DATE <= other.expected_date
            elif not self._ACTUAL_DATE and other._ACTUAL_DATE:
                return self.expected_date <= other._ACTUAL_DATE
            else:
                return self.expected_date <= other.expected_date

        # If they are from different classes, compare by order_id
        return self.order_id <= other.order_id

    def __ge__(self, other):
        # If they are from the same class, compare by date
        if isinstance(other, type(self)):
            if self._ACTUAL_DATE and other._ACTUAL_DATE:
                return self._ACTUAL_DATE >= other._ACTUAL_DATE
            elif self._ACTUAL_DATE and not other._ACTUAL_DATE:
                return self._ACTUAL_DATE >= other.expected_date
            elif not self._ACTUAL_DATE and other._ACTUAL_DATE:
                return self.expected_date >= other._ACTUAL_DATE
            else:
                return self.expected_date >= other.expected_date

        # If they are from different classes, compare by order_id
        return self.order_id >= other.order_id

    def __init__(self, prev_treatment=None, date: dt.date = None):
        if prev_treatment:
            self._EXPECTED_DATE = self.calculate_expected_date(prev_treatment)
        else:
            self._EXPECTED_DATE = date

        self._ACTUAL_DATE = None
        self._NAME = type(self).__name__.lower()
        self.display_name = self._NAME.capitalize()

    def calculate_expected_date(self, prev_treatment):
        if hasattr(self, "_REST_DAYS"):
            rest_days = self._REST_DAYS
        else:
            raise Exception("Rest days not defined")
        date = prev_treatment._ACTUAL_DATE or prev_treatment.expected_date
        return handle_weekends(date + dt.timedelta(days=rest_days))

    def reset(self, planned: dt.date, actual: dt.date | None):
        self._ACTUAL_DATE = actual
        self._EXPECTED_DATE = planned

    def update(self, date: dt.date):
        self._ACTUAL_DATE = date

    def get_date(self) -> dt.date:
        return self._ACTUAL_DATE or self.expected_date

    def get_week(self):
        return (
            self.expected_date.isocalendar().week
            if not self._ACTUAL_DATE
            else self._ACTUAL_DATE.isocalendar().week
        )


class Birth(Treatment):
    _ORDER_ID = 0

    def __init__(self, date: dt.date):
        super().__init__(None, date)
        self._EXPECTED_DATE = date
        self._REST_DAYS = 0


class Bovalto1(Treatment):
    _ORDER_ID = 1

    def __init__(self, prev: Birth):
        self._REST_DAYS = 10
        super().__init__(prev)


class Dehorn(Treatment):
    _ORDER_ID = 2

    def __init__(self, prev: Bovalto1):
        self._REST_DAYS = 5
        super().__init__(prev)


class Restall(Treatment):
    _ORDER_ID = 3

    def __init__(self, prev: Dehorn | Bovalto1):
        self._REST_DAYS = 5
        super().__init__(prev)


class Sell(Treatment):
    _ORDER_ID = 4

    def __init__(self, prev: Birth):
        self._REST_DAYS = 28
        super().__init__(prev)
        self._EXPECTED_DATE = get_next_tuesday(self._EXPECTED_DATE)


class Bovalto2(Treatment):
    _ORDER_ID = 4

    def __init__(self, prev: Bovalto1):
        self._REST_DAYS = 21
        super().__init__(prev)


class Ringworm1(Treatment):
    _ORDER_ID = 5

    def __init__(self, prev: Bovalto2):
        self._REST_DAYS = 5
        super().__init__(prev)


class Ringworm2(Treatment):
    _ORDER_ID = 6

    def __init__(self, prev: Ringworm1):
        self._REST_DAYS = 14
        super().__init__(prev)
