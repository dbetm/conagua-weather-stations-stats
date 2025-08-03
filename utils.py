from typing import Optional

from datetime import datetime, date


def get_date(date_: str) -> Optional[date]:
    try:
        return datetime.strptime(date_, "%Y-%m-%d").date()
    except:
        print(f"Error converting to date this: {date_}")
        return None


def get_numerical_value(value_: str) -> Optional[float]:
    if isinstance(value_, str):
        value_ = value_.replace("\n", "")

    if value_.lower() == "nulo":
        return None

    return float(value_)