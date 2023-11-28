import datetime as dt
from enum import Enum


class Day(Enum):
    Monday = 0
    Tuesday = 1
    Wednesday = 2
    Thursday = 3
    Friday = 4
    Saturday = 5
    Sunday = 6


def get_next_tuesday(input_date: dt.date) -> dt.date:
    match input_date.weekday():
        case Day.Monday.value:
            input_date += dt.timedelta(days=1)
        case Day.Tuesday.value:
            pass
        case Day.Wednesday.value:
            input_date += dt.timedelta(days=6)
        case Day.Thursday.value:
            input_date += dt.timedelta(days=5)
        case Day.Friday.value:
            input_date += dt.timedelta(days=4)
        case Day.Saturday.value:
            input_date += dt.timedelta(days=3)
        case Day.Sunday.value:
            input_date += dt.timedelta(days=2)

    return input_date


def handle_weekends(input_date: dt.date) -> dt.date:
    match input_date.weekday():
        case Day.Saturday.value:
            input_date += dt.timedelta(days=2)
        case Day.Sunday.value:
            input_date += dt.timedelta(days=1)
        case _:  # Monday to Friday
            pass

    return input_date


if __name__ == "__main__":
    date = dt.date(2023, 12, 10)
    print(handle_weekends(date))
