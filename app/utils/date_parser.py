from datetime import datetime


def parse_date(actual_date: str) -> datetime | None:
    try:
        parsed_datetime = datetime.strptime(actual_date, "%d %m %Y")
    except ValueError:
        return
    return parsed_datetime
